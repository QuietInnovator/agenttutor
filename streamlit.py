import streamlit as st
import asyncio
from agents_demo import triage_agent
from agents import Runner

# Async runner utility
def run_async(coro):
    return asyncio.run(coro)

# Function to run triage agent
async def process_question(question: str):
    result = await Runner.run(triage_agent, question)
    return result

# Streamlit UI
st.set_page_config(page_title="Azair - Homework Tutor", page_icon="📘")
st.title("📘 Azair Homework Tutor")
st.markdown("Ask a **math** or **history** homework question:")

# Input box
user_question = st.text_input("Your question")

if st.button("Submit") and user_question:
    with st.spinner("Analyzing your question..."):
        result = run_async(process_question(user_question))

    # If guardrail blocked the question, show error (built-in in result metadata)
    if hasattr(result, "guardrail_outputs"):
        guardrail = result.guardrail_outputs[0]  # only one guardrail used
        if guardrail["tripwire_triggered"]:
            st.error("🚫 This doesn't seem like a homework-related question.")
            st.markdown(f"**Reason:** {guardrail['output_info']['reasoning']}")
        else:
            st.success("✅ Passed guardrail check!")
    else:
        st.success("✅ No guardrail triggered.")

    # Show agent trace if available
    if hasattr(result, "trace"):
        st.markdown("### 🧠 Agent Reasoning Trace")
        for step in result.trace:
            st.markdown(f"**Agent:** {step['agent_name']}")
            st.markdown(f"- **Input:** {step['input']}")
            st.markdown(f"- **Output:** {step['output']}")
            st.markdown("---")

    # Show final result
    st.markdown("### ✅ Final Answer")
    st.success(result.final_output)

