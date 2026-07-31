"""IT Team Framework API v0.2.

The API is intentionally demo-only in v0.2: assessment and execution use
synthetic data. Hermes integration must be implemented as a separate adapter.
"""

import logging
import os
import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
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
    if MODE == "production" and (not API_KEY or credentials is None or credentials.credentials != API_KEY):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


cors_origins = [x.strip() for x in os.environ.get("IT_TEAM_CORS_ORIGINS", "").split(",") if x.strip()]
app = FastAPI(title="IT Team Framework API", version="0.2.0", lifespan=lifespan,
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


def init_db():
    conn = get_conn()
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
    cur.execute("""CREATE TABLE IF NOT EXISTS models (
        name TEXT PRIMARY KEY,
        cost_input_per_1m REAL NOT NULL,
        cost_output_per_1m REAL NOT NULL
    )""")
    if cur.execute("SELECT COUNT(*) AS cnt FROM models").fetchone()["cnt"] == 0:
        cur.executemany(
            "INSERT INTO models VALUES (?,?,?)",
            [("openai/gpt-5.6-luna", 0.70, 0.70), ("xiaomi/mimo-v2.5", 0.42, 0.42)],
        )
    conn.commit()
    conn.close()


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
    conn = get_conn()
    row = conn.execute("SELECT * FROM engagements WHERE id = ?", (eng_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Engagement not found")
    return row


def set_status(eng_id: int, new_status: str):
    if new_status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {new_status}")
    conn = get_conn()
    row = conn.execute("SELECT status FROM engagements WHERE id = ?", (eng_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Engagement not found")
    current = row["status"]
    if new_status != current and new_status not in TRANSITIONS.get(current, set()):
        conn.close()
        raise HTTPException(status_code=409, detail=f"Invalid transition: {current} -> {new_status}")
    conn.execute("UPDATE engagements SET status = ? WHERE id = ?", (new_status, eng_id))
    conn.commit()
    conn.close()


def add_demo_recommendations(eng_id: int):
    conn = get_conn()
    if conn.execute("SELECT COUNT(*) AS cnt FROM recommendations WHERE engagement_id = ?", (eng_id,)).fetchone()["cnt"]:
        conn.close()
        return
    conn.executemany(
        "INSERT INTO recommendations (engagement_id, text) VALUES (?, ?)",
        [(eng_id, "Abilitare MFA sugli account privilegiati"),
         (eng_id, "Eseguire un test di restore Veeam completo"),
         (eng_id, "Segmentare rete server ed endpoint")],
    )
    conn.commit()
    conn.close()


def recommendation_from_row(row):
    import json
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
    conn = get_conn()
    cur = conn.execute("INSERT INTO engagements (status, description, created_at) VALUES (?,?,?)",
                       ("created", payload.description, now))
    eng_id = cur.lastrowid
    conn.commit()
    conn.close()
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
    conn = get_conn()
    rows = conn.execute("SELECT * FROM recommendations WHERE engagement_id = ? ORDER BY id", (eng_id,)).fetchall()
    conn.close()
    return [recommendation_from_row(row) for row in rows]


@app.post("/engagements/{eng_id}/gate-review", status_code=202)
def start_gate_review(eng_id: int, background: BackgroundTasks):
    row = get_engagement(eng_id)
    if row["status"] != "assessed":
        raise HTTPException(status_code=409, detail="Gate review requires an assessed engagement")
    set_status(eng_id, "gate_review")
    set_status(eng_id, "roadmap_ready")
    return {"message": "Gate review started"}


@app.post("/engagements/{eng_id}/gate-review/{rec_id}/decision", response_model=RecommendationOut)
def decide_recommendation(eng_id: int, rec_id: int, body: DecisionBody):
    row = get_engagement(eng_id)
    if row["status"] not in {"gate_review", "roadmap_ready"}:
        raise HTTPException(status_code=409, detail="Recommendation is not currently under gate review")
    import json
    conn = get_conn()
    rec = conn.execute("SELECT * FROM recommendations WHERE id = ? AND engagement_id = ?", (rec_id, eng_id)).fetchone()
    if not rec:
        conn.close()
        raise HTTPException(status_code=404, detail="Recommendation not found for this engagement")
    now = datetime.now(timezone.utc).isoformat()
    conn.execute("UPDATE recommendations SET approved=?, decision=?, reason=?, conditions=?, reviewed_at=?, reviewed_by=? WHERE id=?",
                 (1 if body.decision in {Decision.APPROVED, Decision.APPROVED_WITH_CONDITIONS} else 0,
                  body.decision.value, body.reason, json.dumps(body.conditions), now, body.reviewed_by, rec_id))
    conn.commit()
    updated = conn.execute("SELECT * FROM recommendations WHERE id = ?", (rec_id,)).fetchone()
    conn.close()
    return recommendation_from_row(updated)


@app.post("/engagements/{eng_id}/gate-review/{rec_id}/approve", response_model=RecommendationOut)
def approve_recommendation(eng_id: int, rec_id: int, body: ApproveBody):
    return decide_recommendation(eng_id, rec_id, DecisionBody(decision=Decision.APPROVED if body.approve else Decision.DENIED,
                                                              reason="Rejected through legacy v0.1 endpoint" if not body.approve else None))


@app.get("/engagements/{eng_id}/roadmap")
def get_roadmap(eng_id: int):
    get_engagement(eng_id)
    conn = get_conn()
    rows = conn.execute("SELECT * FROM recommendations WHERE engagement_id = ? AND decision IN (?,?) ORDER BY id",
                        (eng_id, Decision.APPROVED.value, Decision.APPROVED_WITH_CONDITIONS.value)).fetchall()
    conn.close()
    return {"roadmap": [recommendation_from_row(row).model_dump() for row in rows]}


@app.post("/engagements/{eng_id}/execute", status_code=202)
def execute_improvement(eng_id: int, background: BackgroundTasks):
    row = get_engagement(eng_id)
    if row["status"] not in {"roadmap_ready", "approved"}:
        raise HTTPException(status_code=409, detail="Execution requires a reviewed roadmap")
    conn = get_conn()
    pending = conn.execute("SELECT COUNT(*) AS cnt FROM recommendations WHERE engagement_id=? AND decision IS NULL", (eng_id,)).fetchone()["cnt"]
    conn.close()
    if pending:
        raise HTTPException(status_code=409, detail="Every recommendation must be reviewed before execution")
    set_status(eng_id, "approved")
    set_status(eng_id, "executing")

    def task():
        try:
            if MODE != "demo":
                raise RuntimeError("Hermes adapter not implemented in v0.2")
            set_status(eng_id, "completed")
        except Exception:
            logger.exception("Execution failed for engagement %s", eng_id)
            try:
                set_status(eng_id, "execution_failed")
            except Exception:
                logger.exception("Could not mark execution as failed")

    background.add_task(task)
    return {"message": "Execution started", "mode": MODE}


@app.get("/models", response_model=List[ModelOut])
def list_models():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM models ORDER BY name").fetchall()
    conn.close()
    return [ModelOut(name=r["name"], cost_input_per_1m=r["cost_input_per_1m"], cost_output_per_1m=r["cost_output_per_1m"]) for r in rows]


@app.get("/health")
def health_check():
    try:
        conn = get_conn()
        conn.execute("SELECT 1")
        conn.close()
        return {"status": "ok", "mode": MODE, "version": "0.2.0"}
    except sqlite3.Error:
        return {"status": "degraded", "mode": MODE, "version": "0.2.0"}


# Run via: uvicorn server:app --host 127.0.0.1 --port 8080
