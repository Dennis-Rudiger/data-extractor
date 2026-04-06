import re

with open('generate_q1_analysis.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Excel targets
code = re.sub(r'\s*# Target progress.*?ws\.append\(\[\]\)', '', code, flags=re.DOTALL)
code = re.sub(r'\s*ws\.append\(\["MONTHLY TARGET PROGRESS"\].*?ws\.append\(\[\]\)', '', code, flags=re.DOTALL)

# Word targets
code = re.sub(r'\s*# Target Progress.*?(Monthly Target|MONTHLY TARGET PROGRESS).*?t\.cell\(i, j\)\.paragraphs\[0\]\.alignment = WD_ALIGN_PARAGRAPH\.RIGHT', '', code, flags=re.DOTALL)

# Json Targets
code = re.sub(r'\s*"monthly_targets": \{.*?\},\n', '\n', code, flags=re.DOTALL)
code = re.sub(r'\s*target = MONTHLY_TARGETS\.get\(cat, 0\).*?"pct_achieved": round\(pct, 1\)\n\s+}', '', code, flags=re.DOTALL)

# Weekly target line
code = re.sub(r'\s*# Weekly target \(1/4 of monthly\)\nweekly_target = MONTHLY_TARGETS\[\'OVERALL\'\] / 4', '', code, flags=re.DOTALL)

# Print
code = re.sub(r'\s*# Target progress.*?expected 25% after Week 1\)"\)', '', code, flags=re.DOTALL)

with open('generate_q1_analysis.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Targets stripped 2")
