import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Check API key
if not api_key:
    st.error("❌ No API key found. Please add GEMINI_API_KEY in your .env file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=api_key)

# Streamlit page setup
st.set_page_config(page_title="AI Personal Assistant", page_icon="🤖")
st.title("🤖 AI Personal Assistant")
st.write("Ask me to summarize meetings, reply to emails, or find information!")

task = st.text_area("Enter your task/query", placeholder="Example: Summarize today's meeting about project deadlines")

# Model selector (so you can switch if one fails)
model_choice = st.selectbox(
    "Choose AI Model",
    ["gemini-1.5-pro", "gemini-1.5-flash"],  # you can add others if available
    index=0
)

if st.button("Generate Response"):
    if task.strip() == "":
        st.warning("⚠️ Please enter a task or query.")
    else:
        with st.spinner("Thinking..."):
            try:
                model = genai.GenerativeModel(model_choice)
                response = model.generate_content(task)

                if hasattr(response, "text"):
                    st.subheader("✅ AI Response:")
                    st.write(response.text)
                else:
                    st.error("⚠️ No response text received. Try again or switch model.")

            except Exception as e:
                st.error(f"❌ Error while generating response: {str(e)}")
                st.info("Tip: Try switching to gemini-1.5-flash if gemini-1.5-pro fails.")

