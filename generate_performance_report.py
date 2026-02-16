import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.units import inch
from datetime import datetime

def load_analysis():
    with open("performance_analysis_feb2026.json", "r") as f:
        return json.load(f)

def generate_report(output_filename):
    data = load_analysis()
    analysis = data["analysis"]
    
    doc = SimpleDocTemplate(output_filename, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch, leftMargin=0.5*inch, rightMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor('#1a1a1a'), spaceAfter=8, alignment=TA_CENTER, fontName='Helvetica-Bold')
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#666666'), spaceAfter=20, alignment=TA_CENTER)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#2c3e50'), spaceAfter=12, spaceBefore=16, fontName='Helvetica-Bold')
    subheading_style = ParagraphStyle('SubHeading', parent=styles['Heading3'], fontSize=11, textColor=colors.HexColor('#34495e'), spaceAfter=8, spaceBefore=12, fontName='Helvetica-Bold')
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#2c3e50'), spaceAfter=6)
    highlight_style = ParagraphStyle('Highlight', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#27ae60'), spaceAfter=6, fontName='Helvetica-Bold')
    alert_style = ParagraphStyle('Alert', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#e74c3c'), spaceAfter=6, fontName='Helvetica-Bold')
    
    # Title Page
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("SALES PERFORMANCE ANALYSIS", title_style))
    elements.append(Paragraph("BOMAS Hardware Store - February 2026", subtitle_style))
    elements.append(Paragraph(f"Report Generated: {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Executive Summary
    elements.append(Paragraph("EXECUTIVE SUMMARY", heading_style))
    
    combined = analysis["combined"]
    w1 = analysis["week1"]
    w2 = analysis["week2"]
    
    # Calculate week over week changes
    w1_daily_sales = w1["grand_total"]["sales"] / w1["working_days"]
    w2_daily_sales = w2["grand_total"]["sales"] / w2["working_days"]
    w1_daily_profit = w1["grand_total"]["profit"] / w1["working_days"]
    w2_daily_profit = w2["grand_total"]["profit"] / w2["working_days"]
    sales_change = ((w2_daily_sales - w1_daily_sales) / w1_daily_sales) * 100
    profit_change = ((w2_daily_profit - w1_daily_profit) / w1_daily_profit) * 100
    
    summary_data = [
        ["Metric", "Week 1 (6 days)", "Week 2 (5 days)", "Combined (11 days)"],
        ["Total Sales", f"KES {w1['grand_total']['sales']:,.0f}", f"KES {w2['grand_total']['sales']:,.0f}", f"KES {combined['grand_total']['sales']:,.0f}"],
        ["Total Profit", f"KES {w1['grand_total']['profit']:,.0f}", f"KES {w2['grand_total']['profit']:,.0f}", f"KES {combined['grand_total']['profit']:,.0f}"],
        ["Overall Margin", f"{w1['grand_total']['profit']/w1['grand_total']['sales']*100:.1f}%", f"{w2['grand_total']['profit']/w2['grand_total']['sales']*100:.1f}%", f"{combined['grand_total']['profit']/combined['grand_total']['sales']*100:.1f}%"],
        ["Daily Sales Avg", f"KES {w1_daily_sales:,.0f}", f"KES {w2_daily_sales:,.0f}", f"KES {combined['grand_total']['sales']/combined['working_days']:,.0f}"],
        ["Daily Profit Avg", f"KES {w1_daily_profit:,.0f}", f"KES {w2_daily_profit:,.0f}", f"KES {combined['grand_total']['profit']/combined['working_days']:,.0f}"],
    ]
    
    summary_table = Table(summary_data, colWidths=[1.5*inch, 1.6*inch, 1.6*inch, 1.8*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 15))
    
    # Key Insights
    elements.append(Paragraph("KEY INSIGHTS", subheading_style))
    
    if sales_change > 0:
        elements.append(Paragraph(f" Daily sales increased by {sales_change:.1f}% from Week 1 to Week 2", highlight_style))
    else:
        elements.append(Paragraph(f" Daily sales decreased by {abs(sales_change):.1f}% from Week 1 to Week 2", alert_style))
    
    if profit_change > 0:
        elements.append(Paragraph(f" Daily profit increased by {profit_change:.1f}% from Week 1 to Week 2", highlight_style))
    else:
        elements.append(Paragraph(f" Daily profit decreased by {abs(profit_change):.1f}% from Week 1 to Week 2", alert_style))
    
    # Margin analysis
    w1_margin = w1['grand_total']['profit']/w1['grand_total']['sales']*100
    w2_margin = w2['grand_total']['profit']/w2['grand_total']['sales']*100
    if w2_margin < w1_margin:
        elements.append(Paragraph(f" Overall margin decreased from {w1_margin:.1f}% to {w2_margin:.1f}% (need to review pricing)", alert_style))
    
    elements.append(PageBreak())
    
    # Sales Rep Performance
    elements.append(Paragraph("SALES REP PERFORMANCE - COMBINED (Feb 1-13)", heading_style))
    
    rep_data = [["Sales Rep", "Total Sales", "Total Profit", "Margin %", "Daily Average"]]
    sorted_reps = sorted(combined["rep_totals"].items(), key=lambda x: x[1]["sales_incl"], reverse=True)
    
    for rep, vals in sorted_reps:
        daily_avg = vals["sales_incl"] / combined["working_days"]
        rep_data.append([
            rep,
            f"KES {vals['sales_incl']:,.0f}",
            f"KES {vals['profit']:,.0f}",
            f"{vals['margin_pct']:.1f}%",
            f"KES {daily_avg:,.0f}"
        ])
    
    # Add totals row
    rep_data.append([
        "TOTAL",
        f"KES {combined['grand_total']['sales']:,.0f}",
        f"KES {combined['grand_total']['profit']:,.0f}",
        f"{combined['grand_total']['profit']/combined['grand_total']['sales']*100:.1f}%",
        f"KES {combined['grand_total']['sales']/combined['working_days']:,.0f}"
    ])
    
    rep_table = Table(rep_data, colWidths=[1.4*inch, 1.4*inch, 1.4*inch, 0.9*inch, 1.4*inch])
    rep_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#ecf0f1')]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(rep_table)
    elements.append(Spacer(1, 20))
    
    # Rep Rankings
    elements.append(Paragraph("PERFORMANCE RANKINGS", subheading_style))
    
    # Top seller
    top_seller = sorted_reps[0]
    elements.append(Paragraph(f" Top Seller: <b>{top_seller[0]}</b> with KES {top_seller[1]['sales_incl']:,.0f} in sales ({top_seller[1]['sales_incl']/combined['grand_total']['sales']*100:.1f}% of total)", body_style))
    
    # Best margin (among those with significant sales)
    significant_reps = [(r, v) for r, v in sorted_reps if v['sales_incl'] > 500000]
    if significant_reps:
        best_margin = max(significant_reps, key=lambda x: x[1]['margin_pct'])
        elements.append(Paragraph(f" Best Margin: <b>{best_margin[0]}</b> at {best_margin[1]['margin_pct']:.1f}%", body_style))
    
    # Most improved
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("WEEK-OVER-WEEK PERFORMANCE CHANGE", subheading_style))
    
    wow_data = [["Sales Rep", "Week 1 Daily", "Week 2 Daily", "Change %"]]
    all_reps = set(w1["rep_totals"].keys()) | set(w2["rep_totals"].keys())
    
    rep_changes = []
    for rep in sorted(all_reps):
        w1_daily = w1["rep_totals"].get(rep, {"sales_incl": 0})["sales_incl"] / w1["working_days"]
        w2_daily = w2["rep_totals"].get(rep, {"sales_incl": 0})["sales_incl"] / w2["working_days"]
        change = ((w2_daily - w1_daily) / w1_daily * 100) if w1_daily > 0 else 0
        rep_changes.append((rep, w1_daily, w2_daily, change))
    
    rep_changes.sort(key=lambda x: x[3], reverse=True)
    
    for rep, w1_d, w2_d, change in rep_changes:
        change_str = f"+{change:.1f}%" if change > 0 else f"{change:.1f}%"
        wow_data.append([rep, f"KES {w1_d:,.0f}", f"KES {w2_d:,.0f}", change_str])
    
    wow_table = Table(wow_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.2*inch])
    wow_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(wow_table)
    
    elements.append(PageBreak())
    
    # Category Performance
    elements.append(Paragraph("CATEGORY PERFORMANCE - COMBINED (Feb 1-13)", heading_style))
    
    cat_data = [["Category", "Total Sales", "Total Profit", "Margin %", "% of Total Sales"]]
    sorted_cats = sorted(combined["cat_totals"].items(), key=lambda x: x[1]["sales_incl"], reverse=True)
    
    for cat, vals in sorted_cats:
        pct_of_total = vals["sales_incl"] / combined["grand_total"]["sales"] * 100
        cat_data.append([
            cat,
            f"KES {vals['sales_incl']:,.0f}",
            f"KES {vals['profit']:,.0f}",
            f"{vals['margin_pct']:.1f}%",
            f"{pct_of_total:.1f}%"
        ])
    
    cat_table = Table(cat_data, colWidths=[1.6*inch, 1.5*inch, 1.4*inch, 0.9*inch, 1.2*inch])
    cat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(cat_table)
    elements.append(Spacer(1, 20))
    
    # Category Insights
    elements.append(Paragraph("CATEGORY INSIGHTS", subheading_style))
    
    # General Hardware dominance
    gh_pct = combined["cat_totals"]["GENERAL HARDWARE"]["sales_incl"] / combined["grand_total"]["sales"] * 100
    elements.append(Paragraph(f" <b>General Hardware</b> dominates with {gh_pct:.1f}% of total sales, but has lowest margin at {combined['cat_totals']['GENERAL HARDWARE']['margin_pct']:.1f}%", body_style))
    
    # Best margin category
    best_margin_cat = max(sorted_cats, key=lambda x: x[1]['margin_pct'])
    elements.append(Paragraph(f" <b>{best_margin_cat[0]}</b> has highest margin at {best_margin_cat[1]['margin_pct']:.1f}% - opportunity to push more sales here", body_style))
    
    # Margin concerns
    low_margin_cats = [c for c in sorted_cats if c[1]['margin_pct'] < 10]
    if low_margin_cats:
        cats_str = ", ".join([c[0] for c in low_margin_cats])
        elements.append(Paragraph(f" Low margin alert: {cats_str} - review pricing strategy", alert_style))
    
    elements.append(Spacer(1, 20))
    
    # Week-by-week category comparison
    elements.append(Paragraph("CATEGORY WEEK-OVER-WEEK COMPARISON", subheading_style))
    
    cat_wow_data = [["Category", "Week 1 Sales", "Week 2 Sales", "W1 Margin", "W2 Margin"]]
    for cat in ["GENERAL HARDWARE", "PAINTS", "PLUMBING", "ELECTRICALS"]:
        w1_cat = w1["cat_totals"].get(cat, {"sales_incl": 0, "margin_pct": 0})
        w2_cat = w2["cat_totals"].get(cat, {"sales_incl": 0, "margin_pct": 0})
        cat_wow_data.append([
            cat,
            f"KES {w1_cat['sales_incl']:,.0f}",
            f"KES {w2_cat['sales_incl']:,.0f}",
            f"{w1_cat['margin_pct']:.1f}%",
            f"{w2_cat['margin_pct']:.1f}%"
        ])
    
    cat_wow_table = Table(cat_wow_data, colWidths=[1.6*inch, 1.4*inch, 1.4*inch, 1*inch, 1*inch])
    cat_wow_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e67e22')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(cat_wow_table)
    
    elements.append(PageBreak())
    
    # Recommendations
    elements.append(Paragraph("RECOMMENDATIONS", heading_style))
    
    recommendations = [
        ("Focus on High-Margin Categories", "Electricals (24.4%) and Plumbing (21.0%) have the best margins. Train sales reps to upsell these categories when customers buy General Hardware."),
        ("Address General Hardware Margins", "At only 6.3% margin, General Hardware needs pricing review. Consider supplier negotiations or identifying items where margins can be improved."),
        ("Recognize Top Performers", "Gladys leads with KES 12.76M in sales (42.6% of total). Lewis showed the biggest improvement (+59.8% daily sales increase)."),
        ("Support Underperformers", "Bonface Muriu showed a decline (-16.9% daily). Review their challenges and provide additional support or training."),
        ("Maintain Momentum", "Daily sales increased 32.1% from Week 1 to Week 2. Continue strategies that drove this growth."),
        ("Watch Margin Erosion", "Overall margin dropped from 8.2% to 6.9%. Ensure sales growth isn't coming at the expense of profitability.")
    ]
    
    for title, desc in recommendations:
        elements.append(Paragraph(f"<b>{title}</b>", subheading_style))
        elements.append(Paragraph(desc, body_style))
        elements.append(Spacer(1, 8))
    
    # Build PDF
    doc.build(elements)
    print(f"Report generated: {output_filename}")

if __name__ == "__main__":
    generate_report("sales_performance_feb2026.pdf")
