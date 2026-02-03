import pdfplumber
import json
import re

# Extract all stock movement data
items = []
pdf = pdfplumber.open('Stock movement1.pdf')

for page in pdf.pages:
    text = page.extract_text()
    if not text:
        continue
    
    lines = text.split('\n')
    for line in lines:
        # Skip headers
        if 'Inventory Item' in line or 'Opening Balance' in line or 'Page' in line or 'PANNJU' in line:
            continue
        
        # More robust pattern that handles:
        # - Codes with slashes like C/E001, C/S/G, R/P001
        # - Codes with spaces like D 1001, R 6001
        # - Regular codes like SIM001, BAM005
        # Pattern: Code Description OpenBal QtyIn QtyOut CloseBal
        pattern = r'^([A-Z][A-Z0-9/]*\s?\d*)\s+(.+?)\s+([\d,.-]+)\s+([\d,.-]+)\s+([\d,.-]+)\s+([\d,.-]+)$'
        match = re.match(pattern, line.strip())
        
        if match:
            code = match.group(1).strip()
            desc = match.group(2).strip()
            # Remove BOMAS from description
            desc = re.sub(r'\s*BOMAS\s*$', '', desc).strip()
            # Also remove BOMAS that might appear mid-description due to PDF parsing
            desc = re.sub(r'BOMAS$', '', desc).strip()
            desc = re.sub(r'\s*B\s*O\s*M\s*A\s*S\s*$', '', desc).strip()
            qty_in = float(match.group(4).replace(',', ''))
            qty_out = float(match.group(5).replace(',', ''))
            
            items.append({
                'code': code,
                'description': desc,
                'qty_in': qty_in,
                'qty_out': qty_out
            })

pdf.close()
print(f'Total items extracted: {len(items)}')

moving_items = [i for i in items if i['qty_out'] > 0]
slow_items = [i for i in items if i['qty_out'] == 0]

print(f'Items with movement OUT (fast movers): {len(moving_items)}')
print(f'Items with ZERO movement OUT (slow movers): {len(slow_items)}')

# Save for further processing
with open('stock_movement_raw.json', 'w') as f:
    json.dump(items, f, indent=2)
print('Data saved to stock_movement_raw.json')
