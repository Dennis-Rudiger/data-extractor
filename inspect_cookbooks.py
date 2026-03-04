import pdfplumber

pdfs = [
    "kenyan recipes/IN-MY-KITCHEN-by-KALUHI-ADAGALA.pdf",
    "kenyan recipes/Kenya Recipe Book 2018.pdf",
    "kenyan recipes/KFM-CookBook.pdf",
    "kenyan recipes/Smart-Food-Recipe-Book-Kenya-edited.pdf",
]
for pf in pdfs:
    pdf = pdfplumber.open(pf)
    print(f"=== {pf} ({len(pdf.pages)} pages) ===")
    for i in range(min(4, len(pdf.pages))):
        t = pdf.pages[i].extract_text()
        snippet = t[:500] if t else "[empty]"
        print(f"  Page {i+1}:")
        print(snippet)
        print()
    pdf.close()
    print()
