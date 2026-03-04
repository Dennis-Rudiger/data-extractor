import pdfplumber

# Kenya Recipe Book 2018 - the big one
pdf = pdfplumber.open("kenyan recipes/Kenya Recipe Book 2018.pdf")
print("=== Kenya Recipe Book 2018 - Sample pages ===")
for i in [4, 5, 6, 7, 8, 10, 15, 20, 50, 100, 200, 300, 345]:
    if i < len(pdf.pages):
        t = pdf.pages[i].extract_text()
        snippet = t[:800] if t else "[empty]"
        print(f"\n--- Page {i+1} ---")
        print(snippet)
pdf.close()
