import json
import math

# 1. Load Inventory & Prices
with open('inventory_valuation_priced.json', 'r', encoding='utf-8') as f:
    inv = json.load(f)

prices_map = {}
cat_map = {}
for cat in inv:
    cat_name = cat.get('category_name') or cat.get('category')
    for p in cat.get('products', []):
        prices_map[p['item_code']] = p.get('selling_price', 0)
        cat_map[p['item_code']] = cat_name

# fallback to item_category_map.json if exists
try:
    with open('item_category_map.json', 'r', encoding='utf-8') as f:
        # Assuming it's formatted as code -> category
        cat_map_ext = json.load(f)
        for k, v in cat_map_ext.items():
            if k not in cat_map:
                cat_map[k] = v
except:
    pass

def build_branch_moq(branch_name, files, output_file):
    item_stats = {}
    for f_path in files:
        with open(f_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data.get('items', []):
                code = item.get('code')
                desc = item.get('description', '')
                if not code:
                    continue
                if code not in item_stats:
                    item_stats[code] = {
                        'item_code': code,
                        'item_description': desc,
                        'qty_in': 0.0,
                        'qty_out': 0.0,
                        'opening_balance': 0.0,
                        'closing_balance': 0.0
                    }
                item_stats[code]['qty_in'] += float(item.get('qty_in', 0))
                item_stats[code]['qty_out'] += float(item.get('qty_out', 0))
                # For closing balance, just take the last one or accumulate
                item_stats[code]['closing_balance'] = float(item.get('closing', item_stats[code]['closing_balance']))
    
    # Organize by category
    categories = {}
    total_qty_out = 0.0
    total_weekly_moq = 0
    total_weekly_value = 0.0

    for code, stats in item_stats.items():
        cat_name = cat_map.get(code, "UNCATEGORIZED")
        if cat_name not in categories:
            categories[cat_name] = {'products': []}
            
        qty_out = stats['qty_out']
        # 48 days total
        daily_avg = qty_out / 48.0
        weekly_moq = math.ceil(daily_avg * 6)
        # Ensure minimums/zeros
        if weekly_moq == 0 and qty_out > 0:
             weekly_moq = 1
        if qty_out == 0:
             weekly_moq = 0
        
        price = prices_map.get(code, 0)
        val = weekly_moq * price
        
        prod = {
            'item_code': code,
            'item_description': stats['item_description'],
            'qty_in': round(stats['qty_in'], 2),
            'qty_out': round(qty_out, 2),
            'closing_balance': round(stats['closing_balance'], 2),
            'daily_average': round(daily_avg, 2),
            'weekly_moq': weekly_moq,
            'weekly_value': val,
            'category': cat_name,
            'selling_price': price
        }
        categories[cat_name]['products'].append(prod)

    # Summarize
    formatted_cats = {}
    b_fast = 0
    b_slow = 0
    b_items = 0
    for cat_name, cat_data in categories.items():
        prods = sorted(cat_data['products'], key=lambda x: x['qty_out'], reverse=True)
        fast = [p for p in prods if p['qty_out'] > 0]
        slow = [p for p in prods if p['qty_out'] == 0]
        
        c_qty_out = sum(p['qty_out'] for p in prods)
        c_moq = sum(p['weekly_moq'] for p in prods)
        c_val = sum(p['weekly_value'] for p in prods)
        
        total_qty_out += c_qty_out
        total_weekly_moq += c_moq
        total_weekly_value += c_val
        b_fast += len(fast)
        b_slow += len(slow)
        b_items += len(prods)
        
        formatted_cats[cat_name] = {
            'total_items': len(prods),
            'fast_movers': len(fast),
            'slow_movers': len(slow),
            'total_qty_out': round(c_qty_out, 2),
            'total_weekly_moq': c_moq,
            'total_weekly_value': round(c_val, 2),
            'products': prods,
            'fast_movers_list': fast,
            'slow_movers_list': slow
        }

    # remove list keys if my generate report script doesn't want them or wants them flat
    # Actually, previous structure had no fast_movers list directly, we just had products list OR it had it conditionally. We'll just leave them under 'products'.
    for k, v in formatted_cats.items():
        if 'fast_movers_list' in v: del v['fast_movers_list']
        if 'slow_movers_list' in v: del v['slow_movers_list']
        
    out_json = {
        'branch': branch_name.upper(),
        'period': 'Average Jan-Feb 2026',
        'working_days': 48,
        'moq_multiplier': 6,
        'formula': 'MOQ = 6 x (Total Qty Out / 48)',
        'summary': {
            'total_items': b_items,
            'fast_movers': b_fast,
            'slow_movers': b_slow,
            'total_qty_out': round(total_qty_out, 2),
            'total_weekly_moq': total_weekly_moq,
            'total_weekly_value': round(total_weekly_value, 2)
        },
        'categories': formatted_cats
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, indent=4)
    print(f"Generated {output_file} - Qty Out: {total_qty_out}")

build_branch_moq('BOMAS', ['stock_movement_jan.json', 'stock_movement_feb.json'], 'bomas_average_moq.json')
build_branch_moq('KAREN', ['stock_movement_karen_jan.json', 'stock_movement_karen_feb.json'], 'karen_average_moq.json')
