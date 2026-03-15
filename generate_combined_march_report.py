import json
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.units import inch

# Configuration
MONTHLY_TARGETS = {
    'OVERALL': 60_000_000,
    'GENERAL HARDWARE': 48_500_000,
    'PAINTS': 7_000_000,
    'PLUMBING': 3_000_000,
    'ELECTRICALS': 1_500_000,
}

VAT_RATE = 1.16

def load_data(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def process_data(raw_data):
    # Returns totals, category breakdown, rep breakdown
    overall_sales = 0
    overall_profit = 0
    
    cats = {}
    reps = {}
    
    for cat, cat_data in raw_data["categories"].items():
        if cat not in cats:
            cats[cat] = {'sales': 0, 'profit': 0}
            
        for rep, data in cat_data.items():
            rep_name = "Betha Odumo" if rep in ("Magdalene", "WALK IN-BOMAS") else rep
            sales = data['sales_incl']
            profit = data['profit'] * VAT_RATE
            
            if rep_name not in reps:
                reps[rep_name] = {'sales': 0, 'profit': 0}
                
            reps[rep_name]['sales'] += sales
            reps[rep_name]['profit'] += profit
            
            cats[cat]['sales'] += sales
            cats[cat]['profit'] += profit
            
            overall_sales += sales
            overall_profit += profit
            
    return {
        'sales': overall_sales,
        'profit': overall_profit,
        'margin': (overall_profit / overall_sales * 100) if overall_sales > 0 else 0,
        'categories': cats,
        'reps': reps
    }

def main():
    print("Loading valid JSONs...")
    w1 = process_data(load_data("sales_march_w1.json"))
    w2 = process_data(load_data("sales_march_w2.json"))
    
    # Combined calc
    comb_sales = w1['sales'] + w2['sales']
    comb_profit = w1['profit'] + w2['profit']
    comb_margin = (comb_profit / comb_sales * 100) if comb_sales > 0 else 0
    
    comb_cats = {}
    for cat in MONTHLY_TARGETS.keys():
        if cat == 'OVERALL': continue
        c1_s = w1['categories'].get(cat, {}).get('sales', 0)
        c2_s = w2['categories'].get(cat, {}).get('sales', 0)
        c1_p = w1['categories'].get(cat, {}).get('profit', 0)
        c2_p = w2['categories'].get(cat, {}).get('profit', 0)
        
        c_s = c1_s + c2_s
        c_p = c1_p + c2_p
        
        comb_cats[cat] = {
            'sales': c_s,
            'profit': c_p,
            'margin': (c_p / c_s * 100) if c_s > 0 else 0
        }
        
    all_reps = set(w1['reps'].keys()) | set(w2['reps'].keys())
    comb_reps = {}
    for rep in all_reps:
        r1_s = w1['reps'].get(rep, {}).get('sales', 0)
        r2_s = w2['reps'].get(rep, {}).get('sales', 0)
        r1_p = w1['reps'].get(rep, {}).get('profit', 0)
        r2_p = w2['reps'].get(rep, {}).get('profit', 0)
        
        comb_reps[rep] = {
            'sales': r1_s + r2_s,
            'profit': r1_p + r2_p,
            'margin': ((r1_p + r2_p) / (r1_s + r2_s) * 100) if (r1_s + r2_s) > 0 else 0
        }
    
    # PDF GEN
    doc = SimpleDocTemplate("march_combined_report.pdf", pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = styles['Heading1']
    title_style.alignment = TA_CENTER
    h2 = styles['Heading2']
    h2.textColor = colors.HexColor('#2c3e50')
    normal = styles['Normal']
    
    # Title
    elements.append(Paragraph("March 2026 - Combined Performance Report", title_style))
    elements.append(Paragraph("Data covers March 2 - March 14, 2026", ParagraphStyle('Sub', parent=styles['Normal'], alignment=TA_CENTER)))
    elements.append(Spacer(1, 0.4*inch))
    
    # SECTION 1: WEEK 2 STATS
    elements.append(Paragraph("SECTION 1: Week 2 Summary (Mar 9 - Mar 14)", h2))
    elements.append(Spacer(1, 0.1*inch))
    
    kpi_data = [
        ["Total Sales (Week 2)", f"KES {w2['sales']:,.2f}"],
        ["Total Profit (Week 2)", f"KES {w2['profit']:,.2f}"],
        ["Overall Margin (Week 2)", f"{w2['margin']:.2f}%"]
    ]
    t1 = Table(kpi_data, colWidths=[2.5*inch, 2.5*inch])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#ecf0f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica-Bold'),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t1)
    elements.append(Spacer(1, 0.2*inch))
    
    w2_cat_data = [["Category", "Sales", "Profit", "Margin"]]
    for cat, d in sorted(w2['categories'].items(), key=lambda x: x[1]['sales'], reverse=True):
        w2_cat_data.append([
            cat, 
            f"KES {d['sales']:,.0f}", 
            f"KES {d['profit']:,.0f}", 
            f"{(d['profit']/d['sales']*100) if d['sales']>0 else 0:.1f}%"
        ])
        
    t1_cat = Table(w2_cat_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
    t1_cat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(Paragraph("<b>Category Breakdown (Week 2):</b>", normal))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(t1_cat)
    elements.append(Spacer(1, 0.4*inch))
    
    # SECTION 2: COMBINED TOTALS
    elements.append(Paragraph("SECTION 2: Combined Totals (Mar 2 - Mar 14)", h2))
    elements.append(Spacer(1, 0.1*inch))
    
    kpi2_data = [
        ["Grand Total Sales (W1+W2)", f"KES {comb_sales:,.2f}"],
        ["Grand Total Profit (W1+W2)", f"KES {comb_profit:,.2f}"],
        ["Combined Overall Margin", f"{comb_margin:.2f}%"],
        ["Target Progress (Month)", f"{(comb_sales/MONTHLY_TARGETS['OVERALL']*100):.1f}% of 60M"]
    ]
    t2 = Table(kpi2_data, colWidths=[2.5*inch, 2.5*inch])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#ecf0f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica-Bold'),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("<b>Category Performance vs Limits:</b>", normal))
    elements.append(Spacer(1, 0.1*inch))
    cat_comb_data = [["Category", "Combined Sales", "Monthly Target", "% Achieved"]]
    for cat, d in sorted(comb_cats.items(), key=lambda x: x[1]['sales'], reverse=True):
        targ = MONTHLY_TARGETS[cat]
        cat_comb_data.append([
            cat, 
            f"KES {d['sales']:,.0f}", 
            f"KES {targ:,.0f}", 
            f"{(d['sales']/targ*100):.1f}%"
        ])
        
    t2_cat = Table(cat_comb_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
    t2_cat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t2_cat)
    elements.append(Spacer(1, 0.3*inch))
    
    # Top Reps (Combined)
    elements.append(Paragraph("<b>Top Sales Reps (Combined W1 + W2):</b>", normal))
    elements.append(Spacer(1, 0.1*inch))
    rep_comb_data = [["Rep Name", "Total Sales", "Total Profit", "Margin"]]
    for rep, d in sorted(comb_reps.items(), key=lambda x: x[1]['sales'], reverse=True):
        rep_comb_data.append([
            rep,
            f"KES {d['sales']:,.0f}",
            f"KES {d['profit']:,.0f}",
            f"{d['margin']:.1f}%"
        ])
    t2_rep = Table(rep_comb_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
    t2_rep.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#8e44ad')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t2_rep)
    
    doc.build(elements)
    print("Report generated: march_combined_report.pdf")

if __name__ == "__main__":
    main()