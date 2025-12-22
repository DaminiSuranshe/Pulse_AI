import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from api_client import register_patient, upload_pulse, ml_predict

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

    # Save temporary file
    with open("temp.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())

    result = upload_pulse(patient_id, sampling_rate, "temp.csv")

    if "error" in result:
        st.error("Backend error during pulse analysis")
        st.code(result.get("message", "Unknown error"))
        st.stop()

    st.success("Pulse analysis completed")

    # -------------------------------------------------
    # Extracted Pulse Features (SOURCE OF TRUTH)
    # -------------------------------------------------
    st.subheader("Extracted Pulse Features")

    features = result["features"]
    features_df = pd.DataFrame(
        features.items(),
        columns=["Feature", "Value"]
    )
    st.table(features_df)

    # -------------------------------------------------
    # Dosha Analysis (PRIMARY INTERPRETATION)
    # -------------------------------------------------
    st.subheader("Dosha Analysis")

    dosha = result["dosha_analysis"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Vata", dosha["vata"])
    col2.metric("Pitta", dosha["pitta"])
    col3.metric("Kapha", dosha["kapha"])

    st.info(f"**Dominant Dosha:** {dosha['dominant_dosha']}")
    st.write(dosha["explanation"])

    # Visualization
    fig, ax = plt.subplots()
    ax.bar(
        ["Vata", "Pitta", "Kapha"],
        [dosha["vata"], dosha["pitta"], dosha["kapha"]]
    )
    ax.set_ylabel("Score")
    ax.set_title("Dosha Distribution")
    st.pyplot(fig)

    # -------------------------------------------------
    # ML Advisory (OPTIONAL – NEVER BLOCKS)
    # -------------------------------------------------
    st.subheader("ML Advisory (Optional)")

    with st.spinner("Running ML advisory analysis..."):
        ml_result = ml_predict(features)

    if ml_result.get("ml_predicted_dosha") in ["Unavailable", "Insufficient data"]:
        st.info("ML advisory unavailable for this pulse signal.")
        st.caption(ml_result.get("note", ""))
    else:
        st.metric(
            "Predicted Improvement Probability",
            ml_result.get("improvement_probability", "N/A")
        )
        st.info(f"ML Advisory Dosha: {ml_result['ml_predicted_dosha']}")
        st.caption(ml_result.get("note", ""))

