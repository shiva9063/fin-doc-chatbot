Financial Document Q&A Assistant

A Streamlit-based web application that processes financial documents (PDF & Excel) and allows users to interactively ask questions about financial data using natural language. The system extracts revenue, expenses, profits, and other financial metrics from uploaded documents and provides accurate answers with a conversational interface.

🚀 Features
📂 Document Processing

Upload PDF and Excel financial documents

Extract text and numerical data from reports

Supports Income Statements, Balance Sheets, and Cash Flow Statements

Handles varied layouts and formats

💬 Question-Answering System

Ask natural language questions about financial data

Retrieve metrics like Revenue, Expenses, Profits, Liabilities, Assets, Cash Flow

Conversational flow: supports follow-up questions

Provides clear and structured responses

🖥️ Technical Implementation

Streamlit for the web interface

Ollama with LLaMA 3 (local SLM) for Q&A

Pandas & OpenPyXL for Excel handling

PyPDF2 for PDF extraction

Runs locally (no cloud dependency)

Built-in error handling and user feedback

🎨 User Interface

Simple, clean Streamlit interface

Upload and process documents seamlessly

Interactive chat box for asking questions

Display extracted financial data in tables & text format