# DAY 4: GlazingGPT v0.2 — OCR Reads Scanned Glazing Drawings
import PyPDF2
import pytesseract
from PIL import Image
import io

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
                # OCR for scanned/image pages
                if '/XObject' in page['/Resources']:
                    xObject = page['/Resources']['/XObject'].get_object()
                    for obj in xObject:
                        if xObject[obj]['/Subtype'] == '/Image':
                            data = xObject[obj].get_data()
                            img = Image.open(io.BytesIO(data))
                            ocr_text = pytesseract.image_to_string(img)
                            text += ocr_text + "\n"

    # Count glazing takeoff items
    windows = text.lower().count("window")
    glass = text.lower().count("glass")
    sqft = text.lower().count("sq ft") + text.lower().count("sqft") + text.lower().count("s.f.")
    linear = text.lower().count("linear") + text.lower().count("l.f.")

    print("GLAZINGGPT v0.2 — OCR TAKEOFF REPORT")
    print("=" * 55)
    print(f"PDF: {pdf_path}")
    print(f"Windows found: {windows}")
    print(f"Glass references: {glass}")
    print(f"Sq ft references: {sqft}")
    print(f"Linear ft references: {linear}")
    print("=" * 55)
    print("Day 5 → Export to Excel coming!")

except FileNotFoundError:
    print(f"ERROR: '{pdf_path}' not found!")
    print("→ Save PDF in 'day3' folder.")
except Exception as e:
    print(f"OCR ERROR: {e}")