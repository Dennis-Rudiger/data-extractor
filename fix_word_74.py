with open("generate_april_analysis.py", "r", encoding="utf-8") as f:
    text = f.read()
text = text.replace("total_profit/74", "total_profit/WORKING_DAYS")
with open("generate_april_analysis.py", "w", encoding="utf-8") as f:
    f.write(text)
