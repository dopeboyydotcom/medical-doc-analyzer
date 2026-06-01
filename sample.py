from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=12)

lines = [
    "DISCHARGE SUMMARY",
    "",
    "Patient: John Doe",
    "DOB: 15/03/1965",
    "Admission Date: 01/05/2026",
    "Discharge Date: 07/05/2026",
    "",
    "DIAGNOSES:",
    "1. Type 2 Diabetes Mellitus",
    "2. Hypertension",
    "3. Community Acquired Pneumonia",
    "",
    "MEDICATIONS:",
    "1. Metformin 500mg twice daily",
    "2. Lisinopril 10mg once daily",
    "3. Amoxicillin 500mg three times daily for 7 days",
    "",
    "ALLERGIES:",
    "Penicillin - causes rash",
    "Aspirin - causes stomach upset",
    "",
    "RED FLAGS:",
    "Patient oxygen saturation dropped to 88% on day 2.",
    "Urgent chest X-ray ordered.",
    "",
    "Follow up with cardiologist in 2 weeks.",
    "Pt is allergic to PCN and sulfa drugs.",
    "Started on Augmentin 875mg BD."
]

for line in lines:
    pdf.cell(0, 10, line, ln=True)

pdf.output("sample.pdf")
print("sample.pdf created successfully")