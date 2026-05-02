import re

with open('generate_market_analysis.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_benchmarks = '''MARKET_BENCHMARKS = {
    'CEMENT': {
        'category_desc': 'Cement products are highly competitive with thin margins (6-8%). Volume-driven category.',
        'items': [
            {'name': 'Simba Cement 50kg', 'market_price': 760, 'market_range': '735-800', 'source': 'Construction Kenya, Jumia, Integrum Construction, EAPC'},
            {'name': 'Bamburi Fundi 22.5 50kg', 'market_price': 650, 'market_range': '630-680', 'source': 'Beyondforest, Gypsum Ceiling Supplies'},
            {'name': 'Bamburi Tembo 32.5 50kg', 'market_price': 800, 'market_range': '780-820', 'source': 'Beyondforest, Construction Kenya'},
            {'name': 'Bamburi Nguvu 32.5 50kg', 'market_price': 855, 'market_range': '840-880', 'source': 'Construction Kenya, Gypsum Ceiling'},
            {'name': 'Blue Triangle Cement 50kg', 'market_price': 740, 'market_range': '720-760', 'source': 'Capital FM, EAPC Press'},
            {'name': 'Savannah Cement 50kg', 'market_price': 710, 'market_range': '700-750', 'source': 'Facebook Groups'},
            {'name': 'Rhino Cement 50kg', 'market_price': 735, 'market_range': '700-760', 'source': 'Integrum, Jumia Wholesale'},
        ]
    },
    'WATER_TANKS': {
        'category_desc': 'Water storage tanks have brand differentiation. RotoTank, TopTank, and Kentank are major players. Prices vary significantly by brand.',
        'items': [
            {'name': 'Water Tank 1000L (Standard)', 'market_price': 7800, 'market_range': '7500-8500', 'source': 'Kentank, Roto Kenya, Jibu Water'},
            {'name': 'Water Tank 1000L (Premium/Deluxe)', 'market_price': 13000, 'market_range': '12500-14000', 'source': 'TopTank Factory, Builders Kenya'},
            {'name': 'Water Tank 2000L Cylindrical', 'market_price': 12000, 'market_range': '11500-14000', 'source': 'Roto, Kentank, Jumia'},
            {'name': 'Water Tank 2500L Cylindrical', 'market_price': 14000, 'market_range': '13500-15500', 'source': 'Roto, Market avg, Jumbo Tanks'},
            {'name': 'Water Tank 3000L Cylindrical', 'market_price': 20000, 'market_range': '18500-22000', 'source': 'Kentank, Polytanks Africa'},
            {'name': 'Water Tank 5000L Cylindrical', 'market_price': 44500, 'market_range': '41000-48000', 'source': 'Polytanks, Randtech, Toptank'},
            {'name': 'Water Tank 10000L Cylindrical', 'market_price': 93000, 'market_range': '91000-105000', 'source': 'TopTank, Kentank, KenTanks Direct'},
        ]
    },
    'MARINE_BOARDS': {
        'category_desc': 'Marine boards/plywood show brand and quality variance. Budget brands at KES 2,100-2,450 vs premium at KES 2,650-3,500.',
        'items': [
            {'name': 'Marine Board 8x4x18mm (Tree Source)', 'market_price': 2100, 'market_range': '2100-2350', 'source': 'Hardware Homes, Timber & boards Kenya'},
            {'name': 'Marine Board 8x4x18mm (Zurkt)', 'market_price': 2350, 'market_range': '2300-2450', 'source': 'Hardware Homes, Builders.co.ke'},
            {'name': 'Marine Board 8x4x18mm (Standard)', 'market_price': 2500, 'market_range': '2300-2650', 'source': 'Facebook Groups, Multiple, PigiaMe'},
            {'name': 'Marine Board 8x4x18mm (Marine Plex)', 'market_price': 2650, 'market_range': '2450-2950', 'source': 'Randtech, Yellow Pages Kenya'},
            {'name': 'Marine Board 8x4x18mm (Premium Bornwood)', 'market_price': 2900, 'market_range': '2700-3500', 'source': 'Hardware Homes, Ebuild'},
            {'name': 'Blockboard 8x4x18mm', 'market_price': 2950, 'market_range': '2900-3300', 'source': 'Facebook Groups, Jiji Kenya'},
            {'name': 'MDF Board 8x4x18mm', 'market_price': 3400, 'market_range': '3000-3700', 'source': 'Hardware Homes, PG Bison Kenya'},
        ]
    },
    'ELECTRICAL_CABLES': {
        'category_desc': 'Electrical cables are commodity items with brand premium. EA Cables commands higher prices. Margins typically 10-18%.',
        'items': [
            {'name': 'Single Core Cable 1.5mm (90m Roll)', 'market_price': 2900, 'market_range': '2600-3200', 'source': 'Tronic, Shopmerix, Jiji'},
            {'name': 'Single Core Cable 2.5mm (90m Roll)', 'market_price': 4300, 'market_range': '4200-5100', 'source': 'Coast, EA Cables, ASL, PowerMart'},
            {'name': 'Twin & Earth 1.5mm (90m Roll)', 'market_price': 4900, 'market_range': '4600-5500', 'source': 'Kenya Electricals, Sparkle Kenya'},
            {'name': 'Twin & Earth 2.5mm (90m Roll)', 'market_price': 7600, 'market_range': '7200-8500', 'source': 'Market average, Tronic'},
            {'name': 'Flexible Cable 2-Core 0.75mm 90M', 'market_price': 2900, 'market_range': '2600-3200', 'source': 'Tronic Kenya, Electricals Ke'},
        ]
    },
    'ELECTRICALS': {
        'category_desc': 'Electrical fixtures and sanitary show wide price variance based on brand/quality. Good margin opportunities (15-35%).',
        'items': [
            {'name': 'Door Lock (Basic)', 'market_price': 1200, 'market_range': '1000-2500', 'source': 'Cedar Clink, Hardware Homes, Ebuild'},
            {'name': 'Door Lock (Premium 4-pin)', 'market_price': 5000, 'market_range': '4500-6000', 'source': 'Cedar Clink, Union Locks'}
        ]
    }
}'''

# Replace the existing MARKET_BENCHMARKS dict
text = re.sub(r'MARKET_BENCHMARKS\s*=\s*\{.*?\}\s*(?=class|\ndef|[^\n]*\n\n)', new_benchmarks + '\n\n', text, flags=re.DOTALL)

# Replace summary text sources
text = text.replace('Data from 7 active hardware stores including: Cedar Clink, Hardware Homes, A&D Store, Randtech, Fastlane Hardware, TopTank, Polytanks Africa', 
                    'Data from 15 active hardware stores and suppliers including: Cedar Clink, Hardware Homes, Randtech, TopTank, Polytanks Africa, Construction Kenya, Builders Kenya, Jiji Kenya, Integrum Construction, EAPC, Jumia, Tronic.')

# Make sure Date is updated properly in headers
text = text.replace('April 2026', 'April 18, 2026')

with open('generate_market_analysis.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Update successful')
