import re

with open('generate_march_w1_analysis.py', 'r') as f:
    code = f.read()

# Basic replacements
code = code.replace('sales_march_w1.json', 'sales_q1.json')
code = code.replace('March Week 1', 'Q1')
code = code.replace('March 2-7, 2026', 'January 5 - March 31, 2026')
code = code.replace('WORKING_DAYS = 6', 'WORKING_DAYS = 74')
code = code.replace('MONTH = "March"', 'MONTH = "Q1"')
code = code.replace('WEEK_NUM = 1', 'WEEK_NUM = "Q1"')
code = code.replace('sales_analysis_march_w1', 'sales_analysis_q1')
code = code.replace('charts/march_w1', 'charts/q1')

# Remove PDF Target section
code = re.sub(r'elements\.append\(Paragraph\("Monthly Target Progress", header2_style\)\).*?elements\.append\(PageBreak\(\)\)', r'', code, flags=re.DOTALL)

# Remove Excel Target sheet
code = re.sub(r'# 5\. TARGET TRACKING.*?# Save workbook', r'# Save workbook', code, flags=re.DOTALL)

# Remove DOCX Target section
code = re.sub(r'doc\.add_heading\(\"Monthly Target Progress\".*?doc\.add_page_break\(\)', r'', code, flags=re.DOTALL)

# Remove JSON target section
code = re.sub(r'\"monthly_targets\".*?\"department_heads\"', r'\"department_heads\"', code, flags=re.DOTALL)

# Print lines with target pct
code = re.sub(r'print\(f\"\\nMonthly Target Progress.*?\\n\"\)', r'', code, flags=re.DOTALL)

with open('generate_q1_analysis.py', 'w') as f:
    f.write(code)

print("Patched script created.")
