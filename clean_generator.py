import re

with open('generate_march_w1_analysis.py', 'r') as f:
    text = f.read()

text = text.replace('sales_march_w1.json', 'sales_q1.json')
text = text.replace('March Week 1', 'Q1')
text = text.replace('March 2-7, 2026', 'January 5 - March 31, 2026')
text = text.replace('WORKING_DAYS = 6', 'WORKING_DAYS = 74')
text = text.replace('MONTH = "March"', 'MONTH = "Q1"')
text = text.replace('WEEK_NUM = 1', 'WEEK_NUM = "Q1"')
text = text.replace('sales_analysis_march_w1', 'sales_analysis_q1')
text = text.replace('charts/march_w1', 'charts/q1')

# Replace PDF target section
start_str = "    # Target Progress"
end_str = "    elements.append(Spacer(1, 10))"
text = re.sub(start_str + ".*?" + end_str, "    elements.append(Spacer(1, 10))", text, flags=re.DOTALL)

start_str2 = "# --- Target Progress"
end_str2 = "# --- Recommendations"
text = re.sub(start_str2 + ".*?" + end_str2, "# --- Recommendations", text, flags=re.DOTALL)

# Replace DOCX target section 
start_str3 = "# Target Analysis"
end_str3 = "# Report Section"
text = re.sub(start_str3 + ".*?" + end_str3, "# Report Section", text, flags=re.DOTALL)

# Replace XLSX target section
start_str4 = "# 5. TARGET TRACKING"
end_str4 = "# Save workbook"
text = re.sub(start_str4 + ".*?" + end_str4, "# Save workbook", text, flags=re.DOTALL)

# Replace JSON target section
start_str5 = r'"monthly_targets": \{'
end_str5 = r'\},\n\s*"department_heads"'
text = re.sub(start_str5 + ".*?" + end_str5, '"department_heads"', text, flags=re.DOTALL)

text = re.sub(r'print\(f\"\\nMonthly Target Progress.*?\\n\"\)', '', text, flags=re.DOTALL)

with open('generate_q1_analysis.py', 'w') as f:
    f.write(text)
