from fastapi.testclient import TestClient
from main import app
import pytest


@pytest.mark.parametrize("filters,expected_code", [
    ({"city": "lim"}, 200),
    ({"zip_code": "03180002"}, 200),
    ({"neighborhood": "vila"}, 200),
    ({}, 400),
    ({"city": "s."}, 404),
    ({"zip_code": "012"}, 404),
    ({"neighborhood": "jardim"}, 404),
])
def test_search(monkeypatch, filters, expected_code):
    monkeypatch.setenv("LOCATION_TABLE_PATH", "./tests/assets/locations.csv")
    monkeypatch.setenv("ZIP_CODE_TABLE_PATH", "./tests/assets/cep.csv")
    with TestClient(app) as client:
        resp = client.get("/location/v1/search", params=filters)
        assert resp.status_code == expected_code