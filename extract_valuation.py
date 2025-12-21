import json
import PyPDF2
import re
import os
from app import generate_pdf

def is_number(s):
    try:
        float(s.replace(',', ''))
        return True
    except ValueError:
        return False

def load_known_groups(json_path):
    if not os.path.exists(json_path):
        return []
    with open(json_path, 'r') as f:
        data = json.load(f)
    groups = [g['category_name'] for g in data]
    # Sort by length descending to match longest first
    groups.sort(key=len, reverse=True)
    return groups

def extract_valuation(pdf_path, output_path, known_groups):
    print(f"Reading {pdf_path}...")
    text = ""
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
            
    lines = text.split('\n')
    extracted_data = []
    
    # Regex to match the end of the line: Whse Value UnitCost
    # Whse is usually BOMAS, but let's be generic: Word Number Number
    # But Qty might be there too.
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "Inventory Valuation" in line or "Page " in line or "Item Code" in line:
            continue
        if "Sage 200 Evolution" in line:
            continue
            
        tokens = line.split()
        if len(tokens) < 5:
            continue
            
        # Parse from the end
        # Expected tail: [Qty] Whse Value UnitCost
        
        # Check last two tokens (Value, UnitCost)
        if not is_number(tokens[-1]) or not is_number(tokens[-2]):
            # Maybe wrapped line? Skip for now or handle
            continue
            
        unit_cost_str = tokens[-1]
        value_str = tokens[-2]
        whse = tokens[-3]
        
        unit_cost = float(unit_cost_str.replace(',', ''))
        
        # Check for Qty
        qty = 0.0
        qty_index = -3 # Index of Whse
        
        if len(tokens) > 3 and is_number(tokens[-4]):
            qty_str = tokens[-4]
            qty = float(qty_str.replace(',', ''))
            qty_index = -4
            
        # Everything before qty_index (excluding Whse) is Code + Desc + Group
        # tokens[:qty_index]
        
        content_tokens = tokens[:qty_index]
        if not content_tokens:
            continue
            
        full_content_str = " ".join(content_tokens)
        
        # Use regex to extract Item Code
        # Pattern: Starts with alphanumeric/special chars, ends with at least one digit (usually 3)
        # We use the same pattern as in app.py but adapted
        # ^([A-Z0-9\s/\.\-]+?\d+)
        
        code_match = re.match(r'^([A-Z0-9\s/\.\-]+?\d+)\s+(.*)$', full_content_str)
        
        if code_match:
            item_code = code_match.group(1).strip()
            desc_group_str = code_match.group(2).strip()
        else:
            # Fallback: assume first token is code
            item_code = content_tokens[0]
            desc_group_tokens = content_tokens[1:]
            desc_group_str = " ".join(desc_group_tokens)
        
        # Split Description and Group
        item_group = "UNKNOWN"
        item_description = desc_group_str
        
        for group in known_groups:
            if desc_group_str.endswith(group):
                item_group = group
                item_description = desc_group_str[:-len(group)].strip()
                break
        
        # Calculate Buying Price
        buying_price = unit_cost * 1.16
        
        extracted_data.append({
            "item_code": item_code,
            "item_description": item_description,
            "item_group": item_group,
            "unit_cost": unit_cost,
            "buying_price": round(buying_price, 2)
        })
        
    print(f"Extracted {len(extracted_data)} items.")
    
    # Group by Item Group for output consistency with previous format?
    # User asked to "extract the data... get item group...".
    # I'll output a flat list or grouped?
    # The previous format was grouped. The user request "export the data as 'category_name': ..., 'products': ..." was for the paints request.
    # Here the user just said "extract the data...".
    # I'll save as a flat list for now, or grouped if it's cleaner.
    # Let's save as grouped to match the project style.
    
    grouped_data = {}
    for item in extracted_data:
        group = item['item_group']
        if group not in grouped_data:
            grouped_data[group] = {
                "category_name": group,
                "products": []
            }
        
        # Remove item_group from the product dict to avoid redundancy
        product_dict = item.copy()
        del product_dict['item_group']
        grouped_data[group]["products"].append(product_dict)
        
    final_output = list(grouped_data.values())
    
    print(f"Writing to {output_path}...")
    with open(output_path, 'w') as f:
        json.dump(final_output, f, indent=4)
    print("Done.")
    
    # Generate PDF
    pdf_filename = os.path.splitext(output_path)[0] + '_report.pdf'
    print(f"Generating PDF report: {pdf_filename}...")
    try:
        generate_pdf(final_output, pdf_filename)
        print("PDF report generated successfully.")
    except Exception as e:
        print(f"Failed to generate PDF: {e}")

if __name__ == "__main__":
    known_groups = load_known_groups('inventory.json')
    # Fallback if inventory.json is empty or missing
    if not known_groups:
        known_groups = ['AGRICULTURAL TOOLS', 'CEMENT', 'CONCRETE & YARD', 'ELECTRICALS', 'GENERAL HARDWARE', 'GLASSWARE', 'GLUES & SEALANTS', 'IRON SHEETS & PLATES', 'JUA KALI PRODUCTS', 'LOCKS & ACCESSORIES', 'MORTAR AND ADHESIVES', 'NAILS', 'PAINT ACCESSORIES', 'PAINTS', 'PLUMBING MATERIALS', 'STEEL', 'TANKS', 'TILES & ACCESSORIES', 'TIMBER', 'TIMBER PRODUCTS', 'TOOLS & MACHINERY', 'WELDING MATERIALS', 'WIRE PRODUCTS']
        
    extract_valuation('Inventory Valuation.pdf', 'inventory_valuation.json', known_groups)
