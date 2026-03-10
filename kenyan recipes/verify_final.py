import re, json

t = open("kenyan recipes/kenyanMeals.js", "r", encoding="utf-8").read()
ids = re.findall(r'id: "(ke-\d+)"', t)
print(f"Total recipes: {len(ids)}")
print(f"Unique IDs: {len(set(ids))}")
print(f"Range: {ids[0]} to {ids[-1]}")

# Check for leaked "Ingredients Preparation" in descriptions
desc_leaks = re.findall(r'description: "([^"]*Ingredients\s+Preparation[^"]*)"', t)
print(f"\nDescription leaks (Ingredients Preparation): {len(desc_leaks)}")
for d in desc_leaks[:3]:
    print(f"  ...{d[-80:]}")

# Check Kaimati description specifically
kaim = t[t.find('"Kaimati"'):t.find('"Kaimati"')+500]
desc_m = re.search(r'description: "([^"]+)"', kaim)
if desc_m:
    desc = desc_m.group(1)
    print(f"\nKaimati description:")
    print(f"  {desc[:120]}...")
    print(f"  Ends with: ...{desc[-60:]}")
    print(f"  Has leak: {'Ingredients Preparation' in desc}")

# Check quality of FAO recipes
fao_blocks = [m.start() for m in re.finditer(r'source: "Kenya Recipe Book 2018', t)]
print(f"\nFAO recipes in file: {len(fao_blocks)}")

# Check Beef Stew ingredients
beef_idx = t.find('"Beef Stew"')
if beef_idx > 0:
    chunk = t[beef_idx:beef_idx+600]
    print(f"\nBeef Stew snippet:")
    print(chunk[:400])

# Sources breakdown
sources = re.findall(r'source: "([^"]+)"', t)
src_counts = {}
for s in sources:
    src_counts[s] = src_counts.get(s, 0) + 1
print(f"\nSources:")
for s, c in sorted(src_counts.items()):
    print(f"  {s}: {c}")
