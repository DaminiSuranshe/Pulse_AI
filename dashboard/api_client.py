import requests

BASE_URL = "http://127.0.0.1:8000"


def register_patient(name, age, gender):
    response = requests.post(
        f"{BASE_URL}/patients/register",
        params={"name": name, "age": age, "gender": gender}
    )
    return response.json()


def upload_pulse(patient_id, sampling_rate, file_path):
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(
            f"{BASE_URL}/pulse/upload/{patient_id}",
            params={"sampling_rate": sampling_rate},
            files=files
        )

    if response.status_code != 200:
        return {
            "error": True,
            "status_code": response.status_code,
            "message": response.text
        }

    return response.json()
