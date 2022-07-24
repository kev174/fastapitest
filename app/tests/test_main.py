from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_main_resource():
    response_auth = client.get(f"/inventory/foo")
    assert response_auth.status_code == 200