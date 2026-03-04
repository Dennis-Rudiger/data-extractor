import re

text = open("kenyan recipes/kenyanMeals.js", "r", encoding="utf-8").read()

# Count recipes
ids = re.findall(r'id:\s*"(ke-\d+)"', text)
print(f"Total IDs in kenyanMeals.js: {len(ids)}")

# Check which have instructions
for recipe_id in ids:
    idx = text.find(f'"{recipe_id}"')
    # Find next recipe or end
    next_idx = text.find('"ke-', idx + 10)
    if next_idx == -1:
        next_idx = len(text)
    chunk = text[idx:next_idx]
    has_inst = "instructions:" in chunk
    has_source = "source:" in chunk
    if not has_inst:
        print(f"  {recipe_id}: NO instructions")
