import re

with open('generate_april_analysis.py', 'r') as f:
    text = f.read()

bad_pattern = re.compile(r"        if reps_in_cat:\n            doc\.add_paragraph\(\).*?        doc\.add_paragraph\(\)\n", re.DOTALL)

good_text = \"\"\"        for rep_name, c, share in reps_in_cat:
            cat_rows.append([rep_name, f\"{c['sales_incl']:,.0f}\", f\"{c['profit']:,.0f}\",
                              f\"{c['margin_pct']:.1f}%\", f\"{c['qty']:,.0f}\", f\"{share:.1f}%\"])     

        t = Table(cat_rows, colWidths=[1.3*inch, 1.1*inch, 1.0*inch, 0.8*inch, 0.7*inch, 0.8*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS.get(cat, '#2c3e50'))),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),      
        ]))
        elements.append(t)
    elements.append(Spacer(1, 15))
\"\"\"

if bad_pattern.search(text):
    text = bad_pattern.sub(good_text, text)
    with open('generate_april_analysis.py', 'w') as f:
        f.write(text)
    print("Fixed!")
else:
    print("Pattern not found!")
