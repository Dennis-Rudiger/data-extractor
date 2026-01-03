import json

def inspect_timber():
    with open('inventory_valuation_priced.json', 'r') as f:
        data = json.load(f)
    
    for group in data:
        if group['category_name'] == 'TIMBER':
            print(f"Category: TIMBER")
            for p in group['products'][:5]:
                print(f"  {p['item_code']}: {p['item_description']}")
            break

if __name__ == "__main__":
    inspect_timber()
