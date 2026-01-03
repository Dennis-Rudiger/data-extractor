import json

def inspect_glassware():
    with open('inventory_valuation_priced.json', 'r') as f:
        data = json.load(f)
    
    for group in data:
        if group['category_name'] == 'GLASSWARE':
            print(f"Category: GLASSWARE")
            for p in group['products'][:5]:
                print(f"  {p['item_code']}: {p['item_description']}")
            break

if __name__ == "__main__":
    inspect_glassware()
