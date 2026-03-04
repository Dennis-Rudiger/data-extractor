"""
Merge existing kenyanMeals.js recipes with extracted_recipes.json
into a single updated kenyanMeals.js file.

Reads the ORIGINAL kenyanMeals.js (45 recipes, ke-001 to ke-045),
combines with extracted_recipes.json (226 recipes, ke-046 to ke-271),
and writes back a unified kenyanMeals.js (271 recipes total).
"""
import json
import re
import shutil
import os

INPUT_JS = "kenyan recipes/kenyanMeals.js"
EXTRACTED = "kenyan recipes/extracted_recipes.json"
OUTPUT_JS = "kenyan recipes/kenyanMeals.js"
BACKUP_JS = "kenyan recipes/kenyanMeals_backup.js"

# 0. Backup original
shutil.copy2(INPUT_JS, BACKUP_JS)
print(f"Backed up original to {BACKUP_JS}")

# 1. Parse existing kenyanMeals.js 
js_text = open(INPUT_JS, "r", encoding="utf-8").read()

# Safety: check we're working with the original (45 recipes)
if '"ke-046"' in js_text:
    print("ERROR: kenyanMeals.js already contains extracted recipes (ke-046 found).")
    print("Restore the original first with: git checkout main -- \"kenyan recipes/kenyanMeals.js\"")
    exit(1)

# Extract the array content between the first [ and last ]
arr_start = js_text.index("[")
arr_end = js_text.rindex("]") + 1
arr_text = js_text[arr_start:arr_end]

# Convert JS object notation to JSON:
# - Add quotes around property keys
# - Handle trailing commas
# Match property keys: word characters followed by colon, but only in object context
# (after line start+whitespace, or after { or comma)
json_text = re.sub(r'(?<=\{)\s*(\w+)\s*:', r' "\1":', arr_text)  # after {
json_text = re.sub(r'^(\s+)(\w+)\s*:', r'\1"\2":', json_text, flags=re.MULTILINE)  # start of line
json_text = re.sub(r',\s*(\w+)\s*:', r', "\1":', json_text)  # after comma
# Remove trailing commas before } or ]
json_text = re.sub(r',\s*([}\]])', r'\1', json_text)

try:
    existing = json.loads(json_text)
    print(f"Parsed {len(existing)} existing recipes from kenyanMeals.js")
except json.JSONDecodeError as e:
    print(f"Error parsing kenyanMeals.js: {e}")
    # Try to find the error location
    line = json_text[:e.pos].count("\n") + 1
    col = e.pos - json_text[:e.pos].rfind("\n")
    print(f"  At line {line}, col {col}")
    print(f"  Context: ...{json_text[max(0,e.pos-50):e.pos+50]}...")
    exit(1)

# Add source field to existing recipes
for r in existing:
    if "source" not in r:
        r["source"] = "kenyanMeals.js (Original)"
    if "instructions" not in r:
        r["instructions"] = []

# 2. Load extracted recipes
extracted = json.load(open("kenyan recipes/extracted_recipes.json", "r", encoding="utf-8"))
print(f"Loaded {len(extracted)} extracted recipes")

# 3. Combine
all_recipes = existing + extracted
print(f"Combined total: {len(all_recipes)} recipes")

# 4. Generate JS output
def to_js_value(val, indent=4):
    """Convert a Python value to JS literal string."""
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, str):
        # Escape for JS string
        escaped = val.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f'"{escaped}"'
    if isinstance(val, list):
        if not val:
            return "[]"
        # Check if it's a list of simple strings
        if all(isinstance(v, str) for v in val):
            items = ",\n".join(" " * (indent + 2) + to_js_value(v) for v in val)
            return f'[\n{items}\n{" " * indent}]'
        # List of objects (ingredients)
        if all(isinstance(v, dict) for v in val):
            items = []
            for v in val:
                pairs = ", ".join(f'{k}: {to_js_value(v2)}' for k, v2 in v.items())
                items.append(f'{" " * (indent + 2)}{{ {pairs} }}')
            return "[\n" + ",\n".join(items) + f'\n{" " * indent}]'
        return json.dumps(val)
    if isinstance(val, dict):
        pairs = []
        for k, v2 in val.items():
            pairs.append(f'{" " * (indent + 2)}{k}: {to_js_value(v2, indent + 2)}')
        return "{\n" + ",\n".join(pairs) + f'\n{" " * indent}}}'
    return json.dumps(val)

# Define the field order for consistent output
field_order = [
    "id", "name", "source", "type", "description",
    "preparationTime", "cookingTime", "servings",
    "totalCost", "calories", "image", "tags",
    "ingredients", "instructions",
    "nutritionFacts", "region",
    "swahiliName", "kfctCode",
    "pdfUrl", "videoUrl"
]

lines = []
lines.append('/**')
lines.append(' * Collection of traditional Kenyan meals and modern adaptations')
lines.append(' * with nutritional information and budget-friendly details')
lines.append(' * ')
lines.append(f' * Total recipes: {len(all_recipes)}')
lines.append(f' * Sources: kenyanMeals.js (Original), Global Give Back Circle,')
lines.append(f' *   IN MY KITCHEN by Kaluhi Adagala, Smart Food Recipe Book Kenya,')
lines.append(f' *   KFM CookBook, Kenya Recipe Book 2018 (FAO/GOK)')
lines.append(' */')
lines.append('')
lines.append('export const kenyanMeals = [')

for idx, recipe in enumerate(all_recipes):
    lines.append('  {')
    
    # Write fields in order
    written_keys = set()
    for key in field_order:
        if key in recipe:
            val_str = to_js_value(recipe[key], 4)
            lines.append(f'    {key}: {val_str},')
            written_keys.add(key)
    
    # Write any remaining keys not in field_order
    for key in recipe:
        if key not in written_keys:
            val_str = to_js_value(recipe[key], 4)
            lines.append(f'    {key}: {val_str},')
    
    # Remove trailing comma from last property
    if lines[-1].endswith(","):
        lines[-1] = lines[-1][:-1]
    
    if idx < len(all_recipes) - 1:
        lines.append('  },')
    else:
        lines.append('  }')

lines.append('];')
lines.append('')

output = "\n".join(lines)
with open(OUTPUT_JS, "w", encoding="utf-8") as f:
    f.write(output)

print(f"\nWritten {len(all_recipes)} recipes to {OUTPUT_JS}")
print(f"File size: {len(output):,} characters")
print(f"Backup saved at: {BACKUP_JS}")
