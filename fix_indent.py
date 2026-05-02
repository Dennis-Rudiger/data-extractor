with open('generate_q1_analysis.py', 'r') as f:
    text = f.read()

text = text.replace('      elements.append(PageBreak())', '    elements.append(PageBreak())')
text = text.replace('      elements.append(Paragraph("Q1', '    elements.append(Paragraph("Q1')
text = text.replace('      elements.append(Paragraph("1.', '    elements.append(Paragraph("1.')
text = text.replace('      elements.append(Paragraph("2.', '    elements.append(Paragraph("2.')
text = text.replace('      elements.append(Paragraph("3.', '    elements.append(Paragraph("3.')
text = text.replace('      elements.append(Paragraph("4.', '    elements.append(Paragraph("4.')
text = text.replace('      elements.append(Paragraph(f"BO', '    elements.append(Paragraph(f"BO')
text = text.replace('      elements.append(Spacer(1', '    elements.append(Spacer(1')
text = text.replace('      elements.append(Paragraph(f"The', '    elements.append(Paragraph(f"The')
text = text.replace('      elements.append(Paragraph(f"Sales', '    elements.append(Paragraph(f"Sales')
text = text.replace('      elements.append(Paragraph("&bull;', '    elements.append(Paragraph("&bull;')

with open('generate_q1_analysis.py', 'w') as f:
    f.write(text)
