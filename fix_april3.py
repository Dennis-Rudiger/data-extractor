with open('generate_april_analysis.py', 'r') as f:
    text = f.read()

text = text.replace('After Week {WEEK_NUM}', 'in {MONTH} {YEAR}')
text = text.replace('Week 1 Actual', 'April Actual')
text = text.replace('After Week 1,', 'By the end of the month,')

with open('generate_april_analysis.py', 'w') as f:
    f.write(text)
