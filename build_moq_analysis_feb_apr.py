import json

WORKING_DAYS = 76
MOQ_MULTIPLIER = 6

def build_branch_moq(branch_name):
    with open(f'stock_movement_{branch_name.lower()}_feb_apr.json', 'r') as f:
        movement = json.load(f)

    with open('inventory.json', 'r') as f:
        inventory = json.load(f)
    
    cat_lookup = {}
    for cat in inventory:
        cat_name = cat.get('category_name', cat.get('category', 'Unknown'))
        for p in cat.get('products', []):
            cat_lookup[p.get('item_code')] = cat_name

    categories = {}
    all_items = []
    fast_movers = []
    slow_movers = []

    for item in movement:
        code = item['item_code']
        desc = item['item_description']
        qty_in = max(0, item['qty_in'])
        qty_out = item['qty_out']
        closing = item.get('closing_balance', 0)
        
        cat_name = cat_lookup.get(code, 'UNCATEGORIZED')
        
        daily = qty_out / WORKING_DAYS if WORKING_DAYS > 0 else 0
        moq = int((daily * MOQ_MULTIPLIER) + 0.999999) # round up

        item_data = {
            'item_code': code,
            'item_description': desc,
            'qty_in': qty_in,
            'qty_out': qty_out,
            'closing_balance': closing,
            'daily_average': round(daily, 2),
            'weekly_moq': moq,
            'category': cat_name
        }

        if qty_out > 0:
            fast_movers.append(item_data)
        else:
            if qty_in > 0 or closing > 0:
                slow_movers.append(item_data)

        if cat_name not in categories:
            categories[cat_name] = {
                'total_items': 0,
                'fast_movers': 0,
                'slow_movers': 0,
                'total_qty_out': 0,
                'total_weekly_moq': 0,
                'products': []
            }
            
        categories[cat_name]['products'].append(item_data)
        categories[cat_name]['total_items'] += 1
        
        if qty_out > 0:
            categories[cat_name]['fast_movers'] += 1
        else:
            categories[cat_name]['slow_movers'] += 1
            
        categories[cat_name]['total_qty_out'] += qty_out
        categories[cat_name]['total_weekly_moq'] += moq
        all_items.append(item_data)

    fast_movers.sort(key=lambda x: x['qty_out'], reverse=True)
    slow_movers.sort(key=lambda x: x['qty_in'], reverse=True)

    summary = {
        'total_items': len(all_items),
        'fast_movers': len(fast_movers),
        'slow_movers': len([i for i in all_items if i['qty_out'] == 0]),
        'total_qty_out': sum(i['qty_out'] for i in all_items),
        'total_weekly_moq': sum(i['weekly_moq'] for i in all_items)
    }

    analysis = {
        'period': 'Feb 1 - Apr 30, 2026',
        'working_days': WORKING_DAYS,
        'moq_multiplier': MOQ_MULTIPLIER,
        'formula': 'MOQ = 6 x Daily Consumption',
        'summary': summary,
        'categories': categories,
        'fast_movers': fast_movers,
        'slow_movers': slow_movers
    }

    out_file = f'moq_analysis_{branch_name.lower()}_feb_apr.json'
    with open(out_file, 'w') as f:
        json.dump(analysis, f, indent=2)

    print(f'MOQ Analysis Complete for {branch_name}:')
    print(f"  Total Items: {summary['total_items']}")
    print(f"  Fast Movers: {summary['fast_movers']}")
    print(f"  Total Weekly MOQ: {summary['total_weekly_moq']}")
    print(f"  Saved to {out_file}\n")


if __name__ == '__main__':
    build_branch_moq('Bomas')
    build_branch_moq('Karen')
