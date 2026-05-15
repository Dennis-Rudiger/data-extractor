with open("generate_april_analysis.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "WORKING_DAYS =" in line:
        lines[i] = "WORKING_DAYS = 26\n"
    elif "Quarterly Performance" in line:
        lines[i] = line.replace("Quarterly Performance", "Monthly Performance")
    elif "Quarterly Insights" in line:
        lines[i] = line.replace("Quarterly Insights", "Monthly Insights")
    elif "74 working days" in line:
        lines[i] = line.replace("74 working days", "{WORKING_DAYS} working days")
    elif "total_sales/74" in line:
        lines[i] = line.replace("total_sales/74", "total_sales/WORKING_DAYS")
    elif "total_profit/74" in line:
        lines[i] = line.replace("total_profit/74", "total_profit/WORKING_DAYS")
    elif "{top_cat} department remains the dominant revenue driver, accounting for {top_cat_share:.1f}% of total Q1 sales" in line:
        lines[i] = line.replace("Q1 sales", "April sales")

# Clean duplicate insights blocks. We have a block that starts with `elements.append(PageBreak())` and goes to `elements.append(Spacer(1, 20))` and it is duplicated exactly right below it.
content = "".join(lines)

dup_block_search = """    # --- Monthly Insights
    elements.append(PageBreak())
    elements.append(Paragraph("April 2026 STRATEGIC BUSINESS INSIGHTS", heading_s))
      
    elements.append(Paragraph("1. Overall Monthly Performance", subheading_s))
    elements.append(Paragraph(f"BOMAS Hardware Store generated KES {total_sales:,.0f} in revenue and KES {total_profit:,.0f} in gross profit during the first {WORKING_DAYS} working days of April 2026. This translates to an average daily revenue of KES {daily_avg:,.0f} and an average daily profit of KES {daily_profit:,.0f}. The overall profit margin stabilized at {overall_margin:.1f}%.", body_s))
    elements.append(Spacer(1, 10))
      
    elements.append(Paragraph("2. Departmental Contribution & Margin Analysis", subheading_s))
    elements.append(Paragraph(f"The {top_cat} department remains the dominant revenue driver, accounting for {top_cat_share:.1f}% of total April sales (KES {top_cat_sales:,.0f}). However, margin analysis reveals that {highest_margin_cat} operates at the highest profitability rate ({highest_margin_cat_margin:.1f}%). Strategic focus should be placed on pushing higher-margin {highest_margin_cat} items in Q2 to lift the overall {overall_margin:.1f}% store margin.", body_s))
    elements.append(Spacer(1, 10))
      
    elements.append(Paragraph("3. Sales Team Productivity", subheading_s))
    elements.append(Paragraph(f"Sales concentration is notably high among the top performers. {top_rep} led the quarter with KES {top_rep_sales:,.0f} in sales, followed closely by {second_rep} (KES {second_rep_sales:,.0f}). Combined, these top two representatives accounted for {top_2_share:.1f}% of the store's total April volume. To mitigate key-person dependency risks, training and mentorship programs should be implemented for the remaining {len(reps_data)-2} active representatives.", body_s))
    elements.append(Spacer(1, 10))
      
    elements.append(Paragraph("4. Q2 Operational Recommendations", subheading_s))
    elements.append(Paragraph("&bull; Balance cross-selling between volume leader (General Hardware) and margin leaders (Plumbing/Electricals).", body_s))
    elements.append(Paragraph("&bull; Conduct sales training focused on improving the conversion rates and average order values of bottom-quartile representatives.", body_s))
    elements.append(Paragraph("&bull; Align Minimum Order Quantities (MOQs) with April daily consumption averages to ensure optimal working capital allocation.", body_s))
    elements.append(Spacer(1, 20))


"""

content = content.replace(dup_block_search + dup_block_search, dup_block_search)
content = content.replace("Q2", "May")  # Changing expectations from Q2 (Quarter 2) to May for following month.
content = content.replace("Q1", "April")
content = content.replace("quarter", "month")

with open("generate_april_analysis.py", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
