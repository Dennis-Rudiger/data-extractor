import pathlib
p = pathlib.Path('generate_moq_report.py')
content = p.read_text(encoding='utf-8')

old_code = '''def build_jan_feb_comparison():
    \"\"\"Compare January and February stock movement to identify trends.\"\"\"
    import os
    if not os.path.exists('stock_movement_jan.json') or not os.path.exists('stock_movement_feb.json'):
        return None

    with open('stock_movement_jan.json') as f:
        jan = json.load(f)
    with open('stock_movement_feb.json') as f:
        feb = json.load(f)'''

new_code = '''JAN_FILE = 'stock_movement_jan.json'
FEB_FILE = 'stock_movement_feb.json'

def build_jan_feb_comparison():
    \"\"\"Compare January and February stock movement to identify trends.\"\"\"
    import os
    if not os.path.exists(JAN_FILE) or not os.path.exists(FEB_FILE):
        return None

    with open(JAN_FILE, 'r', encoding='utf-8') as f:
        jan = json.load(f)
    with open(FEB_FILE, 'r', encoding='utf-8') as f:
        feb = json.load(f)'''

content = content.replace(old_code, new_code)
p.write_text(content, encoding='utf-8')
