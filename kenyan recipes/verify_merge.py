import re

t = open("kenyan recipes/kenyanMeals.js", "r", encoding="utf-8").read()

# Extract recipe-level names (not ingredient names)
# Recipe names follow "id:" lines
blocks = t.split("id: ")
recipe_names = []
for block in blocks[1:]:
    name_m = re.search(r'name: "([^"]+)"', block)
    if name_m:
        recipe_names.append(name_m.group(1))

print(f"Total recipe names: {len(recipe_names)}")
dupes = set()
for n in recipe_names:
    if recipe_names.count(n) > 1:
        dupes.add(n)
if dupes:
    print(f"Duplicate recipe names ({len(dupes)}):")
    for d in sorted(dupes):
        print(f"  {d}")
else:
    print("No duplicate recipe names!")

# Verify JS syntax by checking balanced braces/brackets
opens = t.count("{") + t.count("[")
closes = t.count("}") + t.count("]")
print(f"\nOpening braces/brackets: {opens}")
print(f"Closing braces/brackets: {closes}")
print(f"Balanced: {opens == closes}")

# Sample a few recipes
import json
for target in ["ke-001", "ke-045", "ke-046", "ke-135", "ke-271"]:
    idx = t.find(f'"{target}"')
    if idx > 0:
        name_m = re.search(r'name: "([^"]+)"', t[idx:idx+200])
        source_m = re.search(r'source: "([^"]+)"', t[idx:idx+300])
        n = name_m.group(1) if name_m else "?"
        s = source_m.group(1) if source_m else "?"
        print(f"  {target}: {n} ({s})")
