import pdfplumber
import json
import re

def parse_sales_pdf(filepath, department):
    reps = {}
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            lines = text.split("\n")
            current_rep = None
            first_data_line = True
            for line in lines:
                line = line.strip()
                if line.startswith("Transaction Rep:"):
                    current_rep = line.replace("Transaction Rep:", "").strip()
                    first_data_line = True
                    continue
                if current_rep and first_data_line:
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

departments = {
    "ELECTRICALS": "electricals march week 3.pdf",
    "GENERAL HARDWARE": "general march week 3.pdf",
    "PAINTS": "paints march week 3.pdf",
    "PLUMBING": "plumbing march week 3.pdf"
}

march_w3_data = {
    "period": "March 16-21, 2026",
    "working_days": 6,
    "categories": {}
}

print("Extracting March Week 3 data...")
print("=" * 60)

for dept, filename in departments.items():
    print(f"\n{dept}: {filename}")
    reps = parse_sales_pdf(filename, dept)
    march_w3_data["categories"][dept] = reps

    dept_total_sales = sum(r["sales_incl"] for r in reps.values())
    dept_total_profit = sum(r["profit"] for r in reps.values())
    print(f"  Reps found: {len(reps)}")
    print(f"  Total Sales: KES {dept_total_sales:,.0f}")
    print(f"  Total Profit: KES {dept_total_profit:,.0f}")

print("\n{'=' * 60}")
print("VERIFICATION: Total Sales PDF")
total_reps = parse_sales_pdf("march week 3 totals.pdf", "TOTAL")
total_from_pdf = sum(r["sales_incl"] for r in total_reps.values())
total_from_depts = sum(sum(r["sales_incl"] for r in reps.values()) for reps in march_w3_data["categories"].values())
print(f"  Total from TOTAL SALES PDF: KES {total_from_pdf:,.0f}")
print(f"  Total from dept PDFs sum:   KES {total_from_depts:,.0f}")
diff = abs(total_from_pdf - total_from_depts)
print(f"  Difference: KES {diff:,.0f} {'(OK)' if diff < 100 else '(CHECK!)'}")

with open("sales_march_w3.json", "w") as f:
    json.dump(march_w3_data, f, indent=2)
