# -*- coding: utf-8 -*-
"""
Recipe Extractor - Kenyan Cookbooks
Extracts recipes from 5 PDF cookbooks and saves them in JSON format
matching the kenyanMeals.js schema.
"""

import pdfplumber
import json
import re
import os

RECIPE_DIR = "kenyan recipes"

def extract_all_text(pdf_path):
    """Extract text from all pages of a PDF."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            pages.append({"page": i + 1, "text": text or ""})
    return pages


def dump_all_texts():
    """Extract and save all text from all PDFs for analysis."""
    pdfs = [
        "Global-Give-Back-Circle-Our-Favorite-Kenyan-Recipes_editable.pdf",
        "IN-MY-KITCHEN-by-KALUHI-ADAGALA.pdf",
        "Kenya Recipe Book 2018.pdf",
        "KFM-CookBook.pdf",
        "Smart-Food-Recipe-Book-Kenya-edited.pdf",
    ]

    all_texts = {}
    for pdf_name in pdfs:
        path = os.path.join(RECIPE_DIR, pdf_name)
        print(f"Extracting: {pdf_name}...")
        pages = extract_all_text(path)
        all_texts[pdf_name] = pages
        print(f"  {len(pages)} pages extracted")

    with open("kenyan recipes/all_cookbook_text.json", "w", encoding="utf-8") as f:
        json.dump(all_texts, f, indent=2, ensure_ascii=False)
    print(f"\nAll text saved to kenyan recipes/all_cookbook_text.json")
    
    total_pages = sum(len(v) for v in all_texts.values())
    total_chars = sum(len(p["text"]) for pages in all_texts.values() for p in pages)
    print(f"Total pages: {total_pages}")
    print(f"Total characters: {total_chars:,}")
    return all_texts


if __name__ == "__main__":
    dump_all_texts()
