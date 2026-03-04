# -*- coding: utf-8 -*-
import json

with open("kenyan recipes/all_cookbook_text.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== IN MY KITCHEN by Kaluhi Adagala (58 pages) ===")
for p in data["IN-MY-KITCHEN-by-KALUHI-ADAGALA.pdf"]:
    if p["text"].strip() and len(p["text"].strip()) > 30:
        print(f"\n--- Page {p['page']} ---")
        print(p["text"][:2000])
