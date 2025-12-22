import requests

BASE_URL = "http://127.0.0.1:8000"


# -------------------------------------------------
# Patient Registration
# -------------------------------------------------
def register_patient(name, age, gender):
    response = requests.post(
        f"{BASE_URL}/patients/register",
        params={
            "name": name,
            "age": age,
            "gender": gender
        }
    )

    try:
        return response.json()
    except Exception:
        return {
            "error": True,
            "message": "Invalid response from backend during patient registration"
        }


# -------------------------------------------------
# Pulse Upload & Core Analysis
# -------------------------------------------------
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

    try:
        return response.json()
    except Exception:
        return {
            "error": True,
            "message": "Invalid response from backend during pulse analysis"
        }


# -------------------------------------------------
# ML Advisory (OPTIONAL – NEVER BLOCKS UI)
# -------------------------------------------------
def ml_predict(features):
    try:
        response = requests.post(
            f"{BASE_URL}/ml/predict",
            json=features,
            timeout=10
        )
    except Exception as e:
        return {
            "ml_predicted_dosha": "Unavailable",
            "confidence": "Low",
            "note": f"ML service unreachable: {str(e)}"
        }

    if response.status_code != 200:
        return {
            "ml_predicted_dosha": "Unavailable",
            "confidence": "Low",
            "note": f"ML API error ({response.status_code})"
        }

    try:
        return response.json()
    except Exception:
        return {
            "ml_predicted_dosha": "Unavailable",
            "confidence": "Low",
            "note": "Invalid ML response format"
        }
