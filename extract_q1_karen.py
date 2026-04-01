import pdfplumber
import json
import re

items = []
pdf = pdfplumber.open('inventory movement summary for jan - march karen.pdf')

for page in pdf.pages:
    lines = page.extract_text().split('\n')
    for line in lines:
        if 'Inventory Item' in line or 'Opening Balance' in line or 'Page' in line or 'PANNJU' in line:
            continue
        
        # Match pattern
        pattern = r'^([A-Z][A-Z0-9/.\-]+)\s+(.+?)\s+([\d,.-]+)\s+([\d,.-]+)\s+([\d,.-]+)\s+([\d,.-]+)$'
        match = re.search(pattern, line.strip())
        
        if match:
            code = match.group(1).strip()
            desc = match.group(2).strip()
            # Remove KAREN from description
            desc = re.sub(r'\s*KAREN\s*$', '', desc, flags=re.IGNORECASE).strip()
            open_bal = float(match.group(3).replace(',', ''))
            qty_in = float(match.group(4).replace(',', ''))
            qty_out = float(match.group(5).replace(',', ''))
            closing = float(match.group(6).replace(',', ''))
            
            items.append({
                'code': code.upper(),
                'description': desc,
                'open_bal': open_bal,
                'qty_in': qty_in,
                'qty_out': qty_out,
                'closing': closing,
            })

pdf.close()
with open('stock_movement_karen_q1.json', 'w') as f:
    json.dump({'items': items}, f, indent=4)
print(f'Extracted {len(items)} items')
