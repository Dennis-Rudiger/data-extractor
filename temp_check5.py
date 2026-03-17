import json
from collections import Counter

for f in ['stock_movement_jan.json', 'stock_movement_feb.json', 'stock_movement_karen_jan.json', 'stock_movement_karen_feb.json']:
    with open(f, 'r', encoding='utf-8') as file:
        data = json.load(file)
        counts = Counter([i.get('code') for i in data.get('items', [])])
        dups = {k: v for k, v in counts.items() if v > 1}
        print(f, \"Duplicates:\", dups)
