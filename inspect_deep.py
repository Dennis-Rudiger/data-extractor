# -*- coding: utf-8 -*-
import json

with open("kenyan recipes/all_cookbook_text.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Global Give Back - all pages
print("=== GLOBAL GIVE BACK CIRCLE (all 16 pages) ===")
for p in data["Global-Give-Back-Circle-Our-Favorite-Kenyan-Recipes_editable.pdf"]:
    if p["text"].strip():
        print(f"\n--- Page {p['page']} ---")
        print(p["text"][:1500])
