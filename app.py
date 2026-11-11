import os
import streamlit as st
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()
st.set_page_config(page_title="Deal-Desk Multi-Agent Triage", page_icon="⚖️")
st.title("⚖️ Autonomous Corporate Deal-Desk & Risk Triage")

client = AIProjectClient(
    endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
    credential=DefaultAzureCredential()
)
prompt = st.text_area("Paste Vendor or Client Deal Proposal:", height=150)

if st.button("Run Multi-Agent Review") and prompt:
    with st.spinner("Orchestrating Compliance Auditor, Margin Analyst & Director..."):
        openai_client = client.get_openai_client()
        response = openai_client.responses.create(
            input=[{"role": "user", "content": prompt}],
            extra_body={"agent": {"name": os.getenv("FOUNDRY_AGENT_NAME"), "type": "agent_reference"}}
        )
        st.markdown(response.output_text)