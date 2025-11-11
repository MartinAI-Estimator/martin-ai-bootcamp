# DAY 5: GlazingGPT v0.3 — OCR + Excel Export
import PyPDF2
import pytesseract
from PIL import Image
import io
import pandas as pd

pdf_path = "glazing_drawing.pdf"

try:
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            
            if page_text and page_text.strip():
                text += page_text + "\n"
            else:
                if '/XObject' in page['/Resources']:
                    xObject = page['/Resources']['/XObject'].get_object()
                    for obj in xObject:
                        if xObject[obj]['/Subtype'] == '/Image':
                            data = xObject[obj].get_data()
                            img = Image.open(io.BytesIO(data))
                            ocr_text = pytesseract.image_to_string(img)
                            text += ocr_text + "\n"

    windows = text.lower().count("window")
    glass = text.lower().count("glass")
    sqft = text.lower().count("sq ft") + text.lower().count("sqft") + text.lower().count("s.f.")
    linear = text.lower().count("linear") + text.lower().count("l.f.")

    # Export to Excel
    df = pd.DataFrame({
        "Item": ["Windows", "Glass References", "Sq Ft", "Linear Ft"],
        "Quantity": [windows, glass, sqft, linear]
    })
    df.to_excel("GlazingGPT_Takeoff.xlsx", index=False)

    print("GLAZINGGPT v0.3 — OCR + EXCEL EXPORT")
    print("=" * 55)
    print(f"PDF: {pdf_path}")
    print(f"Windows: {windows} | Glass: {glass} | Sq ft: {sqft} | Linear ft: {linear}")
    print("Exported to: GlazingGPT_Takeoff.xlsx")
    print("=" * 55)
    print("Day 6 → Cost estimation coming!")

except FileNotFoundError:
    print(f"ERROR: '{pdf_path}' not found!")