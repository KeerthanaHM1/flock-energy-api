
import httpx
import respx

from fastapi.testclient import TestClient

from app.main import app
from app.config import settings


BASE_URL = settings.urja_base_url


def test_root_endpoint():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Flock Energy API is running"


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_openapi_documentation():
    with TestClient(app) as client:
        response = client.get("/openapi.json")

    assert response.status_code == 200

    paths = response.json()["paths"]
    assert "/api/meters" in paths
    assert "/api/meters/{meter_id}/geo" in paths
    assert "/api/meters/{meter_id}/energy" in paths
    assert "/api/transformers" in paths


@respx.mock
def test_list_meters():
    respx.post(f"{BASE_URL}/login").mock(
        return_value=httpx.Response(200)
    )

    respx.get(f"{BASE_URL}/portal/meters/search").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "meterId": "J100001",
                        "serialNo": "GE84132",
                        "make": "L&T",
                    }
                ],
                "total": 1,
                "page": 1,
                "pageSize": 20,
            },
        )
    )

    with TestClient(app) as client:
        response = client.get("/api/meters?page=1")

    assert response.status_code == 200
    assert response.json()["data"][0]["meterId"] == "J100001"


@respx.mock
def test_meter_geo():
    respx.post(f"{BASE_URL}/login").mock(
        return_value=httpx.Response(200)
    )

    respx.get(
        f"{BASE_URL}/portal/meters/J100001/geo"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "data": {
                    "latitude": "12.97",
                    "longitude": "77.59",
                }
            },
        )
    )

    with TestClient(app) as client:
        response = client.get("/api/meters/J100001/geo")

    assert response.status_code == 200
    assert response.json()["data"]["latitude"] == "12.97"


@respx.mock
def test_meter_energy():
    respx.post(f"{BASE_URL}/login").mock(
        return_value=httpx.Response(200)
    )

    respx.get(
        f"{BASE_URL}/portal/meters/J100001/energy"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "timestamp": "23/06/2026 23:30",
                        "kwh": "12.5",
                        "kvah": "13.0",
                    }
                ]
            },
        )
    )

    with TestClient(app) as client:
        response = client.get("/api/meters/J100001/energy")

    assert response.status_code == 200
    assert response.json()["data"][0]["kwh"] == "12.5"


@respx.mock
def test_list_transformers():
    respx.post(f"{BASE_URL}/login").mock(
        return_value=httpx.Response(200)
    )

    respx.get(f"{BASE_URL}/portal/dts").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "code": "DT-001",
                        "name": "Malviya Nagar DT 1",
                        "feederCode": "F-001",
                        "capacityKva": 100,
                    }
                ],
                "total": 1,
                "page": 1,
                "pageSize": 20,
            },
        )
    )

    with TestClient(app) as client:
        response = client.get("/api/transformers?page=1")

    assert response.status_code == 200
    assert response.json()["data"][0]["code"] == "DT-001"

@respx.mock
def test_meter_upstream_failure():
    respx.post(f"{BASE_URL}/login").mock(
        return_value=httpx.Response(200)
    )

    respx.get(
        f"{BASE_URL}/portal/meters/search"
    ).mock(
        return_value=httpx.Response(503)
    )

    with TestClient(app) as client:
        response = client.get("/api/meters?page=1")

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "Unable to retrieve meter data from the legacy portal."
    )
