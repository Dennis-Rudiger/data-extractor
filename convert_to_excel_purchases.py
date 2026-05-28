import pandas as pd
import re

def process_purchases(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    
    data = []
    
    # We want rows: Supplier, Date, Ref, Details, Debit, Credit, Balance
    for line in lines:
        if line.startswith('Supplier:'):
            current_supplier = line.strip()
            data.append([current_supplier, "", "", "", "", ""])
            # Or we can write the header here
            data.append(["Date", "Ref.", "Details", "Debit", "Credit", "Balance"])
            continue
            
        # Match lines that start with DD/MM/YYYY
        if re.match(r'^\d{2}/\d{2}/\d{4}', line):
            date = line[0:10].strip()
            ref = line[11:20].strip()
            details = line[21:55].strip()
            debit = line[55:69].strip()
            credit = line[69:85].strip()
            balance = line[85:].strip()
            
            data.append([date, ref, details, debit, credit, balance])

    if data:
        df = pd.DataFrame(data, columns=["Date/Supplier", "Ref.", "Details", "Debit", "Credit", "Balance"])
        df.to_excel(output_file, index=False, header=False)
        print(f"Saved {output_file} with {len(df)} rows.")
    else:
        print(f"No data found in {input_file}")

try:
    print("Processing Purchases...")
    process_purchases('Purchases 2023.txt', 'Purchases 2023.xlsx')
    process_purchases('Purchases 2024.txt', 'Purchases 2024.xlsx')
except Exception as e:
    print("Error:", e)
