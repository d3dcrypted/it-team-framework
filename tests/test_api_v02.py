import importlib
import os
import sys
from pathlib import Path

import pytest


@pytest.fixture
def api(tmp_path, monkeypatch):
    monkeypatch.setenv("IT_TEAM_DB_PATH", str(tmp_path / "test.db"))
    monkeypatch.setenv("IT_TEAM_MODE", "demo")
    sys.path.insert(0, str(tmp_path.parent))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))
    sys.modules.pop("server", None)
    server = importlib.import_module("server")
    server.init_db()
    return server


def test_demo_lifecycle_and_gate_decisions(api):
    from fastapi.testclient import TestClient

    with TestClient(api.app) as client:
        created = client.post("/engagements", json={"description": "Acme Logistics Ltd"})
        assert created.status_code == 200
        engagement_id = created.json()["id"]

        assessed = client.post(f"/engagements/{engagement_id}/assess")
        assert assessed.status_code == 202
        assert client.get(f"/engagements/{engagement_id}").json()["status"] == "assessed"

        duplicate = client.post(f"/engagements/{engagement_id}/assess")
        assert duplicate.status_code == 409

        gate = client.post(f"/engagements/{engagement_id}/gate-review")
        assert gate.status_code == 202
        # v0.4.0: the gate stays open until it is closed explicitly.
        assert client.get(f"/engagements/{engagement_id}").json()["status"] == "gate_review"
        recommendations = client.get(f"/engagements/{engagement_id}/recommendations").json()
        assert len(recommendations) == 3

        decision = client.post(
            f"/engagements/{engagement_id}/gate-review/{recommendations[0]['id']}/decision",
            json={"decision": "APPROVED_WITH_CONDITIONS", "conditions": ["Verifiable criterion"]},
        )
        assert decision.status_code == 200
        for recommendation in recommendations[1:]:
            response = client.post(
                f"/engagements/{engagement_id}/gate-review/{recommendation['id']}/decision",
                json={"decision": "APPROVED"},
            )
            assert response.status_code == 200

        gate_close = client.post(f"/engagements/{engagement_id}/gate-review/close")
        assert gate_close.status_code == 200
        assert client.get(f"/engagements/{engagement_id}").json()["status"] == "roadmap_ready"

        roadmap = client.get(f"/engagements/{engagement_id}/roadmap").json()["roadmap"]
        assert len(roadmap) == 3
        assert roadmap[0]["decision"] == "APPROVED_WITH_CONDITIONS"

        execution = client.post(f"/engagements/{engagement_id}/execute")
        assert execution.status_code == 202
        assert client.get(f"/engagements/{engagement_id}").json()["status"] == "executing"

        # v0.3.1: the execute path no longer auto-completes; COMPLETED needs a VALIDATED verdict.
        premature = client.post(f"/engagements/{engagement_id}/complete")
        assert premature.status_code == 409

        self_validation = client.post(
            f"/engagements/{engagement_id}/validator-verdict",
            json={
                "engagement_id": engagement_id,
                "verdict": "VALIDATED",
                "validator_agent": "it-team-validator",
                "executor_agent": "it-team-validator",
                "evidence_ref": "synthetic-evidence",
            },
        )
        assert self_validation.status_code == 409

        missing_evidence = client.post(
            f"/engagements/{engagement_id}/validator-verdict",
            json={
                "verdict": "VALIDATED",
                "validator_agent": "it-team-validator",
                "executor_agent": "it-team-orchestrator",
            },
        )
        assert missing_evidence.status_code == 409

        missing_executor = client.post(
            f"/engagements/{engagement_id}/validator-verdict",
            json={
                "verdict": "VALIDATED",
                "validator_agent": "it-team-validator",
                "evidence_ref": "synthetic-evidence",
            },
        )
        assert missing_executor.status_code == 422

        verdict = client.post(
            f"/engagements/{engagement_id}/validator-verdict",
            json={
                "engagement_id": engagement_id,
                "verdict": "VALIDATED",
                "validator_agent": "it-team-validator",
                "executor_agent": "it-team-orchestrator",
                "evidence_ref": "synthetic-evidence",
            },
        )
        assert verdict.status_code == 201

        # Decisions are frozen after the gate closed.
        assert client.post(
            f"/engagements/{engagement_id}/gate-review/{recommendations[0]['id']}/decision",
            json={"decision": "DENIED", "reason": "late"},
        ).status_code == 409

        # A declared action that has not finished holds completion.
        client.post(f"/engagements/{engagement_id}/dependencies", json=[{"action_id": "mfa"}])
        assert client.post(f"/engagements/{engagement_id}/complete").status_code == 409
        client.post(f"/engagements/{engagement_id}/actions/mfa/start")
        client.post(f"/engagements/{engagement_id}/actions/mfa/complete")

        completed = client.post(f"/engagements/{engagement_id}/complete")
        assert completed.status_code == 200
        assert client.get(f"/engagements/{engagement_id}").json()["status"] == "completed"

        trail = client.get(f"/engagements/{engagement_id}/audit-trail").json()["audit_trail"]
        assert [entry["to_state"] for entry in trail][-1] == "completed"
        assert trail[-1]["changed_by"] == "it-team-validator"


def test_gate_decision_requires_reason_or_conditions(api):
    from fastapi.testclient import TestClient

    with TestClient(api.app) as client:
        engagement_id = client.post("/engagements", json={"description": "Test"}).json()["id"]
        client.post(f"/engagements/{engagement_id}/assess")
        client.post(f"/engagements/{engagement_id}/gate-review")
        recommendation = client.get(f"/engagements/{engagement_id}/recommendations").json()[0]

        response = client.post(
            f"/engagements/{engagement_id}/gate-review/{recommendation['id']}/decision",
            json={"decision": "DENIED"},
        )
        assert response.status_code == 422


def test_unknown_engagement_returns_404(api):
    from fastapi.testclient import TestClient

    with TestClient(api.app) as client:
        assert client.get("/engagements/999/recommendations").status_code == 404
        assert client.get("/engagements/999/roadmap").status_code == 404
        assert client.post("/engagements/999/gate-review").status_code == 404
        assert client.post("/engagements/999/gate-review/close").status_code == 404
        assert client.post("/engagements/999/execute").status_code == 404
        assert client.get("/engagements/999/actions").status_code == 404


def _drive_to_executing(client):
    """Walk one engagement through the whole lifecycle up to `executing`."""
    engagement_id = client.post("/engagements", json={"description": "Test"}).json()["id"]
    assert client.post(f"/engagements/{engagement_id}/assess").status_code == 202
    assert client.post(f"/engagements/{engagement_id}/gate-review").status_code == 202
    for recommendation in client.get(f"/engagements/{engagement_id}/recommendations").json():
        assert client.post(
            f"/engagements/{engagement_id}/gate-review/{recommendation['id']}/decision",
            json={"decision": "APPROVED"},
        ).status_code == 200
    assert client.post(f"/engagements/{engagement_id}/gate-review/close").status_code == 200
    assert client.post(f"/engagements/{engagement_id}/execute").status_code == 202
    return engagement_id


def test_gate_review_can_fail(api):
    """The gate is a step, not a formality: v0.3.4 closed it in the same call."""
    from fastapi.testclient import TestClient

    with TestClient(api.app) as client:
        engagement_id = client.post("/engagements", json={"description": "Test"}).json()["id"]
        client.post(f"/engagements/{engagement_id}/assess")
        client.post(f"/engagements/{engagement_id}/gate-review")
        assert client.get(f"/engagements/{engagement_id}").json()["status"] == "gate_review"

        # An undecided recommendation holds the gate open.
        assert client.post(f"/engagements/{engagement_id}/gate-review/close").status_code == 409

        recommendations = client.get(f"/engagements/{engagement_id}/recommendations").json()
        for recommendation in recommendations:
            client.post(
                f"/engagements/{engagement_id}/gate-review/{recommendation['id']}/decision",
                json={"decision": "DENIED", "reason": "Not justified by the evidence"},
            )
        rejected = client.post(f"/engagements/{engagement_id}/gate-review/close")
        assert rejected.status_code == 409
        assert "rejected" in rejected.json()["detail"]
        # No approved recommendation means no roadmap and no execution.
        assert client.get(f"/engagements/{engagement_id}").json()["status"] == "gate_review"
        assert client.post(f"/engagements/{engagement_id}/execute").status_code == 409

        # One approval is enough to pass, and the decision is audited as the gatekeeper's.
        client.post(
            f"/engagements/{engagement_id}/gate-review/{recommendations[0]['id']}/decision",
            json={"decision": "APPROVED"},
        )
        assert client.post(f"/engagements/{engagement_id}/gate-review/close").json()["approved"] == 1
        trail = client.get(f"/engagements/{engagement_id}/audit-trail").json()["audit_trail"]
        assert trail[-1]["changed_by"] == "it-team-gatekeeper"


def test_verdict_cannot_precede_execution(api):
    from fastapi.testclient import TestClient

    with TestClient(api.app) as client:
        engagement_id = client.post("/engagements", json={"description": "Test"}).json()["id"]
        premature = client.post(
            f"/engagements/{engagement_id}/validator-verdict",
            json={
                "verdict": "VALIDATED",
                "validator_agent": "it-team-validator",
                "executor_agent": "it-team-orchestrator",
                "evidence_ref": "synthetic-evidence",
            },
        )
        assert premature.status_code == 409

        # Actions cannot run before execution either.
        client.post(f"/engagements/{engagement_id}/dependencies", json=[{"action_id": "a"}])
        assert client.post(f"/engagements/{engagement_id}/actions/a/start").status_code == 409

        executing = _drive_to_executing(client)
        blank_evidence = client.post(
            f"/engagements/{executing}/validator-verdict",
            json={"verdict": "VALIDATED", "validator_agent": "it-team-validator",
                  "executor_agent": "it-team-orchestrator", "evidence_ref": "  "},
        )
        assert blank_evidence.status_code == 409
        mismatch = client.post(
            f"/engagements/{executing}/validator-verdict",
            json={
                "engagement_id": executing + 1,
                "verdict": "REJECTED",
                "validator_agent": "it-team-validator",
                "executor_agent": "it-team-orchestrator",
            },
        )
        assert mismatch.status_code == 409


def test_action_dependencies_are_enforced(api):
    from fastapi.testclient import TestClient

    with TestClient(api.app) as client:
        engagement_id = _drive_to_executing(client)
        endpoint = f"/engagements/{engagement_id}/dependencies"

        assert client.post(endpoint, json=[{"action_id": "mfa", "depends_on": ["ghost"]}]).status_code == 422
        assert client.post(endpoint, json=[{"action_id": "mfa", "depends_on": ["mfa"]}]).status_code == 422
        assert client.post(endpoint, json=[
            {"action_id": "a", "depends_on": ["b"]},
            {"action_id": "b", "depends_on": ["a"]},
        ]).status_code == 422

        graph = client.post(endpoint, json=[
            {"action_id": "ad-connect", "depends_on": []},
            {"action_id": "mfa", "depends_on": ["ad-connect"]},
        ])
        assert graph.status_code == 200
        assert client.get(f"/engagements/{engagement_id}/actions").json()["actions"][1]["blocked_by"] == ["ad-connect"]

        blocked = client.post(f"/engagements/{engagement_id}/actions/mfa/start")
        assert blocked.status_code == 409
        assert "ad-connect" in blocked.json()["detail"]
        assert client.post(f"/engagements/{engagement_id}/actions/unknown/start").status_code == 404

        assert client.post(f"/engagements/{engagement_id}/actions/ad-connect/start").status_code == 200
        # Completing an action that never ran is not a thing.
        assert client.post(f"/engagements/{engagement_id}/actions/ad-connect/complete").status_code == 200
        assert client.post(f"/engagements/{engagement_id}/actions/ad-connect/complete").status_code == 409
        assert client.post(f"/engagements/{engagement_id}/actions/mfa/start").status_code == 200
        assert client.get(f"/engagements/{engagement_id}/actions").json()["actions"][1]["blocked_by"] == []


def test_health_is_available(api):
    from fastapi.testclient import TestClient

    with TestClient(api.app) as client:
        health = client.get("/health").json()
        assert health["status"] == "ok"
        # The version has one source of truth: the VERSION file.
        assert health["version"] == (Path(__file__).resolve().parents[1] / "VERSION").read_text(encoding="utf-8").strip()
