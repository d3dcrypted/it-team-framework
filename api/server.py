"""IT Team Framework API.

The API is intentionally demo-only: assessment and execution use synthetic
data. Hermes integration must be implemented as a separate adapter.

What it enforces is the order of the workflow. It does not verify who is
calling: there is one shared API key, and reviewed_by, validator_agent and
executor_agent are strings the caller supplies. "Validator differs from
executor" is a consistency rule on those strings, not proof of independence.
"""

import json
import logging
import os
import sqlite3
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import List, Optional

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field, model_validator

logger = logging.getLogger("it_team_api")
logging.basicConfig(level=os.environ.get("IT_TEAM_LOG_LEVEL", "INFO"))

DB_PATH = os.environ.get(
    "IT_TEAM_DB_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "it_team.db"),
)
API_KEY = os.environ.get("IT_TEAM_API_KEY")
MODE = os.environ.get("IT_TEAM_MODE", "demo").lower()
# Single source of truth for the version: the VERSION file at the repo root.
VERSION = (Path(__file__).resolve().parents[1] / "VERSION").read_text(encoding="utf-8").strip()
VALID_STATUSES = {
    "created", "assessing", "assessed", "gate_review", "roadmap_ready",
    "approved", "executing", "completed", "assessment_failed", "execution_failed",
}
TRANSITIONS = {
    "created": {"assessing"},
    "assessing": {"assessed", "assessment_failed"},
    "assessed": {"gate_review"},
    "gate_review": {"roadmap_ready"},
    "roadmap_ready": {"approved"},
    "approved": {"executing"},
    "executing": {"completed", "execution_failed"},
}


class Decision(str, Enum):
    APPROVED = "APPROVED"
    APPROVED_WITH_CONDITIONS = "APPROVED_WITH_CONDITIONS"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    DENIED = "DENIED"


@asynccontextmanager
async def lifespan(_: FastAPI):
    if MODE not in {"demo", "production"}:
        raise RuntimeError("IT_TEAM_MODE must be demo or production")
    if MODE == "production" and not API_KEY:
        raise RuntimeError("IT_TEAM_API_KEY is required in production mode")
    init_db()
    yield


_bearer = HTTPBearer(auto_error=False)


def require_api_key(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer),
):
    if request.url.path == "/health":
        return
    if not API_KEY:
        # Demo mode without a key is unauthenticated by design: loopback only,
        # see docs/configuration.md. A key that IS configured is enforced in
        # every mode; ignoring it in demo was a silent downgrade.
        return
    if credentials is None or credentials.credentials != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


cors_origins = [x.strip() for x in os.environ.get("IT_TEAM_CORS_ORIGINS", "").split(",") if x.strip()]
app = FastAPI(title="IT Team Framework API", version=VERSION, lifespan=lifespan,
              dependencies=[Depends(require_api_key)])
if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )


def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=5)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 5000")
    return conn


@contextmanager
def db():
    """One connection per unit of work: commits on success, always closes.

    Callers raise freely inside the block; the exception skips the commit and
    the connection is closed either way, which is what the earlier
    get_conn()/close() pairs did not do on the error paths.
    """
    conn = get_conn()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with db() as conn:
        _init_db(conn)


def _init_db(conn):
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS engagements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT NOT NULL,
        description TEXT,
        created_at TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        engagement_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        approved INTEGER,
        decision TEXT,
        reason TEXT,
        conditions TEXT,
        reviewed_at TEXT,
        reviewed_by TEXT,
        FOREIGN KEY (engagement_id) REFERENCES engagements(id) ON DELETE CASCADE
    )""")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_recommendations_engagement ON recommendations(engagement_id)")
    # v0.3.1 P1: append-only audit trail of every state transition (immutable).
    cur.execute("""CREATE TABLE IF NOT EXISTS state_transitions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        engagement_id INTEGER NOT NULL,
        from_state TEXT,
        to_state TEXT NOT NULL,
        changed_at TEXT NOT NULL,
        changed_by TEXT NOT NULL DEFAULT 'system',
        FOREIGN KEY (engagement_id) REFERENCES engagements(id) ON DELETE CASCADE
    )""")
    # v0.3.1 P1: action dependency graph (blocks[]). An action cannot start until predecessors COMPLETED.
    cur.execute("""CREATE TABLE IF NOT EXISTS action_dependencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        engagement_id INTEGER NOT NULL,
        action_id TEXT NOT NULL,
        depends_on TEXT NOT NULL,
        FOREIGN KEY (engagement_id) REFERENCES engagements(id) ON DELETE CASCADE
    )""")
    # v0.3.1 P1: independent validator verdict, required before COMPLETED.
    cur.execute("""CREATE TABLE IF NOT EXISTS validator_verdicts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        engagement_id INTEGER NOT NULL,
        verdict TEXT NOT NULL,
        validator_agent TEXT NOT NULL,
        executor_agent TEXT,
        evidence_ref TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (engagement_id) REFERENCES engagements(id) ON DELETE CASCADE
    )""")
    # v0.4.0 P1: per-action state, so BLOCKED is a fact and not a convention.
    cur.execute("""CREATE TABLE IF NOT EXISTS action_states (
        engagement_id INTEGER NOT NULL,
        action_id TEXT NOT NULL,
        state TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        PRIMARY KEY (engagement_id, action_id),
        FOREIGN KEY (engagement_id) REFERENCES engagements(id) ON DELETE CASCADE
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS models (
        name TEXT PRIMARY KEY,
        cost_input_per_1m REAL NOT NULL,
        cost_output_per_1m REAL NOT NULL
    )""")
    if cur.execute("SELECT COUNT(*) AS cnt FROM models").fetchone()["cnt"] == 0:
        cur.executemany(
            "INSERT INTO models VALUES (?,?,?)",
            # Demonstration seeds only — placeholder names, replace with the
            # operator's catalog. Do NOT pin explicit OpenRouter model IDs here.
            [("demo-orchestrator-model", 0.70, 0.70), ("demo-worker-model", 0.42, 0.42)],
        )
    # committed and closed by db()


class EngagementCreate(BaseModel):
    description: Optional[str] = None


class EngagementOut(BaseModel):
    id: int
    status: str
    description: Optional[str] = None
    created_at: str


class RecommendationOut(BaseModel):
    id: int
    text: str
    approved: Optional[bool]
    decision: Optional[Decision] = None
    reason: Optional[str] = None
    conditions: List[str] = Field(default_factory=list)
    reviewed_at: Optional[str] = None
    reviewed_by: Optional[str] = None


class ModelOut(BaseModel):
    name: str
    cost_input_per_1m: float
    cost_output_per_1m: float


class DecisionBody(BaseModel):
    decision: Decision
    reason: Optional[str] = None
    conditions: List[str] = Field(default_factory=list)
    reviewed_by: str = "human"

    @model_validator(mode="after")
    def validate_decision(self):
        if self.decision in {Decision.DENIED, Decision.CHANGES_REQUESTED} and not self.reason:
            raise ValueError("reason is required for DENIED and CHANGES_REQUESTED")
        if self.decision == Decision.APPROVED_WITH_CONDITIONS and not self.conditions:
            raise ValueError("conditions are required for APPROVED_WITH_CONDITIONS")
        return self


class ApproveBody(BaseModel):
    """Backward-compatible v0.1 payload; maps to a four-state decision."""
    approve: bool


def get_engagement(eng_id: int):
    with db() as conn:
        row = conn.execute("SELECT * FROM engagements WHERE id = ?", (eng_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Engagement not found")
    return row


def set_status(eng_id: int, new_status: str, changed_by: str = "system"):
    if new_status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {new_status}")
    with db() as conn:
        row = conn.execute("SELECT status FROM engagements WHERE id = ?", (eng_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Engagement not found")
        current = row["status"]
        if new_status != current and new_status not in TRANSITIONS.get(current, set()):
            raise HTTPException(status_code=409, detail=f"Invalid transition: {current} -> {new_status}")
        if new_status == current:
            return  # idempotent no-op, no audit row for non-transitions
        # Compare-and-swap on the state we just read: two concurrent requests
        # cannot both move the same engagement out of the same state.
        updated = conn.execute(
            "UPDATE engagements SET status = ? WHERE id = ? AND status = ?",
            (new_status, eng_id, current),
        ).rowcount
        if updated != 1:
            raise HTTPException(status_code=409, detail=f"Concurrent state change on engagement {eng_id}")
        # v0.3.1 P1: append-only audit trail. Never UPDATE/DELETE these rows.
        conn.execute(
            "INSERT INTO state_transitions (engagement_id, from_state, to_state, changed_at, changed_by) VALUES (?,?,?,?,?)",
            (eng_id, current, new_status, datetime.now(timezone.utc).isoformat(), changed_by),
        )


def add_demo_recommendations(eng_id: int):
    with db() as conn:
        if conn.execute("SELECT COUNT(*) AS cnt FROM recommendations WHERE engagement_id = ?", (eng_id,)).fetchone()["cnt"]:
            return
        conn.executemany(
            "INSERT INTO recommendations (engagement_id, text) VALUES (?, ?)",
            [(eng_id, "Abilitare MFA sugli account privilegiati"),
             (eng_id, "Eseguire un test di restore Veeam completo"),
             (eng_id, "Segmentare rete server ed endpoint")],
        )


def recommendation_from_row(row):
    return RecommendationOut(
        id=row["id"], text=row["text"],
        approved=bool(row["approved"]) if row["approved"] is not None else None,
        decision=row["decision"], reason=row["reason"],
        conditions=json.loads(row["conditions"] or "[]"),
        reviewed_at=row["reviewed_at"], reviewed_by=row["reviewed_by"],
    )


@app.post("/engagements", response_model=EngagementOut)
def create_engagement(payload: EngagementCreate):
    now = datetime.now(timezone.utc).isoformat()
    with db() as conn:
        cur = conn.execute("INSERT INTO engagements (status, description, created_at) VALUES (?,?,?)",
                           ("created", payload.description, now))
        eng_id = cur.lastrowid
    return EngagementOut(id=eng_id, status="created", description=payload.description, created_at=now)


@app.get("/engagements/{eng_id}", response_model=EngagementOut)
def read_engagement(eng_id: int):
    row = get_engagement(eng_id)
    return EngagementOut(id=row["id"], status=row["status"], description=row["description"], created_at=row["created_at"])


@app.post("/engagements/{eng_id}/assess", status_code=202)
def start_assessment(eng_id: int, background: BackgroundTasks):
    row = get_engagement(eng_id)
    if row["status"] != "created":
        raise HTTPException(status_code=409, detail="Assessment already started or completed")
    set_status(eng_id, "assessing")

    def task():
        try:
            if MODE != "demo":
                raise RuntimeError("Hermes adapter not implemented in v0.2")
            add_demo_recommendations(eng_id)
            set_status(eng_id, "assessed")
        except Exception:
            logger.exception("Assessment failed for engagement %s", eng_id)
            try:
                set_status(eng_id, "assessment_failed")
            except Exception:
                logger.exception("Could not mark assessment as failed")

    background.add_task(task)
    return {"message": "Assessment started", "mode": MODE}


@app.get("/engagements/{eng_id}/recommendations", response_model=List[RecommendationOut])
def list_recommendations(eng_id: int):
    get_engagement(eng_id)
    with db() as conn:
        rows = conn.execute("SELECT * FROM recommendations WHERE engagement_id = ? ORDER BY id", (eng_id,)).fetchall()
    return [recommendation_from_row(row) for row in rows]


@app.post("/engagements/{eng_id}/gate-review", status_code=202)
def start_gate_review(eng_id: int):
    """Opens the gate. It stays open until close_gate_review() decides."""
    row = get_engagement(eng_id)
    if row["status"] != "assessed":
        raise HTTPException(status_code=409, detail="Gate review requires an assessed engagement")
    set_status(eng_id, "gate_review")
    return {"message": "Gate review open", "status": "gate_review"}


@app.post("/engagements/{eng_id}/gate-review/close")
def close_gate_review(eng_id: int):
    """Closes the gate: the step the v0.3.4 API skipped.

    It used to move assessed -> gate_review -> roadmap_ready inside one
    request, so the review was never a state anyone could fail. The gate now
    passes only when every recommendation has a decision and at least one was
    approved; an all-rejected roadmap cannot reach execution.
    """
    row = get_engagement(eng_id)
    if row["status"] != "gate_review":
        raise HTTPException(status_code=409, detail="No gate review is currently open")
    with db() as conn:
        counts = conn.execute(
            "SELECT COUNT(*) AS total,"
            " SUM(CASE WHEN decision IS NULL THEN 1 ELSE 0 END) AS pending,"
            " SUM(CASE WHEN decision IN (?,?) THEN 1 ELSE 0 END) AS approved,"
            " SUM(CASE WHEN decision IN (?,?) THEN 1 ELSE 0 END) AS rejected"
            " FROM recommendations WHERE engagement_id = ?",
            (Decision.APPROVED.value, Decision.APPROVED_WITH_CONDITIONS.value,
             Decision.DENIED.value, Decision.CHANGES_REQUESTED.value, eng_id),
        ).fetchone()
    if not counts["total"]:
        raise HTTPException(status_code=409, detail="No recommendations to review")
    if counts["pending"]:
        raise HTTPException(status_code=409, detail=f"{counts['pending']} recommendation(s) still undecided")
    if not counts["approved"]:
        raise HTTPException(status_code=409, detail="Every recommendation was rejected: the gate cannot pass")
    set_status(eng_id, "roadmap_ready", changed_by="it-team-gatekeeper")
    return {"message": "Gate passed", "approved": counts["approved"], "rejected": counts["rejected"]}


@app.post("/engagements/{eng_id}/gate-review/{rec_id}/decision", response_model=RecommendationOut)
def decide_recommendation(eng_id: int, rec_id: int, body: DecisionBody):
    row = get_engagement(eng_id)
    # Decisions are frozen once the gate closes: a roadmap that could still be
    # edited in roadmap_ready was never the one the gate passed.
    if row["status"] != "gate_review":
        raise HTTPException(status_code=409, detail="Recommendation is not currently under gate review")
    with db() as conn:
        rec = conn.execute("SELECT id FROM recommendations WHERE id = ? AND engagement_id = ?", (rec_id, eng_id)).fetchone()
        if not rec:
            raise HTTPException(status_code=404, detail="Recommendation not found for this engagement")
        now = datetime.now(timezone.utc).isoformat()
        conn.execute("UPDATE recommendations SET approved=?, decision=?, reason=?, conditions=?, reviewed_at=?, reviewed_by=? WHERE id=?",
                     (1 if body.decision in {Decision.APPROVED, Decision.APPROVED_WITH_CONDITIONS} else 0,
                      body.decision.value, body.reason, json.dumps(body.conditions), now, body.reviewed_by, rec_id))
        updated = conn.execute("SELECT * FROM recommendations WHERE id = ?", (rec_id,)).fetchone()
    return recommendation_from_row(updated)


@app.post("/engagements/{eng_id}/gate-review/{rec_id}/approve", response_model=RecommendationOut)
def approve_recommendation(eng_id: int, rec_id: int, body: ApproveBody):
    return decide_recommendation(eng_id, rec_id, DecisionBody(decision=Decision.APPROVED if body.approve else Decision.DENIED,
                                                              reason="Rejected through legacy v0.1 endpoint" if not body.approve else None))


@app.get("/engagements/{eng_id}/roadmap")
def get_roadmap(eng_id: int):
    get_engagement(eng_id)
    with db() as conn:
        rows = conn.execute("SELECT * FROM recommendations WHERE engagement_id = ? AND decision IN (?,?) ORDER BY id",
                            (eng_id, Decision.APPROVED.value, Decision.APPROVED_WITH_CONDITIONS.value)).fetchall()
    return {"roadmap": [recommendation_from_row(row).model_dump() for row in rows]}


@app.post("/engagements/{eng_id}/execute", status_code=202)
def execute_improvement(eng_id: int, background: BackgroundTasks):
    row = get_engagement(eng_id)
    if row["status"] not in {"roadmap_ready", "approved"}:
        raise HTTPException(status_code=409, detail="Execution requires a reviewed roadmap")
    with db() as conn:
        counts = conn.execute(
            "SELECT SUM(CASE WHEN decision IS NULL THEN 1 ELSE 0 END) AS pending,"
            " SUM(CASE WHEN decision IN (?,?) THEN 1 ELSE 0 END) AS approved"
            " FROM recommendations WHERE engagement_id=?",
            (Decision.APPROVED.value, Decision.APPROVED_WITH_CONDITIONS.value, eng_id),
        ).fetchone()
    if counts["pending"]:
        raise HTTPException(status_code=409, detail="Every recommendation must be reviewed before execution")
    if not counts["approved"]:
        # A roadmap where everything was rejected is not an execution plan.
        raise HTTPException(status_code=409, detail="Execution requires at least one approved recommendation")
    set_status(eng_id, "approved")
    set_status(eng_id, "executing")

    def task():
        try:
            if MODE != "demo":
                raise RuntimeError("Hermes adapter not implemented")
            # v0.3.1 P1: no auto-COMPLETED. The orchestrator must record a
            # VALIDATED verdict from it-team-validator before completion.
            logger.info("Demo execution running for engagement %s", eng_id)
        except Exception:
            logger.exception("Execution failed for engagement %s", eng_id)
            try:
                set_status(eng_id, "execution_failed")
            except Exception:
                logger.exception("Could not mark execution as failed")

    background.add_task(task)
    return {"message": "Execution started", "mode": MODE}


class ValidatorVerdictBody(BaseModel):
    """Independent validator verdict — required before COMPLETED (v0.3.1 P1)."""
    engagement_id: Optional[int] = None  # must match the path when supplied
    verdict: str  # VALIDATED | REJECTED | EVIDENCE_INSUFFICIENT
    validator_agent: str
    # Required since v0.4.0: while it was optional, omitting it bypassed the
    # independence check entirely (validator != executor was never tested).
    executor_agent: str
    evidence_ref: Optional[str] = None


class DependencyBody(BaseModel):
    """Action dependency graph entry (v0.3.1 P1)."""
    action_id: str
    depends_on: List[str] = Field(default_factory=list)


@app.post("/engagements/{eng_id}/validator-verdict", status_code=201)
def record_validator_verdict(eng_id: int, body: ValidatorVerdictBody):
    row = get_engagement(eng_id)
    if body.engagement_id is not None and body.engagement_id != eng_id:
        raise HTTPException(status_code=409, detail="engagement_id in the body does not match the path")
    if body.verdict not in {"VALIDATED", "REJECTED", "EVIDENCE_INSUFFICIENT"}:
        raise HTTPException(status_code=422, detail="verdict must be VALIDATED|REJECTED|EVIDENCE_INSUFFICIENT")
    # A verdict before execution is an assumption, not a verification.
    if row["status"] != "executing":
        raise HTTPException(status_code=409,
                           detail=f"Verdicts apply to an executing engagement, currently '{row['status']}'")
    if body.validator_agent == body.executor_agent:
        raise HTTPException(status_code=409, detail="Self-validation is void: validator_agent must differ from executor_agent")
    if body.verdict == "VALIDATED" and not (body.evidence_ref or "").strip():
        raise HTTPException(status_code=409, detail="A VALIDATED verdict requires evidence_ref")
    with db() as conn:
        conn.execute(
            "INSERT INTO validator_verdicts (engagement_id, verdict, validator_agent, executor_agent, evidence_ref, created_at) VALUES (?,?,?,?,?,?)",
            (eng_id, body.verdict, body.validator_agent, body.executor_agent, body.evidence_ref,
             datetime.now(timezone.utc).isoformat()),
        )
    return {"message": "Verdict recorded", "verdict": body.verdict}


def find_cycle(edges: dict) -> List[str]:
    """Return one dependency cycle as a closed path, or [] when acyclic.

    ponytail: recursive DFS — roadmaps are tens of actions, not thousands.
    """
    UNVISITED, VISITING, DONE = 0, 1, 2
    seen: dict = {}
    stack: List[str] = []

    def visit(node: str) -> List[str]:
        if seen.get(node) == VISITING:
            return stack[stack.index(node):] + [node]
        if seen.get(node) == DONE:
            return []
        seen[node] = VISITING
        stack.append(node)
        for predecessor in sorted(edges.get(node, ())):
            cycle = visit(predecessor)
            if cycle:
                return cycle
        stack.pop()
        seen[node] = DONE
        return []

    for node in sorted(edges):
        cycle = visit(node)
        if cycle:
            return cycle
    return []


@app.post("/engagements/{eng_id}/dependencies")
def set_dependencies(eng_id: int, body: List[DependencyBody]):
    """Record the action graph and reject the graphs the orchestrator would abort on.

    v0.3.1 declared 'an action cannot start until its predecessors COMPLETED'
    and left the check to the prompt. The graph is now validated on write
    (unknown predecessors, self-loops, cycles) and enforced when an action
    starts, through the action_states table.
    """
    get_engagement(eng_id)
    declared = [dep.action_id for dep in body]
    if any(not action.strip() for action in declared):
        raise HTTPException(status_code=422, detail="action_id must not be empty")
    if len(set(declared)) != len(declared):
        raise HTTPException(status_code=422, detail="Duplicate action_id in the dependency payload")
    edges: dict = {}
    for dep in body:
        for predecessor in dep.depends_on:
            if predecessor not in declared:
                raise HTTPException(status_code=422,
                                    detail=f"Unknown predecessor '{predecessor}': declare it as an action first")
            if predecessor == dep.action_id:
                raise HTTPException(status_code=422, detail=f"Action '{predecessor}' cannot depend on itself")
            edges.setdefault(dep.action_id, set()).add(predecessor)
    cycle = find_cycle(edges)
    if cycle:
        raise HTTPException(status_code=422, detail="Dependency cycle: " + " -> ".join(cycle))
    now = datetime.now(timezone.utc).isoformat()
    with db() as conn:
        conn.execute("DELETE FROM action_dependencies WHERE engagement_id = ?", (eng_id,))
        for action_id, predecessors in edges.items():
            for predecessor in sorted(predecessors):
                conn.execute(
                    "INSERT INTO action_dependencies (engagement_id, action_id, depends_on) VALUES (?,?,?)",
                    (eng_id, action_id, predecessor),
                )
        # INSERT OR IGNORE: re-declaring the graph never resets a completed action.
        conn.executemany(
            "INSERT OR IGNORE INTO action_states (engagement_id, action_id, state, updated_at) VALUES (?,?,?,?)",
            [(eng_id, action_id, "PENDING", now) for action_id in declared],
        )
    return {"message": "Dependencies recorded", "actions": len(declared),
            "count": sum(len(d.depends_on) for d in body)}


def action_state(conn, eng_id: int, action_id: str) -> str:
    row = conn.execute(
        "SELECT state FROM action_states WHERE engagement_id = ? AND action_id = ?", (eng_id, action_id)
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"Action '{action_id}' is not declared for this engagement")
    return row["state"]


@app.get("/engagements/{eng_id}/actions")
def list_actions(eng_id: int):
    get_engagement(eng_id)
    with db() as conn:
        states = {r["action_id"]: r["state"] for r in
                  conn.execute("SELECT action_id, state FROM action_states WHERE engagement_id = ?", (eng_id,))}
        dependencies = conn.execute(
            "SELECT action_id, depends_on FROM action_dependencies WHERE engagement_id = ?", (eng_id,)
        ).fetchall()
    blocked: dict = {}
    for dep in dependencies:
        if states.get(dep["depends_on"]) != "COMPLETED":
            blocked.setdefault(dep["action_id"], []).append(dep["depends_on"])
    return {"actions": [{"action_id": action_id, "state": state, "blocked_by": sorted(blocked.get(action_id, []))}
                        for action_id, state in sorted(states.items())]}


@app.post("/engagements/{eng_id}/actions/{action_id}/start")
def start_action(eng_id: int, action_id: str):
    """A blocked action cannot start: the rule the skills state, enforced here."""
    if get_engagement(eng_id)["status"] != "executing":
        raise HTTPException(status_code=409, detail="Actions run only while the engagement is executing")
    with db() as conn:
        state = action_state(conn, eng_id, action_id)
        if state == "COMPLETED":
            raise HTTPException(status_code=409, detail=f"Action '{action_id}' is already COMPLETED")
        if state == "RUNNING":
            raise HTTPException(status_code=409, detail=f"Action '{action_id}' is already RUNNING")
        unmet = conn.execute(
            "SELECT d.depends_on FROM action_dependencies d"
            " LEFT JOIN action_states s ON s.engagement_id = d.engagement_id AND s.action_id = d.depends_on"
            " WHERE d.engagement_id = ? AND d.action_id = ? AND COALESCE(s.state, 'PENDING') != 'COMPLETED'"
            " ORDER BY d.depends_on",
            (eng_id, action_id),
        ).fetchall()
        if unmet:
            raise HTTPException(status_code=409, detail="Blocked by "
                                + ", ".join(r["depends_on"] for r in unmet))
        conn.execute("UPDATE action_states SET state = 'RUNNING', updated_at = ? WHERE engagement_id = ? AND action_id = ?",
                     (datetime.now(timezone.utc).isoformat(), eng_id, action_id))
    return {"action_id": action_id, "state": "RUNNING"}


@app.post("/engagements/{eng_id}/actions/{action_id}/complete")
def complete_action(eng_id: int, action_id: str):
    get_engagement(eng_id)
    with db() as conn:
        state = action_state(conn, eng_id, action_id)
        if state != "RUNNING":
            raise HTTPException(status_code=409, detail=f"Action '{action_id}' is {state}: only a RUNNING action can complete")
        conn.execute("UPDATE action_states SET state = 'COMPLETED', updated_at = ? WHERE engagement_id = ? AND action_id = ?",
                     (datetime.now(timezone.utc).isoformat(), eng_id, action_id))
    return {"action_id": action_id, "state": "COMPLETED"}


@app.post("/engagements/{eng_id}/complete", status_code=200)
def complete_engagement(eng_id: int):
    """v0.3.1 P1: COMPLETED reachable ONLY from a VALIDATED verdict."""
    get_engagement(eng_id)
    with db() as conn:
        verdict = conn.execute(
            "SELECT verdict FROM validator_verdicts WHERE engagement_id = ? ORDER BY id DESC LIMIT 1",
            (eng_id,),
        ).fetchone()
        unfinished = [r["action_id"] for r in conn.execute(
            "SELECT action_id FROM action_states WHERE engagement_id = ? AND state != 'COMPLETED' ORDER BY action_id",
            (eng_id,))]
    if not verdict or verdict["verdict"] != "VALIDATED":
        raise HTTPException(status_code=409, detail="COMPLETED requires a VALIDATED verdict from it-team-validator")
    if unfinished:
        raise HTTPException(status_code=409, detail="Actions not completed: " + ", ".join(unfinished))
    set_status(eng_id, "completed", changed_by="it-team-validator")
    return {"message": "Engagement completed", "status": "completed"}


@app.get("/engagements/{eng_id}/audit-trail")
def get_audit_trail(eng_id: int):
    get_engagement(eng_id)
    with db() as conn:
        rows = conn.execute(
            "SELECT id, from_state, to_state, changed_at, changed_by FROM state_transitions WHERE engagement_id = ? ORDER BY id",
            (eng_id,),
        ).fetchall()
    return {"audit_trail": [dict(r) for r in rows]}


@app.get("/models", response_model=List[ModelOut])
def list_models():
    with db() as conn:
        rows = conn.execute("SELECT * FROM models ORDER BY name").fetchall()
    return [ModelOut(name=r["name"], cost_input_per_1m=r["cost_input_per_1m"], cost_output_per_1m=r["cost_output_per_1m"]) for r in rows]


@app.get("/health")
def health_check():
    try:
        with db() as conn:
            conn.execute("SELECT 1")
        return {"status": "ok", "mode": MODE, "version": VERSION}
    except sqlite3.Error:
        return {"status": "degraded", "mode": MODE, "version": VERSION}


# Run via: uvicorn server:app --host 127.0.0.1 --port 8080
