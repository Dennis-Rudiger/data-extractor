import re

with open('generate_q1_analysis.py', 'r') as f:
    code = f.read()

# Shared insight variables to define before PDF & Word generate functions
vars_code = """
# Calculate top level insights
sorted_cats = sorted(cat_totals.items(), key=lambda x: x[1]['sales'], reverse=True)
top_cat = sorted_cats[0][0]
top_cat_sales = sorted_cats[0][1]['sales']
top_cat_share = top_cat_sales / total_sales * 100 if total_sales > 0 else 0
highest_margin_cat = max(cat_totals.items(), key=lambda x: (x[1]['profit']/x[1]['sales']) if x[1]['sales'] > 0 else 0)[0]
highest_margin_cat_margin = (cat_totals[highest_margin_cat]['profit']/cat_totals[highest_margin_cat]['sales']*100) if cat_totals[highest_margin_cat]['sales'] > 0 else 0
if len(sorted_reps) >= 2:
    top_rep = sorted_reps[0][0]
    top_rep_sales = sorted_reps[0][1]['total_sales']
    second_rep = sorted_reps[1][0]
    second_rep_sales = sorted_reps[1][1]['total_sales']
    top_2_share = (top_rep_sales + second_rep_sales) / total_sales * 100 if total_sales > 0 else 0
else:
    top_rep = "N/A"
    top_rep_sales = 0
    second_rep = "N/A"
    second_rep_sales = 0
    top_2_share = 0
"""
code = code.replace("def generate_pdf():", vars_code + "\n\n" + "def generate_pdf():")

# 1. PDF Insights
pdf_insights = """
      # --- Quarterly Insights
      elements.append(PageBreak())
      elements.append(Paragraph("Q1 2026 STRATEGIC BUSINESS INSIGHTS", heading_s))
      
      elements.append(Paragraph("1. Overall Quarterly Performance", subheading_s))
      elements.append(Paragraph(f"BOMAS Hardware Store generated KES {total_sales:,.0f} in revenue and KES {total_profit:,.0f} in gross profit during the first 74 working days of Q1 2026. This translates to an average daily revenue of KES {daily_avg:,.0f} and an average daily profit of KES {daily_profit:,.0f}. The overall profit margin stabilized at {overall_margin:.1f}%.", body_s))
      elements.append(Spacer(1, 10))
      
      elements.append(Paragraph("2. Departmental Contribution & Margin Analysis", subheading_s))
      elements.append(Paragraph(f"The {top_cat} department remains the dominant revenue driver, accounting for {top_cat_share:.1f}% of total Q1 sales (KES {top_cat_sales:,.0f}). However, margin analysis reveals that {highest_margin_cat} operates at the highest profitability rate ({highest_margin_cat_margin:.1f}%). Strategic focus should be placed on pushing higher-margin {highest_margin_cat} items in Q2 to lift the overall {overall_margin:.1f}% store margin.", body_s))
      elements.append(Spacer(1, 10))
      
      elements.append(Paragraph("3. Sales Team Productivity", subheading_s))
      elements.append(Paragraph(f"Sales concentration is notably high among the top performers. {top_rep} led the quarter with KES {top_rep_sales:,.0f} in sales, followed closely by {second_rep} (KES {second_rep_sales:,.0f}). Combined, these top two representatives accounted for {top_2_share:.1f}% of the store's total Q1 volume. To mitigate key-person dependency risks, training and mentorship programs should be implemented for the remaining {len(reps_data)-2} active representatives.", body_s))
      elements.append(Spacer(1, 10))
      
      elements.append(Paragraph("4. Q2 Operational Recommendations", subheading_s))
      elements.append(Paragraph("&bull; Balance cross-selling between volume leader (General Hardware) and margin leaders (Plumbing/Electricals).", body_s))
      elements.append(Paragraph("&bull; Conduct sales training focused on improving the conversion rates and average order values of bottom-quartile representatives.", body_s))
      elements.append(Paragraph("&bull; Align Minimum Order Quantities (MOQs) with Q1 daily consumption averages to ensure optimal working capital allocation.", body_s))
      elements.append(Spacer(1, 20))
"""
code = code.replace("elements.append(summary_table)\n    elements.append(Spacer(1, 15))", "elements.append(summary_table)\n    elements.append(Spacer(1, 15))\n" + pdf_insights)

# 2. Word Insights
word_insights = """
    doc.add_page_break()
    p = doc.add_paragraph()
    run = p.add_run("Q1 2026 STRATEGIC BUSINESS INSIGHTS")
    run.bold = True
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0x2c, 0x3e, 0x50)

    p = doc.add_paragraph()
    run = p.add_run("1. Overall Quarterly Performance")
    run.bold = True
    doc.add_paragraph(f"BOMAS Hardware Store generated KES {total_sales:,.0f} in revenue and KES {total_profit:,.0f} in gross profit during the first 74 working days of Q1 2026. This translates to an average daily revenue of KES {total_sales/74:,.0f} and an average daily profit of KES {total_profit/74:,.0f}. The overall profit margin stabilized at {overall_margin:.1f}%.")
    
    p = doc.add_paragraph()
    run = p.add_run("2. Departmental Contribution & Margin Analysis")
    run.bold = True
    doc.add_paragraph(f"The {top_cat} department remains the dominant revenue driver, accounting for {top_cat_share:.1f}% of total Q1 sales (KES {top_cat_sales:,.0f}). However, margin analysis reveals that {highest_margin_cat} operates at the highest profitability rate ({highest_margin_cat_margin:.1f}%). Strategic focus should be placed on pushing higher-margin {highest_margin_cat} items in Q2 to lift the overall {overall_margin:.1f}% store margin.")
    
    p = doc.add_paragraph()
    run = p.add_run("3. Sales Team Productivity")
    run.bold = True
    doc.add_paragraph(f"Sales concentration is notably high among the top performers. {top_rep} led the quarter with KES {top_rep_sales:,.0f} in sales, followed closely by {second_rep} (KES {second_rep_sales:,.0f}). Combined, these top two representatives accounted for {top_2_share:.1f}% of the store's total Q1 volume. To mitigate key-person dependency risks, training and mentorship programs should be implemented for the remaining {len(reps_data)-2} active representatives.")
    
    p = doc.add_paragraph()
    run = p.add_run("4. Q2 Operational Recommendations")
    run.bold = True
    doc.add_paragraph("- Balance cross-selling between volume leader (General Hardware) and margin leaders (Plumbing/Electricals).")
    doc.add_paragraph("- Conduct sales training focused on improving the conversion rates and average order values of bottom-quartile representatives.")
    doc.add_paragraph("- Align Minimum Order Quantities (MOQs) with Q1 daily consumption averages to ensure optimal working capital allocation.")
"""
code = code.replace("def generate_word():", "def generate_word():\n" + word_insights.replace('    ', '    '))


with open('generate_q1_analysis.py', 'w') as f:
    f.write(code)
