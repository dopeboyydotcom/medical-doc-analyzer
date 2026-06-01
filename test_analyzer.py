import json
from Analyzer import analyze_document

with open("sample.pdf", "rb") as f:
    pdf_bytes = f.read()

result = analyze_document(pdf_bytes)

print(json.dumps(result, indent=2))