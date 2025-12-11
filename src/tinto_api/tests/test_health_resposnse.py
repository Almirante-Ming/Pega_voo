from fastapi.testclient import TestClient
from tinto.main import tinto

client = TestClient(tinto)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "working" in str(data)

