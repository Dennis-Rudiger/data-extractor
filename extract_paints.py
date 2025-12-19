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
            paints_data.append(group)
            
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
