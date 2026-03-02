"""
Update MOQ Analysis for February 2026
======================================
Reads: stock_movement_feb.json  (from INVENTORY MOVEMENT FEBRUARY.pdf)
       item_category_map.json   (from INVENTORY COUNT feb.pdf)
       inventory.json           (master product catalog with pricing)

Outputs:
  - inventory.json  (updated with feb_qty_out, feb_closing, daily_consumption, moq)
  - moq_analysis.json (full MOQ analysis for February)

Period: February 1-28, 2026 (24 working days)
Formula: MOQ = 6 × Daily Consumption (daily = qty_out / 24)
"""

import json
import math
import re
from collections import defaultdict

# ===== PARAMETERS =====
WORKING_DAYS = 24
MOQ_MULTIPLIER = 6
PERIOD = "February 1-28, 2026"
PERIOD_SHORT = "February 2026"

# ===== LOAD DATA =====
print("=" * 60)
print("MOQ UPDATE — FEBRUARY 2026")
print("=" * 60)

with open('stock_movement_feb.json', 'r') as f:
    feb_data = json.load(f)

with open('inventory.json', 'r') as f:
    inventory = json.load(f)

# Primary category source: extracted from INVENTORY COUNT feb.pdf
try:
    with open('item_category_map.json', 'r') as f:
        pdf_category_map = json.load(f)
    print(f"Loaded {len(pdf_category_map)} items from item_category_map.json")
except FileNotFoundError:
    pdf_category_map = {}
    print("WARNING: item_category_map.json not found — using fallback only")

feb_items = feb_data['items']
print(f"Loaded {len(feb_items)} items from February movement data")
print(f"Loaded {len(inventory)} categories from inventory.json")

# ===== BUILD LOOKUPS =====
feb_lookup = {}
for item in feb_items:
    feb_lookup[item['code']] = item

# Inventory lookup: code -> category and pricing
inv_category_map = {}
code_to_price = {}
for cat in inventory:
    cat_name = cat.get('category_name', '')
    for prod in cat.get('products', []):
        code = prod.get('item_code', '').strip()
        if code:
            inv_category_map[code] = cat_name
            code_to_price[code] = prod.get('buying_price', 0)


def infer_category(code, desc):
    """Last-resort inference for items not in PDF map or inventory.json"""
    cu = code.upper().strip()
    du = desc.upper()

    # ---- Steel / D-bars / Tubes / R-bars ----
    if re.match(r'^D\s?\d', cu):                          # D 10, D8A, D12, D25, D16, D 8, D 1001 etc
        return 'STEEL'
    if cu.startswith('R/S'):                               # R/S roofing sheets
        return 'IRON SHEETS & PLATES'
    if re.match(r'^R\s?\d', cu):                           # R 6, R 16 (round bars)
        return 'STEEL'
    if cu.startswith('TUB'):                               # Tubes
        return 'STEEL'
    if cu.startswith('SQ '):                               # Square tubes
        return 'STEEL'
    if any(kw in du for kw in ['MAISHA', 'FLAT BAR', 'SQUARE BAR', 'ROUND BAR',
                                'REINFORCEMENT', 'ANGLE LINE', 'KIFARU', 'ACCURATE']):
        return 'STEEL'

    # ---- Cement ----
    if cu.startswith('BAM') or cu.startswith('SIM') or cu.startswith('NYU') or cu.startswith('CEM'):
        return 'CEMENT'
    if any(kw in du for kw in ['CEMENT', 'SIMBA', 'TEMBO', 'BAMBURI', 'NGUVU', 'NYUMBA',
                                'POWERMAX', 'LIME']):
        return 'CEMENT'

    # ---- Paints (code-based) ----
    if any(cu.startswith(p) for p in ['C/E', 'C/S', 'C/ ', 'D/E', 'D/G', 'D/S', 'D/R',
                                       'CSG', 'BAS', 'SPR']):
        return 'PAINTS'
    if any(kw in du for kw in ['COVERMATT', 'SILK', 'GLOSS', 'EMULSION', 'VARNISH',
                                'PRIMER', 'AQUAGLOW', 'AQUA GLOW', 'LACQUER', 'UNDERCOAT',
                                'SANDING SEALER', 'RUFF & TUFF', 'ROADLINE', 'TRANSEAL',
                                'ROOFMASTER', 'EGGSHELL', 'VESTA', 'TWOPACK', 'SHELLAC',
                                'SPRAY PAINT', 'THINNER', 'STAIN']):
        return 'PAINTS'

    # ---- Paint Accessories ----
    if cu.startswith('SAN') and 'SAND PAPER' in du or 'SANDPAPER' in du:
        return 'PAINT ACCESSORIES'
    if cu.startswith('PUT') and 'PUTTY' in du:
        return 'PAINT ACCESSORIES'
    if any(kw in du for kw in ['BRUSH', 'ROLLER', 'MASKING TAPE', 'PAINT SCRAPER',
                                'SAND PAPER', 'SANDPAPER', 'PUTTY']):
        return 'PAINT ACCESSORIES'

    # ---- Plumbing Materials ----
    if cu.startswith('GI ') or cu.startswith('GI') and len(cu) > 2 and cu[2:3] == ' ':
        return 'PLUMBING MATERIALS'
    if any(cu.startswith(p) for p in ['PPR', 'HDP', 'PVC', 'CYP', 'FLA0']):
        return 'PLUMBING MATERIALS'
    if cu.startswith('NEM'):                               # Nemsi bathroom fixtures
        return 'PLUMBING MATERIALS'
    if cu.startswith('WAT') and 'HEATER' in du:
        return 'ELECTRICALS'
    if any(kw in du for kw in ['PIPE', 'VALVE', 'FITTING', 'PPR', 'HDPE',
                                'BUTTERFLY', 'SHOWER', 'CISTERN', 'BALLCOCK',
                                'STOPPER', 'ELBOW', 'COUPLING', 'REDUCER', 'NIPPLE',
                                'FLUSHER', 'MIXER', 'PILLAR TAP', 'BIB', 'PLUG',
                                'GI HEX', 'GI SOCKET', 'GI TEE', 'GI ELBOW',
                                'GI CUP', 'GI BUSH', 'GI UNION', 'GI CROSS',
                                'NEMSI', 'TOWEL', 'GRAB BAR', 'SHELF', 'TISSUE HOLDER']):
        return 'PLUMBING MATERIALS'

    # ---- Electricals ----
    if any(cu.startswith(p) for p in ['MCB', 'INS', '1GA', 'LED', 'DOW', 'PAN0',
                                       'AUT', 'ELE', 'CAB', 'BUL', 'DOO', 'ADA',
                                       'PAT0']):           # PAT004 = Pattress
        return 'ELECTRICALS'
    if any(kw in du for kw in ['CABLE', 'SWITCH', 'SOCKET', 'CONDUIT', 'BULB',
                                'INSULATING', 'MCB', 'ADAPTOR BOX', 'GANG',
                                'FLOOD LIGHT', 'DOWN LIGHTER', 'PANEL LIGHT',
                                'VOLTAGE REGULATOR', 'WATER HEATER', 'PATTRESS',
                                'LED', 'EARTH ROD']):
        return 'ELECTRICALS'

    # ---- Mortar and Adhesives / Dr Fixit ----
    if cu.startswith('DR '):
        return 'MORTAR AND ADHESIVES'
    if cu.startswith('USP'):
        return 'MORTAR AND ADHESIVES'
    if any(kw in du for kw in ['MORTAR', 'ADHESIVE', 'SIKA', 'BONDEX', 'DR FIXIT',
                                'TILE ADHESIVE', 'WATERPROOF', 'USPRO', 'FOAM']):
        return 'MORTAR AND ADHESIVES'

    # ---- Glues & Sealants ----
    if cu.startswith('BOS') and 'BOSS WHITE' in du:
        return 'GLUES & SEALANTS'
    if any(kw in du for kw in ['GLUE', 'SEALANT', 'SILICONE', 'ARALDITE', 'EPOXY',
                                'PATTEX', 'BOSS WHITE', 'BODY FILLER']):
        return 'GLUES & SEALANTS'

    # ---- Tools & Machinery ----
    if any(cu.startswith(p) for p in ['BOS', 'DEW', 'CUT']):
        return 'TOOLS & MACHINERY'
    if any(kw in du for kw in ['DRILL', 'SAW', 'HAMMER', 'CHISEL', 'PLIER', 'SPANNER',
                                'WHEELBARROW', 'TAPE MEASURE', 'LEVEL', 'BOSCH', 'DEWALT',
                                'STANLEY', 'GRINDER', 'ROUTER', 'FLAP DISC', 'CUTTING DISK',
                                'SAFETY GLOVES', 'WIRE BRUSH', 'BROOM', 'SHEARS']):
        return 'TOOLS & MACHINERY'

    # ---- Wire products ----
    if cu.startswith('BIN') or 'BINDING WIRE' in du:
        return 'WIRE PRODUCTS'
    if any(kw in du for kw in ['BARBED WIRE', 'CHAIN LINK', 'WIRE MESH', 'BRC']):
        return 'WIRE PRODUCTS'

    # ---- Nails ----
    if cu.startswith('NAI') or 'NAIL' in du:
        return 'NAILS'

    # ---- Timber ----
    if cu.startswith('BLO') and ('BLOCKBOARD' in du or 'BLOCK BOARD' in du):
        return 'TIMBER'
    if cu.startswith('MAR') and 'MARINE BOARD' in du:
        return 'TIMBER PRODUCTS'
    if any(kw in du for kw in ['TIMBER', 'PLYWOOD', 'MDF', 'HARDBOARD', 'CHIPBOARD',
                                'BLOCKBOARD']):
        return 'TIMBER'
    if any(kw in du for kw in ['DOOR', 'HINGE', 'WOOD SCREW', 'WOOD PRESERV']):
        return 'TIMBER PRODUCTS'

    # ---- Iron Sheets ----
    if any(kw in du for kw in ['IRON SHEET', 'MABATI', 'GAUGE', 'RIDGING', 'ROOFING BOLT',
                                'ROOFING SCREW', 'ROOFING WASHER', 'NYLON NETTING']):
        return 'IRON SHEETS & PLATES'

    # ---- Tiles ----
    if any(kw in du for kw in ['TILE', 'GROUT']):
        return 'TILES & ACCESSORIES'

    # ---- Glassware ----
    if any(kw in du for kw in ['GLASS', 'MIRROR']):
        return 'GLASSWARE'

    # ---- Locks ----
    if cu.startswith('LOC') or cu.startswith('PAD'):
        return 'LOCKS & ACCESSORIES'
    if any(kw in du for kw in ['LOCK', 'PADLOCK', 'DEADLOCK', 'LATCH']):
        return 'LOCKS & ACCESSORIES'

    # ---- Welding ----
    if any(kw in du for kw in ['WELDING', 'ELECTRODE', 'WELD ROD']):
        return 'WELDING MATERIALS'

    # ---- Tanks ----
    if cu.startswith('DOV') and 'TANK' in du:
        return 'TANKS'
    if any(kw in du for kw in ['TANK', 'WATER TANK']):
        return 'TANKS'

    # ---- Concrete & Yard ----
    if cu.startswith('BAL') and ('BALLAST' in du or 'SAND' in du):
        return 'CONCRETE & YARD'
    if any(kw in du for kw in ['BALLAST', 'CONCRETE', 'BLOCK']):
        return 'CONCRETE & YARD'

    # ---- Agricultural Tools ----
    if any(kw in du for kw in ['GARDEN', 'HOE', 'MACHETE', 'PANGA', 'RAKE', 'SPADE',
                                'JEMBE', 'SLASHER']):
        return 'AGRICULTURAL TOOLS'

    # ---- Jua Kali ----
    if any(kw in du for kw in ['JUA KALI', 'JIKO']):
        return 'JUA KALI PRODUCTS'

    # ---- General Hardware (broader catch) ----
    if cu.startswith('GYP') or 'GYPSUM' in du:
        return 'GENERAL HARDWARE'
    if cu.startswith('MAN') and 'MANILLA' in du:
        return 'GENERAL HARDWARE'
    if cu.startswith('KHA') and 'KHAKI' in du:
        return 'GENERAL HARDWARE'
    if cu.startswith('POL') and 'POLYTHENE' in du:
        return 'GENERAL HARDWARE'
    if cu.startswith('PAC') and ('PACKING' in du or 'TAPE' in du):
        return 'GENERAL HARDWARE'
    if any(kw in du for kw in ['BOLT', 'NUT', 'SCREW', 'WASHER', 'BRACKET',
                                'MANILLA ROPE', 'KHAKI BAG', 'POLYTHENE',
                                'CHROME BRACKET', 'HANDLE', 'DRAWER',
                                'HOOK', 'WIRE ROPE', 'DUCT TAPE']):
        return 'GENERAL HARDWARE'

    # ---- Transport/Services ----
    if 'TRANSPORT' in du or 'VARIANCE' in du:
        return 'SERVICES'

    return 'GENERAL HARDWARE'   # Default to General Hardware instead of GENERAL


def get_category(code, desc):
    """3-tier category lookup: PDF map → inventory.json → infer"""
    cat = pdf_category_map.get(code)
    if cat:
        return cat
    cat = inv_category_map.get(code)
    if cat and cat != 'GENERAL':
        return cat
    return infer_category(code, desc)


# ===== STEP 1: UPDATE INVENTORY.JSON =====
print("\n--- Step 1: Updating inventory.json with Feb data ---")
updated_count = 0
for category in inventory:
    for product in category.get('products', []):
        code = product.get('item_code', '')
        if code in feb_lookup:
            mov = feb_lookup[code]
            qty_out = mov['qty_out']
            daily_consumption = qty_out / WORKING_DAYS if WORKING_DAYS > 0 else 0
            moq = int(round(MOQ_MULTIPLIER * daily_consumption))

            product['feb_qty_out'] = qty_out
            product['feb_closing'] = mov['closing']
            product['daily_consumption'] = round(daily_consumption, 2)
            product['moq'] = moq
            product['reorder_point'] = moq
            updated_count += 1

with open('inventory.json', 'w') as f:
    json.dump(inventory, f, indent=2)
print(f"Updated {updated_count} items in inventory.json")


# ===== STEP 2: BUILD MOQ ANALYSIS =====
print("\n--- Step 2: Building MOQ analysis ---")

categories = defaultdict(lambda: {
    'total_items': 0,
    'fast_movers': 0,
    'slow_movers': 0,
    'total_qty_out': 0,
    'total_weekly_moq': 0,
    'total_weekly_value': 0,
    'products': []
})

all_fast = []
all_slow = []
cat_source_stats = {'pdf': 0, 'inv': 0, 'infer': 0}

for item in feb_items:
    code = item['code']
    desc = item['description']
    qty_in = item['qty_in']
    qty_out = item['qty_out']
    closing = item['closing']

    # 3-tier category lookup
    category = get_category(code, desc)
    if category == 'SERVICES':
        continue

    # Track source
    if code in pdf_category_map:
        cat_source_stats['pdf'] += 1
    elif code in inv_category_map:
        cat_source_stats['inv'] += 1
    else:
        cat_source_stats['infer'] += 1

    buying_price = code_to_price.get(code, 0)

    daily_avg = qty_out / WORKING_DAYS
    weekly_moq = math.ceil(daily_avg * MOQ_MULTIPLIER) if qty_out > 0 else 0
    weekly_value = weekly_moq * buying_price

    product_data = {
        'item_code': code,
        'item_description': desc,
        'qty_in': qty_in,
        'qty_out': qty_out,
        'closing_balance': closing,
        'daily_average': round(daily_avg, 2),
        'weekly_moq': weekly_moq,
        'buying_price': buying_price,
        'weekly_value': round(weekly_value, 2),
        'category': category,
    }

    cat_data = categories[category]
    cat_data['total_items'] += 1
    cat_data['total_qty_out'] += qty_out
    cat_data['total_weekly_moq'] += weekly_moq
    cat_data['total_weekly_value'] += weekly_value
    cat_data['products'].append(product_data)

    if qty_out > 0:
        cat_data['fast_movers'] += 1
        all_fast.append(product_data)
    else:
        cat_data['slow_movers'] += 1
        all_slow.append(product_data)

# Sort
all_fast.sort(key=lambda x: x['qty_out'], reverse=True)
all_slow.sort(key=lambda x: x['qty_in'], reverse=True)

for cat_name, cat_data in categories.items():
    cat_data['products'].sort(key=lambda x: x['qty_out'], reverse=True)

# Summary
total_items = sum(c['total_items'] for c in categories.values())
total_fast = sum(c['fast_movers'] for c in categories.values())
total_slow = sum(c['slow_movers'] for c in categories.values())
total_qty_out = sum(c['total_qty_out'] for c in categories.values())
total_weekly_moq = sum(c['total_weekly_moq'] for c in categories.values())
total_weekly_value = sum(c['total_weekly_value'] for c in categories.values())

analysis = {
    'period': PERIOD,
    'working_days': WORKING_DAYS,
    'moq_multiplier': MOQ_MULTIPLIER,
    'formula': f'MOQ = {MOQ_MULTIPLIER} x Daily Consumption',
    'summary': {
        'total_items': total_items,
        'fast_movers': total_fast,
        'slow_movers': total_slow,
        'total_qty_out': round(total_qty_out, 2),
        'total_weekly_moq': total_weekly_moq,
        'total_weekly_value': round(total_weekly_value, 2),
    },
    'categories': dict(categories),
    'fast_movers': all_fast,
    'slow_movers': all_slow,
}

with open('moq_analysis.json', 'w') as f:
    json.dump(analysis, f, indent=2)
print(f"MOQ analysis saved to moq_analysis.json")

# ===== STEP 3: PRINT SUMMARY =====
print("\n" + "=" * 70)
print(f"MOQ ANALYSIS — {PERIOD_SHORT.upper()} ({WORKING_DAYS} Working Days)")
print("=" * 70)
print(f"  Total Items:      {total_items:,}")
print(f"  Fast Movers:      {total_fast:,} (qty out > 0)")
print(f"  Slow Movers:      {total_slow:,} (qty out = 0)")
print(f"  Total Qty Out:    {total_qty_out:,.0f}")
print(f"  Weekly MOQ:       {total_weekly_moq:,}")
print(f"  Weekly Value:     KES {total_weekly_value:,.0f}")
print(f"\n  Category source:  PDF map={cat_source_stats['pdf']}  inventory={cat_source_stats['inv']}  inferred={cat_source_stats['infer']}")

hdr = f"\n{'Category':<28} {'Items':>5} {'Fast':>5} {'Slow':>5} {'Qty Out':>10} {'Wk MOQ':>8}"
print(hdr)
print("-" * 72)
sorted_cats = sorted(categories.items(), key=lambda x: x[1]['total_qty_out'], reverse=True)
for cat_name, c in sorted_cats:
    print(f"  {cat_name[:26]:<26} {c['total_items']:>5} {c['fast_movers']:>5} {c['slow_movers']:>5} {c['total_qty_out']:>10,.0f} {c['total_weekly_moq']:>8,}")

print(f"\nTOP 15 FAST MOVERS:")
print("-" * 72)
for i, item in enumerate(all_fast[:15], 1):
    print(f"  {i:2}. {item['item_code']:10} {item['item_description'][:30]:30} Out: {item['qty_out']:>8,.0f}  MOQ: {item['weekly_moq']:>6}")

print("\nDone! Now run: py generate_moq_report.py")
