import json
import os
import docx
import PyPDF2
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def read_csv(file_path):
    """Reads a CSV file and returns a list of dictionaries."""
    import csv
    data = []
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

def read_doc(file_path):
    """Reads a .doc or .docx file and returns its text content."""
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

import re

def parse_pdf_data(text):
    """Parses text extracted from a PDF to find categories and products."""
    
    data = {}
    current_group = None
    
    # Regex to identify group headers
    # Example: "Item Group PLUMBING MATERIALS  PLUMBING MATERIALS"
    group_header_pattern = re.compile(r'^Item Group\s+(.*)')

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Check for group header
        group_match = group_header_pattern.match(line)
        if group_match:
            content = group_match.group(1).strip()
            tokens = content.split()
            
            # Heuristic: The group name is the first part of the string, and it is repeated in the second part.
            # We try to find the split point where the second part starts with the first part.
            found_group = False
            for i in range(1, len(tokens)):
                candidate_group = " ".join(tokens[:i])
                remainder = " ".join(tokens[i:])
                
                # Check if remainder starts with candidate_group
                # We use startswith because sometimes there are extra words in the description part
                # e.g. "CONCRETE & YARD" vs "CONCRETE & YARD MATERIALS"
                if remainder.startswith(candidate_group):
                    current_group = candidate_group
                    found_group = True
                    break
            
            if not found_group and len(tokens) > 0:
                 # Fallback: if exact repetition isn't found, maybe it's just "Item Group NAME" (unlikely based on observation but safe)
                 # But for now, let's stick to the repetition logic as it seems robust for this file.
                 pass
                 
            continue
            
        if current_group:
            # Regex to capture item code, description, and category from a line
            # We use the current_group to anchor the split between description and metadata
            # Pattern: Code (starts with alphanumeric, ends with 3+ digits) + Description + Group Name
            
            # Escape group name for regex (e.g. handle "TILES & ACCESSORIES")
            group_regex = re.escape(current_group)
            
            # Pattern explanation:
            # ^([A-Z0-9\s/\-]+?\d{3,}) : Code. Starts with A-Z, 0-9, space, /, -. Must end with at least 3 digits. Non-greedy start.
            # \s+ : Separator
            # (.*?) : Description. Non-greedy.
            # \s+ : Separator
            # {group_regex} : The current group name.
            # \s+ : Separator before the rest of the line (prices etc)
            # (.*)$ : Capture the rest of the line (Qty, Whse, Value, Unit Cost)
            
            pattern_str = r'^([A-Z0-9\s/\-]+?\d{3,})\s+(.*?)\s+' + group_regex + r'\s+(.*)$'
            match = re.match(pattern_str, line)
            
            if match:
                item_code = match.group(1).strip()
                item_description = match.group(2).strip()
                suffix = match.group(3).strip()
                
                # Extract Unit Cost from suffix
                # The Unit Cost is the last token in the line
                suffix_tokens = suffix.split()
                unit_cost = 0.0
                buying_price = 0.0
                
                if suffix_tokens:
                    try:
                        unit_cost_str = suffix_tokens[-1].replace(',', '')
                        unit_cost = float(unit_cost_str)
                        buying_price = unit_cost * 1.16
                        
                        # TODO: Calculate Selling Price once margins are decided
                        # selling_price = buying_price * (1 + margin)
                    except ValueError:
                        pass # Keep as 0.0 if parsing fails

                if current_group not in data:
                    data[current_group] = {
                        "category_name": current_group,
                        "products": []
                    }
                
                data[current_group]["products"].append({
                    "item_code": item_code,
                    "item_description": item_description,
                    "unit_cost": unit_cost,
                    "buying_price": round(buying_price, 2)
                })
            
    return list(data.values())

def generate_pdf(data, output_filename):
    """Generates a PDF report from the extracted data."""
    doc = SimpleDocTemplate(output_filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    title = Paragraph("Inventory Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Table Header
    table_data = [['Item Code', 'Description', 'Category', 'Unit Cost', 'Buying Price', 'Selling Price']]
    
    for group in data:
        category_name = group['category_name']
        for product in group['products']:
            selling_price = product.get('selling_price', 0)
            row = [
                product['item_code'],
                product['item_description'],
                category_name,
                f"{product['unit_cost']:,.2f}",
                f"{product['buying_price']:,.2f}",
                f"{selling_price:,.2f}"
            ]
            table_data.append(row)
            
    # Create Table
    # Adjust column widths for A4 Portrait (Total width approx 540 points)
    # Old widths: [60, 200, 100, 70, 90] -> Total 520
    # New widths: [50, 180, 90, 60, 70, 70] -> Total 520
    t = Table(table_data, colWidths=[50, 180, 90, 60, 70, 70])
    
    # Add style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8), # Header font size
        ('FONTSIZE', (0, 1), (-1, -1), 6), # Body font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4), # Header padding
        ('BOTTOMPADDING', (0, 1), (-1, -1), 0.5), # Body padding
        ('TOPPADDING', (0, 1), (-1, -1), 0.5), # Body padding
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke]), # Alternating row colors
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ALIGN', (3, 1), (-1, -1), 'RIGHT'), # Align numbers to right
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    t.setStyle(style)
    
    elements.append(t)
    doc.build(elements)

def read_pdf(file_path):
    """Reads a .pdf file and parses it."""
    text = ""
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    return parse_pdf_data(text)

def extract_data(input_file, output_file):
    """
    Extracts data from a file and saves it to a JSON file.
    """
    print(f"Starting data extraction from '{input_file}'...")
    
    if not os.path.exists(input_file):
        if os.path.exists(output_file):
            print(f"Input file '{input_file}' not found, but output file '{output_file}' exists. Using existing data.")
            with open(output_file, 'r') as f:
                data = json.load(f)
            
            # Generate PDF
            pdf_filename = os.path.splitext(output_file)[0] + '_report.pdf'
            print(f"Generating PDF report: {pdf_filename}...")
            try:
                generate_pdf(data, pdf_filename)
                print("PDF report generated successfully.")
            except Exception as e:
                print(f"Failed to generate PDF: {e}")
            return
        else:
            print(f"Error: Input file '{input_file}' not found.")
            return

    _, file_extension = os.path.splitext(input_file)
    data = None

    print(f"File extension identified as: {file_extension}")

    if file_extension.lower() == '.csv':
        print("Processing CSV file...")
        data = read_csv(input_file)
        print("CSV data read successfully.")
    elif file_extension.lower() in ['.doc', '.docx']:
        print("Processing DOC/DOCX file...")
        data = read_doc(input_file)
        print("DOC/DOCX data read successfully.")
    elif file_extension.lower() == '.pdf':
        print("Processing PDF file...")
        data = read_pdf(input_file)
        print("PDF data read successfully.")
    else:
        print(f"Unsupported file type: {file_extension}")
        return

    print(f"Writing data to '{output_file}'...")
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print("Data successfully written to JSON file.")
    
    # Generate PDF
    pdf_filename = os.path.splitext(output_file)[0] + '_report.pdf'
    print(f"Generating PDF report: {pdf_filename}...")
    try:
        generate_pdf(data, pdf_filename)
        print("PDF report generated successfully.")
    except Exception as e:
        print(f"Failed to generate PDF: {e}")

if __name__ == "__main__":
    try:
        # Example usage:
        # You can change 'data.csv' to your .doc or .pdf file.
        # Make sure to have the file in the same directory or provide the full path.
        input_filename = 'inventory.pdf' 
        output_filename = 'inventory.json'
        extract_data(input_filename, output_filename)
        print(f"Data extraction from {input_filename} complete. Check {output_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")
