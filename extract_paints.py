import json
import os
from app import read_pdf

def extract_paints_group(input_pdf, output_json):
    print(f"Reading {input_pdf}...")
    try:
        all_data = read_pdf(input_pdf)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return
    
    paints_data = []
    
    print("Filtering for 'PAINTS' group strictly...")
    for group in all_data:
        category_name = group.get('category_name', '').strip().upper()
        # Strict matching for PAINTS group
        if category_name == 'PAINTS':
            print(f"Found group: {category_name}")
            
            # Calculate selling price with 8% margin
            # Structure: item_code, item_description, price
            formatted_products = []
            for product in group['products']:
                buying_price = product.get('buying_price', 0.0)
                selling_price_raw = buying_price * 1.08
                
                # Round to nearest 5 (e.g. 123.5 -> 125, 127.8 -> 130)
                selling_price = int(selling_price_raw / 5 + 0.5) * 5
                
                formatted_products.append({
                    "item_code": product['item_code'],
                    "item_description": product['item_description'],
                    "price": selling_price
                })
            
            # Create a new group object with the formatted products
            new_group = {
                "category_name": group['category_name'],
                "products": formatted_products
            }
            paints_data.append(new_group)
            
    if not paints_data:
        print("No group containing 'PAINT' was found.")
    else:
        print(f"Found {len(paints_data)} group(s) matching 'PAINT'.")

    print(f"Writing to {output_json}...")
    with open(output_json, 'w') as f:
        json.dump(paints_data, f, indent=4)
    print("Done.")

if __name__ == "__main__":
    input_file = 'inventory.pdf'
    output_file = 'paints1.json'
    
    if os.path.exists(input_file):
        extract_paints_group(input_file, output_file)
    else:
        print(f"Error: {input_file} not found.")
