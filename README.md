# Supply Chain SmartPT: Local LLM Inventory Assistant

## Overview
A privacy-first, local LLM-powered assistant for car parts supply chain optimization. Ingests Excel and PDF inventory data, enables natural language Q&A, summarization, and trend insights via a Streamlit UI. Powered by Mistral LLM, ChromaDB, and LangChain.

## Features
- Upload and parse Excel/PDF inventory files
- Natural language Q&A and summarization
- Trend and anomaly detection (future scope)
- Role-based authentication
- Local vector search (ChromaDB)

## Setup
1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure your local Mistral LLM is running and accessible
4. Run the app:
   ```bash
   streamlit run app/ui/main.py
   ```

## Directory Structure
- `app/etl/` - Data ingestion (Excel, PDF)
- `app/llm/` - LLM interface
- `app/vectordb/` - ChromaDB client
- `app/auth/` - Authentication logic
- `app/ui/` - Streamlit UI
- `data/` - Sample inventory files

## Future Scope
- Fine-tune LLM on historical data
- Voice interface
- IoT integration
- Automated ordering