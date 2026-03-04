import pdfplumber

# KFM CookBook
pdf = pdfplumber.open("kenyan recipes/KFM-CookBook.pdf")
print("=== KFM CookBook - Sample pages ===")
for i in [3, 4, 5, 6, 10, 20, 50, 80, 95]:
    if i < len(pdf.pages):
        t = pdf.pages[i].extract_text()
        snippet = t[:800] if t else "[empty]"
        print(f"\n--- Page {i+1} ---")
        print(snippet)
pdf.close()

print("\n\n")

# Smart Food Recipe Book
pdf = pdfplumber.open("kenyan recipes/Smart-Food-Recipe-Book-Kenya-edited.pdf")
print("=== Smart Food Recipe Book - Sample pages ===")
for i in [4, 5, 6, 7, 8, 10, 15, 20, 30, 40, 50, 60]:
    if i < len(pdf.pages):
        t = pdf.pages[i].extract_text()
        snippet = t[:800] if t else "[empty]"
        print(f"\n--- Page {i+1} ---")
        print(snippet)
pdf.close()
