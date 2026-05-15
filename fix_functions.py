import re

with open("generate_q1_analysis.py", "r", encoding="utf-8") as f:
    lines_q1 = f.readlines()

with open("generate_april_analysis.py", "r", encoding="utf-8") as f:
    lines_april = f.readlines()

# Extract from q1: 569 to 1670 (0-indexed)
good_block = "".join(lines_q1[569:1671])

# Apply replacements
# "q1" -> "april"
good_block = good_block.replace("q1", "april")
good_block = good_block.replace("Q1", "April")

# Then we find where in april it should be inserted
# april top part up to line 533 (0-indexed 0 to 532)
top_part = "".join(lines_april[:533])
# april bottom part from 1321 (0-indexed, def main() and below)
bottom_part = "".join(lines_april[1321:])

new_content = top_part + good_block + bottom_part

with open("generate_april_analysis.py", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Replacement done!")
