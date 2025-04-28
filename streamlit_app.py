import streamlit as st
import json
import plotly.express as px
import pandas as pd
from PIL import Image

# Streamlit App
st.set_page_config(page_title="Clinical Dashboard", layout="wide")

# Add Tailwind CSS via CDN
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown('<h1 class="text-3xl font-bold text-blue-600 mb-4">Clinical Dashboard for Patient (MRN: #1512015)</h1>', unsafe_allow_html=True)
st.markdown('<p class="text-gray-600">Generated: April 28, 2025</p>', unsafe_allow_html=True)

# Load Data
try:
    with open("patient_output_wow.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("Error: patient_output_wow.json not found. Please ensure the file is in the same directory.")
    st.stop()

patient_info = data["Patient Info"]
alerts = data["Clinical Alerts and Diagnoses"]
risk_scores = data["Risk Scores"]
care_plan = data["Care Plan"]

# Sidebar Filters
st.sidebar.markdown('<h2 class="text-xl font-bold text-blue-600">Filters</h2>', unsafe_allow_html=True)
alert_filter = st.sidebar.multiselect("Select Alerts to Display", alerts, default=alerts)
risk_filter = st.sidebar.multiselect("Select Risks to Display", list(risk_scores.keys()), default=list(risk_scores.keys()))

# Patient Info
st.markdown('<h2 class="text-2xl font-bold text-blue-600 mt-6">Patient Information</h2>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
col1.markdown(f'<p class="text-gray-800"><strong>Name:</strong> {patient_info["Name"]}</p>', unsafe_allow_html=True)
col1.markdown(f'<p class="text-gray-800"><strong>DOB:</strong> {patient_info["Date of Birth"]}</p>', unsafe_allow_html=True)
col1.markdown(f'<p class="text-gray-800"><strong>Gender:</strong> {patient_info["Gender"]}</p>', unsafe_allow_html=True)
col2.markdown(f'<p class="text-gray-800"><strong>MRN:</strong> {patient_info["MRN"]}</p>', unsafe_allow_html=True)
col2.markdown(f'<p class="text-gray-800"><strong>PCP:</strong> {patient_info["PCP"]}</p>', unsafe_allow_html=True)
col2.markdown(f'<p class="text-gray-800"><strong>Specialists:</strong> {patient_info["Specialists"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="text-gray-800"><strong>Allergies:</strong> {patient_info["Allergies"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="text-gray-800"><strong>Surgical History:</strong> {patient_info["Past Surgical History"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="text-gray-800"><strong>Imaging:</strong> {patient_info["Imaging"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="text-gray-800"><strong>Labs:</strong> {patient_info["Lab Results"]}</p>', unsafe_allow_html=True)

# Clinical Alerts
st.markdown('<h2 class="text-2xl font-bold text-blue-600 mt-6">Clinical Alerts and Diagnoses</h2>', unsafe_allow_html=True)
for alert in alert_filter:
    # Highlight "ALERT" in red bold
    formatted_alert = alert.replace(
        "ALERT",
        '<span style="color: red; font-weight: bold;">ALERT</span>'
    )
    st.markdown(
        f'<p class="text-gray-800 mb-2">{formatted_alert}</p>',
        unsafe_allow_html=True
    )

# Risk Scores
st.markdown('<h2 class="text-2xl font-bold text-blue-600 mt-6">Risk Scores</h2>', unsafe_allow_html=True)
filtered_risks = {k: v for k, v in risk_scores.items() if k in risk_filter}
df_risks = pd.DataFrame(list(filtered_risks.items()), columns=['Risk', 'Score'])
fig_risks = px.bar(df_risks, x='Risk', y='Score', title='Clinical Risk Scores', color='Risk')
st.plotly_chart(fig_risks)

# Care Plan
st.markdown('<h2 class="text-2xl font-bold text-blue-600 mt-6">Prioritized Care Plan</h2>', unsafe_allow_html=True)
for i, item in enumerate(care_plan):
    st.markdown(f'<p class="text-gray-800">- Priority {i+1}: {item["action"]} (Score: {item["priority"]}%)</p>', unsafe_allow_html=True)
try:
    with open("care_plan_pie.png", "rb") as f:
        img = Image.open(f)
        if img.size[0] * img.size[1] < 1000:  # Detect placeholder
            st.warning("Care Plan Pie chart is unavailable due to rendering issues.")
        else:
            st.image("care_plan_pie.png", caption="Care Plan Priorities")
except FileNotFoundError:
    st.error("Error: care_plan_pie.png not found.")

# Imaging Timeline
st.markdown('<h2 class="text-2xl font-bold text-blue-600 mt-6">Imaging Timeline</h2>', unsafe_allow_html=True)
try:
    with open("imaging_timeline.png", "rb") as f:
        img = Image.open(f)
        if img.size[0] * img.size[1] < 1000:  # Detect placeholder
            st.warning("Imaging Timeline is unavailable due to rendering issues. Check imaging data extraction.")
        else:
            st.image("imaging_timeline.png", caption="Imaging Timeline")
except FileNotFoundError:
    st.error("Error: imaging_timeline.png not found.")

# Download Summary
st.markdown('<h2 class="text-2xl font-bold text-blue-600 mt-6">Download Summary</h2>', unsafe_allow_html=True)
try:
    with open("clinical_summary_wow.txt", "r") as f:
        summary = f.read()
    st.download_button("Download Clinical Summary", summary, file_name="clinical_summary_wow.txt", key="download_summary")
except FileNotFoundError:
    st.error("Error: clinical_summary_wow.txt not found.")

st.markdown('<p class="text-gray-600 mt-6"><strong>Note:</strong> Ensure HIPAA compliance when handling patient data.</p>', unsafe_allow_html=True)
