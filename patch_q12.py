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

# Strip out TARGETS logic
code = re.sub(r'# Monthly targets.*?\}', '', code, count=1, flags=re.DOTALL)
code = re.sub(r'# Weekly target.*?weekly_target.*?$', '', code, flags=re.MULTILINE)
code = re.sub(r'target_pct.*?$', '', code, flags=re.MULTILINE)
code = re.sub(r'pace = .*?$', '', code, flags=re.MULTILINE)
code = re.sub(r'pace_color = .*?$', '', code, flags=re.MULTILINE)
code = re.sub(r'target = MONTHLY_TARGETS.*?$', '', code, flags=re.MULTILINE)
code = re.sub(r'items\.append\(\(cat, cumulative_cat_totals.*?$', 'items.append((cat, cumulative_cat_totals[cat]))', code, flags=re.MULTILINE)
code = re.sub(r'items = \[\(\"OVERALL\".*?$', 'items = [(\"OVERALL\", cumulative_total_sales)]', code, flags=re.MULTILINE)
code = re.sub(r'def draw_bullet.*?def ', 'def ', code, flags=re.DOTALL)

# Delete Target PDF Section
code = re.sub(r'# --- Target Progress.*?# --- Recommendations', '# --- Recommendations', code, flags=re.DOTALL)

# Delete Target Excel Section
code = re.sub(r'# 5\. TARGET TRACKING.*?# Save workbook', '# Save workbook', code, flags=re.DOTALL)

# Delete Target Word Section
code = re.sub(r'# Target Analysis.*?# Report Section', '# Report Section', code, flags=re.DOTALL)

# Delete Target JSON Section
code = re.sub(r'\"monthly_targets\": \{.*?\},(.*?\"department_heads\")', r'\1', code, flags=re.DOTALL)

with open('generate_q1_analysis.py', 'w') as f:
    f.write(code)
