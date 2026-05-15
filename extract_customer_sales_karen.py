import os
import re
import json
import pdfplumber

def extract_sales():
    folder = 'karen customer sales'
    files = [f for f in os.listdir(folder) if f.endswith('.pdf')]
    
    all_data = []
    
    for file in files:
        fname = file.lower()
        if 'jan - apr' in fname: month_label = 'YTD'
        elif 'jan' in fname: month_label = 'January'
        elif 'feb' in fname: month_label = 'February'
        elif 'march' in fname: month_label = 'March'
        elif 'april' in fname: month_label = 'April'
        else: month_label = 'Unknown'

        # Using simpler approach: regex the text blocks
        with pdfplumber.open(os.path.join(folder, file)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text: continue
                lines = text.split('\n')
                
                i = 0
                while i < len(lines):
                    if lines[i].startswith('Customer Name:'):
                        customer = lines[i].replace('Customer Name:', '').strip()
                        if i + 1 < len(lines):
                            parts = lines[i+1].split()
                            if len(parts) >= 6:
                                try:
                                    qty = float(parts[0].replace(',', ''))
                                    amount_exc = float(parts[1].replace(',', ''))
                                    cost = float(parts[3].replace(',', ''))
                                    profit = float(parts[4].replace(',', ''))
                                    
                                    all_data.append({
                                        'Month': month_label,
                                        'Customer': customer,
                                        'Quantity': qty,
                                        'Amount_Exc': amount_exc,
                                        'Cost': cost,
                                        'Profit': profit
                                    })
                                except Exception as e:
                                    pass
                        i += 2
                    else:
                        i += 1
                        
    with open('customer_sales_karen.json', 'w') as f:
        json.dump(all_data, f, indent=4)
        
    print("Extracted records:", len(all_data))

if __name__ == '__main__':
    extract_sales()
