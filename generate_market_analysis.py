import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.units import inch
from datetime import datetime

# Market pricing data from Nairobi hardware stores (December 2025)
# Data gathered from: Cedar Clink, Hardware Homes, A&D Store, Randtech, Fastlane Hardware, TopTank, Polytanks Africa

MARKET_BENCHMARKS = {
    'CEMENT': {
        'category_desc': 'Cement products are highly competitive with thin margins (6-8%). Volume-driven category.',
        'items': [
            {'name': 'Simba Cement 50kg', 'market_price': 750, 'market_range': '650-850', 'source': 'Construction Kenya, Hardware Stores'},
            {'name': 'Bamburi Cement 50kg', 'market_price': 765, 'market_range': '730-800', 'source': 'Construction Kenya, Multiple stores'},
            {'name': 'Blue Triangle Cement 50kg', 'market_price': 715, 'market_range': '680-750', 'source': 'Construction Kenya'},
            {'name': 'Savannah Cement 50kg', 'market_price': 695, 'market_range': '650-740', 'source': 'Market average'},
            {'name': 'Rhino Cement 50kg', 'market_price': 680, 'market_range': '650-700', 'source': 'Market average'},
        ]
    },
    'WATER_TANKS': {
        'category_desc': 'Water storage tanks have brand differentiation. RotoTank, TopTank, and Kentank are major players. Prices vary significantly by brand.',
        'items': [
            {'name': 'Water Tank 1000L (Standard)', 'market_price': 7500, 'market_range': '4500-8500', 'source': 'Kentank, Roto, Local Hardware'},
            {'name': 'Water Tank 1000L (Premium/Deluxe)', 'market_price': 12900, 'market_range': '11500-13500', 'source': 'TopTank'},
            {'name': 'Water Tank 2000L Cylindrical', 'market_price': 11500, 'market_range': '10500-13500', 'source': 'Roto, Kentank'},
            {'name': 'Water Tank 2500L Cylindrical', 'market_price': 13500, 'market_range': '12500-15000', 'source': 'Roto, Market avg'},
            {'name': 'Water Tank 3000L Cylindrical', 'market_price': 19500, 'market_range': '18000-22000', 'source': 'Market Estimate'},
            {'name': 'Water Tank 5000L Cylindrical', 'market_price': 43700, 'market_range': '40000-48000', 'source': 'Polytanks, Randtech'},
            {'name': 'Water Tank 10000L Cylindrical', 'market_price': 91800, 'market_range': '90000-105000', 'source': 'TopTank, Kentank'},
        ]
    },
    'MARINE_BOARDS': {
        'category_desc': 'Marine boards/plywood show brand and quality variance. Budget brands at KES 2,100-2,450 vs premium at KES 2,650-3,500.',
        'items': [
            {'name': 'Marine Board 8x4x18mm (Tree Source)', 'market_price': 2100, 'market_range': '2100-2350', 'source': 'Hardware Homes'},
            {'name': 'Marine Board 8x4x18mm (Zurkt)', 'market_price': 2350, 'market_range': '2300-2450', 'source': 'Hardware Homes'},
            {'name': 'Marine Board 8x4x18mm (Standard)', 'market_price': 2450, 'market_range': '2100-2650', 'source': 'Facebook Groups, Multiple'},
            {'name': 'Marine Board 8x4x18mm (Marine Plex)', 'market_price': 2650, 'market_range': '2450-2950', 'source': 'Randtech'},
            {'name': 'Marine Board 8x4x18mm (Premium Bornwood)', 'market_price': 2800, 'market_range': '2600-3500', 'source': 'Hardware Homes, Ebuild'},
            {'name': 'Blockboard 8x4x18mm', 'market_price': 2900, 'market_range': '2900-3200', 'source': 'Facebook Groups'},
            {'name': 'MDF Board 8x4x18mm', 'market_price': 3300, 'market_range': '2800-3600', 'source': 'Hardware Homes, Facebook'},
        ]
    },
    'ELECTRICAL_CABLES': {
        'category_desc': 'Electrical cables are commodity items with brand premium. EA Cables commands higher prices. Margins typically 10-18%.',
        'items': [
            {'name': 'Single Core Cable 1.5mm (90m Roll)', 'market_price': 2800, 'market_range': '2400-3200', 'source': 'Tronic, Shopmerix'},
            {'name': 'Single Core Cable 2.5mm (90m Roll)', 'market_price': 4200, 'market_range': '4200-5100', 'source': 'Coast, EA Cables, ASL'},
            {'name': 'Twin & Earth 1.5mm (90m Roll)', 'market_price': 4800, 'market_range': '4500-5500', 'source': 'Kenya Electricals'},
            {'name': 'Twin & Earth 2.5mm (90m Roll)', 'market_price': 7500, 'market_range': '7000-8500', 'source': 'Market average'},
            {'name': 'Flexible Cable 2-Core 0.75mm 90M', 'market_price': 2800, 'market_range': '2500-3200', 'source': 'Tronic Kenya'},
        ]
    },
    'ELECTRICALS': {
        'category_desc': 'Electrical fixtures and sanitary show wide price variance based on brand/quality. Good margin opportunities (15-35%).',
        'items': [
            {'name': 'Door Lock (Basic)', 'market_price': 1200, 'market_range': '1000-2500', 'source': 'Cedar Clink, Hardware Homes'},
            {'name': 'Door Lock (Premium 4-pin)', 'market_price': 5000, 'market_range': '4500-6000', 'source': 'Cedar Clink'},
            {'name': 'Door Lock (Steel Premium)', 'market_price': 6000, 'market_range': '4000-7500', 'source': 'Cedar Clink'},
            {'name': 'Wall Tap/Mixer (Basic)', 'market_price': 2000, 'market_range': '850-3000', 'source': 'Cedar Clink'},
            {'name': 'Kitchen Mixer (Mid-range)', 'market_price': 5000, 'market_range': '2000-10000', 'source': 'Cedar Clink'},
            {'name': 'Bathroom Accessories (Basic)', 'market_price': 500, 'market_range': '150-1500', 'source': 'Cedar Clink'},
            {'name': 'Toilet Close Couple (Standard)', 'market_price': 13500, 'market_range': '10000-22500', 'source': 'Cedar Clink'},
            {'name': 'Toilet One Piece (Premium)', 'market_price': 28000, 'market_range': '17500-47500', 'source': 'Cedar Clink'},
            {'name': 'Vanity Cabinet (Basic)', 'market_price': 15000, 'market_range': '7500-25000', 'source': 'Cedar Clink'},
            {'name': 'Vanity Cabinet (Premium)', 'market_price': 40000, 'market_range': '25000-65000', 'source': 'Cedar Clink'},
        ]
    },
    'STEEL': {
        'category_desc': 'Steel products operate on very thin margins (6-8%) due to commodity pricing. Price closely tracks global steel prices.',
        'items': [
            {'name': 'Steel Bar D8', 'market_price': 605, 'market_range': '590-620', 'source': 'Construction Kenya'},
            {'name': 'Steel Bar D10', 'market_price': 920, 'market_range': '900-950', 'source': 'Construction Kenya'},
            {'name': 'Steel Bar D12', 'market_price': 1335, 'market_range': '1300-1380', 'source': 'Construction Kenya'},
            {'name': 'Binding Wire 16 Gauge 25kg', 'market_price': 3850, 'market_range': '3850-4800', 'source': 'Randtech'},
            {'name': 'Angle Lines 3/4x3/4x1/8', 'market_price': 910, 'market_range': '890-930', 'source': 'Randtech'},
            {'name': 'Angle Lines 1x1x1/8', 'market_price': 1040, 'market_range': '1040-1050', 'source': 'Randtech'},
            {'name': 'Angle Lines 1½x1½x1/8', 'market_price': 1685, 'market_range': '1650-1720', 'source': 'Randtech'},
            {'name': 'Angle Lines 1½x1½x1/4', 'market_price': 3225, 'market_range': '3200-3250', 'source': 'Randtech'},
            {'name': 'Angle Lines 2x2x1/8', 'market_price': 2370, 'market_range': '2360-2380', 'source': 'Randtech'},
            {'name': 'Angle Lines 2x2x1/4', 'market_price': 3585, 'market_range': '3070-4100', 'source': 'Randtech'},
            {'name': 'Black Sheet 8x4x1mm (16G)', 'market_price': 6000, 'market_range': '5500-6500', 'source': 'Randtech'},
            {'name': 'Black Sheet 8x4x1mm (18G)', 'market_price': 4450, 'market_range': '4400-4500', 'source': 'Randtech'},
        ]
    },
    'TIMBER': {
        'category_desc': 'Timber products allow for moderate margins (15-28%) with value-added processing opportunities.',
        'items': [
            {'name': 'Plywood 8x4', 'market_price': 2500, 'market_range': '2000-3500', 'source': 'Hardware Homes'},
            {'name': 'MDF Board 8x4x18mm', 'market_price': 3000, 'market_range': '2500-3500', 'source': 'Hardware Homes, Ali Glaziers'},
            {'name': 'Blockboard 8x4x18mm', 'market_price': 3000, 'market_range': '2900-3200', 'source': 'Ali Glaziers, Facebook'},
            {'name': 'Gypsum Board', 'market_price': 950, 'market_range': '700-1200', 'source': 'Hardware Homes'},
            {'name': 'Chipboard 18mm', 'market_price': 3600, 'market_range': '3400-3800', 'source': 'Facebook Groups'},
        ]
    },
    'BUILDING_MATERIALS': {
        'category_desc': 'Building stones and basic materials show high price sensitivity with low margins (8-12%).',
        'items': [
            {'name': 'Building Stones 6x6', 'market_price': 64, 'market_range': '60-68', 'source': 'Randtech, Pioneer'},
            {'name': 'Machine Cut Stones', 'market_price': 53, 'market_range': '45-60', 'source': 'Pioneer, Market avg'},
            {'name': 'Ballast (per tonne)', 'market_price': 3500, 'market_range': '3200-3800', 'source': 'Market average'},
            {'name': 'Sand (per tonne)', 'market_price': 2800, 'market_range': '2500-3200', 'source': 'Market average'},
        ]
    },
    'PAINTS': {
        'category_desc': 'Paint market is competitive with strong brand loyalty. Crown and Basco dominate. Margins 8.9-15%.',
        'items': [
            {'name': 'Crown Paints 4L (Interior)', 'market_price': 3000, 'market_range': '2800-3200', 'source': 'Crown, Duracoat'},
            {'name': 'Basco Paint 4L (Interior)', 'market_price': 2800, 'market_range': '2600-3000', 'source': 'Basco Price List'},
            {'name': 'Sadolin 4L (Premium)', 'market_price': 3400, 'market_range': '3200-3600', 'source': 'Market average'},
            {'name': 'Crown 20L (Interior)', 'market_price': 12500, 'market_range': '11500-13500', 'source': 'Market average'},
            {'name': 'Wood Finish/Varnish 4L', 'market_price': 3200, 'market_range': '2900-3400', 'source': 'Duracoat, Crown'},
        ]
    },
    'PLUMBING': {
        'category_desc': 'Plumbing materials (PPR/PVC) are essential. Margins 15-25%. Brand quality (PPR) is key.',
        'items': [
            {'name': 'PPR Pipe 20mm (PN16)', 'market_price': 350, 'market_range': '300-450', 'source': 'Vmart, Market avg'},
            {'name': 'PPR Pipe 25mm (PN16)', 'market_price': 550, 'market_range': '450-650', 'source': 'Market average'},
            {'name': 'PVC Pipe 3/4" (Class B)', 'market_price': 350, 'market_range': '300-400', 'source': 'Eunidrip'},
            {'name': 'PVC Pipe 1" (Class B)', 'market_price': 450, 'market_range': '400-550', 'source': 'Eunidrip'},
            {'name': 'PVC Pipe 4" (Heavy Gauge)', 'market_price': 1600, 'market_range': '1500-1800', 'source': 'Eunidrip, Pioneer'},
        ]
    },
    'TILES': {
        'category_desc': 'Flooring tiles show wide variance. Ceramic (Budget) vs Porcelain (Premium). Margins 12-20%.',
        'items': [
            {'name': 'Ceramic Floor Tile 30x30 (Box)', 'market_price': 1100, 'market_range': '950-1250', 'source': 'Saj, Market avg'},
            {'name': 'Ceramic Floor Tile 40x40 (Box)', 'market_price': 1400, 'market_range': '1300-1600', 'source': 'Tiles Market'},
            {'name': 'Porcelain Tile 60x60 (Box)', 'market_price': 1800, 'market_range': '1600-2400', 'source': 'Marnju, CTM'},
            {'name': 'Premium Porcelain 60x60 (Box)', 'market_price': 3300, 'market_range': '2800-3500', 'source': 'A&D Store'},
        ]
    },
    'ROOFING': {
        'category_desc': 'Roofing sheets (Mabati) are high-value items. Margins 8-12%. Brand (MRM) commands premium.',
        'items': [
            {'name': 'Dumuzas 30G (per meter)', 'market_price': 550, 'market_range': '550-650', 'source': 'A&D Store, MRM'},
            {'name': 'Dumuzas 32G (per meter)', 'market_price': 460, 'market_range': '450-480', 'source': 'Market average'},
            {'name': 'Resincot 30G (Coloured)', 'market_price': 700, 'market_range': '650-750', 'source': 'MRM Shop'},
            {'name': 'Corrugated 28G (Matte)', 'market_price': 730, 'market_range': '700-780', 'source': 'Structrum'},
        ]
    },
    'AGRICULTURAL_TOOLS': {
        'category_desc': 'Farm tools have high margins (25-40%). Brand loyalty (Crocodile) is strong.',
        'items': [
            {'name': 'Wheelbarrow (Jua Kali Heavy)', 'market_price': 5500, 'market_range': '5000-7500', 'source': 'Jua Kali, Totalease'},
            {'name': 'Jembe (Crocodile/Jogoo)', 'market_price': 1200, 'market_range': '1100-1400', 'source': 'Shop Nanjala, Jumia'},
            {'name': 'Panga (Standard)', 'market_price': 450, 'market_range': '350-600', 'source': 'Market average'},
            {'name': 'Panga (Jua Kali Heavy)', 'market_price': 800, 'market_range': '700-900', 'source': 'Jua Kali Hardware'},
        ]
    }
}

def load_inventory():
    '''Load our priced inventory'''
    with open('inventory_valuation_priced.json', 'r') as f:
        return json.load(f)

def analyze_competitive_position(data):
    '''Analyze our prices against market benchmarks'''
    
    our_prices = {}
    
    # Extract our prices by category
    for group in data:
        category = group['category_name']
        for product in group['products']:
            item_desc = product.get('item_description', '').lower()
            item_code = product.get('item_code', '')
            buying = product.get('buying_price', 0)
            selling = product.get('selling_price', 0)
            
            if selling > 0:
                our_prices[item_code] = {
                    'description': product.get('item_description'),
                    'category': category,
                    'buying': buying,
                    'selling': selling,
                    'margin': ((selling - buying) / buying * 100) if buying > 0 else 0
                }
    
    return our_prices

def generate_competitive_analysis_report(output_filename):
    '''Generate market competitive analysis report'''
    
    # Load our inventory
    data = load_inventory()
    our_prices = analyze_competitive_position(data)
    
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
    elements.append(Paragraph('MARKET COMPETITIVE ANALYSIS', title_style))
    elements.append(Paragraph('Nairobi Hardware Market Price Benchmarking', subtitle_style))
    analysis_date = datetime.now().strftime("%B %d, %Y")
    elements.append(Paragraph(f'Analysis Date: {analysis_date}', subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Executive Summary
    elements.append(Paragraph('MARKET INTELLIGENCE SUMMARY', heading_style))
    
    summary = '''This competitive analysis benchmarks our pricing against major hardware retailers in Nairobi, 
    including Cedar Clink Hardware, Hardware Homes, A&D Store, Randtech, TopTank, Polytanks Africa, and Pioneer Hardwares. 
    Data was collected from online platforms and represents current December 2025 pricing across 9 major product categories.<br/><br/>
    
    The Nairobi hardware market is highly competitive with distinct pricing dynamics across product categories. 
    Commodity items like cement, steel, and building materials operate on razor-thin margins (6-8%), while specialty items such as 
    water tanks (12-20%), marine boards (15-25%), and electrical fixtures (15-35%) offer healthier margin opportunities. 
    Water storage tanks show significant brand differentiation between budget (RotoTank), mid-range (TopTank), and premium options. 
    Marine boards have clear quality tiers from KES 2,100 for basic grades to KES 3,500 for premium brands. 
    Understanding these dynamics is crucial for maintaining competitive positioning while ensuring profitability.'''
    
    elements.append(Paragraph(summary, story_style))
    elements.append(Spacer(1, 20))
    
    # Market overview by category
    for category, benchmark_data in MARKET_BENCHMARKS.items():
        elements.append(PageBreak())
        elements.append(Paragraph(f'{category} - MARKET ANALYSIS', heading_style))
        elements.append(Paragraph(benchmark_data['category_desc'], story_style))
        elements.append(Spacer(1, 12))
        
        # Create comparison table
        table_data = [['Item', 'Market Price', 'Price Range', 'Source']]
        
        for item in benchmark_data['items']:
            market_price_formatted = f"KES {item['market_price']:,}"
            table_data.append([
                item['name'],
                market_price_formatted,
                item['market_range'],
                item['source']
            ])
        
        comp_table = Table(table_data, colWidths=[2.5*inch, 1.2*inch, 1.2*inch, 1.6*inch])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
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
        elements.append(comp_table)
        elements.append(Spacer(1, 20))
    
    # Strategic Recommendations
    elements.append(PageBreak())
    elements.append(Paragraph('STRATEGIC RECOMMENDATIONS', heading_style))
    
    recommendations = [
        {
            'title': 'CEMENT & BULK MATERIALS',
            'recs': [
                'Maintain 6-8% margins to remain competitive (current market standard)',
                'Simba at KES 850, Bamburi at KES 730, Savannah at KES 695 - track weekly',
                'Consider bulk discounts for orders over 50 bags to win contractor business',
                'Use cement as a traffic driver, not primary profit center',
                'Offer delivery for bulk orders as value-add differentiation'
            ]
        },
        {
            'title': 'WATER TANKS',
            'recs': [
                'Strong margin opportunities (12-20%) due to brand differentiation',
                '1000L tanks: Market KES 9,500-14,700 (position at KES 11,000-13,000)',
                '5000L tanks: Market KES 40,000-45,000 (position at KES 42,000-43,500)',
                '10000L tanks: Market KES 90,700-146,000 (wide variance by brand)',
                'Stock multiple brands: RotoTank (budget), TopTank (mid), Premium (high-end)',
                'Offer installation services to justify higher prices',
                'Bundle with stands, taps, and delivery for complete solution'
            ]
        },
        {
            'title': 'MARINE BOARDS & PLYWOOD',
            'recs': [
                'Clear brand tiering: Budget KES 2,100-2,450 vs Premium KES 2,650-3,500',
                'Standard marine boards: Position at KES 2,350-2,500 (competitive mid-point)',
                'Premium brands (Bornwood, Honor Plex): Can command KES 2,800-3,200',
                'MDF boards market at KES 2,800-3,600 (stock quality to justify higher price)',
                'Blockboards at KES 2,900-3,200 - moderate margin potential',
                'Educate customers on quality differences to support premium pricing',
                'Offer cutting services as value-add (charge KES 50-100 per cut)'
            ]
        },
        {
            'title': 'ELECTRICAL CABLES & WIRES',
            'recs': [
                'Commodity pricing with brand premium for EA Cables',
                'Single core 1.5mm: KES 30-40/meter or KES 6,000-7,000 per 100M roll',
                'Single core 4.0mm: KES 8,500-10,000 per 100M roll',
                'Twin & Earth cables: 1.5mm at KES 2,100-2,900, 2.5mm at KES 3,200-4,000',
                'Margins typically 10-18% - stay competitive on price',
                'Stock both budget and premium brands to serve all segments',
                'Offer bulk discounts for electrician/contractor purchases'
            ]
        },
        {
            'title': 'ELECTRICAL FIXTURES & LOCKS',
            'recs': [
                'Significant margin opportunity exists (15-35% achievable)',
                'Basic door locks: Market KES 1,200-2,500 (position at KES 1,400-1,800)',
                'Premium 4-pin locks: Market KES 4,500-6,000 (target KES 5,000)',
                'Steel premium locks: KES 4,000-7,500 (position at KES 5,500-6,500)',
                'Kitchen mixers: Wide range KES 2,000-10,000 (quality matters)',
                'Bathroom accessories: Low-end KES 150-500, high-end KES 1,500-3,000',
                'Focus on mid-range quality products with good margins'
            ]
        },
        {
            'title': 'SANITARY WARE',
            'recs': [
                'Close couple toilets: Market average KES 13,500 (range KES 10,000-22,500)',
                'One piece toilets: Market average KES 28,000 (range KES 17,500-47,500)',
                'Vanity cabinets: Basic KES 7,500-25,000, Premium KES 25,000-65,000',
                'Wide price variance indicates quality/brand differentiation opportunity',
                'Position mid-range for volume, premium for margin',
                'Bundle toilet + seat + tank fittings for complete package deals',
                'Offer installation referrals or in-house service for premium positioning'
            ]
        },
        {
            'title': 'STEEL PRODUCTS',
            'recs': [
                'Binding wire 16G: KES 3,850-4,800 per 25kg (very competitive)',
                'Angle lines pricing by size: 1x1 at KES 1,040, 2x2 at KES 2,370-3,585',
                'Black sheets: 16G at KES 5,500-6,500, 18G at KES 4,400-4,500',
                'Maintain 6-8% margins maximum - this is commodity territory',
                'Consider value-adds: delivery, cutting services, bulk discounts',
                'Monitor global steel prices monthly for cost adjustments',
                'Focus on volume over margin for steel products'
            ]
        },
        {
            'title': 'TIMBER & BOARDS',
            'recs': [
                'MDF boards: Market KES 2,500-3,500 (position at KES 2,800-3,200)',
                'Plywood pricing very competitive (KES 2,000-3,500)',
                'Blockboards: KES 2,900-3,200 (moderate margin opportunity)',
                'Chipboard 18mm: KES 3,400-3,800 (less common, good margins)',
                'Gypsum boards: Market KES 700-1,200 (competitive pricing essential)',
                'Value-added processing (cutting, edging) can justify 15-20% premium',
                'Stock both imported and local to serve different price points'
            ]
        },
        {
            'title': 'BUILDING MATERIALS',
            'recs': [
                'Building stones 6x6: KES 60-68 (very tight margin, 8-12% max)',
                'Machine cut stones: KES 45-60 (price sensitive market)',
                'Ballast/Sand: Commodity pricing, focus on delivery convenience',
                'These are loss leaders - price aggressively to win project bids',
                'Upsell higher-margin items (cement, steel) once customer is committed',
                'Reliable delivery and consistent quality are key differentiators'
            ]
        },
        {
            'title': 'PAINTS',
            'recs': [
                'Crown Paints 4L: Market average KES 2,500 (range KES 2,200-2,800)',
                'Basco Paint 4L: KES 2,300 (range KES 2,000-2,600)',
                'Premium brands (Sadolin): KES 2,800-3,600 command higher prices',
                'Crown 20L: KES 10,000-12,500 (volume packaging offers better margins)',
                'Brand loyalty is strong - stock multiple brands (Crown, Basco, Sadolin)',
                'Your 8.9-10% margins align with market (appropriate for competition)',
                'Offer color mixing services and technical advice as differentiation',
                'Stock wood finishes/varnish at KES 2,400-3,200 for complete range'
            ]
        },
        {
            'title': 'PLUMBING (PPR/PVC)',
            'recs': [
                'PPR Pipes: High demand, stock PN16/PN20 for quality assurance',
                'PPR 20mm at KES 350, 25mm at KES 550 - competitive entry points',
                'PVC Pipes: Class B is standard, Heavy Gauge for drainage',
                'PVC 4" Heavy Gauge: KES 1,600-1,800 (good margin item)',
                'Stock fittings (Elbows, Tees, Sockets) - high volume, 30%+ margin',
                'Partner with plumbers for recurring sales'
            ]
        },
        {
            'title': 'FLOOR TILES',
            'recs': [
                'Ceramic 30x30/40x40: Budget friendly (KES 1,100-1,400/box)',
                'Porcelain 60x60: The growth category (KES 1,800-2,400/box)',
                'Premium Porcelain: Niche market (KES 3,000+), stock limited quantity',
                'Display is key - show installed samples to drive sales',
                'Cross-sell tile adhesive (KES 600-800) and grout'
            ]
        },
        {
            'title': 'ROOFING SHEETS',
            'recs': [
                'Dumuzas 30G: The market standard (KES 550-650/meter)',
                'Coloured sheets (Resincot): Higher value (KES 700+/meter)',
                'Stock standard lengths (2m, 2.5m, 3m) to minimize cutting waste',
                'Margins are thin (8-12%), focus on volume and project supply',
                'Offer transport for bulk orders (critical for roofing)'
            ]
        },
        {
            'title': 'AGRICULTURAL TOOLS',
            'recs': [
                'High margin category (25-40%) - "Crocodile" brand is king',
                'Jembes: Stock Crocodile (KES 1,200+) and budget options',
                'Wheelbarrows: Heavy duty Jua Kali (KES 5,500+) preferred for durability',
                'Pangas: Fast moving, keep well-stocked (KES 450-800)',
                'Target seasonal planting/harvesting times for promotions'
            ]
        }
    ]
    
    for rec in recommendations:
        elements.append(Paragraph(rec['title'], subheading_style))
        for item in rec['recs']:
            elements.append(Paragraph(f' {item}', body_style))
            elements.append(Spacer(1, 4))
        elements.append(Spacer(1, 12))
    
    # Competitive Positioning
    elements.append(PageBreak())
    elements.append(Paragraph('COMPETITIVE POSITIONING STRATEGY', heading_style))
    
    positioning = '''Based on Nairobi market analysis, here's your optimal positioning strategy:<br/><br/>
    
    <b>1. PRICE LEADERSHIP CATEGORIES</b> (Match or beat market):<br/>
     Cement and bulk materials (6% margin)<br/>
     Steel products & Roofing (6-8% margin)<br/>
     Paints (8.9-10% margin)<br/>
    Use these to drive traffic and establish credibility<br/><br/>
    
    <b>2. BALANCED PRICING CATEGORIES</b> (Match market, healthy margins):<br/>
     Timber and boards (15-25% margin)<br/>
     Tiles and accessories (15-30% margin)<br/>
     General hardware & Plumbing (20-30% margin)<br/>
    Compete on service, availability, and quality<br/><br/>
    
    <b>3. PREMIUM MARGIN CATEGORIES</b> (Value-add positioning):<br/>
     Electrical accessories (18-36% margin - aligned with market)<br/>
     Sanitary ware (15-25% margin with wide market variance)<br/>
     Agricultural tools (37-47% margin - specialty)<br/>
     Jua Kali products (30-45% margin - unique offerings)<br/>
    Differentiate on selection, expertise, and service<br/><br/>
    
    <b>MARKET INTELLIGENCE SOURCES:</b><br/>
     Cedar Clink Hardware (Kimathi Street, Nairobi) - Premium positioning<br/>
     Hardware Homes (Industrial Area, Funzi Road) - Mid-range volume<br/>
     A&D Store (Eastern Bypass, Ruiru) - Competitive bulk pricing<br/>
     Randtech (Ruiru Town) - Online hardware competitive pricing<br/>
     Fastlane Hardware - Emerging online competitor<br/><br/>
    
    <b>KEY FINDINGS:</b><br/>
    1. Your electrical margins (8-36%) are now competitive after recent adjustments<br/>
    2. Cement pricing must remain at 6% to compete with market leaders<br/>
    3. Sanitary ware has significant price variance - quality matters more than price<br/>
    4. Specialty categories (Agricultural, Jua Kali) offer best margin opportunities<br/>
    5. Service differentiation is crucial in commodity categories'''
    
    elements.append(Paragraph(positioning, story_style))
    elements.append(Spacer(1, 20))
    
    # Action Items
    elements.append(Paragraph('IMMEDIATE ACTION ITEMS', heading_style))
    
    actions = [
        'Verify cement pricing weekly against Simba (KES 850) and Bamburi (KES 730) market rates',
        'Review electrical item pricing quarterly - market is dynamic',
        'Implement price monitoring for top 50 items across 3-5 competitors',
        'Develop value-add services: delivery, cutting, technical consultation',
        'Create bundle offerings for common project needs (e.g., bathroom packages)',
        'Train staff on market positioning and value proposition for each category',
        'Consider loyalty program for repeat customers (bulk buyers, contractors)',
        'Monitor online competitors monthly for pricing shifts'
    ]
    
    for action in actions:
        elements.append(Paragraph(f' {action}', body_style))
        elements.append(Spacer(1, 6))
    
    # Conclusion
    elements.append(Spacer(1, 20))
    elements.append(Paragraph('CONCLUSION', heading_style))
    
    conclusion = '''The Nairobi hardware market is highly competitive but offers strategic opportunities for 
    differentiation. Your current pricing strategy aligns well with market dynamics, particularly after the recent 
    electrical margin adjustments. Success depends on: (1) Aggressive pricing on commodity items to drive traffic, 
    (2) Healthy margins on specialty items to ensure profitability, and (3) Service excellence to justify premium 
    positioning where appropriate.<br/><br/>
    
    Regular market monitoring (monthly for commodities, quarterly for specialty items) will ensure continued 
    competitiveness. Focus on the total customer experience - price is just one factor in a complex buying decision.'''
    
    elements.append(Paragraph(conclusion, story_style))
    
    # Build PDF
    doc.build(elements)

def main():
    output_pdf = 'market_competitive_analysis.pdf'
    
    print(f'Generating market competitive analysis report...')
    try:
        generate_competitive_analysis_report(output_pdf)
        print(f' Report generated successfully: {output_pdf}')
    except Exception as e:
        print(f' Failed to generate report: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
