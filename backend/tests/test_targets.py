from fastapi.testclient import TestClient
from app.main import app
 
client = TestClient(app)
 
def test_create_and_list_target():
    resp = client.post("/api/v1/targets", json={
        "name": "unit-test-host", "target_type": "generic", "hostname": "10.0.0.1"
    })
    assert resp.status_code == 201
    listed = client.get("/api/v1/targets").json()
    assert any(t["name"] == "unit-test-host" for t in listed)
