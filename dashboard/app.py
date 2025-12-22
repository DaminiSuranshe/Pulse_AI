import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from api_client import (
    register_patient,
    upload_pulse,
    ml_predict,
    get_recommendations
)

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Ayurvedic Pulse Intelligence – Practitioner Dashboard",
    layout="wide"
)

st.title("🩺 Ayurvedic Pulse Intelligence Platform")
st.caption("Clinical Decision Support • Pilot Mode")

st.markdown("---")

# -------------------------------------------------
# Sidebar – Patient Registration
# -------------------------------------------------
st.sidebar.header("Register New Patient")

name = st.sidebar.text_input("Patient Name")
age = st.sidebar.number_input("Age", min_value=1, max_value=120)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])

if st.sidebar.button("Register Patient"):
    if name:
        result = register_patient(name, age, gender)
        st.sidebar.success(f"Patient ID: {result['patient_id']}")
    else:
        st.sidebar.error("Please enter patient name")

# -------------------------------------------------
# Pulse Upload Section
# -------------------------------------------------
st.markdown("## Pulse Upload & Analysis")

patient_id = st.text_input("Enter Patient ID")
sampling_rate = st.number_input("Sampling Rate (Hz)", value=125)
uploaded_file = st.file_uploader("Upload Pulse CSV", type=["csv"])

# -------------------------------------------------
# Main Analysis Trigger
# -------------------------------------------------
if st.button("Analyze Pulse"):

    if not uploaded_file or not patient_id:
        st.error("Please provide patient ID and pulse file")
        st.stop()

    with open("temp.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())

    result = upload_pulse(patient_id, sampling_rate, "temp.csv")

    if "error" in result:
        st.error("Backend error during pulse analysis")
        st.stop()

    st.success("Pulse analysis completed")

    # -------------------------------------------------
    # Extracted Pulse Features
    # -------------------------------------------------
    st.subheader("Extracted Pulse Features")
    features = result["features"]

    features_df = pd.DataFrame(
        features.items(),
        columns=["Feature", "Value"]
    )
    st.table(features_df)

    # -------------------------------------------------
    # Dosha Analysis
    # -------------------------------------------------
    st.subheader("Dosha Analysis")
    dosha = result["dosha_analysis"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Vata", dosha["vata"])
    col2.metric("Pitta", dosha["pitta"])
    col3.metric("Kapha", dosha["kapha"])

    st.info(f"**Dominant Dosha:** {dosha['dominant_dosha']}")
    st.write(dosha["explanation"])

    fig, ax = plt.subplots()
    ax.bar(
        ["Vata", "Pitta", "Kapha"],
        [dosha["vata"], dosha["pitta"], dosha["kapha"]]
    )
    ax.set_ylabel("Score")
    ax.set_title("Dosha Distribution")
    st.pyplot(fig)

    # -------------------------------------------------
    # ML Advisory (Optional)
    # -------------------------------------------------
    st.subheader("ML Advisory (Optional)")
    ml_result = ml_predict(features)

    if ml_result.get("ml_predicted_dosha") not in ["Unavailable", None]:
        st.metric(
            "Predicted Improvement Probability",
            ml_result.get("improvement_probability", "N/A")
        )
        st.info(f"ML Advisory Dosha: {ml_result['ml_predicted_dosha']}")
    else:
        st.info("ML advisory unavailable for this pulse signal.")

    # -------------------------------------------------
    # Diet & Lifestyle Recommendations
    # -------------------------------------------------
    st.subheader("Diet & Lifestyle Recommendations")

    rec = get_recommendations(dosha, season="Winter")

    if "error" in rec:
        st.warning("Recommendations unavailable")
        st.caption(rec.get("message", ""))
    else:
        st.success(f"Confidence Level: {rec['confidence_score']}")
        st.write(rec["explanation"])

        st.markdown("### Foods to Prefer")
        st.write(rec["recommendations"]["diet_prefer"])

        st.markdown("### Foods to Avoid")
        st.write(rec["recommendations"]["diet_avoid"])

        st.markdown("### Lifestyle Guidance")
        st.write(rec["recommendations"]["lifestyle"])
