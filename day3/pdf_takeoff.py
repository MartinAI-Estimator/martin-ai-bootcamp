# DAY 3: GlazingGPT v0.1 — AI Reads Glazing PDFs
import PyPDF2

pdf_path = "glazing_drawing.pdf"

try:
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

    windows = text.lower().count("window")
    glass = text.lower().count("glass")
    sqft = text.lower().count("sq ft") + text.lower().count("sqft")

    print("GLAZINGGPT v0.1 — PDF TAKEOFF REPORT")
    print("=" * 50)
    print(f"PDF: {pdf_path}")
    print(f"Windows found: {windows}")
    print(f"Glass references: {glass}")
    print(f"Sq ft references: {sqft}")
    print("=" * 50)

except FileNotFoundError:
    print(f"ERROR: '{pdf_path}' not found!")
    print("→ Save a glazing PDF in the 'day3' folder.")