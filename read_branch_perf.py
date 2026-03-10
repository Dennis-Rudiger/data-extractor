import pdfplumber

pdf = pdfplumber.open("BRANCH MANAGERS-  WEEKLY BRANCH PERFORMANCE-PANNJU1(4).pdf")
for i, page in enumerate(pdf.pages):
    text = page.extract_text()
    print(f"\n{'='*60}")
    print(f"PAGE {i+1}")
    print(f"{'='*60}")
    print(text)
pdf.close()
