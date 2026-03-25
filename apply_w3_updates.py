import pathlib
import re

content = pathlib.Path('generate_march_w3_analysis.py').read_text(encoding='utf-8')

# Fix merge_reps: Magadalene and WALK IN-BOMAS -> Betha Odumo
old_merge = 'target = "Betha Odumo" if rep == "Magdalene" else rep'
new_merge = 'target = "Betha Odumo" if rep in ["Magdalene", "WALK IN-BOMAS"] else rep'
content = content.replace(old_merge, new_merge)

# Inject accumulated loads after weekly_target
target_anchor = "weekly_target = MONTHLY_TARGETS['OVERALL'] / 4\n"
cumulative_code = '''
# Load prior weeks
with open("sales_march_w1.json", "r") as f: w1_raw = json.load(f)
with open("sales_march_w2.json", "r") as f: w2_raw = json.load(f)

def get_week_sales(data_raw):
    totals_cat = {c: 0 for c in CAT_ORDER}
    totals = 0
    merged = merge_reps(data_raw)
    rep_d = get_rep_data(merged)
    for rep, r_data in rep_d.items():
        totals += r_data['total_sales']
        for cat in CAT_ORDER:
            totals_cat[cat] += r_data['categories'].get(cat, {}).get('sales_incl', 0)
    rep_sales = {rep: r_data['total_sales'] for rep, r_data in rep_d.items()}
    return totals, totals_cat, rep_sales

w1_tot, w1_cat, w1_rep = get_week_sales(w1_raw)
w2_tot, w2_cat, w2_rep = get_week_sales(w2_raw)

cumulative_total_sales = w1_tot + w2_tot + total_sales
cumulative_cat_totals = {c: cat_totals[c]['sales'] + w1_cat[c] + w2_cat[c] for c in CAT_ORDER}

'''

if "cumulative_total_sales =" not in content:
    content = content.replace(target_anchor, target_anchor + cumulative_code)

# Replace target tracking overall
content = content.replace("target_pct = (total_sales / MONTHLY_TARGETS['OVERALL'] * 100)", "target_pct = (cumulative_total_sales / MONTHLY_TARGETS['OVERALL'] * 100)")
content = content.replace("target_pct = total_sales / MONTHLY_TARGETS['OVERALL'] * 100", "target_pct = cumulative_total_sales / MONTHLY_TARGETS['OVERALL'] * 100")

# For target calculations
# 1. Chart: ('OVERALL', total_sales, MONTHLY_TARGETS['OVERALL']) -> cumulative_total_sales
content = content.replace("('OVERALL', total_sales, MONTHLY_TARGETS['OVERALL'])", "('OVERALL', cumulative_total_sales, MONTHLY_TARGETS['OVERALL'])")
content = content.replace("cat, cat_totals[cat]['sales']", "cat, cumulative_cat_totals[cat]")

# 2. PDF Target Progress
content = content.replace("Week 3 Achievement: KES {total_sales:,.0f} ({target_pct:.1f}% of target)", "Accumulated Achievement (W1-3): KES {cumulative_total_sales:,.0f} ({target_pct:.1f}% of target)")
content = content.replace("overall_vals = [\"OVERALL\", f\"KES {MONTHLY_TARGETS['OVERALL']:,.0f}\", f\"KES {total_sales:,.0f}\"", "overall_vals = [\"OVERALL\", f\"KES {MONTHLY_TARGETS['OVERALL']:,.0f}\", f\"KES {cumulative_total_sales:,.0f}\"")
content = content.replace("[\"OVERALL\", f\"KES {MONTHLY_TARGETS['OVERALL']:,.0f}\", f\"KES {total_sales:,.0f}\"", "[\"OVERALL\", f\"KES {MONTHLY_TARGETS['OVERALL']:,.0f}\", f\"KES {cumulative_total_sales:,.0f}\"")
content = content.replace("actual = cat_totals[cat]['sales']", "actual = cumulative_cat_totals[cat]")
content = content.replace("actual = cat_totals[cat]['sales'] if cat != 'OVERALL' else total_sales", "actual = cumulative_cat_totals[cat] if cat != 'OVERALL' else cumulative_total_sales")

# 3. JSON Output
content = content.replace('\"week3_actual\": total_sales', '\"accumulated_actual\": cumulative_total_sales')
content = content.replace('total_sales / MONTHLY_TARGETS', 'cumulative_total_sales / MONTHLY_TARGETS')

# Fix expected pace everywhere
content = content.replace('expected_pct = 25.0', 'expected_pct = 75.0')
content = content.replace('expected 25.0%', 'expected 75.0%')
content = content.replace('>= 25 else', '>= 75 else')
content = content.replace('\"25.0%\"', '\"75.0%\"')

print("Replaced variables.")

pathlib.Path('generate_march_w3_analysis.py').write_text(content, encoding='utf-8')
