import re
with open('generate_q1_analysis.py', 'r') as f:
    c = f.read()
c = re.sub(r'elements\.append\(Paragraph\(f"Monthly Target.*?pace_color\)\)', '', c, flags=re.DOTALL)
c = re.sub(r'target_data = \[\[.*?table\.setStyle\(TableStyle\(\[.*?\]\)\)\s*elements\.append\(table\)\s*elements\.append\(Spacer\(1, 0\.2\*inch\)\)', '', c, flags=re.DOTALL)
c = re.sub(r'# --- Target Progress.*?elements\.append\(PageBreak\(\)\)', '', c, flags=re.DOTALL)
c = re.sub(r'elements\.append\(Paragraph\(\"Monthly Target Progress\".*?PageBreak\(\)\)', '', c, flags=re.DOTALL)
open('generate_q1_analysis.py', 'w').write(c)
