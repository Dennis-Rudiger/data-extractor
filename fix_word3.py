with open('generate_q1_analysis.py', 'r') as f:
    text = f.read()

text = text.replace('def generate_word():\n    doc.add_page_break()', 'def generate_word():\n    output_fn = "sales_analysis_q1.docx"\n    doc = DocxDocument()\n    doc.add_page_break()')

with open('generate_q1_analysis.py', 'w') as f:
    f.write(text)
