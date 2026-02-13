import json

with open('inventory.json', 'r') as f:
    inventory = json.load(f)

WORKING_DAYS = 24
MOQ_MULTIPLIER = 6

categories = {}
all_items = []
fast_movers = []
slow_movers = []

for cat in inventory:
    cat_name = cat.get('category_name', cat.get('category', ''))
    if not cat_name or cat_name.lower() in ['unknown', '']:
        continue
    
    cat_products = []
    cat_fast = 0
    cat_slow = 0
    cat_qty_out = 0
    cat_moq = 0
    
    for product in cat.get('products', []):
        qty_out = product.get('jan_qty_out', 0)
        qty_in = product.get('jan_qty_out', 0) + product.get('jan_closing', 0) - product.get('quantity', 0)
        daily = product.get('daily_consumption', 0)
        moq = product.get('moq', 0)
        desc = product.get('description', product.get('item_description', ''))
        
        item_data = {
            'item_code': product.get('item_code', ''),
            'item_description': desc,
            'qty_in': max(0, qty_in),
            'qty_out': qty_out,
            'daily_average': daily,
            'weekly_moq': moq,
            'category': cat_name
        }
        
        if qty_out > 0:
            cat_fast += 1
            fast_movers.append(item_data)
        else:
            cat_slow += 1
            if qty_in > 0:
                slow_movers.append(item_data)
        
        cat_products.append(item_data)
        cat_qty_out += qty_out
        cat_moq += moq
        all_items.append(item_data)
    
    if len(cat_products) > 0:
        categories[cat_name] = {
            'total_items': len(cat_products),
            'fast_movers': cat_fast,
            'slow_movers': cat_slow,
            'total_qty_out': cat_qty_out,
            'total_weekly_moq': cat_moq,
            'products': cat_products
        }

fast_movers.sort(key=lambda x: x['qty_out'], reverse=True)
slow_movers.sort(key=lambda x: x['qty_in'], reverse=True)

summary = {
    'total_items': len(all_items),
    'fast_movers': len([i for i in all_items if i['qty_out'] > 0]),
    'slow_movers': len([i for i in all_items if i['qty_out'] == 0]),
    'total_qty_out': sum(i['qty_out'] for i in all_items),
    'total_weekly_moq': sum(i['weekly_moq'] for i in all_items)
}

analysis = {
    'period': 'January 5-31, 2026',
    'working_days': WORKING_DAYS,
    'moq_multiplier': MOQ_MULTIPLIER,
    'formula': 'MOQ = 6 x Daily Consumption',
    'summary': summary,
    'categories': categories,
    'fast_movers': fast_movers,
    'slow_movers': slow_movers
}

with open('moq_analysis.json', 'w') as f:
    json.dump(analysis, f, indent=2)

print('MOQ Analysis Complete:')
print(f"  Total Items: {summary['total_items']}")
print(f"  Fast Movers: {summary['fast_movers']}")
print(f"  Slow Movers: {summary['slow_movers']}")
print(f"  Categories: {len(categories)}")
print('')
print('Categories:')
for cat_name in sorted(categories.keys()):
    c = categories[cat_name]
    print(f"  {cat_name}: {c['total_items']} items, MOQ: {c['total_weekly_moq']}")
