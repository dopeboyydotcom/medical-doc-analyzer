from dotenv import load_dotenv
from groq import Groq
import fitz
import json
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

ABBREVIATIONS = {
    "pcn": "penicillin",
    "asa": "aspirin",
    "htn": "hypertension",
    "dm": "diabetes mellitus",
    "bd": "twice daily",
    "od": "once daily",
    "tds": "three times daily",
}

def resolve_abbreviations(items):
    resolved = []
    for item in items:
        lower = item.lower().strip()
        resolved.append(ABBREVIATIONS.get(lower, item))
    return resolved

def deduplicate(items):
    unique = []
    for item in items:
        item_lower = item.lower().strip()
        is_duplicate = False
        for kept in unique:
            kept_lower = kept.lower().strip()
            if item_lower in kept_lower or kept_lower in item_lower:
                is_duplicate = True
                break
        if not is_duplicate:
            unique.append(item)
    return unique

def validate_pdf(file_bytes):
    if not file_bytes:
        return False, "No file was uploaded. Please upload a PDF."
    if len(file_bytes) < 100:
        return False, "File is too small to be a valid PDF."
    if not file_bytes.startswith(b"%PDF"):
        return False, "This does not appear to be a valid PDF file."
    if len(file_bytes) > 10 * 1024 * 1024:
        return False, "File is too large. Please upload a PDF under 10MB."
    return True, "ok"

def extract_text_from_pdf(pdf_bytes):
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        if not text.strip():
            return None, "This PDF appears to be a scanned image. Only text-based PDFs are supported currently."
        return text, "ok"
    except Exception as e:
        return None, f"Could not read PDF: {str(e)}"
    

def analyze_document(pdf_bytes):
    is_valid, message = validate_pdf(pdf_bytes)
    if not is_valid:
        return {"error": message}

    pdf_text, message = extract_text_from_pdf(pdf_bytes)
    if pdf_text is None:
        return {"error": message}

    if len(pdf_text) > 80000:
        pdf_text = pdf_text[:80000]

    system_prompt = """You are a medical document analyst.
Extract the following from the clinical document and return
ONLY valid JSON, no other text, no backticks, no explanation:

{
  "diagnoses": ["list of conditions"],
  "medications": [{"name": "...", "dose": "..."}],
  "allergies": ["list"],
  "key_dates": {"admission": "...", "discharge": "..."},
  "red_flags": ["anything urgent or abnormal"]
}

If a field is not found, return an empty list or null."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": pdf_text}
            ]
        )
        raw = response.choices[0].message.content

        try:
            data = json.loads(raw)
            if "allergies" in data and data["allergies"]:
                data["allergies"] = deduplicate(resolve_abbreviations(data["allergies"]))
            if "diagnoses" in data and data["diagnoses"]:
                data["diagnoses"] = deduplicate(data["diagnoses"])
            return data
        except json.JSONDecodeError:
            return {"error": "Could not parse response", "raw": raw}

    except Exception as e:
        return {"error": f"AI request failed: {str(e)}"}

def extract_pdf_text(pdf_bytes):
    text, _ = extract_text_from_pdf(pdf_bytes)
    return text or ""
    

def ask_question(pdf_text, messages):
    system = f"""You are a medical document assistant.
Answer questions about the following clinical document clearly and concisely.
If the answer is not in the document, say so honestly.

DOCUMENT:
{pdf_text}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system}] + messages
    )
    return response.choices[0].message.content
    