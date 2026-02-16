import pdfplumber
pdfs = {"PLUMBING": "TOTAL PLUMBING.pdf", "ELECTRICALS": "TOTAL ELECTRICALS.pdf", "PAINTS": "TOTAL PAINTS.pdf", "GENERAL HARDWARE": "TOTAL GENERAL HARDWARE.pdf"}
for cat, pdf_file in pdfs.items():
    pdf = pdfplumber.open(pdf_file)
    text = pdf.pages[0].extract_text()
    lines = text.split(chr(10))
    print(f"{cat}:")
    current_rep = None
    for line in lines:
        if "Transaction Rep:" in line:
            current_rep = line.replace("Transaction Rep:", "").strip()
        elif current_rep and line.strip():
            parts = line.replace(",", "").split()
            if len(parts) >= 6 and parts[0].replace(".", "").isdigit():
                qty = float(parts[0])
                amount_incl = float(parts[2])
                cost = float(parts[3])
                profit = float(parts[4])
                print(f"  {current_rep}: qty={qty}, sales_incl={int(amount_incl)}, cost={cost}, profit={profit}")
            current_rep = None
    print()
