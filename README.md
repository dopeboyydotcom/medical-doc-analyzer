# Medical Document Analyzer
**Live app:** https://medical-doc-analyzer-clms4v3mbswhh9byfrm9aj.streamlit.app

An intelligent web app that helps turn messy clinical PDFs into clear, structured medical data.

## What it does

- Upload any clinical PDF (discharge summary, medical report, prescription)
- Automatically extracts diagnoses, medications, allergies, key dates, and red flags
- Highlights potentially dangerous drug-allergy interactions
- Lets you ask follow‑up questions about the document in plain language.

## Important note on data privacy

This project uses only synthetic and publicly available sample documents.
No real patient data was used or stored at any point during development.
Any real-world deployment would require full HIPAA compliance review.

## Tech stack

- Python 3.11
- Groq API (Llama 3.3 70B)
- Streamlit
- PyMuPDF
- python-dotenv

## How to run locally

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your Groq API key: `GROQ_API_KEY=your_key_here`
6. Run: `streamlit run app.py`

## Built by

Ugorji Maxwell.  Built as part of a healthcare AI engineering portfolio