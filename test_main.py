
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Healthcare AI Platform is running"
    )


def test_get_patients():
    response = client.get("/fhir/Patient")

    assert response.status_code == 200
    assert response.json()["resourceType"] == "Bundle"


def test_create_patient():
    new_patient = {
        "resourceType": "Patient",
        "name": [
            {
                "family": "Test",
                "given": ["Maria"]
            }
        ],
        "gender": "female",
        "birthDate": "2000-01-01"
    }

    response = client.post(
        "/fhir/Patient",
        json=new_patient
    )

    assert response.status_code == 201
    assert response.json()["resourceType"] == "Patient"
    assert "id" in response.json()
