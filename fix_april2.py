with open('generate_april_analysis.py', 'r') as f:
    text = f.read()

text = text.replace('0.25', '1.0')
text = text.replace('25%', '100%')

with open('generate_april_analysis.py', 'w') as f:
    f.write(text)
