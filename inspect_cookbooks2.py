import pdfplumber

# Check more pages from each PDF

# 1. IN-MY-KITCHEN - check pages with recipes
pdf = pdfplumber.open("kenyan recipes/IN-MY-KITCHEN-by-KALUHI-ADAGALA.pdf")
print("=== IN MY KITCHEN - Sample recipe pages ===")
for i in [4, 5, 6, 7, 8, 10, 15, 20, 30, 40, 50, 55]:
    if i < len(pdf.pages):
        t = pdf.pages[i].extract_text()
        snippet = t[:600] if t else "[empty]"
        print(f"\n--- Page {i+1} ---")
        print(snippet)
pdf.close()
