import json

def inspect_unpriced():
    with open('inventory_valuation_priced.json', 'r') as f:
        data = json.load(f)

    unpriced_electricals = []
    unpriced_tools = []

    for item in data:
        if item.get('selling_price', 0) == 0:
            cat = item.get('category_name', 'Unknown')
            if cat == 'ELECTRICALS':
                unpriced_electricals.append(item)
            elif cat == 'TOOLS & MACHINERY':
                unpriced_tools.append(item)

    print(f"--- Unpriced ELECTRICALS ({len(unpriced_electricals)}) ---")
    for item in unpriced_electricals[:10]: # Show first 10
        print(f"{item.get('item_id')}: {item.get('description')} - Buying Price: {item.get('buying_price')}")
    
    # Check price range for Electricals
    if unpriced_electricals:
        prices = [float(i.get('buying_price', 0)) for i in unpriced_electricals]
        print(f"Price Range: {min(prices)} - {max(prices)}")

    print(f"\n--- Unpriced TOOLS & MACHINERY ({len(unpriced_tools)}) ---")
    for item in unpriced_tools[:10]: # Show first 10
        print(f"{item.get('item_id')}: {item.get('description')} - Buying Price: {item.get('buying_price')}")

    # Check price range for Tools
    if unpriced_tools:
        prices = [float(i.get('buying_price', 0)) for i in unpriced_tools]
        print(f"Price Range: {min(prices)} - {max(prices)}")
        
        # Let's see all unique prices to find the gaps
        prices.sort()
        print(f"All Prices: {prices}")

if __name__ == "__main__":
    inspect_unpriced()
