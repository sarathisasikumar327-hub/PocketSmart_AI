from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    r = client.get("/")
    assert r.status_code == 200
    assert "PocketSmart" in r.text

def test_docs():
    r = client.get("/docs")
    assert r.status_code == 200
