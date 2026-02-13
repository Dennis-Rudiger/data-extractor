import json

# Load data
with open('stock_movement_jan.json', 'r') as f:
    movement = json.load(f)

with open('inventory.json', 'r') as f:
    inventory = json.load(f)

# Parameters
WORKING_DAYS = 24  # 4 weeks x 6 days
LEAD_TIME_DAYS = 6  # MOQ = 6 x Daily Consumption

# Build lookup from movement data
movement_lookup = {item['code']: item for item in movement['items']}

# Update inventory with new calculations
updated_count = 0
for category in inventory:
    for product in category.get('products', []):
        code = product.get('item_code', '')
        if code in movement_lookup:
            mov = movement_lookup[code]
            qty_out = mov.get('qty_out', 0)
            
            # Calculate daily consumption and MOQ
            daily_consumption = qty_out / WORKING_DAYS if WORKING_DAYS > 0 else 0
            moq = int(round(LEAD_TIME_DAYS * daily_consumption))
            reorder_point = int(round(LEAD_TIME_DAYS * daily_consumption))
            
            product['jan_qty_out'] = qty_out
            product['jan_closing'] = mov.get('closing', 0)
            product['daily_consumption'] = round(daily_consumption, 2)
            product['moq'] = moq
            product['reorder_point'] = reorder_point
            updated_count += 1

with open('inventory.json', 'w') as f:
    json.dump(inventory, f, indent=2)

# Also update inventory_valuation_priced.json
with open('inventory_valuation_priced.json', 'r') as f:
    priced = json.load(f)

priced_updated = 0
for item in priced:
    code = item.get('item_code', '')
    if code in movement_lookup:
        mov = movement_lookup[code]
        qty_out = mov.get('qty_out', 0)
        daily_consumption = qty_out / WORKING_DAYS if WORKING_DAYS > 0 else 0
        moq = int(round(LEAD_TIME_DAYS * daily_consumption))
        
        item['jan_qty_out'] = qty_out
        item['jan_closing'] = mov.get('closing', 0)
        item['daily_consumption'] = round(daily_consumption, 2)
        item['moq'] = moq
        item['reorder_point'] = moq
        priced_updated += 1

with open('inventory_valuation_priced.json', 'w') as f:
    json.dump(priced, f, indent=2)

print('=' * 60)
print('MOQ UPDATE COMPLETE')
print('=' * 60)
print(f'Updated {updated_count} items in inventory.json')
print(f'Updated {priced_updated} items in inventory_valuation_priced.json')
print(f'\nParameters:')
print(f'  Working days: {WORKING_DAYS} (4 weeks x 6 days/week)')
print(f'  MOQ Formula: {LEAD_TIME_DAYS} x Daily Consumption')

# Verify key items
print('\n' + '-' * 60)
print('VERIFICATION - Key items:')
print('-' * 60)
check_codes = ['SIM001', 'BAM005', 'C/E005', 'GI 001']
for code in check_codes:
    if code in movement_lookup:
        mov = movement_lookup[code]
        daily = mov['qty_out'] / WORKING_DAYS
        moq = int(round(LEAD_TIME_DAYS * daily))
        print(f"  {code}: qty_out={mov['qty_out']}, daily={daily:.2f}, MOQ={moq}")
