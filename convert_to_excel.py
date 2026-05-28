import pandas as pd
import re

def process_sales(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    
    data = []
    headers = ["DATE", "SALES EXCL.", "SALES EXCEMPT", "V.A.T.", "TOTAL COSTS", "PROFIT", "G.P.%", "PETTY CASH", "CASH TAKEN", "LAYBYE PMNTS", "LAYBYE SALES", "EXPIRED REFUNDS"]
    
    for line in lines:
        parts = line.split()
        if len(parts) >= 12 and parts[0][0].isdigit() and len(parts[0]) == 6:
            # Maybe the DATE is 6 digits long? Yes, '230103'
            data.append(parts[:12])
                
    if data:
        df = pd.DataFrame(data, columns=headers)
        
        # Convert numeric columns where possible
        for col in df.columns:
            if col not in ["DATE"]:
                # strip stars for now
                df[col] = df[col].astype(str).str.replace('******.**', '0.00', regex=False)
                df[col] = df[col].astype(str).str.replace(',', '', regex=False)
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except:
                    pass

        # Also format DATE text
        df.to_excel(output_file, index=False)
        print(f"Saved {output_file} with {len(df)} rows.")
    else:
        print(f"No data found in {input_file}")

import sys
try:
    print("Processing Sales...")
    process_sales('Sales 2023.txt', 'Sales 2023.xlsx')
    process_sales('Sales 2024.txt', 'Sales 2024.xlsx')
except Exception as e:
    print("Error:", e)
