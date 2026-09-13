import os
import streamlit as st
from PIL import Image
from google import genai

from agents.state import TutorState
from agents.parser import parse_multimodal_submission
from agents.verifier import run_verification
from agents.tutor import generate_socratic_intervention

st.set_page_config(page_title="SocraticAI Tutor", page_icon="🎓", layout="wide")

# API Initialization
api_key = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key) if api_key else None

if "tutor_state" not in st.session_state:
    st.session_state.tutor_state = TutorState()
if "step_expectations" not in st.session_state:
    st.session_state.step_expectations = []

st.title("🎓 SocraticAI: Autonomous Multi-Step Assignment Reviewer")
st.caption("Closed-Loop Agentic Tutoring powered by Deterministic Verification Tools")

with st.sidebar:
    st.header("⚙️ Configuration")
    input_key = st.text_input("Gemini API Key", value=api_key, type="password")
    if input_key:
        client = genai.Client(api_key=input_key)
        
    st.markdown("---")
    st.markdown("### 📊 Agent Status")
    st.write(f"**Current Scaffolding Tier:** Tier {st.session_state.tutor_state.hint_tier} / 4")
    st.write(f"**Active Error Step:** {st.session_state.tutor_state.active_error_step or 'None'}")
    st.write(f"**Assignment Resolved:** {st.session_state.tutor_state.resolved}")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Student Artifact Input")
    uploaded_file = st.file_uploader("Upload handwritten work or diagram", type=["png", "jpg", "jpeg"])
    text_input = st.text_area("Or enter code / steps directly", height=150)
    
    if st.button("🚀 Analyze & Review Assignment", use_container_width=True):
        if not client:
            st.error("Please enter a valid Gemini API Key in the sidebar.")
        else:
            with st.spinner("Agent parsing multimodal input and checking with tools..."):
                img = Image.open(uploaded_file) if uploaded_file else None
                parsed = parse_multimodal_submission(client, image=img, text_submission=text_input)
                
                state = TutorState(
                    submission_type=parsed.get("submission_type", "math"),
                    parsed_steps=parsed.get("steps", []),
                    hint_tier=1
                )
                st.session_state.step_expectations = parsed.get("step_expectations", [])
                
                # Deterministic tool verification
                state = run_verification(state, st.session_state.step_expectations)
                st.session_state.tutor_state = state
                
                # Initial Socratic Intervention
                hint = generate_socratic_intervention(client, state)
                st.session_state.tutor_state.conversation_history.append({"role": "assistant", "content": hint})

with col2:
    st.subheader("🔍 Verification Trace & Socratic Dialogue")
    state = st.session_state.tutor_state
    
    if state.parsed_steps:
        st.markdown("#### Parsed Steps & Tool Validation")
        for v in state.verifications:
            status_icon = "✅" if v.is_correct else "❌"
            st.markdown(f"**Step {v.step_number}:** `{v.raw_content}` | {status_icon} *{v.diagnostic_details}*")
            
        st.markdown("---")
        st.markdown("#### Interactive Socratic Conversation")
        for msg in state.conversation_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        if not state.resolved:
            student_reply = st.chat_input("Enter your corrected step or ask a question...")
            if student_reply:
                state.conversation_history.append({"role": "user", "content": student_reply})
                
                # Dynamic hint tier escalation on consecutive attempts
                if state.hint_tier < 4:
                    state.hint_tier += 1
                    
                new_hint = generate_socratic_intervention(client, state)
                state.conversation_history.append({"role": "assistant", "content": new_hint})
                st.rerun()
