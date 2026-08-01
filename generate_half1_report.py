#!/usr/bin/env python3
"""Generate Half 1 report from Thus far data files.

Reads:
- Thus far/data/Sales Analysis Summary Customers.csv
- Thus far/data/Inventory Sales Analysis_20260713_123405.csv
- Thus far/data/customer_sales_extracted.json (optional)

Writes: half1_report.md
"""
import csv
import json
import re
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / 'Thus far' / 'data'


def parse_money(s):
    if s is None:
        return 0.0
    s = str(s).strip()
    s = s.replace('"', '')
    s = s.replace(',', '')
    try:
        return float(s)
    except Exception:
        return 0.0


def parse_sales_summary(csv_path):
    customers = {}
    current_customer = None
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            first = row[0].strip() if len(row) > 0 else ''
            # detect customer label lines
            if first.startswith('Customer Name:'):
                # label format: 'Customer Name:  NAME'
                parts = first.split(':', 1)
                current_customer = parts[1].strip() if len(parts) > 1 else None
                continue

            # candidate data rows: rows that have numeric Amount(Exc) in column 2 (index 2)
            if len(row) >= 4:
                amt_exc = parse_money(row[2])
                amt_inc = parse_money(row[3])
                cost = parse_money(row[6]) if len(row) > 6 else 0.0
                profit = parse_money(row[7]) if len(row) > 7 else 0.0
                qty = parse_money(row[1]) if len(row) > 1 else 0.0
                if amt_exc > 0 and current_customer:
                    # accumulate for customer
                    if current_customer not in customers:
                        customers[current_customer] = {'qty': 0.0, 'amt_exc': 0.0, 'amt_inc': 0.0, 'cost': 0.0, 'profit': 0.0}
                    c = customers[current_customer]
                    c['qty'] += qty
                    c['amt_exc'] += amt_exc
                    c['amt_inc'] += amt_inc
                    c['cost'] += cost
                    c['profit'] += profit
    return customers


def parse_inventory(csv_path):
    products = {}
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            code = row[0].strip() if len(row) > 0 else ''
            # crude item code detection: starts with letters and digits
            if re.match(r'^[A-Z]{2,}[0-9]', code):
                desc = row[1].strip() if len(row) > 1 else ''
                # Quantity at index 4 (per file layout)
                qty = parse_money(row[4]) if len(row) > 4 else 0.0
                cost = parse_money(row[5]) if len(row) > 5 else 0.0
                profit = parse_money(row[6]) if len(row) > 6 else 0.0
                products[code] = {'desc': desc, 'qty': qty, 'cost': cost, 'profit': profit}
    return products


def main():
    sales_csv = DATA_DIR / 'Sales Analysis Summary Customers.csv'
    inv_csv = DATA_DIR / 'Inventory Sales Analysis_20260713_123405.csv'
    cust_json = DATA_DIR / 'customer_sales_extracted.json'

    sales = parse_sales_summary(sales_csv)
    products = parse_inventory(inv_csv)

    # totals
    total_amt_exc = sum(c['amt_exc'] for c in sales.values())
    total_amt_inc = sum(c['amt_inc'] for c in sales.values())
    total_cost = sum(c['cost'] for c in sales.values())
    total_profit = sum(c['profit'] for c in sales.values())
    avg_margin = (total_profit / total_amt_exc * 100) if total_amt_exc else 0.0

    # top customers
    top_customers = sorted(sales.items(), key=lambda kv: kv[1]['amt_exc'], reverse=True)[:10]

    # top products by qty and profit
    top_by_qty = sorted(products.items(), key=lambda kv: kv[1]['qty'], reverse=True)[:10]
    top_by_profit = sorted(products.items(), key=lambda kv: kv[1]['profit'], reverse=True)[:10]

    # build report
    out = []
    out.append('# Half 1 Report — Customers & Inventory Summary')
    out.append('Date: 2026-07-15')
    out.append('')
    out.append('## Executive summary')
    out.append(f'- Total Sales (Excl): {total_amt_exc:,.2f}')
    out.append(f'- Total Sales (Incl): {total_amt_inc:,.2f}')
    out.append(f'- Total Cost: {total_cost:,.2f}')
    out.append(f'- Total Profit: {total_profit:,.2f} ({avg_margin:.2f}% margin)')
    out.append('')
    out.append('## Top 10 Customers (by Sales Excl)')
    out.append('| Rank | Customer | Qty | Amount (Excl) | Profit |')
    out.append('|---:|---|---:|---:|---:|')
    for i, (cust, v) in enumerate(top_customers, 1):
        out.append(f'| {i} | {cust} | {v["qty"]:,.0f} | {v["amt_exc"]:,.2f} | {v["profit"]:,.2f} |')

    out.append('')
    out.append('## Top 10 Products by Quantity')
    out.append('| Rank | Item Code | Description | Qty |')
    out.append('|---:|---|---|---:|')
    for i, (code, v) in enumerate(top_by_qty, 1):
        out.append(f'| {i} | {code} | {v["desc"]} | {v["qty"]:,.0f} |')

    out.append('')
    out.append('## Top 10 Products by Profit')
    out.append('| Rank | Item Code | Description | Profit |')
    out.append('|---:|---|---|---:|')
    for i, (code, v) in enumerate(top_by_profit, 1):
        out.append(f'| {i} | {code} | {v["desc"]} | {v["profit"]:,.2f} |')

    out.append('')
    out.append('## Notes & Next Steps')
    out.append('- This report is generated from the supplied summary CSVs and inventory sales export.')
    out.append('- Next steps: include sales-rep breakdown, monthly trend charts, and inventory turnover metrics.')

    report_path = ROOT / 'half1_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))

    print('Wrote', report_path)


if __name__ == '__main__':
    main()
