import json

for branch in ['bomas', 'karen']:
    with open(f'{branch}_average_moq.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fast = []
    slow = []
    for cat_name, cat in data['categories'].items():
        for p in cat.get('products', []):
            if p['qty_out'] > 0:
                fast.append(p)
            else:
                slow.append(p)
                
    fast = sorted(fast, key=lambda x: x['qty_out'], reverse=True)
    slow = sorted(slow, key=lambda x: x['item_code'])
    
    data['fast_movers'] = fast
    data['slow_movers'] = slow
    
    with open(f'{branch}_average_moq.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
