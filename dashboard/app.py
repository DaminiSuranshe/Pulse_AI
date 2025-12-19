import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from api_client import register_patient, upload_pulse

st.set_page_config(
    page_title="Ayurvedic Pulse Intelligence – Practitioner Dashboard",
    layout="wide"
)

st.title("🩺 Ayurvedic Pulse Intelligence Platform")
st.caption("Clinical Decision Support • Pilot Mode")

st.markdown("---")

# Sidebar – Patient Registration
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

st.markdown("## Pulse Upload & Analysis")

patient_id = st.text_input("Enter Patient ID")
sampling_rate = st.number_input("Sampling Rate (Hz)", value=125)

uploaded_file = st.file_uploader("Upload Pulse CSV", type=["csv"])

if st.button("Analyze Pulse"):
    if uploaded_file and patient_id:
        with open("temp.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())

        result = upload_pulse(patient_id, sampling_rate, "temp.csv")

        if "error" in result:
            st.error("Backend error during pulse analysis")
            st.code(result["message"])
            st.stop()

        st.success("Pulse analysis completed")

        st.subheader("Extracted Pulse Features")
        features_df = pd.DataFrame(result["features"].items(), columns=["Feature", "Value"])
        st.table(features_df)

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
        ax.bar(["Vata", "Pitta", "Kapha"],
               [dosha["vata"], dosha["pitta"], dosha["kapha"]])
        ax.set_ylabel("Score")
        ax.set_title("Dosha Distribution")
        st.pyplot(fig)

    else:
        st.error("Please provide patient ID and pulse file")
