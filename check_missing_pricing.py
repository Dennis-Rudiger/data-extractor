import json

def check_missing_pricing():
    input_file = 'inventory_valuation_priced.json'
    
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {input_file} not found. Please run apply_pricing.py first.")
        return

    missing_categories = set()
    priced_categories = set()
    
    total_items = 0
    unpriced_items = 0

    print("Analyzing pricing coverage...")

    for group in data:
        category = group.get('category_name', 'Unknown')
        products = group.get('products', [])
        
        category_has_unpriced = False
        category_has_priced = False
        
        for product in products:
            total_items += 1
            selling_price = product.get('selling_price', 0)
            
            if selling_price == 0:
                unpriced_items += 1
                category_has_unpriced = True
            else:
                category_has_priced = True
        
        if category_has_unpriced:
            # If a category has ANY unpriced items, we might want to know.
            # But if it has NO priced items, it's definitely "missing" a rule.
            if not category_has_priced:
                missing_categories.add(category)
            else:
                # Partial coverage - maybe specific items missed by filters
                pass
        
        if category_has_priced:
            priced_categories.add(category)

    print(f"\nTotal Items: {total_items}")
    print(f"Unpriced Items: {unpriced_items}")
    
    print("\n--- Categories with NO pricing rules applied (Completely Missing) ---")
    if missing_categories:
        for cat in sorted(missing_categories):
            print(f"- {cat}")
    else:
        print("None. All categories have at least some priced items.")

    print("\n--- Categories with PARTIAL pricing (Check filters) ---")
    partial_categories = set()
    for group in data:
        category = group.get('category_name', 'Unknown')
        products = group.get('products', [])
        
        unpriced_in_cat = [p['item_code'] for p in products if p.get('selling_price', 0) == 0]
        priced_in_cat = [p['item_code'] for p in products if p.get('selling_price', 0) != 0]
        
        if unpriced_in_cat and priced_in_cat:
            print(f"- {category}: {len(unpriced_in_cat)} unpriced items (e.g., {unpriced_in_cat[:3]})")

if __name__ == "__main__":
    check_missing_pricing()
