
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Healthcare AI Platform",
    description="Cloud-native Healthcare API using HL7 FHIR",
    version="0.1.0"
)

# Definiert, wie ein Patient aussehen muss
class Patient(BaseModel):
    id: str
    name: str
    age: int

# Synthetische Testdaten
patients = [
    Patient(id="001", name="Max Mustermann", age=45),
    Patient(id="002", name="Anna Beispiel", age=32)
]

@app.get("/")
def home():
    return {"message": "Healthcare AI Platform is running"}

@app.get("/patients")
def get_patients():
    return patients

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    for patient in patients:
        if patient.id == patient_id:
            return patient

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )






from datetime import date

# Synthetische FHIR-R4-Patientendaten
fhir_patients = [
    {
        "resourceType": "Patient",
        "id": "001",
        "name": [
            {
                "use": "official",
                "family": "Mustermann",
                "given": ["Max"]
            }
        ],
        "gender": "male",
        "birthDate": "1981-04-12"
    },
    {
        "resourceType": "Patient",
        "id": "002",
        "name": [
            {
                "use": "official",
                "family": "Beispiel",
                "given": ["Anna"]
            }
        ],
        "gender": "female",
        "birthDate": "1994-06-15"
    }
]

@app.get("/fhir/Patient")
def get_fhir_patients():
    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(fhir_patients),
        "entry": [
            {"resource": patient}
            for patient in fhir_patients
        ]
    }

@app.get("/fhir/Patient/{patient_id}")
def get_fhir_patient(patient_id: str):
    for patient in fhir_patients:
        if patient["id"] == patient_id:
            return patient

    raise HTTPException(
        status_code=404,
        detail="FHIR Patient not found"
    )







from typing import Literal
from pydantic import Field

class HumanName(BaseModel):
    family: str = Field(min_length=1)
    given: list[str] = Field(min_length=1)


class FHIRPatientCreate(BaseModel):
    resourceType: Literal["Patient"]
    name: list[HumanName] = Field(min_length=1)
    gender: Literal[
        "male", "female", "other", "unknown"
    ] | None = None
    birthDate: str | None = None


@app.post("/fhir/Patient", status_code=201)
def create_fhir_patient(patient: FHIRPatientCreate):
    new_id = str(
        max(int(p["id"]) for p in fhir_patients) + 1
    ).zfill(3)

    new_patient = patient.model_dump(
        exclude_none=True
    )
    new_patient["id"] = new_id

    fhir_patients.append(new_patient)

    return new_patient
