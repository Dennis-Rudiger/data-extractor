import json
import math

def calculate_selling_price(buying_price, min_buying, max_buying, min_target, max_target):
    if max_buying == min_buying:
        return min_target
    
    # Linear interpolation
    selling_price = min_target + ((buying_price - min_buying) / (max_buying - min_buying)) * (max_target - min_target)
    
    # Round to nearest 5
    return math.ceil(selling_price / 5) * 5

def calculate_sliding_margin_price(buying_price, min_buying, max_buying, min_margin, max_margin, exponent=1.0):
    """
    Calculates selling price with a sliding margin.
    Lower buying price -> Higher margin (max_margin)
    Higher buying price -> Lower margin (min_margin)
    exponent < 1.0: Margin drops faster (concave)
    exponent > 1.0: Margin drops slower (convex)
    """
    if max_buying == min_buying:
        margin = max_margin
    else:
        # Clamp buying price to range
        clamped_buying_price = max(min_buying, min(buying_price, max_buying))
        
        # Inverse interpolation for margin
        # buying_price at min_buying -> max_margin
        # buying_price at max_buying -> min_margin
        ratio = (clamped_buying_price - min_buying) / (max_buying - min_buying)
        
        # Apply exponent for non-linear sliding
        adjusted_ratio = math.pow(ratio, exponent)
        
        margin = max_margin - (adjusted_ratio * (max_margin - min_margin))
    
    selling_price = buying_price * (1 + margin / 100)
    return math.ceil(selling_price / 5) * 5

def apply_pricing():
    input_file = 'inventory_valuation.json'
    output_file = 'inventory_valuation_priced.json'
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Define pricing rules
    # Each rule is a dictionary with:
    # - 'name': Description of the group
    # - 'filter': Function that takes a product dict and returns True if it belongs to the group
    # - 'min_target': Minimum selling price (Optional if margin is used)
    # - 'max_target': Maximum selling price (Optional if margin is used)
    # - 'margin': Percentage margin (e.g., 10 for 10%) (Optional if min/max target is used)
    pricing_rules = [
        {
            'name': 'ADA Items',
            'filter': lambda p: p['item_code'].startswith('ADA'),
            'min_target': 150,
            'max_target': 700
        },
        {
            'name': 'Blanking Covers',
            'filter': lambda p: "Blanking Cover" in p['item_description'],
            'min_target': 15,
            'max_target': 30
        },
        {
            'name': 'Bulbs (BUL001-BUL004)',
            'filter': lambda p: p['item_code'] in ['BUL001', 'BUL002', 'BUL003', 'BUL004'],
            'min_target': 100,
            'max_target': 100
        },
        {
            'name': 'Cable Clips/Ties (CAB001-CAB011)',
            'filter': lambda p: p['item_code'].startswith('CAB') and p['item_code'] <= 'CAB011',
            'min_target': 10,
            'max_target': 250
        },
        {
            'name': 'Consumer Units',
            'filter': lambda p: "Consumer Unit" in p['item_description'],
            'margin': 10
        },
        {
            'name': 'Locks & Accessories',
            'filter': lambda p: False, # Placeholder, will be handled by category check in loop
            'category_name': 'LOCKS & ACCESSORIES',
            'min_margin': 12,
            'max_margin': 20
        },
        {
            'name': 'General Hardware',
            'category_name': 'GENERAL HARDWARE',
            'min_margin': 20,
            'max_margin': 150,
            'min_buying_threshold': 5.00,
            'max_buying_threshold': 1000.00,
            'margin_exponent': 0.15
        },
        {
            'name': 'Plumbing (Low Cost < 10)',
            'category_name': 'PLUMBING MATERIALS',
            'filter': lambda p: p['buying_price'] < 10,
            'min_margin': 65,
            'max_margin': 130,
            'min_buying_threshold': 0,
            'max_buying_threshold': 10
        },
        {
            'name': 'Plumbing (Gap 10-20)',
            'category_name': 'PLUMBING MATERIALS',
            'filter': lambda p: 10 <= p['buying_price'] < 20,
            'margin': 65
        },
        {
            'name': 'Plumbing (Mid Low 20-50)',
            'category_name': 'PLUMBING MATERIALS',
            'filter': lambda p: 20 <= p['buying_price'] < 50,
            'min_margin': 45,
            'max_margin': 65,
            'min_buying_threshold': 20,
            'max_buying_threshold': 50
        },
        {
            'name': 'Plumbing (Gap 50-90)',
            'category_name': 'PLUMBING MATERIALS',
            'filter': lambda p: 50 <= p['buying_price'] < 90,
            'margin': 45
        },
        {
            'name': 'Plumbing (Mid Avg 90-250)',
            'category_name': 'PLUMBING MATERIALS',
            'filter': lambda p: 90 <= p['buying_price'] < 250,
            'min_margin': 40,
            'max_margin': 50,
            'min_buying_threshold': 90,
            'max_buying_threshold': 250
        },
        {
            'name': 'Plumbing (Mid High 250-800)',
            'category_name': 'PLUMBING MATERIALS',
            'filter': lambda p: 250 <= p['buying_price'] < 800,
            'min_margin': 35,
            'max_margin': 40,
            'min_buying_threshold': 250,
            'max_buying_threshold': 800
        },
        {
            'name': 'Plumbing (Gap 800-1000)',
            'category_name': 'PLUMBING MATERIALS',
            'filter': lambda p: 800 <= p['buying_price'] < 1000,
            'margin': 35
        },
        {
            'name': 'Plumbing (High > 1000)',
            'category_name': 'PLUMBING MATERIALS',
            'filter': lambda p: p['buying_price'] >= 1000,
            'min_margin': 8,
            'max_margin': 28,
            'min_buying_threshold': 1000,
            'max_buying_threshold': 10000
        },
        {
            'name': 'Paint Accessories (Low Cost < 10)',
            'category_name': 'PAINT ACCESSORIES',
            'filter': lambda p: p['buying_price'] < 10,
            'min_margin': 65,
            'max_margin': 130,
            'min_buying_threshold': 0,
            'max_buying_threshold': 10
        },
        {
            'name': 'Paint Accessories (Gap 10-20)',
            'category_name': 'PAINT ACCESSORIES',
            'filter': lambda p: 10 <= p['buying_price'] < 20,
            'margin': 65
        },
        {
            'name': 'Paint Accessories (Mid Low 20-50)',
            'category_name': 'PAINT ACCESSORIES',
            'filter': lambda p: 20 <= p['buying_price'] < 50,
            'min_margin': 45,
            'max_margin': 65,
            'min_buying_threshold': 20,
            'max_buying_threshold': 50
        },
        {
            'name': 'Paint Accessories (Gap 50-90)',
            'category_name': 'PAINT ACCESSORIES',
            'filter': lambda p: 50 <= p['buying_price'] < 90,
            'margin': 45
        },
        {
            'name': 'Paint Accessories (Mid Avg 90-250)',
            'category_name': 'PAINT ACCESSORIES',
            'filter': lambda p: 90 <= p['buying_price'] < 250,
            'min_margin': 40,
            'max_margin': 50,
            'min_buying_threshold': 90,
            'max_buying_threshold': 250
        },
        {
            'name': 'Paint Accessories (Mid High 250-800)',
            'category_name': 'PAINT ACCESSORIES',
            'filter': lambda p: 250 <= p['buying_price'] < 800,
            'min_margin': 35,
            'max_margin': 40,
            'min_buying_threshold': 250,
            'max_buying_threshold': 800
        },
        {
            'name': 'Paint Accessories (Gap 800-1000)',
            'category_name': 'PAINT ACCESSORIES',
            'filter': lambda p: 800 <= p['buying_price'] < 1000,
            'margin': 35
        },
        {
            'name': 'Paint Accessories (High > 1000)',
            'category_name': 'PAINT ACCESSORIES',
            'filter': lambda p: p['buying_price'] >= 1000,
            'min_margin': 8,
            'max_margin': 28,
            'min_buying_threshold': 1000,
            'max_buying_threshold': 10000
        },
        {
            'name': 'Glues & Sealants (Low Cost < 10)',
            'category_name': 'GLUES & SEALANTS',
            'filter': lambda p: p['buying_price'] < 10,
            'min_margin': 65,
            'max_margin': 130,
            'min_buying_threshold': 0,
            'max_buying_threshold': 10
        },
        {
            'name': 'Glues & Sealants (Gap 10-20)',
            'category_name': 'GLUES & SEALANTS',
            'filter': lambda p: 10 <= p['buying_price'] < 20,
            'margin': 65
        },
        {
            'name': 'Glues & Sealants (Mid Low 20-50)',
            'category_name': 'GLUES & SEALANTS',
            'filter': lambda p: 20 <= p['buying_price'] < 50,
            'min_margin': 45,
            'max_margin': 65,
            'min_buying_threshold': 20,
            'max_buying_threshold': 50
        },
        {
            'name': 'Glues & Sealants (Gap 50-90)',
            'category_name': 'GLUES & SEALANTS',
            'filter': lambda p: 50 <= p['buying_price'] < 90,
            'margin': 45
        },
        {
            'name': 'Glues & Sealants (Mid Avg 90-250)',
            'category_name': 'GLUES & SEALANTS',
            'filter': lambda p: 90 <= p['buying_price'] < 250,
            'min_margin': 40,
            'max_margin': 50,
            'min_buying_threshold': 90,
            'max_buying_threshold': 250
        },
        {
            'name': 'Glues & Sealants (Mid High 250-800)',
            'category_name': 'GLUES & SEALANTS',
            'filter': lambda p: 250 <= p['buying_price'] < 800,
            'min_margin': 35,
            'max_margin': 40,
            'min_buying_threshold': 250,
            'max_buying_threshold': 800
        },
        {
            'name': 'Glues & Sealants (Gap 800-1000)',
            'category_name': 'GLUES & SEALANTS',
            'filter': lambda p: 800 <= p['buying_price'] < 1000,
            'margin': 35
        },
        {
            'name': 'Glues & Sealants (High > 1000)',
            'category_name': 'GLUES & SEALANTS',
            'filter': lambda p: p['buying_price'] >= 1000,
            'min_margin': 8,
            'max_margin': 28,
            'min_buying_threshold': 1000,
            'max_buying_threshold': 10000
        },
        {
            'name': 'Wire Products (Low Cost < 10)',
            'category_name': 'WIRE PRODUCTS',
            'filter': lambda p: p['buying_price'] < 10,
            'min_margin': 65,
            'max_margin': 130,
            'min_buying_threshold': 0,
            'max_buying_threshold': 10
        },
        {
            'name': 'Wire Products (Gap 10-20)',
            'category_name': 'WIRE PRODUCTS',
            'filter': lambda p: 10 <= p['buying_price'] < 20,
            'margin': 65
        },
        {
            'name': 'Wire Products (Mid Low 20-50)',
            'category_name': 'WIRE PRODUCTS',
            'filter': lambda p: 20 <= p['buying_price'] < 50,
            'min_margin': 45,
            'max_margin': 65,
            'min_buying_threshold': 20,
            'max_buying_threshold': 50
        },
        {
            'name': 'Wire Products (Gap 50-90)',
            'category_name': 'WIRE PRODUCTS',
            'filter': lambda p: 50 <= p['buying_price'] < 90,
            'margin': 45
        },
        {
            'name': 'Wire Products (Mid Avg 90-250)',
            'category_name': 'WIRE PRODUCTS',
            'filter': lambda p: 90 <= p['buying_price'] < 250,
            'min_margin': 40,
            'max_margin': 50,
            'min_buying_threshold': 90,
            'max_buying_threshold': 250
        },
        {
            'name': 'Wire Products (Mid High 250-800)',
            'category_name': 'WIRE PRODUCTS',
            'filter': lambda p: 250 <= p['buying_price'] < 800,
            'min_margin': 35,
            'max_margin': 40,
            'min_buying_threshold': 250,
            'max_buying_threshold': 800
        },
        {
            'name': 'Wire Products (Gap 800-1000)',
            'category_name': 'WIRE PRODUCTS',
            'filter': lambda p: 800 <= p['buying_price'] < 1000,
            'margin': 35
        },
        {
            'name': 'Wire Products (High > 1000)',
            'category_name': 'WIRE PRODUCTS',
            'filter': lambda p: p['buying_price'] >= 1000,
            'min_margin': 8,
            'max_margin': 28,
            'min_buying_threshold': 1000,
            'max_buying_threshold': 10000
        },
        {
            'name': 'Locks & Accessories (Low Cost < 10)',
            'category_name': 'LOCKS & ACCESSORIES',
            'filter': lambda p: p['buying_price'] < 10,
            'min_margin': 65,
            'max_margin': 130,
            'min_buying_threshold': 0,
            'max_buying_threshold': 10
        },
        {
            'name': 'Locks & Accessories (Gap 10-20)',
            'category_name': 'LOCKS & ACCESSORIES',
            'filter': lambda p: 10 <= p['buying_price'] < 20,
            'margin': 65
        },
        {
            'name': 'Locks & Accessories (Mid Low 20-50)',
            'category_name': 'LOCKS & ACCESSORIES',
            'filter': lambda p: 20 <= p['buying_price'] < 50,
            'min_margin': 45,
            'max_margin': 65,
            'min_buying_threshold': 20,
            'max_buying_threshold': 50
        },
        {
            'name': 'Locks & Accessories (Gap 50-90)',
            'category_name': 'LOCKS & ACCESSORIES',
            'filter': lambda p: 50 <= p['buying_price'] < 90,
            'margin': 45
        },
        {
            'name': 'Locks & Accessories (Mid Avg 90-250)',
            'category_name': 'LOCKS & ACCESSORIES',
            'filter': lambda p: 90 <= p['buying_price'] < 250,
            'min_margin': 40,
            'max_margin': 50,
            'min_buying_threshold': 90,
            'max_buying_threshold': 250
        },
        {
            'name': 'Locks & Accessories (Mid High 250-800)',
            'category_name': 'LOCKS & ACCESSORIES',
            'filter': lambda p: 250 <= p['buying_price'] < 800,
            'min_margin': 35,
            'max_margin': 40,
            'min_buying_threshold': 250,
            'max_buying_threshold': 800
        },
        {
            'name': 'Locks & Accessories (Gap 800-1000)',
            'category_name': 'LOCKS & ACCESSORIES',
            'filter': lambda p: 800 <= p['buying_price'] < 1000,
            'margin': 35
        },
        {
            'name': 'Locks & Accessories (High > 1000)',
            'category_name': 'LOCKS & ACCESSORIES',
            'filter': lambda p: p['buying_price'] >= 1000,
            'min_margin': 8,
            'max_margin': 28,
            'min_buying_threshold': 1000,
            'max_buying_threshold': 10000
        },
        {
            'name': 'Mortar and Adhesives (Low Cost < 10)',
            'category_name': 'MORTAR AND ADHESIVES',
            'filter': lambda p: p['buying_price'] < 10,
            'min_margin': 55,
            'max_margin': 110,
            'min_buying_threshold': 0,
            'max_buying_threshold': 10
        },
        {
            'name': 'Mortar and Adhesives (Gap 10-20)',
            'category_name': 'MORTAR AND ADHESIVES',
            'filter': lambda p: 10 <= p['buying_price'] < 20,
            'margin': 55
        },
        {
            'name': 'Mortar and Adhesives (Mid Low 20-50)',
            'category_name': 'MORTAR AND ADHESIVES',
            'filter': lambda p: 20 <= p['buying_price'] < 50,
            'min_margin': 40,
            'max_margin': 55,
            'min_buying_threshold': 20,
            'max_buying_threshold': 50
        },
        {
            'name': 'Mortar and Adhesives (Gap 50-90)',
            'category_name': 'MORTAR AND ADHESIVES',
            'filter': lambda p: 50 <= p['buying_price'] < 90,
            'margin': 40
        },
        {
            'name': 'Mortar and Adhesives (Mid Avg 90-250)',
            'category_name': 'MORTAR AND ADHESIVES',
            'filter': lambda p: 90 <= p['buying_price'] < 250,
            'min_margin': 35,
            'max_margin': 45,
            'min_buying_threshold': 90,
            'max_buying_threshold': 250
        },
        {
            'name': 'Mortar and Adhesives (Mid High 250-800)',
            'category_name': 'MORTAR AND ADHESIVES',
            'filter': lambda p: 250 <= p['buying_price'] < 800,
            'min_margin': 30,
            'max_margin': 35,
            'min_buying_threshold': 250,
            'max_buying_threshold': 800
        },
        {
            'name': 'Mortar and Adhesives (Gap 800-1000)',
            'category_name': 'MORTAR AND ADHESIVES',
            'filter': lambda p: 800 <= p['buying_price'] < 1000,
            'margin': 30
        },
        {
            'name': 'Mortar and Adhesives (High > 1000)',
            'category_name': 'MORTAR AND ADHESIVES',
            'filter': lambda p: p['buying_price'] >= 1000,
            'min_margin': 8,
            'max_margin': 25,
            'min_buying_threshold': 1000,
            'max_buying_threshold': 10000
        },
        {
            'name': 'Tanks',
            'category_name': 'TANKS',
            'margin': 20
        },
        {
            'name': 'Nails',
            'category_name': 'NAILS',
            'margin': 20
        },
        {
            'name': 'Iron Sheets & Plates (<= 2000)',
            'category_name': 'IRON SHEETS & PLATES',
            'filter': lambda p: p['buying_price'] <= 2000,
            'margin': 24
        },
        {
            'name': 'Iron Sheets & Plates (> 2000)',
            'category_name': 'IRON SHEETS & PLATES',
            'filter': lambda p: p['buying_price'] > 2000,
            'margin': 14
        },
        {
            'name': 'Welding Rods Simba',
            'category_name': 'WELDING MATERIALS',
            'filter': lambda p: 'simba' in p['item_description'].lower(),
            'fixed_price': 240
        },
        {
            'name': 'Welding Materials (General)',
            'category_name': 'WELDING MATERIALS',
            'filter': lambda p: 'simba' not in p['item_description'].lower(),
            'min_margin': 15,
            'max_margin': 22
        },
        {
            'name': 'Tools & Machinery (Low Cost < 10)',
            'category_name': 'TOOLS & MACHINERY',
            'filter': lambda p: p['buying_price'] < 10 and not any(x in p['item_description'].lower() for x in ['bosch', 'dewalt', 'stanley']),
            'min_margin': 65,
            'max_margin': 130,
            'min_buying_threshold': 0,
            'max_buying_threshold': 10
        },
        {
            'name': 'Tools & Machinery (Gap 10-20)',
            'category_name': 'TOOLS & MACHINERY',
            'filter': lambda p: 10 <= p['buying_price'] < 20 and not any(x in p['item_description'].lower() for x in ['bosch', 'dewalt', 'stanley']),
            'margin': 65
        },
        {
            'name': 'Tools & Machinery (Mid Low 20-50)',
            'category_name': 'TOOLS & MACHINERY',
            'filter': lambda p: 20 <= p['buying_price'] < 50 and not any(x in p['item_description'].lower() for x in ['bosch', 'dewalt', 'stanley']),
            'min_margin': 45,
            'max_margin': 65,
            'min_buying_threshold': 20,
            'max_buying_threshold': 50
        },
        {
            'name': 'Tools & Machinery (Gap 50-90)',
            'category_name': 'TOOLS & MACHINERY',
            'filter': lambda p: 50 <= p['buying_price'] < 90 and not any(x in p['item_description'].lower() for x in ['bosch', 'dewalt', 'stanley']),
            'margin': 45
        },
        {
            'name': 'Tools & Machinery (Mid Avg 90-250)',
            'category_name': 'TOOLS & MACHINERY',
            'filter': lambda p: 90 <= p['buying_price'] < 250 and not any(x in p['item_description'].lower() for x in ['bosch', 'dewalt', 'stanley']),
            'min_margin': 40,
            'max_margin': 50,
            'min_buying_threshold': 90,
            'max_buying_threshold': 250
        },
        {
            'name': 'Tools & Machinery (Mid High 250-800)',
            'category_name': 'TOOLS & MACHINERY',
            'filter': lambda p: 250 <= p['buying_price'] < 800 and not any(x in p['item_description'].lower() for x in ['bosch', 'dewalt', 'stanley']),
            'min_margin': 35,
            'max_margin': 40,
            'min_buying_threshold': 250,
            'max_buying_threshold': 800
        },
        {
            'name': 'Tools & Machinery (Gap 800-1000)',
            'category_name': 'TOOLS & MACHINERY',
            'filter': lambda p: 800 <= p['buying_price'] < 1000 and not any(x in p['item_description'].lower() for x in ['bosch', 'dewalt', 'stanley']),
            'margin': 35
        },
        {
            'name': 'Tools & Machinery (High > 1000)',
            'category_name': 'TOOLS & MACHINERY',
            'filter': lambda p: p['buying_price'] >= 1000 and not any(x in p['item_description'].lower() for x in ['bosch', 'dewalt', 'stanley']),
            'min_margin': 8,
            'max_margin': 28,
            'min_buying_threshold': 1000,
            'max_buying_threshold': 10000
        },
        {
            'name': 'Branded Tools (Bosch/DeWalt/Stanley)',
            'category_name': 'TOOLS & MACHINERY',
            'filter': lambda p: any(x in p['item_description'].lower() for x in ['bosch', 'dewalt', 'stanley']),
            'min_margin': 15,
            'max_margin': 20
        },
        {
            'name': 'Electricals (Low Cost < 10)',
            'category_name': 'ELECTRICALS',
            'filter': lambda p: p['buying_price'] < 10,
            'min_margin': 18,
            'max_margin': 36,
            'min_buying_threshold': 0,
            'max_buying_threshold': 10
        },
        {
            'name': 'Electricals (Gap 10-20)',
            'category_name': 'ELECTRICALS',
            'filter': lambda p: 10 <= p['buying_price'] < 20,
            'margin': 20
        },
        {
            'name': 'Electricals (Mid Low 20-50)',
            'category_name': 'ELECTRICALS',
            'filter': lambda p: 20 <= p['buying_price'] < 50,
            'min_margin': 18,
            'max_margin': 20,
            'min_buying_threshold': 20,
            'max_buying_threshold': 50
        },
        {
            'name': 'Electricals (Gap 50-90)',
            'category_name': 'ELECTRICALS',
            'filter': lambda p: 50 <= p['buying_price'] < 90,
            'margin': 18
        },
        {
            'name': 'Electricals (Mid Avg 90-250)',
            'category_name': 'ELECTRICALS',
            'filter': lambda p: 90 <= p['buying_price'] < 250,
            'min_margin': 15,
            'max_margin': 18,
            'min_buying_threshold': 90,
            'max_buying_threshold': 250
        },
        {
            'name': 'Electricals (Mid High 250-800)',
            'category_name': 'ELECTRICALS',
            'filter': lambda p: 250 <= p['buying_price'] < 800,
            'min_margin': 12,
            'max_margin': 15,
            'min_buying_threshold': 250,
            'max_buying_threshold': 800
        },
        {
            'name': 'Electricals (Gap 800-1000)',
            'category_name': 'ELECTRICALS',
            'filter': lambda p: 800 <= p['buying_price'] < 1000,
            'margin': 12
        },
        {
            'name': 'Electricals (High > 1000)',
            'category_name': 'ELECTRICALS',
            'filter': lambda p: p['buying_price'] >= 1000,
            'min_margin': 8,
            'max_margin': 12,
            'min_buying_threshold': 1000,
            'max_buying_threshold': 10000
        },
        {
            'name': 'Paints',
            'category_name': 'PAINTS',
            'min_margin': 8.9,
            'max_margin': 12
        },
        {
            'name': 'Agricultural Tools',
            'category_name': 'AGRICULTURAL TOOLS',
            'min_margin': 67,
            'max_margin': 77
        },
        {
            'name': 'Cement',
            'category_name': 'CEMENT',
            'margin': 4.5
        },
        {
            'name': 'Concrete & Yard',
            'category_name': 'CONCRETE & YARD',
            'min_margin': 15,
            'max_margin': 19
        },
        {
            'name': 'Jua Kali Products',
            'category_name': 'JUA KALI PRODUCTS',
            'min_margin': 50,
            'max_margin': 75
        },
        {
            'name': 'Steel',
            'category_name': 'STEEL',
            'min_margin': 5.5,
            'max_margin': 7
        },
        {
            'name': 'Tiles & Accessories',
            'category_name': 'TILES & ACCESSORIES',
            'min_margin': 25,
            'max_margin': 40
        },
        {
            'name': 'Timber Products',
            'category_name': 'TIMBER PRODUCTS',
            'min_margin': 15,
            'max_margin': 28
        },
        {
            'name': 'Timber',
            'category_name': 'TIMBER',
            'min_margin': 15,
            'max_margin': 28
        },
        {
            'name': 'Glassware',
            'category_name': 'GLASSWARE',
            'margin': 20
        },
        {
            'name': 'Unknown',
            'category_name': 'UNKNOWN',
            'margin': 15
        }
    ]
    
    # Apply each rule
    for rule in pricing_rules:
        print(f"Processing rule: {rule['name']}")
        
        # 1. Collect items matching the rule
        matching_items = []
        for group in data:
            # Check if rule applies to entire category
            is_category_match = 'category_name' in rule and group['category_name'] == rule['category_name']
            
            if is_category_match:
                if 'filter' not in rule:
                    # Rule applies to entire category without filter
                    matching_items.extend(group['products'])
                    continue
                else:
                    # Rule applies to category BUT has a filter (e.g. price range)
                    for product in group['products']:
                        if rule['filter'](product):
                            matching_items.append(product)
                    continue
            
            # If rule has a category constraint but this group doesn't match, skip
            if 'category_name' in rule and not is_category_match:
                continue

            # Global filter (no category constraint)
            for product in group['products']:
                if 'filter' in rule and rule['filter'](product):
                    matching_items.append(product)
        
        if not matching_items:
            print(f"  No items found for {rule['name']}")
            continue
            
        # 2. Find min/max buying price (Only needed for interpolation or sliding margin)
        if ('min_target' in rule and 'max_target' in rule) or ('min_margin' in rule and 'max_margin' in rule):
            min_buying = min(item['buying_price'] for item in matching_items)
            max_buying = max(item['buying_price'] for item in matching_items)
            
            # Override with fixed thresholds if provided
            if 'min_buying_threshold' in rule:
                min_buying = rule['min_buying_threshold']
            if 'max_buying_threshold' in rule:
                max_buying = rule['max_buying_threshold']
            
            print(f"  Found {len(matching_items)} items. Buying Price Range: {min_buying} - {max_buying}")
            
            # 3. Apply pricing
            for item in matching_items:
                buying_price = item['buying_price']
                
                if 'min_target' in rule:
                    selling_price = calculate_selling_price(
                        buying_price, 
                        min_buying, 
                        max_buying, 
                        rule['min_target'], 
                        rule['max_target']
                    )
                else: # Sliding margin
                    exponent = rule.get('margin_exponent', 1.0)
                    selling_price = calculate_sliding_margin_price(
                        buying_price,
                        min_buying,
                        max_buying,
                        rule['min_margin'],
                        rule['max_margin'],
                        exponent
                    )
                    
                item['selling_price'] = selling_price
                
                margin = ((selling_price - buying_price) / buying_price) * 100 if buying_price > 0 else 0
                print(f"    {item['item_code']}: Buying {buying_price} -> Selling {selling_price} (Margin: {margin:.2f}%)")
        
        elif 'fixed_price' in rule:
             # 3. Apply pricing (Fixed Price)
             print(f"  Found {len(matching_items)} items. Applying fixed price {rule['fixed_price']}.")
             for item in matching_items:
                buying_price = item['buying_price']
                selling_price = rule['fixed_price']
                item['selling_price'] = selling_price
                
                margin = ((selling_price - buying_price) / buying_price) * 100 if buying_price > 0 else 0
                print(f"    {item['item_code']}: Buying {buying_price} -> Selling {selling_price} (Margin: {margin:.2f}%)")

        elif 'margin' in rule:
             # 3. Apply pricing (Margin)
             print(f"  Found {len(matching_items)} items. Applying {rule['margin']}% margin.")
             for item in matching_items:
                buying_price = item['buying_price']
                selling_price = buying_price * (1 + rule['margin'] / 100)
                # Round to nearest 5
                selling_price = math.ceil(selling_price / 5) * 5
                item['selling_price'] = selling_price
                
                margin = ((selling_price - buying_price) / buying_price) * 100 if buying_price > 0 else 0
                print(f"    {item['item_code']}: Buying {buying_price} -> Selling {selling_price} (Margin: {margin:.2f}%)")

    # Ensure all items have a selling_price (default to buying_price if not set)
    for group in data:
        for product in group['products']:
            if 'selling_price' not in product:
                product['selling_price'] = 0 # Placeholder or product['buying_price']

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Pricing applied. Saved to {output_file}")

if __name__ == "__main__":
    apply_pricing()
