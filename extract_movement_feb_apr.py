import pdfplumber
import json
import re

def extract_movement(pdf_path, branch):
    items = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')
            for line in lines:
                if 'Inventory Item' in line or 'Opening Balance' in line or 'Page' in line or 'PANNJU' in line:
                    continue

                pattern = r'^([A-Z][A-Z0-9/]*\s?\d*)\s+(.+?)\s+([\d,.-]+)\s+([\d,.-]+)\s+([\d,.-]+)\s+([\d,.-]+)$'
                match = re.match(pattern, line.strip())

                if match:
                    code = match.group(1).strip()
                    desc = match.group(2).strip()
                    desc = re.sub(r'\s*BOMAS\s*$', '', desc).strip()
                    desc = re.sub(r'BOMAS$', '', desc).strip()
                    desc = re.sub(r'\s*B\s*O\s*M\s*A\s*S\s*$', '', desc).strip()
                    desc = re.sub(r'\s*KAREN\s*$', '', desc, flags=re.IGNORECASE).strip()
                    desc = re.sub(r'KAREN$', '', desc, flags=re.IGNORECASE).strip()
                    
                    qty_in = float(match.group(4).replace(',', ''))
                    qty_out = float(match.group(5).replace(',', ''))
                    closing = float(match.group(6).replace(',', ''))

                    items.append({
                        'item_code': code,
                        'item_description': desc,
                        'qty_in': qty_in,
                        'qty_out': qty_out,
                        'closing_balance': closing
                    })

    print(f'{branch} - Total items extracted: {len(items)}')
    
    moving_items = [i for i in items if i['qty_out'] > 0]
    print(f'{branch} - Items with movement OUT: {len(moving_items)}')

    out_file = f'stock_movement_{branch.lower()}_feb_apr.json'
    with open(out_file, 'w') as f:
        json.dump(items, f, indent=2)
    print(f'Saved to {out_file}\n')

if __name__ == '__main__':
    extract_movement("BOMAS STOCK MOVEMENT FEB-APR.pdf", "Bomas")
    extract_movement("KAREN STOCK MOVEMENT FEB-APR.pdf", "Karen")
