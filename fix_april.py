with open('generate_april_analysis.py', 'r') as f:
    text = f.read()

text = text.replace('WEEK_NUM = "April"', 'WEEK_NUM = "All"')

with open('generate_april_analysis.py', 'w') as f:
    f.write(text)
