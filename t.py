import json
def get_raw_out_by_item(files):
    items_out = {}
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data.get("items", []):
                code = item.get("code")
                if code is None:
                    continue
                items_out[code] = items_out.get(code, 0) + item.get("qty_out", 0)
    return items_out

def get_calc_out_by_item(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    items_out = {}
    for cat_name, cat_data in data.get("categories", {}).items():
        if "products" in cat_data:
            for item in cat_data["products"]:
                items_out[item["item_code"]] = items_out.get(item["item_code"], 0) + item.get("qty_out", 0)
    return items_out

for prefix, files in [('BOMAS', ["stock_movement_jan.json", "stock_movement_feb.json"]), ('KAREN', ["stock_movement_karen_jan.json", "stock_movement_karen_feb.json"])]:
    b_raw = get_raw_out_by_item(files)
    b_calc = get_calc_out_by_item(f"{prefix.lower()}_average_moq.json")

    print(f"\n{prefix} Raw sum:", sum(b_raw.values()))
    print(f"{prefix} Calc sum:", sum(b_calc.values()))

    for code in set(b_raw.keys()).union(set(b_calc.keys())):
        r = b_raw.get(code, 0)
        c = b_calc.get(code, 0)
        if abs(r - c) > 0.001:
            print(f"{prefix} MISMATCH - {code}: Raw = {r}, Calc = {c}")
