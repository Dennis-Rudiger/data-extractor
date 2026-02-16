import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.units import inch
from datetime import datetime

# Week 1 Data (Feb 1-7, 2026)
week1_data = {
    "period": "February 1-7, 2026",
    "working_days": 6,
    "categories": {
        "PLUMBING": {
            "Betha Odumo": {"qty": 25, "sales_incl": 5790, "cost": 3563.36, "profit": 1428.02},
            "Bonface Kitheka": {"qty": 149, "sales_incl": 74120, "cost": 50318.18, "profit": 13578.36},
            "Bonface Muriu": {"qty": 59, "sales_incl": 21120, "cost": 14755.56, "profit": 3451.33},
            "Eliza": {"qty": 392, "sales_incl": 100035, "cost": 63234.79, "profit": 23002.29},
            "Gladys": {"qty": 99, "sales_incl": 58630, "cost": 38174.12, "profit": 12368.98},
            "Lewis": {"qty": 538, "sales_incl": 208330, "cost": 135995.12, "profit": 43599.69},
            "Stephen": {"qty": 36, "sales_incl": 156730, "cost": 114305.37, "profit": 20806.71}
        },
        "ELECTRICALS": {
            "Betha Odumo": {"qty": 29, "sales_incl": 4640, "cost": 3270.29, "profit": 729.71},
            "Bonface Kitheka": {"qty": 421, "sales_incl": 37635, "cost": 21481.84, "profit": 10962.11},
            "Bonface Muriu": {"qty": 103, "sales_incl": 26760, "cost": 12548.86, "profit": 10520.1},
            "Eliza": {"qty": 339, "sales_incl": 38940, "cost": 26449.59, "profit": 7119.38},
            "Lewis": {"qty": 21, "sales_incl": 4840, "cost": 3229.89, "profit": 942.51}
        },
        "PAINTS": {
            "Betha Odumo": {"qty": 135, "sales_incl": 109900, "cost": 74676.1, "profit": 20065.3},
            "Bonface Kitheka": {"qty": 113, "sales_incl": 142420, "cost": 107533.97, "profit": 15241.91},
            "Bonface Muriu": {"qty": 329, "sales_incl": 323270, "cost": 229016.28, "profit": 49664.73},
            "Eliza": {"qty": 523, "sales_incl": 595550, "cost": 438908.57, "profit": 74496.57},
            "Gladys": {"qty": 18, "sales_incl": 33800, "cost": 23375.42, "profit": 5762.51},
            "Lewis": {"qty": 103, "sales_incl": 71660, "cost": 47183.19, "profit": 14592.67},
            "Stephen": {"qty": 67, "sales_incl": 74360, "cost": 51984.76, "profit": 12118.68}
        },
        "GENERAL HARDWARE": {
            "Betha Odumo": {"qty": 2996, "sales_incl": 2163840, "cost": 1703316.1, "profit": 162063.16},
            "Bonface Kitheka": {"qty": 420, "sales_incl": 232485, "cost": 171841.89, "profit": 28576.2},
            "Bonface Muriu": {"qty": 1175, "sales_incl": 1128619, "cost": 864689.69, "profit": 108257.76},
            "Eliza": {"qty": 2292, "sales_incl": 1636135, "cost": 1271278.16, "profit": 139182.99},
            "Gladys": {"qty": 6661, "sales_incl": 5538955, "cost": 4512274.33, "profit": 262686.92},
            "Lewis": {"qty": 709.25, "sales_incl": 552707, "cost": 423471.03, "profit": 53000.48},
            "Stephen": {"qty": 1392.5, "sales_incl": 925821, "cost": 726157.7, "profit": 71963.83}
        }
    }
}

# Week 2 Data (Feb 9-13, 2026) - extracted from PDFs
week2_data = {
    "period": "February 9-13, 2026",
    "working_days": 5,
    "categories": {
        "PLUMBING": {
            "Betha Odumo": {"qty": 127, "sales_incl": 19995, "cost": 11935.22, "profit": 5301.87},
            "Bonface Kitheka": {"qty": 133, "sales_incl": 23310, "cost": 12603.30, "profit": 7491.52},
            "Bonface Muriu": {"qty": 109, "sales_incl": 43520, "cost": 27642.44, "profit": 9874.80},
            "Eliza": {"qty": 32, "sales_incl": 13980, "cost": 6036.78, "profit": 6014.93},
            "Gladys": {"qty": 110, "sales_incl": 26540, "cost": 16600.17, "profit": 6279.15},
            "Lewis": {"qty": 544, "sales_incl": 132125, "cost": 81966.06, "profit": 31934.72},
            "Stephen": {"qty": 8, "sales_incl": 4730, "cost": 2513.60, "profit": 1563.99},
            "WALK IN-BOMAS": {"qty": 38, "sales_incl": 2361, "cost": 1783.32, "profit": 252.03}
        },
        "ELECTRICALS": {
            "Betha Odumo": {"qty": 116, "sales_incl": 10170, "cost": 5671.39, "profit": 3095.83},
            "Bonface Kitheka": {"qty": 1342, "sales_incl": 78815, "cost": 50522.65, "profit": 17421.30},
            "Bonface Muriu": {"qty": 3, "sales_incl": 430, "cost": 163.67, "profit": 207.02},
            "Eliza": {"qty": 9, "sales_incl": 1880, "cost": 905.15, "profit": 715.54},
            "Gladys": {"qty": 5, "sales_incl": 650, "cost": 340.75, "profit": 219.59},
            "Lewis": {"qty": 26, "sales_incl": 18715, "cost": 13545.01, "profit": 2588.62},
            "WALK IN-BOMAS": {"qty": 7, "sales_incl": 241, "cost": 205.30, "profit": 2.46}
        },
        "PAINTS": {
            "Betha Odumo": {"qty": 35, "sales_incl": 55670, "cost": 40076.26, "profit": 7915.11},
            "Bonface Kitheka": {"qty": 116, "sales_incl": 72080, "cost": 51244.29, "profit": 10893.63},
            "Bonface Muriu": {"qty": 386, "sales_incl": 362340, "cost": 255517.67, "profit": 56844.37},
            "Eliza": {"qty": 238, "sales_incl": 282400, "cost": 204165.86, "profit": 39282.34},
            "Gladys": {"qty": 19, "sales_incl": 24160, "cost": 17288.48, "profit": 3539.10},
            "Lewis": {"qty": 52, "sales_incl": 40680, "cost": 27319.38, "profit": 7749.60},
            "Stephen": {"qty": 48, "sales_incl": 42750, "cost": 30110.75, "profit": 6742.69},
            "WALK IN-BOMAS": {"qty": 1, "sales_incl": 3106, "cost": 2677.50, "profit": 0.09}
        },
        "GENERAL HARDWARE": {
            "Betha Odumo": {"qty": 3140.5, "sales_incl": 2548690, "cost": 2067272.04, "profit": 129874.52},
            "Bonface Kitheka": {"qty": 447.25, "sales_incl": 328895, "cost": 255712.50, "profit": 27817.67},
            "Bonface Muriu": {"qty": 965.5, "sales_incl": 631905, "cost": 495266.71, "profit": 49478.98},
            "Eliza": {"qty": 1768, "sales_incl": 1678295, "cost": 1323155.13, "profit": 123650.87},
            "Gladys": {"qty": 7210, "sales_incl": 7079535, "cost": 5738804.65, "profit": 364242.81},
            "Lewis": {"qty": 1236.25, "sales_incl": 923755, "cost": 739658.94, "profit": 56681.58},
            "Stephen": {"qty": 1795, "sales_incl": 1235205, "cost": 967433.38, "profit": 97398.50},
            "WALK IN-BOMAS": {"qty": 36, "sales_incl": 13327, "cost": 6905.34, "profit": 4583.44}
        }
    }
}

def merge_walk_in_to_kitheka(data):
    """Merge WALK IN-BOMAS transactions into Bonface Kitheka"""
    for cat, reps in data["categories"].items():
        if "WALK IN-BOMAS" in reps:
            walk_in = reps.pop("WALK IN-BOMAS")
            if "Bonface Kitheka" in reps:
                reps["Bonface Kitheka"]["qty"] += walk_in["qty"]
                reps["Bonface Kitheka"]["sales_incl"] += walk_in["sales_incl"]
                reps["Bonface Kitheka"]["cost"] += walk_in["cost"]
                reps["Bonface Kitheka"]["profit"] += walk_in["profit"]
            else:
                reps["Bonface Kitheka"] = walk_in
    return data

def calculate_rep_totals(data):
    """Calculate totals for each rep across all categories"""
    rep_totals = {}
    for cat, reps in data["categories"].items():
        for rep, vals in reps.items():
            if rep not in rep_totals:
                rep_totals[rep] = {"qty": 0, "sales_incl": 0, "cost": 0, "profit": 0, "categories": {}}
            rep_totals[rep]["qty"] += vals["qty"]
            rep_totals[rep]["sales_incl"] += vals["sales_incl"]
            rep_totals[rep]["cost"] += vals["cost"]
            rep_totals[rep]["profit"] += vals["profit"]
            rep_totals[rep]["categories"][cat] = vals.copy()
    
    # Calculate margin %
    for rep, vals in rep_totals.items():
        vals["margin_pct"] = (vals["profit"] / vals["sales_incl"] * 100) if vals["sales_incl"] > 0 else 0
    
    return rep_totals

def calculate_category_totals(data):
    """Calculate totals for each category"""
    cat_totals = {}
    for cat, reps in data["categories"].items():
        cat_totals[cat] = {"qty": 0, "sales_incl": 0, "cost": 0, "profit": 0}
        for rep, vals in reps.items():
            cat_totals[cat]["qty"] += vals["qty"]
            cat_totals[cat]["sales_incl"] += vals["sales_incl"]
            cat_totals[cat]["cost"] += vals["cost"]
            cat_totals[cat]["profit"] += vals["profit"]
        cat_totals[cat]["margin_pct"] = (cat_totals[cat]["profit"] / cat_totals[cat]["sales_incl"] * 100) if cat_totals[cat]["sales_incl"] > 0 else 0
    return cat_totals

def combine_periods(w1, w2):
    """Combine two periods of data"""
    combined = {
        "period": "February 1-13, 2026",
        "working_days": w1["working_days"] + w2["working_days"],
        "categories": {}
    }
    
    all_cats = set(w1["categories"].keys()) | set(w2["categories"].keys())
    
    for cat in all_cats:
        combined["categories"][cat] = {}
        reps1 = w1["categories"].get(cat, {})
        reps2 = w2["categories"].get(cat, {})
        all_reps = set(reps1.keys()) | set(reps2.keys())
        
        for rep in all_reps:
            v1 = reps1.get(rep, {"qty": 0, "sales_incl": 0, "cost": 0, "profit": 0})
            v2 = reps2.get(rep, {"qty": 0, "sales_incl": 0, "cost": 0, "profit": 0})
            combined["categories"][cat][rep] = {
                "qty": v1["qty"] + v2["qty"],
                "sales_incl": v1["sales_incl"] + v2["sales_incl"],
                "cost": v1["cost"] + v2["cost"],
                "profit": v1["profit"] + v2["profit"]
            }
    
    return combined

def generate_analysis():
    """Generate comprehensive performance analysis"""
    # Merge walk-ins into Kitheka for week 2
    week2_merged = merge_walk_in_to_kitheka(week2_data.copy())
    
    # Calculate totals for each period
    w1_rep_totals = calculate_rep_totals(week1_data)
    w2_rep_totals = calculate_rep_totals(week2_merged)
    
    w1_cat_totals = calculate_category_totals(week1_data)
    w2_cat_totals = calculate_category_totals(week2_merged)
    
    # Combine periods
    combined = combine_periods(week1_data, week2_merged)
    combined_rep_totals = calculate_rep_totals(combined)
    combined_cat_totals = calculate_category_totals(combined)
    
    # Grand totals
    w1_total = {"sales": sum(r["sales_incl"] for r in w1_rep_totals.values()),
                "profit": sum(r["profit"] for r in w1_rep_totals.values()),
                "cost": sum(r["cost"] for r in w1_rep_totals.values())}
    w2_total = {"sales": sum(r["sales_incl"] for r in w2_rep_totals.values()),
                "profit": sum(r["profit"] for r in w2_rep_totals.values()),
                "cost": sum(r["cost"] for r in w2_rep_totals.values())}
    combined_total = {"sales": sum(r["sales_incl"] for r in combined_rep_totals.values()),
                      "profit": sum(r["profit"] for r in combined_rep_totals.values()),
                      "cost": sum(r["cost"] for r in combined_rep_totals.values())}
    
    return {
        "week1": {"rep_totals": w1_rep_totals, "cat_totals": w1_cat_totals, "grand_total": w1_total, "period": week1_data["period"], "days": week1_data["working_days"]},
        "week2": {"rep_totals": w2_rep_totals, "cat_totals": w2_cat_totals, "grand_total": w2_total, "period": week2_merged["period"], "days": week2_merged["working_days"]},
        "combined": {"rep_totals": combined_rep_totals, "cat_totals": combined_cat_totals, "grand_total": combined_total, "period": combined["period"], "days": combined["working_days"]}
    }

def print_analysis(analysis):
    """Print analysis summary"""
    print("=" * 90)
    print("SALES PERFORMANCE ANALYSIS - FEBRUARY 2026")
    print("=" * 90)
    
    for period_key, period_name in [("week1", "WEEK 1"), ("week2", "WEEK 2"), ("combined", "COMBINED")]:
        data = analysis[period_key]
        print(f"\n{'='*90}")
        print(f"{period_name}: {data['period']} ({data['days']} working days)")
        print("=" * 90)
        
        print(f"\nGrand Total: Sales KES {data['grand_total']['sales']:,.0f} | Profit KES {data['grand_total']['profit']:,.0f} | Margin {data['grand_total']['profit']/data['grand_total']['sales']*100:.1f}%")
        print(f"Daily Average: Sales KES {data['grand_total']['sales']/data['days']:,.0f} | Profit KES {data['grand_total']['profit']/data['days']:,.0f}")
        
        # Rep performance
        print(f"\n--- SALES REP PERFORMANCE ---")
        print(f"{'Rep':<20} {'Sales (KES)':>15} {'Profit (KES)':>15} {'Margin %':>10} {'Daily Sales':>15}")
        print("-" * 75)
        
        sorted_reps = sorted(data['rep_totals'].items(), key=lambda x: x[1]['sales_incl'], reverse=True)
        for rep, vals in sorted_reps:
            daily = vals['sales_incl'] / data['days']
            print(f"{rep:<20} {vals['sales_incl']:>15,.0f} {vals['profit']:>15,.0f} {vals['margin_pct']:>9.1f}% {daily:>15,.0f}")
        
        # Category performance
        print(f"\n--- CATEGORY PERFORMANCE ---")
        print(f"{'Category':<20} {'Sales (KES)':>15} {'Profit (KES)':>15} {'Margin %':>10}")
        print("-" * 60)
        
        sorted_cats = sorted(data['cat_totals'].items(), key=lambda x: x[1]['sales_incl'], reverse=True)
        for cat, vals in sorted_cats:
            print(f"{cat:<20} {vals['sales_incl']:>15,.0f} {vals['profit']:>15,.0f} {vals['margin_pct']:>9.1f}%")
    
    # Week over week comparison
    print("\n" + "=" * 90)
    print("WEEK OVER WEEK COMPARISON")
    print("=" * 90)
    
    w1 = analysis["week1"]
    w2 = analysis["week2"]
    
    # Normalize to daily for fair comparison
    w1_daily_sales = w1["grand_total"]["sales"] / w1["days"]
    w2_daily_sales = w2["grand_total"]["sales"] / w2["days"]
    w1_daily_profit = w1["grand_total"]["profit"] / w1["days"]
    w2_daily_profit = w2["grand_total"]["profit"] / w2["days"]
    
    sales_change = ((w2_daily_sales - w1_daily_sales) / w1_daily_sales) * 100
    profit_change = ((w2_daily_profit - w1_daily_profit) / w1_daily_profit) * 100
    
    print(f"\nDaily Sales: Week 1 KES {w1_daily_sales:,.0f} -> Week 2 KES {w2_daily_sales:,.0f} ({sales_change:+.1f}%)")
    print(f"Daily Profit: Week 1 KES {w1_daily_profit:,.0f} -> Week 2 KES {w2_daily_profit:,.0f} ({profit_change:+.1f}%)")
    
    # Rep comparison
    print(f"\n--- REP DAILY PERFORMANCE CHANGE ---")
    print(f"{'Rep':<20} {'W1 Daily':>12} {'W2 Daily':>12} {'Change':>10}")
    print("-" * 55)
    
    all_reps = set(w1["rep_totals"].keys()) | set(w2["rep_totals"].keys())
    for rep in sorted(all_reps):
        w1_daily = w1["rep_totals"].get(rep, {"sales_incl": 0})["sales_incl"] / w1["days"]
        w2_daily = w2["rep_totals"].get(rep, {"sales_incl": 0})["sales_incl"] / w2["days"]
        change = ((w2_daily - w1_daily) / w1_daily * 100) if w1_daily > 0 else 0
        print(f"{rep:<20} {w1_daily:>12,.0f} {w2_daily:>12,.0f} {change:>+9.1f}%")

if __name__ == "__main__":
    analysis = generate_analysis()
    print_analysis(analysis)
    
    # Save to JSON
    output = {
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "analysis": {
            "week1": {
                "period": analysis["week1"]["period"],
                "working_days": analysis["week1"]["days"],
                "grand_total": analysis["week1"]["grand_total"],
                "rep_totals": {k: {kk: vv for kk, vv in v.items() if kk != "categories"} for k, v in analysis["week1"]["rep_totals"].items()},
                "cat_totals": analysis["week1"]["cat_totals"]
            },
            "week2": {
                "period": analysis["week2"]["period"],
                "working_days": analysis["week2"]["days"],
                "grand_total": analysis["week2"]["grand_total"],
                "rep_totals": {k: {kk: vv for kk, vv in v.items() if kk != "categories"} for k, v in analysis["week2"]["rep_totals"].items()},
                "cat_totals": analysis["week2"]["cat_totals"]
            },
            "combined": {
                "period": analysis["combined"]["period"],
                "working_days": analysis["combined"]["days"],
                "grand_total": analysis["combined"]["grand_total"],
                "rep_totals": {k: {kk: vv for kk, vv in v.items() if kk != "categories"} for k, v in analysis["combined"]["rep_totals"].items()},
                "cat_totals": analysis["combined"]["cat_totals"]
            }
        }
    }
    
    with open("performance_analysis_feb2026.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("\n\nAnalysis saved to performance_analysis_feb2026.json")
