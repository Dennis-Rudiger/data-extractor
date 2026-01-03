import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.units import inch
from datetime import datetime

def analyze_pricing_strategy(data):
    """Analyze the pricing data and extract comprehensive statistics"""
    
    stats = {
        'total_items': 0,
        'priced_items': 0,
        'unpriced_items': 0,
        'total_buying_value': 0,
        'total_selling_value': 0,
        'categories': {},
        'margin_distribution': {
            '0-10%': 0,
            '10-20%': 0,
            '20-30%': 0,
            '30-40%': 0,
            '40-50%': 0,
            '50%+': 0
        },
        'price_segments': {
            'Low (<100)': {'count': 0, 'buying': 0, 'selling': 0},
            'Mid (100-500)': {'count': 0, 'buying': 0, 'selling': 0},
            'High (500-2000)': {'count': 0, 'buying': 0, 'selling': 0},
            'Premium (2000+)': {'count': 0, 'buying': 0, 'selling': 0}
        }
    }
    
    for group in data:
        category_name = group['category_name']
        category_stats = {
            'item_count': 0,
            'priced_count': 0,
            'total_buying': 0,
            'total_selling': 0,
            'avg_margin': 0,
            'min_margin': float('inf'),
            'max_margin': 0,
            'margins': [],
            'projected_profit': 0
        }
        
        for product in group['products']:
            stats['total_items'] += 1
            category_stats['item_count'] += 1
            
            buying_price = product.get('buying_price', 0)
            selling_price = product.get('selling_price', 0)
            
            stats['total_buying_value'] += buying_price
            category_stats['total_buying'] += buying_price
            
            if selling_price > 0:
                stats['priced_items'] += 1
                category_stats['priced_count'] += 1
                stats['total_selling_value'] += selling_price
                category_stats['total_selling'] += selling_price
                
                margin = ((selling_price - buying_price) / buying_price) * 100 if buying_price > 0 else 0
                category_stats['margins'].append(margin)
                category_stats['min_margin'] = min(category_stats['min_margin'], margin)
                category_stats['max_margin'] = max(category_stats['max_margin'], margin)
                category_stats['projected_profit'] += (selling_price - buying_price)
                
                # Margin distribution
                if margin < 10:
                    stats['margin_distribution']['0-10%'] += 1
                elif margin < 20:
                    stats['margin_distribution']['10-20%'] += 1
                elif margin < 30:
                    stats['margin_distribution']['20-30%'] += 1
                elif margin < 40:
                    stats['margin_distribution']['30-40%'] += 1
                elif margin < 50:
                    stats['margin_distribution']['40-50%'] += 1
                else:
                    stats['margin_distribution']['50%+'] += 1
                
                # Price segment analysis
                if selling_price < 100:
                    stats['price_segments']['Low (<100)']['count'] += 1
                    stats['price_segments']['Low (<100)']['buying'] += buying_price
                    stats['price_segments']['Low (<100)']['selling'] += selling_price
                elif selling_price < 500:
                    stats['price_segments']['Mid (100-500)']['count'] += 1
                    stats['price_segments']['Mid (100-500)']['buying'] += buying_price
                    stats['price_segments']['Mid (100-500)']['selling'] += selling_price
                elif selling_price < 2000:
                    stats['price_segments']['High (500-2000)']['count'] += 1
                    stats['price_segments']['High (500-2000)']['buying'] += buying_price
                    stats['price_segments']['High (500-2000)']['selling'] += selling_price
                else:
                    stats['price_segments']['Premium (2000+)']['count'] += 1
                    stats['price_segments']['Premium (2000+)']['buying'] += buying_price
                    stats['price_segments']['Premium (2000+)']['selling'] += selling_price
            else:
                stats['unpriced_items'] += 1
        
        if category_stats['margins']:
            category_stats['avg_margin'] = sum(category_stats['margins']) / len(category_stats['margins'])
            # Calculate weighted average margin for category
            category_stats['weighted_margin'] = ((category_stats['total_selling'] - category_stats['total_buying']) / category_stats['total_buying'] * 100) if category_stats['total_buying'] > 0 else 0
        else:
            category_stats['min_margin'] = 0
            category_stats['weighted_margin'] = 0
        
        stats['categories'][category_name] = category_stats
    
    # Calculate overall average margin (only for priced items)
    priced_buying_value = sum(
        p.get('buying_price', 0) 
        for g in data 
        for p in g['products'] 
        if p.get('selling_price', 0) > 0
    )
    priced_selling_value = sum(
        p.get('selling_price', 0) 
        for g in data 
        for p in g['products'] 
        if p.get('selling_price', 0) > 0
    )
    
    if priced_buying_value > 0:
        stats['overall_margin'] = ((priced_selling_value - priced_buying_value) / priced_buying_value) * 100
        stats['priced_buying_value'] = priced_buying_value
        stats['priced_selling_value'] = priced_selling_value
        stats['projected_profit'] = priced_selling_value - priced_buying_value
        stats['unpriced_buying_value'] = stats['total_buying_value'] - priced_buying_value
        
        # Calculate ROI percentage
        stats['roi_percentage'] = (stats['projected_profit'] / priced_buying_value) * 100
    else:
        stats['overall_margin'] = 0
        stats['priced_buying_value'] = 0
        stats['priced_selling_value'] = 0
        stats['projected_profit'] = 0
        stats['unpriced_buying_value'] = stats['total_buying_value']
        stats['roi_percentage'] = 0
    
    return stats

def generate_pricing_logic_report(output_filename):
    """Generate a comprehensive pricing strategy report with insights and storytelling"""
    
    # Load data
    with open('inventory_valuation_priced.json', 'r') as f:
        data = json.load(f)
    
    # Analyze data
    stats = analyze_pricing_strategy(data)
    
    # Create PDF
    doc = SimpleDocTemplate(output_filename, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=8,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#7f8c8d'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=16,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    story_style = ParagraphStyle(
        'StoryStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        leading=14
    )
    
    # Title Page
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("INVENTORY PRICING STRATEGY", title_style))
    elements.append(Paragraph("Comprehensive Analysis & Strategic Insights", subtitle_style))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Executive Narrative
    elements.append(Paragraph("EXECUTIVE OVERVIEW", heading_style))
    
    priced_pct = (stats['priced_items'] / stats['total_items'] * 100) if stats['total_items'] > 0 else 0
    
    narrative = f"""Our inventory comprises <b>{stats['total_items']:,} unique items</b> across <b>24 product categories</b>, 
    representing a total buying investment of <b>KES {stats['total_buying_value']:,.2f}</b>. Through our strategic 
    pricing methodology, we have successfully priced <b>{stats['priced_items']:,} items ({priced_pct:.1f}%)</b>, 
    achieving a weighted average margin of <b>{stats['overall_margin']:.2f}%</b>.<br/><br/>
    
    Based on current pricing, our priced inventory has a projected selling value of <b>KES {stats['priced_selling_value']:,.2f}</b>, 
    translating to an anticipated gross profit of <b>KES {stats['projected_profit']:,.2f}</b>. This represents a 
    <b>{stats['roi_percentage']:.2f}% return on investment</b> for our priced inventory alone.<br/><br/>
    
    Our pricing strategy employs a sophisticated tiered approach that balances market competitiveness with healthy 
    profit margins. Lower-cost items utilize higher percentage margins to ensure profitability on smaller transactions, 
    while high-value items employ moderate margins to remain competitive in the marketplace."""
    
    elements.append(Paragraph(narrative, story_style))
    elements.append(Spacer(1, 20))
    
    # Key Performance Indicators
    elements.append(Paragraph("KEY PERFORMANCE INDICATORS", heading_style))
    
    summary_data = [
        ['Metric', 'Value', 'Insight'],
        ['Total Inventory Items', f"{stats['total_items']:,}", 'Complete product range'],
        ['Priced Items', f"{stats['priced_items']:,}", f"{priced_pct:.1f}% coverage"],
        ['Buying Investment (Priced)', f"KES {stats['priced_buying_value']:,.2f}", 'Capital deployed'],
        ['Projected Selling Value', f"KES {stats['priced_selling_value']:,.2f}", 'Revenue potential'],
        ['Gross Profit Projection', f"KES {stats['projected_profit']:,.2f}", f"{stats['roi_percentage']:.1f}% ROI"],
        ['Weighted Average Margin', f"{stats['overall_margin']:.2f}%", 'Blended profitability'],
    ]
    
    summary_table = Table(summary_data, colWidths=[2.2*inch, 2*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))
    
    # Price Segment Analysis
    elements.append(Paragraph("INVENTORY SEGMENTATION BY PRICE POINT", heading_style))
    
    segment_narrative = """Understanding our inventory distribution across price segments reveals strategic opportunities 
    for targeted marketing and inventory management. Each segment requires distinct approaches to pricing, promotion, and customer engagement."""
    elements.append(Paragraph(segment_narrative, story_style))
    elements.append(Spacer(1, 10))
    
    segment_data = [['Price Segment', 'Item Count', 'Buying Value', 'Selling Value', 'Profit', 'Avg Margin']]
    
    for segment_name, segment_stats in stats['price_segments'].items():
        if segment_stats['count'] > 0:
            profit = segment_stats['selling'] - segment_stats['buying']
            avg_margin = (profit / segment_stats['buying'] * 100) if segment_stats['buying'] > 0 else 0
            segment_data.append([
                segment_name,
                f"{segment_stats['count']:,}",
                f"{segment_stats['buying']:,.0f}",
                f"{segment_stats['selling']:,.0f}",
                f"{profit:,.0f}",
                f"{avg_margin:.1f}%"
            ])
    
    segment_table = Table(segment_data, colWidths=[1.3*inch, 0.9*inch, 1.2*inch, 1.2*inch, 1*inch, 0.9*inch])
    segment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16a085')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(segment_table)
    elements.append(Spacer(1, 20))
    
    # Margin Distribution
    elements.append(PageBreak())
    elements.append(Paragraph("MARGIN DISTRIBUTION ANALYSIS", heading_style))
    
    margin_narrative = """Our margin distribution reflects a balanced pricing strategy that accommodates various 
    product categories and competitive dynamics. The concentration of items in specific margin bands indicates 
    strategic positioning relative to market conditions and product characteristics."""
    elements.append(Paragraph(margin_narrative, story_style))
    elements.append(Spacer(1, 10))
    
    margin_data = [['Margin Range', 'Item Count', 'Percentage', 'Strategy Rationale']]
    
    margin_insights = {
        '0-10%': 'Competitive bulk items (cement, steel, paints)',
        '10-20%': 'High-value items & branded products',
        '20-30%': 'Balanced profitability items',
        '30-40%': 'Specialty & mid-range products',
        '40-50%': 'Premium margin items',
        '50%+': 'Low-cost high-margin accessories'
    }
    
    for range_name, count in stats['margin_distribution'].items():
        percentage = (count / stats['priced_items'] * 100) if stats['priced_items'] > 0 else 0
        insight = margin_insights.get(range_name, '')
        margin_data.append([range_name, f"{count:,}", f"{percentage:.1f}%", insight])
    
    margin_table = Table(margin_data, colWidths=[1.1*inch, 1*inch, 1*inch, 3.2*inch])
    margin_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2980b9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (2, -1), 'LEFT'),
        ('ALIGN', (1, 1), (2, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(margin_table)
    elements.append(Spacer(1, 20))
    
    # Category-by-Category Analysis
    elements.append(PageBreak())
    elements.append(Paragraph("CATEGORY PERFORMANCE ANALYSIS", heading_style))
    
    category_narrative = """Each product category exhibits unique margin characteristics based on market dynamics, 
    competition levels, and product nature. This analysis identifies top performers and areas requiring attention."""
    elements.append(Paragraph(category_narrative, story_style))
    elements.append(Spacer(1, 10))
    
    category_data = [['Category', 'Items', 'Projected Profit', 'Wtd Margin', 'Min-Max Range']]
    
    # Sort categories by projected profit (descending)
    sorted_categories = sorted(stats['categories'].items(), key=lambda x: x[1]['projected_profit'], reverse=True)
    
    for category_name, cat_stats in sorted_categories:
        if cat_stats['priced_count'] > 0:
            margin_range = f"{cat_stats['min_margin']:.0f}-{cat_stats['max_margin']:.0f}%"
            category_data.append([
                category_name[:25],  # Truncate long names
                f"{cat_stats['priced_count']}/{cat_stats['item_count']}",
                f"{cat_stats['projected_profit']:,.0f}",
                f"{cat_stats['weighted_margin']:.1f}%",
                margin_range
            ])
    
    category_table = Table(category_data, colWidths=[2.2*inch, 0.8*inch, 1.3*inch, 1*inch, 1.2*inch])
    category_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(category_table)
    elements.append(Spacer(1, 20))
    
    # Top and Bottom Performers
    elements.append(Paragraph("CATEGORY HIGHLIGHTS", subheading_style))
    
    if len(sorted_categories) >= 3:
        top_3 = sorted_categories[:3]
        elements.append(Paragraph("<b>Top Revenue Contributors:</b>", body_style))
        for i, (cat_name, cat_stats) in enumerate(top_3, 1):
            elements.append(Paragraph(
                f"{i}. <b>{cat_name}</b>: KES {cat_stats['projected_profit']:,.0f} profit "
                f"({cat_stats['weighted_margin']:.1f}% margin, {cat_stats['priced_count']} items)",
                body_style
            ))
        elements.append(Spacer(1, 12))
    
    # Find highest margin categories
    high_margin_cats = [(n, s) for n, s in stats['categories'].items() if s['weighted_margin'] > 25 and s['priced_count'] > 5]
    high_margin_cats.sort(key=lambda x: x[1]['weighted_margin'], reverse=True)
    
    if high_margin_cats:
        elements.append(Paragraph("<b>High-Margin Categories (>25%):</b>", body_style))
        for cat_name, cat_stats in high_margin_cats[:5]:
            elements.append(Paragraph(
                f"• <b>{cat_name}</b>: {cat_stats['weighted_margin']:.1f}% margin, "
                f"KES {cat_stats['projected_profit']:,.0f} profit potential",
                body_style
            ))
        elements.append(Spacer(1, 12))
    
    # Find low margin but high volume categories
    bulk_cats = [(n, s) for n, s in stats['categories'].items() if s['weighted_margin'] < 15 and s['total_selling'] > 50000]
    bulk_cats.sort(key=lambda x: x[1]['total_selling'], reverse=True)
    
    if bulk_cats:
        elements.append(Paragraph("<b>Strategic Bulk Categories (Low margin, high volume):</b>", body_style))
        for cat_name, cat_stats in bulk_cats[:5]:
            elements.append(Paragraph(
                f"• <b>{cat_name}</b>: {cat_stats['weighted_margin']:.1f}% margin, "
                f"KES {cat_stats['total_selling']:,.0f} selling value (Competitive driver)",
                body_style
            ))
    
    elements.append(Spacer(1, 20))
    
    # Pricing Logic Explanation
    elements.append(PageBreak())
    elements.append(Paragraph("PRICING METHODOLOGY & STRATEGY", heading_style))
    
    logic_intro = """Our pricing framework employs a multi-tiered approach combining fixed margins, sliding scales, 
    and category-specific rules. This methodology ensures optimal profitability while maintaining competitive positioning 
    across all product segments."""
    elements.append(Paragraph(logic_intro, story_style))
    elements.append(Spacer(1, 12))
    
    logic_sections = [
        {
            'title': '1. SLIDING MARGIN STRATEGY',
            'description': """Most categories utilize a dynamic sliding margin approach where margins decrease as 
            buying prices increase. This ensures affordability on high-value items while maximizing returns on 
            lower-cost products. The formula applies exponential smoothing to create natural price curves.""",
            'formula': 'Margin = Max_Margin - (Price_Ratio^Exponent × Margin_Range)'
        },
        {
            'title': '2. ELECTRICALS - 8-TIER PRICING SYSTEM',
            'description': """Electrical items employ a sophisticated 8-tier system optimized for competitiveness 
            and profitability. Recent adjustments increased margins from overly aggressive levels to balanced ranges.""",
            'tiers': [
                'Low Cost (<10 KES): 18-36% sliding margins - High margins on accessories',
                'Gap Tier (10-20 KES): 20% fixed margin - Standardized small items',
                'Mid Low (20-50 KES): 18-20% sliding margins - Balanced pricing',
                'Gap Tier (50-90 KES): 18% fixed margin - Consistent mid-range',
                'Mid Avg (90-250 KES): 15-18% sliding margins - Competitive positioning',
                'Mid High (250-800 KES): 12-15% sliding margins - Premium items',
                'Gap Tier (800-1000 KES): 12% fixed margin - High-value consistency',
                'High Value (>1000 KES): 8-12% sliding margins - Market competitive'
            ]
        },
        {
            'title': '3. COMMODITY CATEGORIES',
            'description': """Bulk building materials operate on thin margins due to intense market competition 
            and price transparency. These categories drive foot traffic and establish market credibility.""",
            'rules': [
                'Paints: 8.9-10% margins (Highly competitive market)',
                'Cement: 6% fixed margin (Bulk commodity pricing)',
                'Steel Products: 6-8% margins (Heavy construction materials)',
                'Concrete & Yard: 15-19% margins (Specialty materials)'
            ]
        },
        {
            'title': '4. SPECIALTY CATEGORIES',
            'description': """Categories with unique market positioning or lower competition support higher margins.""",
            'rules': [
                'Agricultural Tools: 30-40% margins (Seasonal specialty)',
                'Jua Kali Products: 10-25% margins (Local manufacturing)',
                'Timber Products: 15-28% sliding margins (Value-added processing)',
                'Tiles & Accessories: 15-30% margins (Design premium)',
                'Glassware: 20% fixed margin (Fragile handling premium)'
            ]
        },
        {
            'title': '5. BRANDED PRODUCTS',
            'description': """Premium brands command moderate margins while maintaining perceived value.""",
            'special': [
                'Bosch/DeWalt/Stanley Tools: 15-20% sliding margins',
                'Branded Tools (104 items): Quality positioning premium'
            ]
        },
        {
            'title': '6. PRICE ROUNDING POLICY',
            'description': """All selling prices round up to the nearest 5 KES for: (a) Customer convenience, 
            (b) Reduced cash handling complexity, (c) Professional price presentation."""
        }
    ]
    
    for section in logic_sections:
        elements.append(Paragraph(section['title'], subheading_style))
        elements.append(Paragraph(section['description'], body_style))
        
        if 'formula' in section:
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"<i>{section['formula']}</i>", body_style))
        
        if 'tiers' in section:
            elements.append(Spacer(1, 6))
            for tier in section['tiers']:
                elements.append(Paragraph(f"• {tier}", body_style))
        
        if 'rules' in section:
            elements.append(Spacer(1, 6))
            for rule in section['rules']:
                elements.append(Paragraph(f"• {rule}", body_style))
        
        if 'special' in section:
            elements.append(Spacer(1, 6))
            for special in section['special']:
                elements.append(Paragraph(f"• {special}", body_style))
        
        elements.append(Spacer(1, 12))
    
    # Strategic Insights
    elements.append(PageBreak())
    elements.append(Paragraph("STRATEGIC INSIGHTS & DATA STORY", heading_style))
    
    insights = []
    
    # Find highest and lowest margin categories
    priced_cats = {k: v for k, v in stats['categories'].items() if v['weighted_margin'] > 0 and v['priced_count'] > 0}
    if priced_cats:
        highest_margin_cat = max(priced_cats.items(), key=lambda x: x[1]['weighted_margin'])
        lowest_margin_cat = min(priced_cats.items(), key=lambda x: x[1]['weighted_margin'])
        highest_profit_cat = max(priced_cats.items(), key=lambda x: x[1]['projected_profit'])
        
        insights.append({
            'title': 'MARGIN LEADERSHIP',
            'text': f"<b>{highest_margin_cat[0]}</b> leads with a weighted margin of {highest_margin_cat[1]['weighted_margin']:.1f}%, "
                   f"generating KES {highest_margin_cat[1]['projected_profit']:,.0f} in projected profit from "
                   f"{highest_margin_cat[1]['priced_count']} items. This category represents an opportunity for "
                   f"premium positioning and should be promoted prominently."
        })
        
        insights.append({
            'title': 'VOLUME DRIVER',
            'text': f"<b>{lowest_margin_cat[0]}</b> operates at {lowest_margin_cat[1]['weighted_margin']:.1f}% margin, "
                   f"representing our competitive positioning strategy. These low-margin categories attract customers "
                   f"and establish market credibility, creating opportunities for cross-selling higher-margin items."
        })
        
        if highest_profit_cat[0] != highest_margin_cat[0]:
            insights.append({
                'title': 'PROFIT POWERHOUSE',
                'text': f"<b>{highest_profit_cat[0]}</b> delivers the highest absolute profit at "
                       f"KES {highest_profit_cat[1]['projected_profit']:,.0f} "
                       f"({highest_profit_cat[1]['weighted_margin']:.1f}% margin), demonstrating that volume "
                       f"can be as important as margin percentage. Focus on inventory availability for this category."
            })
    
    # Pricing coverage insight
    priced_pct = (stats['priced_items'] / stats['total_items'] * 100) if stats['total_items'] > 0 else 0
    insights.append({
        'title': 'PRICING COVERAGE',
        'text': f"We have successfully priced {stats['priced_items']:,} items ({priced_pct:.1f}% of inventory), "
               f"representing KES {stats['priced_buying_value']:,.2f} in capital deployment. Our {stats['roi_percentage']:.2f}% "
               f"ROI on priced inventory indicates healthy profitability. The remaining {stats['unpriced_items']} unpriced items "
               f"(primarily electricals and branded tools) use external market pricing."
    })
    
    # Segment insight
    low_segment = stats['price_segments']['Low (<100)']
    premium_segment = stats['price_segments']['Premium (2000+)']
    if low_segment['count'] > 0 and premium_segment['count'] > 0:
        low_margin = ((low_segment['selling'] - low_segment['buying']) / low_segment['buying'] * 100) if low_segment['buying'] > 0 else 0
        premium_margin = ((premium_segment['selling'] - premium_segment['buying']) / premium_segment['buying'] * 100) if premium_segment['buying'] > 0 else 0
        
        insights.append({
            'title': 'SEGMENT DYNAMICS',
            'text': f"Our inventory spans from low-cost accessories ({low_segment['count']} items at {low_margin:.1f}% margin) "
                   f"to premium products ({premium_segment['count']} items at {premium_margin:.1f}% margin). "
                   f"This balanced portfolio allows us to serve diverse customer segments while maintaining overall profitability."
        })
    
    # Electrical pricing insight
    elec_cat = stats['categories'].get('ELECTRICALS', None)
    if elec_cat and elec_cat['priced_count'] > 0:
        insights.append({
            'title': 'ELECTRICALS STRATEGY',
            'text': f"The electrical category ({elec_cat['priced_count']} items) operates at "
                   f"{elec_cat['weighted_margin']:.1f}% weighted margin after recent optimization. "
                   f"Previous adjustments reduced margins from excessive levels (65-130%) to competitive rates (8-36%), "
                   f"then increased to current balanced levels. This iterative approach ensures market competitiveness "
                   f"while maintaining viability. Projected profit: KES {elec_cat['projected_profit']:,.0f}."
        })
    
    for insight in insights:
        elements.append(Paragraph(insight['title'], subheading_style))
        elements.append(Paragraph(insight['text'], story_style))
        elements.append(Spacer(1, 12))
    
    elements.append(Spacer(1, 20))
    
    # Strategic Recommendations
    elements.append(PageBreak())
    elements.append(Paragraph("STRATEGIC RECOMMENDATIONS", heading_style))
    
    recommendations = [
        {
            'category': 'PRICING OPTIMIZATION',
            'items': [
                'Monitor competitor pricing weekly for cement, steel, and paints (bulk categories)',
                'Review electrical margins quarterly - market is dynamic and requires regular adjustment',
                'Consider dynamic pricing for high-volume categories based on supplier cost fluctuations',
                'Test 5-10% margin increases on specialty items with low competition'
            ]
        },
        {
            'category': 'INVENTORY MANAGEMENT',
            'items': [
                f"Prioritize stock availability for top 3 profit categories: {', '.join([c[0] for c in sorted_categories[:3]])}",
                'Implement fast-moving item tracking for sub-KES 100 items (high volume, high turnover)',
                'Review slow-moving items in premium segment (>KES 2000) for potential markdown or bundle strategies',
                'Maintain 30-day buffer stock for bulk commodities (cement, steel) to capitalize on demand spikes'
            ]
        },
        {
            'category': 'SALES & MARKETING',
            'items': [
                'Promote high-margin categories (>25% margin) through in-store displays and staff incentives',
                'Bundle low-margin items with high-margin accessories to improve transaction profitability',
                'Create seasonal campaigns for agricultural tools and concrete/yard products',
                'Develop loyalty programs focused on repeat purchases in commodity categories'
            ]
        },
        {
            'category': 'COMPETITIVE POSITIONING',
            'items': [
                'Use bulk categories (6-10% margin) as loss leaders to drive foot traffic',
                'Maintain price parity on branded tools (Bosch/DeWalt/Stanley) to preserve brand perception',
                'Differentiate on service, availability, and bundled solutions rather than price alone',
                'Monitor market entry of new competitors and adjust electrical pricing accordingly'
            ]
        },
        {
            'category': 'FINANCIAL PLANNING',
            'items': [
                f"Target gross profit of KES {stats['projected_profit']:,.0f} based on current pricing",
                f"Allocate working capital prioritizing categories with ROI above {stats['roi_percentage']:.1f}%",
                'Track actual vs. projected margins monthly to refine pricing algorithms',
                'Build cash flow buffer for bulk inventory purchases (cement, steel) during off-peak seasons'
            ]
        }
    ]
    
    for rec in recommendations:
        elements.append(Paragraph(rec['category'], subheading_style))
        for item in rec['items']:
            elements.append(Paragraph(f"• {item}", body_style))
            elements.append(Spacer(1, 4))
        elements.append(Spacer(1, 12))
    
    # Conclusion
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("CONCLUSION", heading_style))
    
    conclusion = f"""This pricing strategy represents a carefully balanced approach to market competitiveness and 
    business profitability. With {stats['priced_items']:,} items priced across 24 categories and a projected gross 
    profit of KES {stats['projected_profit']:,.0f} ({stats['roi_percentage']:.1f}% ROI), we have established a 
    solid foundation for sustainable growth.<br/><br/>
    
    The key to success lies in continuous monitoring, agile adjustments, and strategic focus on both high-margin 
    specialty items and volume-driving bulk categories. Our tiered pricing approach, particularly the refined 8-tier 
    electrical system, demonstrates sophistication in balancing complex market dynamics.<br/><br/>
    
    Moving forward, emphasis should be placed on inventory optimization for top profit categories, competitive 
    monitoring of bulk commodities, and strategic marketing of high-margin products. By treating pricing as a 
    dynamic tool rather than a static formula, we position ourselves for both immediate profitability and 
    long-term market leadership."""
    
    elements.append(Paragraph(conclusion, story_style))
    
    # Build PDF
    doc.build(elements)

def main():
    output_pdf = 'breakdown_pricing.pdf'
    
    print(f"Generating comprehensive pricing strategy report...")
    try:
        generate_pricing_logic_report(output_pdf)
        print(f"✓ Report generated successfully: {output_pdf}")
    except Exception as e:
        print(f"✗ Failed to generate report: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
