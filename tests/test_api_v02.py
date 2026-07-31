import importlib
import os
import sys

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
        recommendations = client.get(f"/engagements/{engagement_id}/recommendations").json()
        assert len(recommendations) == 3

        decision = client.post(
            f"/engagements/{engagement_id}/gate-review/{recommendations[0]['id']}/decision",
            json={"decision": "APPROVED_WITH_CONDITIONS", "conditions": ["Test verificabile"]},
        )
        assert decision.status_code == 200
        for recommendation in recommendations[1:]:
            response = client.post(
                f"/engagements/{engagement_id}/gate-review/{recommendation['id']}/decision",
                json={"decision": "APPROVED"},
            )
            assert response.status_code == 200

        roadmap = client.get(f"/engagements/{engagement_id}/roadmap").json()["roadmap"]
        assert len(roadmap) == 3
        assert roadmap[0]["decision"] == "APPROVED_WITH_CONDITIONS"

        execution = client.post(f"/engagements/{engagement_id}/execute")
        assert execution.status_code == 202
        assert client.get(f"/engagements/{engagement_id}").json()["status"] == "completed"


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
        assert client.post("/engagements/999/execute").status_code == 404


def test_health_is_available(api):
    from fastapi.testclient import TestClient

    with TestClient(api.app) as client:
        health = client.get("/health").json()
        assert health["status"] == "ok"
        assert health["version"] == "0.2.0"
