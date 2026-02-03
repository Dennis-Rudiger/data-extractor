import json
import math
from collections import defaultdict

# Load stock movement data
with open('stock_movement_raw.json', 'r') as f:
    movement_data = json.load(f)

# Load inventory for category mapping
with open('inventory.json', 'r') as f:
    inventory = json.load(f)

# Build code-to-category and code-to-price mapping
code_to_category = {}
code_to_price = {}
for cat in inventory:
    cat_name = cat['category_name']
    for prod in cat['products']:
        code = prod.get('item_code', '').strip()
        if code:
            code_to_category[code] = cat_name
            code_to_price[code] = prod.get('buying_price', 0)

# Category inference rules for items not found in inventory
# Based on item code prefix or description keywords
def infer_category(code, desc):
    code_upper = code.upper().strip()
    desc_upper = desc.upper()
    
    # Paints - C/E, C/S, D/E, D/G, D/S, D/R and paint keywords
    if any(code_upper.startswith(prefix) for prefix in ['C/E', 'C/S', 'C/ ', 'D/E', 'D/G', 'D/S', 'D/R']):
        return 'PAINTS'
    if any(kw in desc_upper for kw in ['COVERMATT', 'SILK', 'GLOSS', 'MATT', 'EMULSION', 'VARNISH', 
                                        'PRIMER', 'AQUAGLOW', 'AQUA GLOW', 'LACQUER', 'UNDERCOAT',
                                        'SANDING SEALER', 'RUFF & TUFF', 'ROADLINE', 'TRANSEAL',
                                        'ROOFMASTER', 'EGGSHELL', 'VESTA', 'TWOPACK']):
        return 'PAINTS'
    
    # Steel - R/S (Rolled Steel Maisha), R Pipe, reinforcement bars
    if code_upper.startswith('R/S') or code_upper.startswith('R '):
        return 'STEEL'
    if 'MAISHA' in desc_upper and ('R/S' in code_upper or 'PIPE' in desc_upper):
        return 'STEEL'
    
    # Wire products
    if code_upper.startswith('BIN') or 'BINDING WIRE' in desc_upper:
        return 'WIRE PRODUCTS'
    
    # Gypsum - General Hardware
    if code_upper.startswith('GYP') or 'GYPSUM' in desc_upper:
        return 'GENERAL HARDWARE'
    
    # Nails
    if code_upper.startswith('NAI') or 'NAIL' in desc_upper:
        return 'NAILS'
    
    # Cutting disks - Tools
    if code_upper.startswith('CUT') or 'CUTTING DISK' in desc_upper:
        return 'TOOLS & MACHINERY'
    
    # Electricals - MCB, Insulating tape
    if code_upper.startswith('MCB') or code_upper.startswith('INS'):
        return 'ELECTRICALS'
    if any(kw in desc_upper for kw in ['CABLE', 'WIRE', 'SWITCH', 'SOCKET', 'CONDUIT', 'BULB', 'INSULATING']):
        return 'ELECTRICALS'
    
    # Plumbing - valves, pipes, butterfly, cyphone
    if code_upper.startswith('ANG') and 'VALVE' in desc_upper:
        return 'PLUMBING MATERIALS'
    if code_upper.startswith('BUT') or code_upper.startswith('CYP'):
        return 'PLUMBING MATERIALS'
    if any(kw in desc_upper for kw in ['PIPE', 'VALVE', 'TAP', 'FITTING', 'PPR', 'HDPE', 'BUTTERFLY', 'FLASH']):
        return 'PLUMBING MATERIALS'
    
    # J Bolts/Boxes - General Hardware (handle codes like "J            B001")
    if 'J BOLT' in desc_upper or 'J BOX' in desc_upper or code_upper.replace(' ', '').startswith('JB'):
        return 'GENERAL HARDWARE'
    
    # T Stoppers - Plumbing (handle codes like "T            S001")
    if 'STOPPER' in desc_upper or code_upper.replace(' ', '').startswith('TS'):
        return 'PLUMBING MATERIALS'
    
    # Transport/Services - exclude from product categories
    if 'TRANSPORT' in desc_upper:
        return 'SERVICES'
    
    # Tiles
    if 'TILE' in desc_upper or 'GROUT' in desc_upper:
        return 'TILES & ACCESSORIES'
    if any(kw in desc_upper for kw in ['CABLE', 'WIRE', 'SWITCH', 'SOCKET', 'CONDUIT', 'BULB']):
        return 'ELECTRICALS'
    
    return 'UNKNOWN'

# Constants
WORKING_DAYS = 19
DAYS_PER_WEEK = 6  # Working days per week

# Process movement data and calculate MOQ
results = {
    'parameters': {
        'monitoring_period': '19 working days',
        'period': 'January 2026',
        'formula': 'Daily Avg = Qty Out / 19 days | Weekly MOQ = Daily Avg x 6'
    },
    'summary': {
        'total_items': len(movement_data),
        'fast_movers': 0,
        'slow_movers': 0,
        'total_qty_in': 0,
        'total_qty_out': 0
    },
    'categories': defaultdict(lambda: {
        'total_items': 0,
        'fast_movers': 0,
        'slow_movers': 0,
        'total_qty_out': 0,
        'total_weekly_moq': 0,
        'total_weekly_value': 0,
        'products': []
    }),
    'fast_movers': [],
    'slow_movers': []
}

for item in movement_data:
    code = item['code']
    desc = item['description']
    qty_in = item['qty_in']
    qty_out = item['qty_out']
    
    # Get category - try exact match first, then infer from code/description
    category = code_to_category.get(code)
    if not category:
        category = infer_category(code, desc)
    buying_price = code_to_price.get(code, 0)
    
    # Calculate MOQ
    daily_avg = qty_out / WORKING_DAYS
    weekly_moq = math.ceil(daily_avg * DAYS_PER_WEEK)
    weekly_value = weekly_moq * buying_price
    
    product_data = {
        'item_code': code,
        'item_description': desc,
        'qty_in': qty_in,
        'qty_out': qty_out,
        'daily_average': round(daily_avg, 2),
        'weekly_moq': weekly_moq,
        'buying_price': buying_price,
        'weekly_value': round(weekly_value, 2)
    }
    
    # Update category data
    cat_data = results['categories'][category]
    cat_data['total_items'] += 1
    cat_data['total_qty_out'] += qty_out
    cat_data['total_weekly_moq'] += weekly_moq
    cat_data['total_weekly_value'] += weekly_value
    cat_data['products'].append(product_data)
    
    # Classify as fast or slow mover
    if qty_out > 0:
        results['fast_movers'].append(product_data)
        cat_data['fast_movers'] += 1
        results['summary']['fast_movers'] += 1
    else:
        results['slow_movers'].append(product_data)
        cat_data['slow_movers'] += 1
        results['summary']['slow_movers'] += 1
    
    results['summary']['total_qty_in'] += qty_in
    results['summary']['total_qty_out'] += qty_out

# Sort fast movers by qty_out descending
results['fast_movers'].sort(key=lambda x: x['qty_out'], reverse=True)

# Sort slow movers by qty_in descending (high stock but no sales)
results['slow_movers'].sort(key=lambda x: x['qty_in'], reverse=True)

# Convert defaultdict to regular dict and sort products
results['categories'] = dict(results['categories'])
for cat_name, cat_data in results['categories'].items():
    cat_data['products'].sort(key=lambda x: x['qty_out'], reverse=True)

# Calculate totals
total_weekly_moq = sum(c['total_weekly_moq'] for c in results['categories'].values())
total_weekly_value = sum(c['total_weekly_value'] for c in results['categories'].values())
results['summary']['total_weekly_moq'] = total_weekly_moq
results['summary']['total_weekly_value'] = round(total_weekly_value, 2)

# Save results
with open('moq_analysis.json', 'w') as f:
    json.dump(results, f, indent=2)

print('=' * 60)
print('MOQ ANALYSIS SUMMARY - 19 WORKING DAYS')
print('=' * 60)
print(f"Total Items: {results['summary']['total_items']}")
print(f"Fast Movers (Qty Out > 0): {results['summary']['fast_movers']}")
print(f"Slow Movers (Qty Out = 0): {results['summary']['slow_movers']}")
print(f"Total Qty In: {results['summary']['total_qty_in']:,.0f}")
print(f"Total Qty Out: {results['summary']['total_qty_out']:,.0f}")
print(f"Total Weekly MOQ: {total_weekly_moq:,}")
print(f"Total Weekly Value: KES {total_weekly_value:,.0f}")
print()
print('TOP 15 FAST MOVERS:')
print('-' * 60)
for i, item in enumerate(results['fast_movers'][:15], 1):
    print(f"{i:2}. {item['item_code']:10} {item['item_description'][:30]:30} Out: {item['qty_out']:>8,.0f}  MOQ: {item['weekly_moq']:>6}")
print()
print('CATEGORIES WITH FAST MOVERS:')
print('-' * 60)
sorted_cats = sorted(results['categories'].items(), key=lambda x: x[1]['total_qty_out'], reverse=True)
for cat_name, cat_data in sorted_cats[:15]:
    if cat_data['fast_movers'] > 0:
        print(f"{cat_name[:25]:25} Fast: {cat_data['fast_movers']:>4}  Slow: {cat_data['slow_movers']:>4}  Weekly MOQ: {cat_data['total_weekly_moq']:>6,}")

print()
print('Results saved to moq_analysis.json')
