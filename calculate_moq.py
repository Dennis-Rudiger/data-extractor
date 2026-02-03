import json
from datetime import datetime, timedelta
import re

"""
Minimum Order Quantity (MOQ) Calculator - Weekly Reorder

Formula:
    Daily Average = Total Consumed / Number of Days Monitored
    Weekly Average = Daily Average × 7
    MOQ (Weekly) = Weekly Average (rounded up)

Data Source:
    Real consumption data from stock movement reports (January 5-26, 2026)
"""

def load_inventory():
    """Load the priced inventory data"""
    with open('inventory_valuation_priced.json', 'r') as f:
        return json.load(f)

def load_consumption_data():
    """Load real consumption data extracted from stock movement PDFs"""
    with open('consumption_data.json', 'r') as f:
        return json.load(f)

def clean_description(desc):
    """Remove BOMAS from description and clean up"""
    if not desc:
        return ''
    # Remove BOMAS suffix
    desc = re.sub(r'\s*BOMAS\s*$', '', desc, flags=re.IGNORECASE)
    desc = re.sub(r'\s*BOMAS\s*', ' ', desc, flags=re.IGNORECASE)
    return desc.strip()

def build_inventory_lookup(inventory_data):
    """Build a lookup dictionary for inventory items by item_code"""
    lookup = {}
    for group in inventory_data:
        category = group['category_name']
        for product in group['products']:
            item_code = product['item_code']
            lookup[item_code] = {
                'category': category,
                'item_description': clean_description(product['item_description']),
                'buying_price': product.get('buying_price', 0),
                'selling_price': product.get('selling_price', 0),
                'quantity': product.get('quantity', 0)
            }
    return lookup

def merge_consumption_with_inventory(consumption_data, inventory_lookup):
    """
    Merge real consumption data with inventory data for MOQ calculation.
    Uses quantity_out from stock movement as consumption.
    """
    period = consumption_data['monitoring_period']
    merged_data = {
        'monitoring_period_days': period['days'],
        'start_date': period['start_date'],
        'end_date': period['end_date'],
        'sales_by_rep': consumption_data.get('sales_by_rep', {}),
        'categories': {}
    }
    
    for item_code, item_data in consumption_data['items'].items():
        # Use quantity_out as the consumption metric
        total_consumed = item_data['quantity_out']
        
        # Get inventory data if available
        inv_data = inventory_lookup.get(item_code, {})
        category = inv_data.get('category', 'UNCATEGORIZED')
        
        # Clean description - remove BOMAS
        description = clean_description(item_data.get('description', '')) or inv_data.get('item_description', 'Unknown')
        
        if category not in merged_data['categories']:
            merged_data['categories'][category] = {'products': {}}
        
        merged_data['categories'][category]['products'][item_code] = {
            'item_description': description,
            'total_consumed': total_consumed,
            'quantity_sold': item_data.get('quantity_sold', 0),
            'total_revenue': item_data.get('total_revenue', 0),
            'total_profit': item_data.get('total_profit', 0),
            'buying_price': inv_data.get('buying_price', 0),
            'selling_price': inv_data.get('selling_price', 0),
            'current_stock': item_data.get('closing_balance', 0),
            'opening_balance': item_data.get('opening_balance', 0),
            'sales_reps': item_data.get('sales_reps', [])
        }
    
    return merged_data

def calculate_moq_weekly(consumption_data):
    """
    Calculate Weekly Minimum Order Quantity for each item.
    
    Formula:
        Daily Average = Total Consumed / Number of Days Monitored
        Weekly Average = Daily Average × 7
        MOQ (Weekly) = Weekly Average (rounded up)
    """
    monitoring_days = consumption_data['monitoring_period_days']
    results = {
        'parameters': {
            'monitoring_period_days': monitoring_days,
            'start_date': consumption_data.get('start_date', ''),
            'end_date': consumption_data.get('end_date', ''),
            'reorder_period': 'Weekly (7 days)',
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M')
        },
        'formula': {
            'daily_average': 'Total Consumed ÷ Monitoring Days',
            'weekly_average': 'Daily Average × 7',
            'moq_weekly': 'Weekly Average (rounded up)'
        },
        'sales_summary': consumption_data.get('sales_by_rep', {}),
        'categories': {},
        'fast_movers': [],
        'low_stock_alerts': []
    }
    
    all_products = []
    
    for category, cat_data in consumption_data['categories'].items():
        category_results = {
            'category_name': category,
            'total_items': 0,
            'items_with_movement': 0,
            'total_consumed': 0,
            'total_weekly_moq': 0,
            'total_weekly_value': 0,
            'products': []
        }
        
        for item_code, item_data in cat_data['products'].items():
            total_consumed = item_data['total_consumed']
            buying_price = item_data.get('buying_price', 0)
            current_stock = item_data.get('current_stock', 0)
            
            # Calculate daily average consumption
            daily_average = total_consumed / monitoring_days if monitoring_days > 0 else 0
            
            # Calculate weekly average (MOQ for weekly reorder)
            weekly_average = daily_average * 7
            
            # Round up to nearest whole number for MOQ
            moq_weekly = int(weekly_average) + (1 if weekly_average % 1 > 0 else 0) if weekly_average > 0 else 0
            
            # Calculate weekly order value
            weekly_order_value = moq_weekly * buying_price
            
            # Calculate weeks of stock remaining
            weeks_remaining = current_stock / weekly_average if weekly_average > 0 else float('inf')
            
            # Low stock alert if less than 1 week of stock
            low_stock = weeks_remaining < 1 and weekly_average > 0
            
            product_result = {
                'item_code': item_code,
                'item_description': item_data['item_description'],
                'category': category,
                'total_consumed': total_consumed,
                'daily_average': round(daily_average, 2),
                'weekly_average': round(weekly_average, 2),
                'moq_weekly': moq_weekly,
                'current_stock': current_stock,
                'weeks_remaining': round(weeks_remaining, 1) if weeks_remaining != float('inf') else 'N/A',
                'buying_price': buying_price,
                'weekly_order_value': round(weekly_order_value, 2),
                'low_stock': low_stock
            }
            
            category_results['products'].append(product_result)
            category_results['total_items'] += 1
            category_results['total_consumed'] += total_consumed
            
            if total_consumed > 0:
                category_results['items_with_movement'] += 1
                category_results['total_weekly_moq'] += moq_weekly
                category_results['total_weekly_value'] += weekly_order_value
            
            all_products.append(product_result)
            
            # Add to low stock alerts if needed
            if low_stock:
                results['low_stock_alerts'].append(product_result)
        
        # Sort by weekly MOQ descending (highest demand first)
        category_results['products'].sort(key=lambda x: x['moq_weekly'], reverse=True)
        category_results['total_weekly_value'] = round(category_results['total_weekly_value'], 2)
        
        results['categories'][category] = category_results
    
    # Get top 50 fast movers across all categories
    all_products.sort(key=lambda x: x['moq_weekly'], reverse=True)
    results['fast_movers'] = all_products[:50]
    
    # Sort low stock alerts by weeks remaining
    results['low_stock_alerts'].sort(key=lambda x: x['weeks_remaining'] if x['weeks_remaining'] != 'N/A' else float('inf'))
    
    return results

def save_moq_results(data, filename='moq_results.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f'MOQ results saved: {filename}')

def print_summary(moq_results):
    print('\n' + '='*75)
    print('WEEKLY MINIMUM ORDER QUANTITY (MOQ) REPORT')
    print('Based on Real Sales Data')
    print('='*75)
    
    params = moq_results['parameters']
    print(f"\nMonitoring Period: {params['start_date']} to {params['end_date']} ({params['monitoring_period_days']} days)")
    print(f"Reorder Period: {params['reorder_period']}")
    
    print('\nFormula Used:')
    print(f"  Daily Average = Total Consumed ÷ {params['monitoring_period_days']} days")
    print(f"  Weekly Average = Daily Average × 7")
    print(f"  MOQ (Weekly) = Weekly Average (rounded up)")
    
    # Sales by rep summary
    if moq_results.get('sales_summary'):
        print('\n' + '-'*75)
        print('SALES BY REPRESENTATIVE')
        print('-'*75)
        print(f"{'Sales Rep':<40} {'Items':>8} {'Qty Sold':>12} {'Revenue':>12}")
        for rep, data in sorted(moq_results['sales_summary'].items(), key=lambda x: x[1]['total_amount'], reverse=True):
            if rep and rep.strip():
                print(f"{rep[:40]:<40} {data['items_sold']:>8} {data['total_quantity']:>12,.0f} {data['total_amount']:>12,.0f}")
    
    # Fast movers summary
    if moq_results.get('fast_movers'):
        print('\n' + '-'*75)
        print('TOP 20 FAST MOVERS (by Weekly MOQ)')
        print('-'*75)
        print(f"{'Item Code':<12} {'Description':<25} {'Consumed':>10} {'Daily':>8} {'Weekly MOQ':>10}")
        for item in moq_results['fast_movers'][:20]:
            desc = item['item_description'][:23] if item['item_description'] else 'Unknown'
            print(f"{item['item_code']:<12} {desc:<25} {item['total_consumed']:>10,.0f} {item['daily_average']:>8.1f} {item['moq_weekly']:>10}")
    
    # Category summary
    print('\n' + '-'*75)
    print('WEEKLY MOQ BY CATEGORY')
    print('-'*75)
    print(f"{'Category':<30} {'Items':>6} {'Moving':>7} {'Consumed':>10} {'Weekly MOQ':>10} {'Value (KES)':>12}")
    
    grand_total_moq = 0
    grand_total_value = 0
    total_consumed = 0
    sorted_cats = sorted(moq_results['categories'].items(), key=lambda x: x[1]['total_consumed'], reverse=True)
    for category, data in sorted_cats:
        if data['total_consumed'] > 0:
            print(f"{category[:30]:<30} {data['total_items']:>6} {data['items_with_movement']:>7} {data['total_consumed']:>10,.0f} {data['total_weekly_moq']:>10,} {data['total_weekly_value']:>12,.0f}")
            grand_total_moq += data['total_weekly_moq']
            grand_total_value += data['total_weekly_value']
            total_consumed += data['total_consumed']
    
    print('-'*75)
    print(f"{'TOTAL':<30} {'':<6} {'':<7} {total_consumed:>10,.0f} {grand_total_moq:>10,} {grand_total_value:>12,.0f}")
    
    # Low stock alerts
    if moq_results.get('low_stock_alerts'):
        print('\n' + '-'*75)
        print(f"⚠️  LOW STOCK ALERTS ({len(moq_results['low_stock_alerts'])} items with less than 1 week of stock)")
        print('-'*75)
        for item in moq_results['low_stock_alerts'][:15]:
            desc = item['item_description'][:30] if item['item_description'] else item['item_code']
            weeks = item['weeks_remaining']
            weeks_str = f"{weeks:.1f} weeks" if isinstance(weeks, (int, float)) else weeks
            print(f"  {item['item_code']}: {desc} | Stock={item['current_stock']:.0f}, Weekly MOQ={item['moq_weekly']}, {weeks_str} left")
    
    print('='*75)

if __name__ == '__main__':
    print('Loading inventory data...')
    inventory = load_inventory()
    inventory_lookup = build_inventory_lookup(inventory)
    
    print('Loading real consumption data from stock movement reports...')
    raw_consumption = load_consumption_data()
    
    print('Merging consumption with inventory data...')
    consumption = merge_consumption_with_inventory(raw_consumption, inventory_lookup)
    
    print(f"Period: {consumption['start_date']} to {consumption['end_date']} ({consumption['monitoring_period_days']} days)")
    print(f"Categories: {len(consumption['categories'])}")
    
    print('\nCalculating Weekly MOQ...')
    moq = calculate_moq_weekly(consumption)
    save_moq_results(moq)
    
    print_summary(moq)
    print('\nDone! Results saved to moq_results.json')
