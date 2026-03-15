"""
Extract sales data from March Week 1 PDFs and save to JSON.
Period: March 2-7, 2026 (6 working days)
"""
import pdfplumber
import json
import re

def parse_sales_pdf(filepath, department):
    """Parse a Sage 200 sales analysis PDF and extract rep-level data."""
    reps = {}
    
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            
            lines = text.split("\n")
            current_rep = None
            first_data_line = True  # Track if next numeric line is the detail (not cumulative)
            
            for line in lines:
                line = line.strip()
                
                # Detect rep header
                if line.startswith("Transaction Rep:"):
                    current_rep = line.replace("Transaction Rep:", "").strip()
                    first_data_line = True
                    continue
                
                if current_rep and first_data_line:
                    # Try to parse the first data line after rep header
                    # Format: qty amount_exc amount_incl cost profit profit_pct markup_pct
                    # Numbers have commas: 4,398.00 284,525.82 330,050.00 226,024.94 58,500.88 20.56 25.88
                    nums = re.findall(r'[\d,]+\.?\d*', line)
                    if len(nums) >= 5:
                        try:
                            qty = float(nums[0].replace(",", ""))
                            amount_exc = float(nums[1].replace(",", ""))
                            amount_incl = float(nums[2].replace(",", ""))
                            cost = float(nums[3].replace(",", ""))
                            profit = float(nums[4].replace(",", ""))
                            
                            reps[current_rep] = {
                                "qty": qty,
                                "sales_incl": amount_incl,
                                "cost": cost,
                                "profit": profit
                            }
                            first_data_line = False
                        except (ValueError, IndexError):
                            pass
    
    return reps

# Parse all department PDFs
departments = {
    "ELECTRICALS": "ELECTRICALS WEEK 1 MARCH.pdf",
    "GENERAL HARDWARE": "GENERAL HARDWARE WEEK 1 MARCH.pdf",
    "PAINTS": "PAINTS WEEK 1 MARCH.pdf",
    "PLUMBING": "PLUMBING WEEK 1 MARCH.pdf"
}

march_w1_data = {
    "period": "March 2-7, 2026",
    "working_days": 6,
    "categories": {}
}

print("Extracting March Week 1 data...")
print("=" * 60)

for dept, filename in departments.items():
    print(f"\n{dept}: {filename}")
    reps = parse_sales_pdf(filename, dept)
    march_w1_data["categories"][dept] = reps
    
    dept_total_sales = sum(r["sales_incl"] for r in reps.values())
    dept_total_profit = sum(r["profit"] for r in reps.values())
    print(f"  Reps found: {len(reps)}")
    print(f"  Total Sales: KES {dept_total_sales:,.0f}")
    print(f"  Total Profit: KES {dept_total_profit:,.0f}")
    for rep, vals in sorted(reps.items(), key=lambda x: x[1]["sales_incl"], reverse=True):
        print(f"    {rep:<20} Sales: KES {vals['sales_incl']:>12,.0f}  Profit: KES {vals['profit']:>10,.0f}  Qty: {vals['qty']:,.0f}")

# Also parse total sales to verify
print(f"\n{'=' * 60}")
print("VERIFICATION: Total Sales PDF")
total_reps = parse_sales_pdf("MARCH WEEK 1 TOTAL SALES.pdf", "TOTAL")
total_from_pdf = sum(r["sales_incl"] for r in total_reps.values())
total_from_depts = sum(
    sum(r["sales_incl"] for r in reps.values())
    for reps in march_w1_data["categories"].values()
)
print(f"  Total from TOTAL SALES PDF: KES {total_from_pdf:,.0f}")
print(f"  Total from dept PDFs sum:   KES {total_from_depts:,.0f}")
diff = abs(total_from_pdf - total_from_depts)
print(f"  Difference: KES {diff:,.0f} {'(OK)' if diff < 100 else '(CHECK!)'}")

# Save to JSON
with open("sales_march_w1.json", "w") as f:
    json.dump(march_w1_data, f, indent=2)
print(f"\nData saved to: sales_march_w1.json")

# Summary
grand_total_sales = sum(
    sum(r["sales_incl"] for r in reps.values())
    for reps in march_w1_data["categories"].values()
)
grand_total_profit = sum(
    sum(r["profit"] for r in reps.values())
    for reps in march_w1_data["categories"].values()
)
margin = (grand_total_profit / grand_total_sales * 100) if grand_total_sales > 0 else 0

print(f"\n{'=' * 60}")
print(f"MARCH WEEK 1 SUMMARY (Mar 2-7, 2026)")
print(f"{'=' * 60}")
print(f"Grand Total Sales:  KES {grand_total_sales:>12,.0f}")
print(f"Grand Total Profit: KES {grand_total_profit:>12,.0f}")
print(f"Overall Margin:     {margin:.1f}%")
print(f"Daily Average:      KES {grand_total_sales/6:>12,.0f}")
