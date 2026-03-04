import json

d = json.load(open("kenyan recipes/extracted_recipes.json", "r", encoding="utf-8"))

print(f"Total recipes: {len(d)}")
print(f"ID range: {d[0]['id']} to {d[-1]['id']}")
print()

# Check all required fields
fields = ["id", "name", "type", "description", "preparationTime", "cookingTime", 
          "servings", "totalCost", "calories", "image", "tags", "ingredients", 
          "nutritionFacts", "region", "instructions", "source"]

for field in fields:
    has = sum(1 for r in d if field in r)
    print(f"  {field}: {has}/{len(d)}")

print()
# Type distribution
types = {}
for r in d:
    t = r.get("type", "?")
    types[t] = types.get(t, 0) + 1
print("Meal types:")
for t, c in sorted(types.items()):
    print(f"  {t}: {c}")

print()
# Ingredient count distribution
ing_counts = [len(r.get("ingredients", [])) for r in d]
print(f"Ingredients: min={min(ing_counts)}, max={max(ing_counts)}, avg={sum(ing_counts)/len(ing_counts):.1f}")

# Instruction count distribution
ins_counts = [len(r.get("instructions", [])) for r in d]
print(f"Instructions: min={min(ins_counts)}, max={max(ins_counts)}, avg={sum(ins_counts)/len(ins_counts):.1f}")

# Nutrition coverage
has_cal = sum(1 for r in d if r.get("nutritionFacts", {}).get("calories", 0) > 0)
print(f"Has nutrition calories: {has_cal}/{len(d)}")

# Extra fields
extra = set()
for r in d:
    for k in r.keys():
        if k not in fields:
            extra.add(k)
if extra:
    print(f"\nExtra fields found: {extra}")
    for ef in extra:
        count = sum(1 for r in d if ef in r)
        print(f"  {ef}: {count}/{len(d)}")

# Sample recipe
print("\n--- Sample recipe (first FAO) ---")
fao = [r for r in d if "FAO" in r.get("source", "")]
if fao:
    r = fao[5]
    for k, v in r.items():
        if k in ("ingredients", "instructions"):
            print(f"  {k}: [{len(v)} items]")
        else:
            val = str(v)[:80]
            print(f"  {k}: {val}")
