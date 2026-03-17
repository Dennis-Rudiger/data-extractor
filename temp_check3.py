import json
def get_raw_out_by_item(files):
    items_out = {}
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data.get('items', []):
                code = item.get('code')
                items_out[code] = items_out.get(code, 0) + item.get('qty_out', 0)
    return items_out

def get_calc_out_by_item(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    items_out = {}
    for cat_name, cat_data in data.get('categories', {}).items():
        if 'products' in cat_data:
            for item in cat_data['products']:
                items_out[item['item_code']] = items_out.get(item['item_code'], 0) + item.get('qty_out', 0)
    return items_out

b_raw = get_raw_out_by_item(['stock_movement_jan.json', 'stock_movement_feb.json'])
b_calc = get_calc_out_by_item('bomas_average_moq.json')

for code in b_raw:
    c = b_calc.get(code, 0)
    if abs(b_raw[code] - c) > 0.001:
        print(f'{code!r}: raw={b_raw[code]} calc={c}')
