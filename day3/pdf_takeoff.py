# DAY 6: GlazingGPT v0.4 — Full Bid with Cost & Profit
import PyPDF2
import pytesseract
from PIL import Image
import io
import pandas as pd

pdf_path = "glazing_drawing.pdf"

try:
    # === OCR EXTRACT TEXT ===
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

    # === COUNT ITEMS ===
    windows = text.lower().count("window")
    glass = text.lower().count("glass")
    sqft = text.lower().count("sq ft") + text.lower().count("sqft") + text.lower().count("s.f.")
    linear = text.lower().count("linear") + text.lower().count("l.f.") + text.lower().count("lin.")

    # === COST DATABASE (your real rates) ===
    costs = {
        "Windows": 475,
        "Glass": 92,
        "Sq Ft": 1.35,
        "Linear Ft": 138
    }

    # === BUILD BID ===
    df = pd.DataFrame([
        {"Item": "Windows", "Qty": windows, "Unit": "$/ea", "Cost": costs["Windows"]},
        {"Item": "Glass", "Qty": glass, "Unit": "$/ref", "Cost": costs["Glass"]},
        {"Item": "Sq Ft", "Qty": sqft, "Unit": "$/sqft", "Cost": costs["Sq Ft"]},
        {"Item": "Linear Ft", "Qty": linear, "Unit": "$/ft", "Cost": costs["Linear Ft"]}
    ])

    df["Total"] = df["Qty"] * df["Cost"]
    df["Markup (30%)"] = df["Total"] * 0.30
    df["Bid Price"] = df["Total"] + df["Markup (30%)"]

    subtotal = df["Total"].sum()
    profit = df["Markup (30%)"].sum()
    total_bid = df["Bid Price"].sum()

    # === EXPORT TO EXCEL ===
    with pd.ExcelWriter("GlazingGPT_FULL_BID.xlsx", engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Takeoff", index=False)
        pd.DataFrame([{"SUBTOTAL": subtotal, "PROFIT": profit, "TOTAL BID": total_bid}]).to_excel(writer, sheet_name="Summary", index=False)

    print("GLAZINGGPT v0.4 — FULL BID READY")
    print("=" * 60)
    print(df[["Item", "Qty", "Bid Price"]])
    print(f"\nSUBTOTAL: ${subtotal:,.2f}")
    print(f"PROFIT (30%): ${profit:,.2f}")
    print(f"TOTAL BID: ${total_bid:,.2f}")
    print("Exported to: GlazingGPT_FULL_BID.xlsx")
    print("=" * 60)

except FileNotFoundError:
    print(f"ERROR: '{pdf_path}' not found!")