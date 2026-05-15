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
    "ELECTRICALS": "Electricals April.pdf",
    "GENERAL HARDWARE": "General hardware April.pdf",
    "PAINTS": "Paints April.pdf",
    "PLUMBING": "plumbing April.pdf"
}

april_data = {
    "period": "April 2026",
    "working_days": 24,
    "categories": {}
}

print("Extracting April data...")
for dept, filename in departments.items():
    print(f"\n{dept}: {filename}")
    try:
        reps = parse_sales_pdf(filename, dept)
        april_data["categories"][dept] = reps
        print(f"Found {len(reps)} reps.")
    except Exception as e:
        print(f"Error parsing {filename}: {e}")

with open("sales_april.json", "w") as f:
    json.dump(april_data, f, indent=2)
print("Saved to sales_april.json")
