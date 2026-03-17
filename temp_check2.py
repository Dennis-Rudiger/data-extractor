import json
for file in ['stock_movement_jan.json', 'stock_movement_feb.json', 'stock_movement_karen_jan.json', 'stock_movement_karen_feb.json']:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data['items']:
            code = str(item.get('code', '')).strip()
            if code in ['J', 'R']:
                print(file, item)
