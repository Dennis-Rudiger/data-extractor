import re

with open('generate_q1_analysis.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove MONTHLY_TARGETS def
code = re.sub(r'# Monthly targets \(March\)\s*MONTHLY_TARGETS = \{.*?\n\}\n*', '', code, flags=re.DOTALL)
code = re.sub(r'# Monthly targets \(March\)\s*Q1_TARGETS = \{.*?\n\}\n*', '', code, flags=re.DOTALL)

# 2. Remove create_target_progress function
create_target_progress_pattern = r'def create_target_progress\(output_dir="charts/q1"\):.*?return fn\n\n'
code = re.sub(create_target_progress_pattern, '', code, flags=re.DOTALL)
code = code.replace("'target': create_target_progress(),\n", "")

# 3. Remove Target Progress section from PDF (lines around MONTHLY TARGET PROGRESS)
pdf_target_pattern = r'# Target Progress.*?t\.setStyle\(TableStyle\(\[\n.*?\]\)\)\n\s+elements\.append\(t\)'
code = re.sub(pdf_target_pattern, '', code, flags=re.DOTALL)

# Remove TARGET PROGRESS image
pdf_target_image = r"if os\.path\.exists\(chart_files\['target'\]\):\n\s+elements\.append\(Paragraph\(\"TARGET PROGRESS\", heading_s\)\)\n\s+elements\.append\(Image\(chart_files\['target'\], width=6\.5\*inch, height=2\*inch\)\)"
code = re.sub(pdf_target_image, '', code, flags=re.DOTALL)

# 4. Remove from excel
excel_target_pattern = r'# Target progress.*?ws\.append\(\[\]\).*?ws\.append\(\[\]\)'
code = re.sub(excel_target_pattern, '', code, flags=re.DOTALL)
excel_target_pattern = r'ws\.append\(\["MONTHLY TARGET PROGRESS"\]\).*?ws\.append\(\[\]\)\n\s+ws\.append\(\[\]\)'
code = re.sub(excel_target_pattern, '', code, flags=re.DOTALL)

# 5. Remove Target Progress from Word doc
word_target_pattern = r'# Target Progress.*?t\.cell\(i, j\)\.paragraphs\[0\]\.alignment = WD_ALIGN_PARAGRAPH\.RIGHT\n\n'
code = re.sub(word_target_pattern, '', code, flags=re.DOTALL)

# 6. Remove from JSON payload
json_target_pattern = r'"monthly_targets": \{.*?\n\s+\},\n'
code = re.sub(json_target_pattern, '', code, flags=re.DOTALL)
# Also remove the category population for json
json_cat_target = r'target \= MONTHLY_TARGETS\.get\(cat.*?output\["monthly_targets"\]\["categories"\]\[cat\] = \{.*?"pct_achieved": round\(pct, 1\)\n\s+\}'
code = re.sub(json_cat_target, '', code, flags=re.DOTALL)

# 7. Remove print
print_target = r'# Target progress.*?print\(f"\\nMonthly Target Progress.*?after Week 1\)"\)'
code = re.sub(print_target, '', code, flags=re.DOTALL)
print_target = r'target_pct = total_sales / MONTHLY_TARGETS\[\'OVERALL\'\] \* 100.*?print\(f"\\nMonthly Target Progress: \{target_pct:\.1f\}%.*?\)'
code = re.sub(print_target, '', code, flags=re.DOTALL)

with open('generate_q1_analysis.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Targets stripped")
