import pdfplumber
import json
import re

# 1. Load Bomas to create exact code dictionaries
with open('bomas_average_moq.json', 'r', encoding='utf-8') as f:
    bomas_data = json.load(f)

item_details = {}
valid_codes = set()
for cat_name, cat_data in bomas_data['categories'].items():
    for prod in cat_data['products']:
        code = str(prod.get('item_code', '')).strip()
        valid_codes.add(code)
        item_details[code] = {
            'category': cat_name,
            'buying_price': prod.get('buying_price', 0)
        }
        
# Add a few manual fallbacks if needed (handling weird spacing)
for c in list(valid_codes):
    if ' ' in c:
        valid_codes.add(c.replace(' ', ''))
        
WORKING_DAYS = 36
MOQ_MULTIPLIER = 6
new_products = []

pdf = pdfplumber.open('movement summary March.pdf')
for page in pdf.pages:
    text = page.extract_text()
    if not text: continue
    for line in text.split('\n'):
        if any(skip in line for skip in ['Inventory Item', 'Opening Balance', 'Page', 'PANNJU', 'Inventory Movement']):
            continue
            
        # Parse using split BOMAS since 'BOMAS' is always the bridge before num values
        parts = line.split(' BOMAS ')
        if len(parts) != 2:
            parts = line.split(' BOMAS')
            if len(parts) != 2:
                continue
                
        left_str = parts[0].strip()
        num_str = parts[-1].strip()
        
        # Numbers: OpenBal QtyIn QtyOut CloseBal
        nums = num_str.split()
        if len(nums) < 4:
            continue
            
        try:
            qty_in = float(nums[1].replace(',', ''))
            qty_out = float(nums[2].replace(',', ''))
            closing = float(nums[3].replace(',', ''))
        except:
            continue
            
        # Code logic: left_str contains [Code] [Description]
        tokens = left_str.split()
        code = None
        desc = ""
        
        # Try 3-word code (rare but possible)
        if len(tokens) > 2 and f"{tokens[0]} {tokens[1]} {tokens[2]}" in valid_codes:
            code = f"{tokens[0]} {tokens[1]} {tokens[2]}"
            desc = " ".join(tokens[3:])
        # Try 2-word code
        elif len(tokens) > 1 and f"{tokens[0]} {tokens[1]}" in valid_codes:
            code = f"{tokens[0]} {tokens[1]}"
            desc = " ".join(tokens[2:])
        # Try 1-word code
        elif tokens[0] in valid_codes:
            code = tokens[0]
            desc = " ".join(tokens[1:])
        elif len(tokens) > 1 and tokens[0] + tokens[1] in valid_codes: # Handled spacing differences
            code = tokens[0] + tokens[1]
            desc = " ".join(tokens[2:])
        else:
            # No exact match, fallback to heuristic
            if len(tokens) > 1 and len(tokens[0]) <= 3 and tokens[0].isalpha(): # like D 1001, R 12, etc
                 code = f"{tokens[0]} {tokens[1]}"
                 desc = " ".join(tokens[2:])
            else:
                 code = tokens[0]
                 desc = " ".join(tokens[1:])
                 
        daily_avg = qty_out / WORKING_DAYS
        moq = round(daily_avg * MOQ_MULTIPLIER)
        
        info = item_details.get(code, item_details.get(code.replace(' ', ''), {'category': 'UNKNOWN', 'buying_price': 0}))
        cat = info['category']
        bp = info['buying_price']
        
        new_products.append({
            'item_code': code,
            'item_description': desc,
            'qty_in': qty_in,
            'qty_out': qty_out,
            'closing_balance': closing,
            'daily_average': round(daily_avg, 2),
            '1_week_moq': moq,
            '2_week_moq': moq * 2,
            'buying_price': bp,
            'weekly_value': moq * bp,
            'category': cat
        })

pdf.close()

categories = {}
total_qty = 0
total_1_moq = 0
total_2_moq = 0
total_val = 0
fast_movers = 0

for p in new_products:
    c = p['category']
    if c not in categories:
        categories[c] = {
            "total_items": 0, "fast_movers": 0, "slow_movers": 0,
            "total_qty_out": 0, "total_1_week_moq": 0, "total_2_week_moq": 0, "total_weekly_value": 0,
            "products": []
        }
    categories[c]['products'].append(p)
    categories[c]['total_items'] += 1
    if p['qty_out'] > 0:
        categories[c]['fast_movers'] += 1
        fast_movers += 1
    else:
        categories[c]['slow_movers'] += 1
        
    categories[c]['total_qty_out'] += p['qty_out']
    categories[c]['total_1_week_moq'] += p['1_week_moq']
    categories[c]['total_2_week_moq'] += p['2_week_moq']
    categories[c]['total_weekly_value'] += p['weekly_value']

    total_qty += p['qty_out']
    total_1_moq += p['1_week_moq']
    total_2_moq += p['2_week_moq']
    total_val += p['weekly_value']

out_data = {
  "period": "March - April (36 Days)",
  "working_days": WORKING_DAYS,
  "moq_multiplier": 6,
  "summary": {
    "total_items": len(new_products),
    "fast_movers": fast_movers,
    "slow_movers": len(new_products) - fast_movers,
    "total_qty_out": round(total_qty, 2),
    "total_1_week_moq": total_1_moq,
    "total_2_week_moq": total_2_moq,
    "total_weekly_value": round(total_val, 2)
  },
  "categories": categories
}

with open('march_april_moq.json', 'w', encoding='utf-8') as f:
    json.dump(out_data, f, indent=2)

print(f'Extracted {len(new_products)} products to march_april_moq.json!')
