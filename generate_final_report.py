import json
from app import generate_pdf

def main():
    input_file = 'inventory_valuation_priced.json'
    output_pdf = 'inventory_valuation_priced_report.pdf'
    
    print(f"Loading data from {input_file}...")
    with open(input_file, 'r') as f:
        data = json.load(f)
        
    print(f"Generating PDF report: {output_pdf}...")
    try:
        generate_pdf(data, output_pdf)
        print("PDF report generated successfully.")
    except Exception as e:
        print(f"Failed to generate PDF: {e}")

if __name__ == "__main__":
    main()
