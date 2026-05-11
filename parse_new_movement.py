import pdfplumber
import json
import re
import pandas as pd

def extract_from_pdf(filepath):
    items = []
    try:
        pdf = pdfplumber.open(filepath)
    except Exception as e:
        print(f'Error opening {filepath}: {e}')
        return items
        
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
                desc = re.sub(r'(BOMAS|KAREN)\s*$', '', desc, flags=re.IGNORECASE).strip()
                qty_out = float(match.group(5).replace(',', ''))
                items.append({'code': code, 'description': desc, 'qty_out': qty_out})
    pdf.close()
    return items

def process():
    files = {
        'bomas_q1': 'bomas movement Jan -April.pdf',
        'bomas_apr': 'Bomas movement April.pdf',
        'karen_q1': 'karen movement Jan - Apr.pdf',
        'karen_apr': 'karen movement april.pdf'
    }
    
    data = {}
    for key, path in files.items():
        print(f'Extracting {path}...')
        res = extract_from_pdf(path)
        df = pd.DataFrame(res)
        if not df.empty:
            df = df.groupby('code').agg({'description': 'first', 'qty_out': 'sum'}).reset_index()
            df.to_csv(f'{key}_extracted.csv', index=False)
        data[key] = df
        print(f'Extracted {len(df)} items.')

if __name__ == '__main__':
    process()
