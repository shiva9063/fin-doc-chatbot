import streamlit as st
import ollama

import os
from utils.pdf_reader import pdf_read
from utils.excel_reader import excel_read

# Define paths for saving user files
BASE_DIR = "user_files"
PDF_DIR = os.path.join(BASE_DIR, "pdfs")
EXCEL_DIR = os.path.join(BASE_DIR, "excels")

# Create folders if not exist
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(EXCEL_DIR, exist_ok=True)


# --- Page Config ---
st.set_page_config(page_title="Financial Document Q&A", layout="wide")

# --- Title & Description ---
st.title("Financial Document Q&A Assistant")
st.markdown("Upload a **PDF** or **Excel** file containing financial data, then ask questions interactively.")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_text" not in st.session_state:
    st.session_state.file_text = ""
if "file_processed" not in st.session_state:
    st.session_state.file_processed = False

# --- Sidebar for Upload ---
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "xlsx"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.type == "application/pdf":
                # geting text from utils pdf python file
                text=pdf_read(uploaded_file,PDF_DIR) # utils pdf_reader
                if text.strip():
                    st.session_state.file_text = text
                    st.session_state.file_processed = True
                    st.success("PDF uploaded and processed.")
                else:
                    st.warning("No text extracted from PDF.")
            
            elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
                # read text from the uploaded file 
                text=excel_read(uploaded_file,EXCEL_DIR) # function in utils excel_reader

                st.session_state.file_text = text
                st.session_state.file_processed = True
                st.success("Excel uploaded and processed.")
        
        except Exception as e:
            st.error(f"Error processing file: {e}")

    if st.button("Clear Chat & Reset"):
        st.session_state.messages = []
        st.session_state.file_text = ""
        st.session_state.file_processed = False
        st.success("Chat and file reset!")

# --- Display Extracted Info (Collapsible) ---
if st.session_state.file_processed:
    with st.expander("Extracted Document Content (Preview)"):
        st.text_area("Extracted Content", st.session_state.file_text[:3000], height=200)

# --- Chat History ---
st.subheader("Chat with your document")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Chat Input ---
if prompt := st.chat_input("Ask a question about your document..."):
    try:
        # Build context prompt
        if st.session_state.file_text:
            context_prompt = (
                "You are a financial assistant. Use the following document content "
                "to answer clearly and concisely.\n\n"
                f"Document Content:\n{st.session_state.file_text}\n\n"
                f"User Question: {prompt}"
            )
        else:
            context_prompt = prompt

        # Save user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Query Ollama
        response = ollama.chat(
            model="llama3",  
            messages=[{"role": "user", "content": context_prompt}],
            stream=False
        )

        if "message" in response and "content" in response["message"]:
            answer = response["message"]["content"]
        else:
            answer = "No response received from the model."

        # Save assistant message
        st.session_state.messages.append({"role": "assistant", "content": answer})

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(answer)

    except Exception as e:
        st.error(f"Failed to get response from Ollama: {e}")
