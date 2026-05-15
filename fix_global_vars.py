with open("generate_april_analysis.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

pdf_idx = -1
for i, line in enumerate(lines):
    if line.startswith("def generate_pdf():"):
        pdf_idx = i
        break

# The vars are lines idx+1 to idx+16
vars_block = lines[pdf_idx+1:pdf_idx+17]
# Outdent them
new_vars = []
for line in vars_block:
    if line.startswith("    "):
        new_vars.append(line[4:])
    else:
        new_vars.append(line)

# Remove them from inside generate_pdf
new_lines = lines[:pdf_idx] + new_vars + [lines[pdf_idx]] + lines[pdf_idx+17:]

with open("generate_april_analysis.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
print("Done moving vars to global")
