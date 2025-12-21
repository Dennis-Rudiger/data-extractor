import PyPDF2

def inspect_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        if len(reader.pages) > 0:
            print(reader.pages[0].extract_text())

if __name__ == "__main__":
    inspect_pdf("Inventory Valuation.pdf")