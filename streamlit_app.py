import streamlit as st
import json
import plotly.express as px
import pandas as pd
from PIL import Image

# Streamlit App
st.set_page_config(page_title="Clinical Dashboard", layout="wide")

st.title("Clinical Dashboard for Patient (MRN: #1512015)")
st.markdown("Generated: April 28, 2025")

# Load Data
with open("patient_output_wow.json", "r") as f:
    data = json.load(f)

patient_info = data["Patient Info"]
alerts = data["Clinical Alerts and Diagnoses"]
risk_scores = data["Risk Scores"]
care_plan = data["Care Plan"]

# Sidebar Filters
st.sidebar.header("Filters")
alert_filter = st.sidebar.multiselect("Select Alerts to Display", alerts, default=alerts)
risk_filter = st.sidebar.multiselect("Select Risks to Display", list(risk_scores.keys()), default=list(risk_scores.keys()))

# Patient Info
st.header("Patient Information")
col1, col2 = st.columns(2)
col1.write(f"**Name**: {patient_info['Name']}")
col1.write(f"**DOB**: {patient_info['Date of Birth']}")
col1.write(f"**Gender**: {patient_info['Gender']}")
col2.write(f"**MRN**: {patient_info['MRN']}")
col2.write(f"**PCP**: {patient_info['PCP']}")
col2.write(f"**Specialists**: {patient_info['Specialists']}")
st.write(f"**Allergies**: {patient_info['Allergies']}")
st.write(f"**Surgical History**: {patient_info['Past Surgical History']}")
st.write(f"**Imaging**: {patient_info['Imaging']}")
st.write(f"**Labs**: {patient_info['Lab Results']}")

# Clinical Alerts
st.header("Clinical Alerts and Diagnoses")
for alert in alert_filter:
    st.markdown(f"- {alert}")

# Risk Scores
st.header("Risk Scores")
filtered_risks = {k: v for k, v in risk_scores.items() if k in risk_filter}
df_risks = pd.DataFrame(list(filtered_risks.items()), columns=['Risk', 'Score'])
fig_risks = px.bar(df_risks, x='Risk', y='Score', title='Clinical Risk Scores', color='Risk')
st.plotly_chart(fig_risks)
st.image("risk_scores.png", caption="Static Risk Scores")

# Care Plan
st.header("Prioritized Care Plan")
for i, item in enumerate(care_plan):
    st.markdown(f"- Priority {i+1}: {item['action']} (Score: {item['priority']}%)")
st.image("care_plan_pie.png", caption="Care Plan Priorities")

# Imaging Timeline
st.header("Imaging Timeline")
st.image("imaging_timeline.png", caption="Imaging Timeline")

# Download Summary
st.header("Download Summary")
with open("clinical_summary_wow.txt", "r") as f:
    summary = f.read()
st.download_button("Download Clinical Summary", summary, file_name="clinical_summary_wow.txt")

st.markdown("**Note**: Ensure HIPAA compliance when handling patient data.")