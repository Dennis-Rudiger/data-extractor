with open("generate_april_analysis.py", "r", encoding="utf-8") as f:
    lines_april = f.readlines()

with open("generate_q1_analysis.py", "r", encoding="utf-8") as f:
    lines_q1 = f.readlines()

# Find generate_pdf in april
idx_april = 0
for i, line in enumerate(lines_april):
    if line.startswith("def generate_pdf"):
        idx_april = i
        break

# Find generate_pdf in q1
idx_q1 = 0
for i, line in enumerate(lines_q1):
    if line.startswith("def generate_pdf"):
        idx_q1 = i
        break

top_part = "".join(lines_april[:idx_april-1]) # exclude the ========== PDF REPORT ========== line if it's there
bottom_part = "".join(lines_q1[idx_q1-1:])

bottom_part = bottom_part.replace("q1", "april")
bottom_part = bottom_part.replace("Q1", "April")

with open("generate_april_analysis.py", "w", encoding="utf-8") as f:
    f.write(top_part + bottom_part)
print("done")
