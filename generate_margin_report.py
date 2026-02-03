import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.units import inch
from datetime import datetime

def load_inventory():
    with open('inventory_valuation_priced.json', 'r') as f:
        return json.load(f)

def calculate_margin(buying, selling):
    if buying > 0:
        return ((selling - buying) / buying) * 100
    return 0

def generate_margin_report(output_filename):
    data = load_inventory()
    
    target_categories = ['ELECTRICALS', 'PLUMBING MATERIALS']
    filtered_data = [g for g in data if g['category_name'] in target_categories]
    
    doc = SimpleDocTemplate(output_filename, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#1a1a1a'), spaceAfter=8, alignment=TA_CENTER, fontName='Helvetica-Bold')
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#7f8c8d'), spaceAfter=20, alignment=TA_CENTER)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#2c3e50'), spaceAfter=12, spaceBefore=16, fontName='Helvetica-Bold')
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#2c3e50'), spaceAfter=6, alignment=TA_LEFT)
    
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph('MARGIN ANALYSIS REPORT', title_style))
    elements.append(Paragraph('Electricals and Plumbing Materials', subtitle_style))
    elements.append(Paragraph('Generated: ' + datetime.now().strftime('%B %d, %Y'), subtitle_style))
    elements.append(Spacer(1, 0.2*inch))
    
    for group in filtered_data:
        category = group['category_name']
        products = group['products']
        
        margins = []
        for p in products:
            if p.get('selling_price', 0) > 0 and p.get('buying_price', 0) > 0:
                margins.append(calculate_margin(p['buying_price'], p['selling_price']))
        
        if not margins:
            continue
            
        avg_margin = sum(margins) / len(margins)
        min_margin = min(margins)
        max_margin = max(margins)
        
        elements.append(Paragraph(category, heading_style))
        stats_text = 'Total Items: {} | Avg Margin: {:.1f}% | Range: {:.1f}% - {:.1f}%'.format(len(products), avg_margin, min_margin, max_margin)
        elements.append(Paragraph(stats_text, body_style))
        elements.append(Spacer(1, 8))
        
        table_data = [['Item Code', 'Description', 'Buying (KES)', 'Selling (KES)', 'Margin %']]
        
        # Use default order (no sorting)
        valid_products = [p for p in products if p.get('selling_price', 0) > 0 and p.get('buying_price', 0) > 0]
        
        for p in valid_products:
            margin = calculate_margin(p['buying_price'], p['selling_price'])
            desc = p['item_description']
            if len(desc) > 35:
                desc = desc[:35] + '...'
            table_data.append([
                p['item_code'],
                desc,
                '{:,.0f}'.format(p['buying_price']),
                '{:,.0f}'.format(p['selling_price']),
                '{:.1f}%'.format(margin)
            ])
        
        t = Table(table_data, colWidths=[0.8*inch, 2.5*inch, 1*inch, 1*inch, 0.8*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(t)
        elements.append(PageBreak())
    
    doc.build(elements)
    print('Report generated: ' + output_filename)

if __name__ == '__main__':
    generate_margin_report('electricals_plumbing_margins.pdf')
