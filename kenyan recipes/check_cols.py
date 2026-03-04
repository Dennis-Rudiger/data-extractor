import pdfplumber
pdf = pdfplumber.open("kenyan recipes/Kenya Recipe Book 2018.pdf")
p = pdf.pages[77]
split_x = 285  # bullets at 295, so split at 285

left = p.crop((0, 0, split_x, p.height)).extract_text() or ""
right = p.crop((split_x, 0, p.width, p.height)).extract_text() or ""
print("=== LEFT ===")
print(left[:600])
print("\n=== RIGHT ===")
print(right[:600])
pdf.close()
