import pdfplumber

pdf = pdfplumber.open("kenyan recipes/Kenya Recipe Book 2018.pdf")
print("=== Kenya Recipe Book 2018 - Actual recipe pages ===")

# Look at the table of contents and first recipes
for i in [13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25]:
    if i < len(pdf.pages):
        t = pdf.pages[i].extract_text()
        snippet = t[:1000] if t else "[empty]"
        print(f"\n--- Page {i+1} ---")
        print(snippet)
pdf.close()
