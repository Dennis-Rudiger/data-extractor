# -*- coding: utf-8 -*-
"""
Comprehensive Kenyan Recipe Extractor
======================================
Extracts recipes from 5 PDF cookbooks and outputs JSON matching kenyanMeals.js format.

PDFs:
1. Global Give Back Circle (16 pages, ~9 recipes)
2. IN MY KITCHEN by Kaluhi Adagala (58 pages, ~28 recipes)  
3. Kenya Recipe Book 2018 (351 pages, ~150+ recipes)
4. KFM CookBook (99 pages, ~16 recipes)
5. Smart Food Recipe Book Kenya (62 pages, ~25 recipes)
"""

import json
import re
import pdfplumber
import os

BASE = "kenyan recipes"

def clean(text):
    """Clean extracted text."""
    if not text:
        return ""
    text = text.replace("\x00", "").replace("\ufffd", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_time_str(s):
    """Parse time strings like '30 Minutes', '1 hour', '2 hours' into minutes."""
    s = s.lower().strip()
    total = 0
    h = re.search(r"(\d+)\s*h", s)
    m = re.search(r"(\d+)\s*m", s)
    if h:
        total += int(h.group(1)) * 60
    if m:
        total += int(m.group(1))
    if not h and not m:
        nums = re.findall(r"\d+", s)
        if nums:
            total = int(nums[0])
    return total


# ============================================================
# 1. GLOBAL GIVE BACK CIRCLE
# ============================================================
def extract_global_giveback():
    """Extract recipes from Global Give Back Circle PDF."""
    recipes = []
    pdf_path = os.path.join(BASE, "Global-Give-Back-Circle-Our-Favorite-Kenyan-Recipes_editable.pdf")
    
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                full_text += t + "\n\n"

    # Manual extraction based on the known structure
    recipes.append({
        "name": "Chapati",
        "source": "Global Give Back Circle",
        "type": "dinner, lunch",
        "description": "Chapati is unleavened flat bread adopted from the Indian Rotti. It was first introduced to Kenya during colonial times as Indian laborers constructed the railroads throughout East Africa. After decades of integration, Kenyan Chapati has become a more layered and thicker version of Indian Rotti. Today, Kenyans prepare Chapati as part of a celebratory meal or to welcome special guests.",
        "preparationTime": 30,
        "cookingTime": 20,
        "servings": 8,
        "tags": ["Traditional", "Bread", "Budget-Friendly"],
        "ingredients": [
            {"name": "Wheat Flour", "amount": "3 cups"},
            {"name": "Warm Water", "amount": "1 1/2 cups"},
            {"name": "Salt", "amount": "2 tsp"},
            {"name": "Vegetable Oil", "amount": "5-6 tbsp"},
            {"name": "Lemon Rind", "amount": "1, grated"},
            {"name": "Vegetable Oil", "amount": "for frying"}
        ],
        "instructions": [
            "In a large bowl add flour and salt. Incorporate the grated lemon rind to the flour, followed by 3 tablespoons of vegetable oil and mix well.",
            "Make a hole in the middle of the flour mixture; add the warm water and start kneading until the water has been absorbed.",
            "Knead the mixture for 5-10 minutes and add flour if needed, until the dough is non-sticky on your bowl and hands.",
            "Add 2-3 tablespoons of vegetable oil and continue kneading until the oil mixes well and the dough feels soft.",
            "Cover the dough and leave it to rest for 20-30 minutes.",
            "On a smooth flat surface, roll out the kneaded dough using a rolling pin (make sure the surface is dusted with flour).",
            "After completely stretching it out, divide it into 8 straight strips using a sharp knife. Coil each of the strips to form a ball-like shape.",
            "Dust the flat surface with more flour and take one of the balls and roll it out using a rolling pin to a flat circular shape.",
            "On a hot pan, place the rolled out circular Chapati and fry (using medium heat) each side with a little bit of vegetable oil until its golden brown.",
            "Place your cooked Chapati on a flat plate and cover with aluminum foil or store them in a hot pot."
        ],
        "region": "Nationwide"
    })

    recipes.append({
        "name": "Mahamri",
        "source": "Global Give Back Circle",
        "type": "breakfast, snack",
        "description": "Mahamri is a type of doughnut incorporating special ingredients such as coconut milk and cardamom. This authentic type of snack originated from the Swahili coastal regions of Kenya and Tanzania and is still very popular in both regions. Normally, it is eaten at breakfast, accompanied by Kenyan Chai.",
        "preparationTime": 60,
        "cookingTime": 20,
        "servings": 20,
        "tags": ["Breakfast", "Sweet", "Coastal", "Snack"],
        "ingredients": [
            {"name": "Wheat Flour", "amount": "3 cups"},
            {"name": "Raw Sugar", "amount": "8-10 tbsp"},
            {"name": "Instant Yeast", "amount": "1 tsp"},
            {"name": "Cardamom", "amount": "1 tsp"},
            {"name": "Butter or Margarine", "amount": "1 tsp"},
            {"name": "Egg", "amount": "1 medium (optional)"},
            {"name": "Coconut Milk", "amount": "1 cup"},
            {"name": "Vegetable Oil", "amount": "for deep frying"}
        ],
        "instructions": [
            "In a mixing bowl add flour, sugar, yeast and cardamom, butter/margarine, and the egg. Mix the ingredients together. Slowly add coconut milk, a little at a time, as you knead the dough.",
            "Knead the dough for a minimum of 15-20 minutes until it is soft, smooth and not sticky.",
            "Place the dough in a container and cover it. Let it rest and rise for at least 3-4 hours at room temperature. The dough should double in size.",
            "Using a dough cutter or knife, divide the dough into 4-5 equal balls and coat each with flour, cover them again for 15 minutes and let them rise.",
            "Roll each ball of dough into a circle of about 6 inches. Cut each of the dough circles into 4 pieces.",
            "Heat the vegetable oil in a frying pan or a wok.",
            "Fry 4 Mahamris at a time. Use your metal strainer to splash oil over the top to help them puff up. Turn them until they have a nice golden-brown color on both sides.",
            "Remove from the hot oil and place on a serving plate lined with paper towels. Serve warm with Kenyan Chai."
        ],
        "region": "Coastal Kenya"
    })

    recipes.append({
        "name": "Chai (Kenyan Tea)",
        "source": "Global Give Back Circle",
        "type": "breakfast, snack",
        "description": "In Kenya, any time is considered Tea Time. Chai is a beverage guaranteed to be in any Kenyan family's menu. It is the most common beverage enjoyed by Kenyans for breakfast and the first beverage offered to visiting guests.",
        "preparationTime": 5,
        "cookingTime": 10,
        "servings": 1,
        "tags": ["Drink", "Traditional", "Quick", "Budget-Friendly"],
        "ingredients": [
            {"name": "Milk", "amount": "1 cup"},
            {"name": "Chopped Tea Leaves", "amount": "2 tsp"},
            {"name": "Water", "amount": "1/4 cup"},
            {"name": "Sugar", "amount": "3 tsp"}
        ],
        "instructions": [
            "Boil water in a saucepan.",
            "Add sugar and tea and boil for 3-4 minutes on medium flame.",
            "Add milk and boil it over medium flame for 6-7 minutes or until bubbles start to rise.",
            "Turn off the gas and strain the tea in cups.",
            "Serve with cookies, Mahamri, Bread or Chapati."
        ],
        "region": "Nationwide"
    })

    recipes.append({
        "name": "Dawa",
        "source": "Global Give Back Circle",
        "type": "drink",
        "description": "The Dawa (medicine) cocktail, invented in Nairobi, was inspired by the Brazilian Caipirinha drink. Dawa is commonly prepared when fighting a cold or sore throat. Today Dawa is a very popular drink found at tables and cafes throughout Kenya, loved for its strong ginger aroma.",
        "preparationTime": 5,
        "cookingTime": 5,
        "servings": 2,
        "tags": ["Drink", "Healthy", "Traditional"],
        "ingredients": [
            {"name": "Ginger Root", "amount": "1 piece, grated"},
            {"name": "Root Turmeric", "amount": "1 tbsp (or 1/2 tbsp ground)"},
            {"name": "Lemon Juice", "amount": "from 1 lemon"},
            {"name": "Honey", "amount": "to sweeten (optional)"},
            {"name": "Water", "amount": "2 glasses"}
        ],
        "instructions": [
            "In a pot, add 2 glasses of water, ginger, and turmeric.",
            "Once it boils, reduce heat and simmer for 3-4 minutes.",
            "Remove from heat and settle for 1-2 minutes.",
            "Strain, add honey, and serve.",
            "Dawa can either be served chilled or hot. In the summer, it is lovely over ice with fresh mint."
        ],
        "region": "Nairobi"
    })

    recipes.append({
        "name": "Ugali",
        "source": "Global Give Back Circle",
        "type": "lunch, dinner",
        "description": "Ugali is the most common staple food in Kenya. It is a polenta-like dish made from maize, millet or sorghum flour, added to boiling water and cooked until it becomes a dense block. It is usually eaten with meat stew, Nyama Choma or most commonly with Sukuma Wiki.",
        "preparationTime": 5,
        "cookingTime": 20,
        "servings": 2,
        "tags": ["Traditional", "Staple", "Budget-Friendly"],
        "ingredients": [
            {"name": "Maize (Corn) Flour", "amount": "1 cup"},
            {"name": "Water", "amount": "2 cups"}
        ],
        "instructions": [
            "Boil water until it bubbles. The water should be very hot.",
            "Add a cup of maize flour into the water. Let it cook a few seconds until water starts to cover the flour.",
            "Use a wooden spoon to quickly start mixing the flour and water.",
            "Add a handful of flour and continue to mix the water and flour as it starts to come together.",
            "Reduce heat to medium and keep turning the Ugali as it continues to stick together.",
            "Gather the Ugali and press it onto the side of the cooking pot.",
            "Place the wooden spoon under the Ugali and form into a ball in the middle of the cooking pot.",
            "Repeat pressing the Ugali on the side of the cooking pot and turning it to the middle.",
            "Once the Ugali has become firm, turn it once more and smoothen it into a round.",
            "Place the cooked Ugali over onto a plate and smooth into a ball.",
            "Serve the Ugali whole or sliced with your favorite stew, meat, veggies, fish and more."
        ],
        "region": "Nationwide"
    })

    recipes.append({
        "name": "Sukuma Wiki",
        "source": "Global Give Back Circle",
        "type": "lunch, dinner",
        "description": "Sukuma Wiki is a Swahili phrase meaning push the week. What is really being pushed is the family food budget to stretch a bit longer. Sukuma wiki is a mixture of kale, meat, spices and at times spinach to make a savory dish. It is commonly served alongside Ugali.",
        "preparationTime": 10,
        "cookingTime": 10,
        "servings": 4,
        "tags": ["Traditional", "Vegetarian", "Budget-Friendly", "Quick"],
        "ingredients": [
            {"name": "Kale and Spinach", "amount": "1 bunch each"},
            {"name": "Vegetable Oil", "amount": "3 tbsp"},
            {"name": "Salt", "amount": "a pinch"},
            {"name": "Tomatoes", "amount": "2"},
            {"name": "Beef Bouillon Cubes", "amount": "2"},
            {"name": "Onion", "amount": "1 large"}
        ],
        "instructions": [
            "Remove the stalks from the vegetable.",
            "Shred them into your desired size using a sharp knife.",
            "In a saucepan, heat oil then brown the onions.",
            "Chop the tomatoes and add them into the light brown onions.",
            "Add salt and crush the bouillon cubes and cook for 1 min.",
            "Add the cut vegetables and cook for 3 mins.",
            "Remove from fire and serve."
        ],
        "region": "Nationwide"
    })

    recipes.append({
        "name": "Pilau",
        "source": "Global Give Back Circle",
        "type": "dinner, lunch",
        "description": "A wedding in Kenya without Pilau is a big No-No. Pilau is a traditional meal among the coastal people of Kenya and Tanzania. It is a fragrant rice dish cooked using whole organic spices, beef, chicken or mutton, and is commonly served with Kachumbari.",
        "preparationTime": 15,
        "cookingTime": 45,
        "servings": 6,
        "tags": ["Traditional", "Spiced", "Celebratory", "Coastal"],
        "ingredients": [
            {"name": "Long Grain Basmati Rice", "amount": "2 cups"},
            {"name": "Water", "amount": "4 cups"},
            {"name": "Onion", "amount": "1, sliced"},
            {"name": "Chicken", "amount": "1/2, sliced into bite-size pieces"},
            {"name": "Vegetable Oil", "amount": "as needed"},
            {"name": "Whole Cloves", "amount": "4"},
            {"name": "Cinnamon Sticks", "amount": "2, whole"},
            {"name": "Cardamoms", "amount": "5, whole"},
            {"name": "Black Peppercorns", "amount": "9, whole"},
            {"name": "Cumin Seeds", "amount": "1 tsp"},
            {"name": "Ginger and Garlic", "amount": "1 tsp each, crushed"},
            {"name": "Potatoes", "amount": "2, peeled (optional)"},
            {"name": "Salt", "amount": "to taste"}
        ],
        "instructions": [
            "In a cooking pot, add onions and vegetable oil and cook until the onions start to brown.",
            "Add all whole spices and fry for 1 minute.",
            "Add chicken and fry for 6 minutes.",
            "Add potatoes (optional) and water and bring it to boil.",
            "Add salt to taste.",
            "Once the water boils, add rice and simmer until the rice is a little wet, not completely dry.",
            "Place the cooking pan in an oven, cover it and let it cook in a little water so it does not become completely dry.",
            "Serve hot with salad, gravy, chili or Kachumbari."
        ],
        "region": "Coastal Kenya"
    })

    recipes.append({
        "name": "Kachumbari",
        "source": "Global Give Back Circle",
        "type": "side dish, salad",
        "description": "For Kenyans, a Pilau dish is not complete without a side dish of Kachumbari. Kachumbari is a popular accompaniment for main dishes like Pilau, Nyama Choma and Ugali.",
        "preparationTime": 15,
        "cookingTime": 0,
        "servings": 4,
        "tags": ["Salad", "No-Cook", "Quick", "Vegetarian"],
        "ingredients": [
            {"name": "Tomatoes", "amount": "4 large"},
            {"name": "Onions", "amount": "2 medium"},
            {"name": "Coriander", "amount": "1 bunch"},
            {"name": "Lemons", "amount": "2"},
            {"name": "Salt", "amount": "to taste"},
            {"name": "Vinegar", "amount": "optional"},
            {"name": "Chili Pepper", "amount": "optional"}
        ],
        "instructions": [
            "Clean the tomatoes and chop into small pieces and set aside.",
            "Dice the onions, finely chop the coriander and slice the lemons into halves.",
            "Place the ingredients in one bowl and gently mix.",
            "Squeeze the lemon juice into your kachumbari and mix again adding a pinch of salt and the vinegar to taste.",
            "Leave to set for 10 minutes."
        ],
        "region": "Nationwide"
    })

    recipes.append({
        "name": "Matoke",
        "source": "Global Give Back Circle",
        "type": "lunch, dinner",
        "description": "Matoke is a dish originating from Uganda and a very popular dish among Kenyans. Though the original recipe from Uganda uses unripe bananas as the main ingredient, Kenyans have their own version with an addition of potatoes and sometimes arrow roots.",
        "preparationTime": 20,
        "cookingTime": 50,
        "servings": 6,
        "tags": ["Traditional", "Stew", "Budget-Friendly"],
        "ingredients": [
            {"name": "Green Bananas", "amount": "8 medium size (not quite ripe)"},
            {"name": "Potatoes", "amount": "4"},
            {"name": "Beef", "amount": "2 pounds, chopped"},
            {"name": "Tomatoes", "amount": "3, chopped"},
            {"name": "Onion", "amount": "1 large, chopped"},
            {"name": "Carrots", "amount": "2, cubed"},
            {"name": "Coriander", "amount": "small bunch, chopped"},
            {"name": "Salt", "amount": "1 tbsp"},
            {"name": "Curry Powder", "amount": "1 tbsp"},
            {"name": "Vegetable Oil", "amount": "as needed"}
        ],
        "instructions": [
            "Prepare the ingredients by covering your hands with cooking oil, then peel the unripe bananas.",
            "Peel the potatoes and cut them into even wedges.",
            "Put the beef in a cooking pot with a pinch of salt and add one cup of water, then place on heat and cover. Let it boil for 30 minutes till the meat is tender.",
            "Drain the broth and put aside for soup later. Add oil to the meat and heat for a few minutes, then add the onion. Let the onions fry with the meat for 3 minutes then add tomatoes and carrots, stir to mix, then cover and simmer until the tomatoes have softened.",
            "Add the bananas and the potato wedges to beef and stir. Then add the preserved meat broth.",
            "Add coriander and curry powder. Cover then let it simmer for 15 minutes or until the bananas and potatoes are soft.",
            "Remove from heat and serve."
        ],
        "region": "Western Kenya"
    })

    print(f"  Global Give Back Circle: {len(recipes)} recipes")
    return recipes


# ============================================================
# 2. IN MY KITCHEN by Kaluhi Adagala
# ============================================================
def extract_kaluhi():
    """Extract recipes from IN MY KITCHEN by Kaluhi Adagala."""
    recipes = []

    # Veggies & Salads section (pages 7-24)
    recipes.append({
        "name": "Kachumbari with Basil Honey Vinaigrette",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "salad, side dish",
        "description": "A gourmet twist on the cherished Kenyan tomato salsa, inspired by street food sausages with kachumbari filling. Features a delicious basil honey vinaigrette.",
        "preparationTime": 10,
        "cookingTime": 30,
        "servings": 2,
        "tags": ["Salad", "Modern Adaptation", "Vegetarian"],
        "ingredients": [
            {"name": "Tomatoes", "amount": "2, diced"},
            {"name": "Red Onion", "amount": "1, finely diced"},
            {"name": "Fresh Basil", "amount": "a handful"},
            {"name": "Honey", "amount": "1 tbsp"},
            {"name": "Olive Oil", "amount": "2 tbsp"},
            {"name": "Lemon Juice", "amount": "1 tbsp"},
            {"name": "Salt and Pepper", "amount": "to taste"}
        ],
        "instructions": [
            "Dice your red onion and soak it in hot water and 1/2 a teaspoon of vinegar for 10 minutes to reduce sharpness.",
            "Dice the tomatoes and place in a serving bowl.",
            "Make the vinaigrette by whisking together honey, olive oil, lemon juice, and finely chopped basil.",
            "Drain the onions and add to the tomatoes.",
            "Drizzle with the basil honey vinaigrette, toss gently and serve."
        ],
        "region": "Modern Adaptation"
    })

    recipes.append({
        "name": "Coconut Oil Sauteed Sukuma Wiki and Spinach",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "lunch, dinner",
        "description": "A delicious combination of kale and spinach sauteed in coconut oil with garlic and ginger. A healthier and more flavorful take on the classic Kenyan veggie.",
        "preparationTime": 15,
        "cookingTime": 15,
        "servings": 4,
        "tags": ["Vegetarian", "Healthy", "Traditional"],
        "ingredients": [
            {"name": "Kale", "amount": "500g, finely chopped"},
            {"name": "Spinach", "amount": "500g, finely chopped"},
            {"name": "Coconut Oil", "amount": "2 tbsp"},
            {"name": "Red Onion", "amount": "1, diced"},
            {"name": "Ginger", "amount": "1 thumb-sized, minced"},
            {"name": "Garlic", "amount": "4 cloves, minced"},
            {"name": "Salt", "amount": "to taste"}
        ],
        "instructions": [
            "Finely chop the kale and spinach.",
            "Heat coconut oil in a sufuria and add the diced red onion, ginger and garlic.",
            "Saute until fragrant, then add the kale and spinach.",
            "Cook until the vegetables are tender but still vibrant.",
            "Season with salt and serve."
        ],
        "region": "Modern Adaptation"
    })

    recipes.append({
        "name": "Pineapple Glazed Honey Carrots",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "side dish",
        "description": "Sweet pineapple glazed honey carrots that capture the true essence of sunny days in Nairobi. A simple yet elegant side dish.",
        "preparationTime": 5,
        "cookingTime": 15,
        "servings": 2,
        "tags": ["Vegetarian", "Healthy", "Quick", "Side Dish"],
        "ingredients": [
            {"name": "Fresh Pineapple", "amount": "1 cup, diced"},
            {"name": "Carrots", "amount": "3, sliced"},
            {"name": "Honey", "amount": "2 tbsp"},
            {"name": "Butter", "amount": "1 tbsp"},
            {"name": "Salt", "amount": "to taste"}
        ],
        "instructions": [
            "Slice the carrots and boil until just tender.",
            "In a pan, melt butter and add the diced pineapple.",
            "Add honey and cook until it forms a glaze.",
            "Add the cooked carrots and toss in the pineapple honey glaze.",
            "Serve as a side dish."
        ],
        "region": "Modern Adaptation"
    })

    recipes.append({
        "name": "Creamed Managu",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "lunch, dinner",
        "description": "A rich and creamy take on the traditional Luhya vegetable dish. Managu (African nightshade) is known for its high nutritional value and rich taste.",
        "preparationTime": 10,
        "cookingTime": 40,
        "servings": 5,
        "tags": ["Traditional", "Vegetarian", "Luhya"],
        "ingredients": [
            {"name": "Managu Leaves", "amount": "900g"},
            {"name": "Heavy Cream", "amount": "1 cup"},
            {"name": "Red Onion", "amount": "1, diced"},
            {"name": "Garlic", "amount": "3 cloves, minced"},
            {"name": "Salt", "amount": "to taste"}
        ],
        "instructions": [
            "Wash your managu leaves and dry them.",
            "Fold the leaves into a roll then finely chop them.",
            "Saute onion and garlic in oil until fragrant.",
            "Add the managu and cook for about 15 minutes.",
            "Pour in the heavy cream and let it simmer until the sauce thickens.",
            "Season with salt and serve with ugali or rice."
        ],
        "region": "Western Kenya"
    })

    recipes.append({
        "name": "Nutmeg and Cinnamon Drop Scones",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "breakfast",
        "description": "Perfect drop scones with nutmeg and cinnamon. A breakfast favorite with small tweaks that make them irresistible.",
        "preparationTime": 5,
        "cookingTime": 20,
        "servings": 3,
        "tags": ["Breakfast", "Sweet", "Quick"],
        "ingredients": [
            {"name": "Flour", "amount": "1 1/2 cups"},
            {"name": "Milk", "amount": "250ml"},
            {"name": "Sugar", "amount": "4 spoons"},
            {"name": "Egg", "amount": "1"},
            {"name": "Nutmeg", "amount": "1/2 tsp"},
            {"name": "Cinnamon", "amount": "1/2 tsp"},
            {"name": "Baking Powder", "amount": "1 tsp"},
            {"name": "Vegetable Oil", "amount": "for frying"}
        ],
        "instructions": [
            "Crack your egg into a bowl and add the sugar. Whisk until frothy and pale yellow.",
            "Add milk and mix well.",
            "Sift in flour, baking powder, nutmeg and cinnamon. Mix until smooth.",
            "Heat a pan with a little oil.",
            "Drop spoonfuls of batter onto the pan.",
            "Cook until bubbles form on the surface, then flip and cook the other side until golden.",
            "Serve warm with tea or honey."
        ],
        "region": "Modern Adaptation"
    })

    recipes.append({
        "name": "Chili and Garlic Matumbo",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "dinner, lunch",
        "description": "Tripe (matumbo) cooked with chili and garlic in a rich tomato base. A beloved family recipe that transforms this humble cut into a delicacy.",
        "preparationTime": 180,
        "cookingTime": 40,
        "servings": 3,
        "tags": ["Traditional", "Protein", "Spicy"],
        "ingredients": [
            {"name": "Tripe", "amount": "1/2 kg"},
            {"name": "Garlic", "amount": "5 cloves"},
            {"name": "Tomatoes", "amount": "4, roughly chopped"},
            {"name": "Fresh Coriander", "amount": "finely chopped"},
            {"name": "Royco All Spice Mix", "amount": "1 1/2 tbsp"},
            {"name": "Red Onion", "amount": "1 large, diced"},
            {"name": "Milk", "amount": "1 cup"},
            {"name": "Birds Eye Chili", "amount": "2"},
            {"name": "Vegetable Oil", "amount": "for frying"}
        ],
        "instructions": [
            "Thoroughly wash your matumbo until the water runs clear.",
            "Boil the tripe until it tenderizes. Add the chili and milk after about 2 hours and let simmer for 45 minutes.",
            "Remove from the heat, chop into bite-sized pieces and set aside.",
            "Pound garlic cloves into a paste. Dice onions and add into sufuria with heated oil and the minced garlic.",
            "Add salt and let these saute until the onions are soft. Add tomatoes and let simmer for about 5 minutes.",
            "Add the chili-infused boiled matumbo and mix in. Let simmer for about 2 minutes.",
            "Add royco all spice mix, 1/4 cup of water, cover and simmer for 10-20 minutes.",
            "Add finely chopped coriander and serve immediately."
        ],
        "region": "Nationwide"
    })

    recipes.append({
        "name": "Sweet Chili Nyama Choma Dry Fry",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "dinner",
        "description": "A twist on the traditional Kenyan grilled goat meat. Flame-grilled goat meat strips tossed in a sweet chili sauce that takes nyama choma to another level.",
        "preparationTime": 10,
        "cookingTime": 45,
        "servings": 3,
        "tags": ["Traditional", "Protein", "Spicy", "Special Occasion"],
        "ingredients": [
            {"name": "Goat Meat, boneless", "amount": "1 kg"},
            {"name": "Spring Onion", "amount": "1/2 cup, finely chopped"},
            {"name": "Tomato Paste", "amount": "1 tbsp"},
            {"name": "Brown Sugar", "amount": "2 tbsp"},
            {"name": "Cayenne Pepper", "amount": "1/2 tbsp"},
            {"name": "Soy Sauce", "amount": "1 tbsp"},
            {"name": "Garlic", "amount": "4 cloves, minced"},
            {"name": "Ginger Root", "amount": "1/2 thumb-sized, minced"},
            {"name": "Black Pepper", "amount": "1/2 tsp"},
            {"name": "Salt", "amount": "to taste"},
            {"name": "Onion Chives", "amount": "for garnish"}
        ],
        "instructions": [
            "Take your goat meat and flame grill it until the outside has just browned.",
            "Once done, slice it up into 3 inch strips and set aside.",
            "In a pan, add spring onion, minced ginger and garlic and saute until soft and fragrant.",
            "Add tomato paste, soy sauce, cayenne pepper, sugar, black pepper together with 1/2 a cup of hot water.",
            "Let this simmer for about 10-15 minutes on medium low heat until it thickens.",
            "Add the goat meat strips and toss them in the sauce for 2-3 minutes.",
            "Once fully coated, garnish with onion chives and serve."
        ],
        "region": "Nationwide"
    })

    recipes.append({
        "name": "Thyme and Chili Liver",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "dinner, lunch",
        "description": "Liver cooked with thyme and chili in a rich tomato sauce. A nutritious recipe passed down through generations.",
        "preparationTime": 10,
        "cookingTime": 20,
        "servings": 4,
        "tags": ["Traditional", "Protein", "Healthy", "Quick"],
        "ingredients": [
            {"name": "Liver", "amount": "1/2 kg"},
            {"name": "Garlic", "amount": "6 cloves, minced"},
            {"name": "Ginger Root", "amount": "1/2 thumb-sized"},
            {"name": "Red Onion", "amount": "1 large, finely diced"},
            {"name": "Green Bell Pepper", "amount": "1 large, finely diced"},
            {"name": "Tomatoes", "amount": "2, blended"},
            {"name": "Tomato Paste", "amount": "1 tbsp"},
            {"name": "Coriander Powder", "amount": "1 tbsp"},
            {"name": "Milk", "amount": "1 cup"},
            {"name": "Black Pepper", "amount": "1 tbsp"},
            {"name": "Birds Eye Chili", "amount": "2"},
            {"name": "Dried Thyme", "amount": "1/2 tsp"},
            {"name": "Fresh Coriander", "amount": "for garnish"}
        ],
        "instructions": [
            "Chop liver into bite-size pieces. Rinse with clean water until most blood is rinsed off (about 3 rinses).",
            "Pour in milk and allow to sit for about 30 minutes. The milk draws out the excess blood.",
            "Put garlic, ginger, chopped chilies and dried thyme in a kinu and grind until they form a paste.",
            "In a saucepan, heat oil and add onion and garlic-ginger-thyme paste. Saute until fragrant.",
            "Add tomato paste and tomatoes with 1/4 cup of hot water. Simmer for about 5 minutes.",
            "Add liver and green bell pepper, let simmer for about 7-10 minutes.",
            "Once tender and cooked through, remove from heat and serve."
        ],
        "region": "Nationwide"
    })

    recipes.append({
        "name": "Lamb Samosa",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "snack",
        "description": "A gourmet twist on the classic Kenyan samosa using tender minced lamb with mustard, cayenne and fresh mint leaves.",
        "preparationTime": 30,
        "cookingTime": 30,
        "servings": 6,
        "tags": ["Snack", "Street Food", "Meat", "Modern Adaptation"],
        "ingredients": [
            {"name": "Minced Lamb", "amount": "1 kg"},
            {"name": "Mustard Powder", "amount": "1/2 tsp"},
            {"name": "Cayenne Pepper", "amount": "1/2 tsp"},
            {"name": "Fresh Mint Leaves", "amount": "7, finely chopped"},
            {"name": "Garlic", "amount": "4 cloves, minced"},
            {"name": "Lemon", "amount": "1/2, juice and zest"},
            {"name": "Black Pepper", "amount": "1 tsp"},
            {"name": "Spring Onion", "amount": "1 cup, finely chopped"},
            {"name": "Coriander", "amount": "1 bunch, finely chopped"},
            {"name": "Salt", "amount": "to taste"},
            {"name": "Hot Water", "amount": "1 cup (for crust)"},
            {"name": "All Purpose Flour", "amount": "as needed (for crust)"},
            {"name": "Vegetable Oil", "amount": "for frying"}
        ],
        "instructions": [
            "For the crust: Pour hot water in a bowl. Add the salt, oil. Add flour bit by bit while mixing. Knead until it stops being sticky. Allow to rest for about 30 minutes.",
            "Heat some vegetable oil and add spring onion, half of the coriander, and garlic. Saute until softened.",
            "Add minced lamb, cayenne pepper, lemon juice and zest, mint leaves and mustard powder. Cook for 5-7 minutes.",
            "Divide dough into golf ball size portions. Roll them out into a circular shape then cut into quarters.",
            "Fold the ends of the circular part towards the center. Add the lamb filling and fold the remaining flap over.",
            "Use some dough as glue to seal.",
            "Flash fry for about 2-3 minutes in hot oil until golden brown then serve."
        ],
        "region": "Modern Adaptation"
    })

    recipes.append({
        "name": "Lemon Infused Chili Omena",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "lunch, dinner",
        "description": "Sun-dried omena (small fish from Lake Victoria) cooked with plenty of lemon flavor, chili and garlic. Arguably the best omena recipe, rich in flavor and nutrition.",
        "preparationTime": 90,
        "cookingTime": 35,
        "servings": 5,
        "tags": ["Traditional", "Protein", "Lake Region", "Budget-Friendly"],
        "ingredients": [
            {"name": "Sun Dried Omena", "amount": "125g"},
            {"name": "Apple Cider Vinegar", "amount": "3 tbsp"},
            {"name": "Lemon", "amount": "1, squeezed"},
            {"name": "Lemon Zest", "amount": "1 tsp"},
            {"name": "Black Pepper Seeds", "amount": "1/2 tsp, crushed"},
            {"name": "Garlic", "amount": "6 cloves"},
            {"name": "Red Onion", "amount": "1, finely chopped"},
            {"name": "Ginger Root", "amount": "1/2 thumb-sized"},
            {"name": "Birds Eye Chili", "amount": "1"},
            {"name": "Tomatoes", "amount": "2, grated"},
            {"name": "Coriander", "amount": "finely chopped"},
            {"name": "Salt", "amount": "to taste"},
            {"name": "Vegetable Oil", "amount": "for frying"}
        ],
        "instructions": [
            "Place omena in a bowl. Add hot water and apple cider vinegar and soak for about 45 minutes.",
            "Crush black pepper, garlic and chili in a kinu until it forms a paste.",
            "Heat oil and add the red onion, garlic and ginger paste. Saute until fragrant.",
            "Add tomatoes and tomato paste and let simmer for 5-7 minutes.",
            "Completely drain the water from the omena and add to the tomatoes.",
            "Pour the lemon juice over it. Mix and allow to simmer for 5 minutes.",
            "Add the lemon zest and cook for a further 10 minutes.",
            "Add finely chopped coriander and serve."
        ],
        "region": "Lake Victoria Region"
    })

    recipes.append({
        "name": "Mbuzi Meatball Mshikaki",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "snack, dinner",
        "description": "Goat meat meatballs on skewers, tossed in barbecue sauce. A spicy and flavorful twist on the traditional mshikaki.",
        "preparationTime": 10,
        "cookingTime": 20,
        "servings": 5,
        "tags": ["Street Food", "Protein", "Spicy", "Modern Adaptation"],
        "ingredients": [
            {"name": "Minced Goat Meat", "amount": "1/2 kg"},
            {"name": "Red Onion", "amount": "1, finely diced"},
            {"name": "Coriander", "amount": "1/2 cup, finely chopped"},
            {"name": "Garlic", "amount": "6 cloves"},
            {"name": "Ginger Root", "amount": "1/2 thumb-sized"},
            {"name": "Cayenne Pepper", "amount": "1 tsp"},
            {"name": "Garam Masala", "amount": "1/2 tbsp"},
            {"name": "Salt", "amount": "1/2 tsp"},
            {"name": "Egg", "amount": "1"},
            {"name": "Bread Crumbs", "amount": "3/4 cup"},
            {"name": "Barbecue Sauce", "amount": "to taste"},
            {"name": "Vegetable Oil", "amount": "for frying"}
        ],
        "instructions": [
            "Put minced goat meat in a bowl. Add coriander, red onion, ginger and garlic, spices and roughly mix.",
            "Add the egg and bread crumbs then mix until evenly distributed.",
            "Roll into plum-sized balls.",
            "Heat vegetable oil and shallow fry meatballs until they have a lovely char and are cooked through (5-8 minutes).",
            "Toss in your favorite barbecue sauce and skewer them.",
            "Garnish with finely chopped onion chives and serve."
        ],
        "region": "Modern Adaptation"
    })

    recipes.append({
        "name": "Peppery Carrot and Garlic Ndengu",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "lunch, dinner",
        "description": "Green grams (ndengu) cooked with plenty of black pepper, garlic and carrots. Their nature allows them to easily absorb flavors of other ingredients.",
        "preparationTime": 60,
        "cookingTime": 35,
        "servings": 8,
        "tags": ["Vegetarian", "High Protein", "Budget-Friendly", "Traditional"],
        "ingredients": [
            {"name": "Ndengu (Green Grams)", "amount": "2 cups"},
            {"name": "Tomatoes", "amount": "4, grated"},
            {"name": "Spring Onion", "amount": "a handful"},
            {"name": "Garlic", "amount": "6 cloves, minced"},
            {"name": "Ginger Root", "amount": "1 thumb-sized, minced"},
            {"name": "Black Pepper", "amount": "1 heaped tbsp"},
            {"name": "Whole Cumin Seeds", "amount": "1/2 tbsp"},
            {"name": "Tomato Paste", "amount": "2 tbsp"},
            {"name": "Royco", "amount": "2 heaped tbsp"},
            {"name": "Carrots", "amount": "3, finely diced"}
        ],
        "instructions": [
            "Boil your ndengu until tender, then drain excess liquid and set aside.",
            "In a separate sufuria, heat vegetable oil and add cumin seeds. Once they sizzle, add spring onion.",
            "Add grated tomatoes, minced ginger and garlic, then add tomato paste with 1/4 cup of hot water. Simmer for 5 minutes.",
            "Add ndengu and diced carrots and mix in.",
            "Mix royco and black pepper with some water to form a paste. Add to the ndengu with 1/2 a cup of hot water.",
            "Cover and simmer for 10-15 minutes so all flavors meld.",
            "Serve with your favorite starch."
        ],
        "region": "Modern Adaptation"
    })

    recipes.append({
        "name": "Curry and Cumin Seed Matoke",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "lunch, dinner",
        "description": "A culinary transformation of one of Kenya's signature meals. Green bananas cooked with curry, cumin and mustard seeds for an aromatic experience.",
        "preparationTime": 10,
        "cookingTime": 30,
        "servings": 5,
        "tags": ["Traditional", "Vegetarian", "Spiced"],
        "ingredients": [
            {"name": "Matoke (Green Bananas)", "amount": "10, peeled and chopped"},
            {"name": "Garlic", "amount": "4 cloves, minced"},
            {"name": "Ginger", "amount": "1/4 tsp, grated"},
            {"name": "Tomatoes", "amount": "3, grated"},
            {"name": "Tomato Paste", "amount": "1 tbsp"},
            {"name": "Red Onion", "amount": "1 large, diced"},
            {"name": "Turmeric", "amount": "1/4 tsp"},
            {"name": "Curry Powder", "amount": "1/4 tsp"},
            {"name": "Mustard Seeds", "amount": "1/2 tsp"},
            {"name": "Cumin Seeds", "amount": "1/2 tsp"},
            {"name": "Salt", "amount": "to taste"},
            {"name": "Vegetable Oil", "amount": "for frying"},
            {"name": "Garlic Chives", "amount": "for garnish"}
        ],
        "instructions": [
            "Put the cumin and mustard seeds in a sufuria with vegetable oil on low heat until fragrant.",
            "Add onions, garlic and ginger. Cook until softened.",
            "Add tomatoes and tomato paste. Simmer for 3-8 minutes.",
            "Add the peeled and sliced matoke with curry powder, salt and turmeric.",
            "Pour in a cup of hot water or vegetable stock.",
            "Simmer on medium low heat for about 20 minutes until matoke are tender and yellow.",
            "Garnish with garlic chives or fresh coriander and serve."
        ],
        "region": "Western Kenya"
    })

    recipes.append({
        "name": "Garlic Mukimo",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "dinner, lunch",
        "description": "Mashed potatoes on steroids! Traditional mukimo elevated with garlic, parmesan cheese, dill and blended pumpkin leaves for an incredibly flavorful dish.",
        "preparationTime": 15,
        "cookingTime": 25,
        "servings": 3,
        "tags": ["Traditional", "Kikuyu", "Vegetarian", "Modern Adaptation"],
        "ingredients": [
            {"name": "Large Potatoes", "amount": "5"},
            {"name": "Tender Boiled Maize", "amount": "250g"},
            {"name": "Large Pumpkin Leaves", "amount": "3"},
            {"name": "Coriander", "amount": "1 bunch"},
            {"name": "Garlic", "amount": "2 cloves"},
            {"name": "Dill", "amount": "1 tbsp, finely chopped"},
            {"name": "Spring Onion", "amount": "1 cup, finely chopped"},
            {"name": "Parmesan Cheese", "amount": "1/2 cup"},
            {"name": "Milk", "amount": "1/4 cup"}
        ],
        "instructions": [
            "Skin pumpkin leaves and finely chop them. Blanch for about 5 minutes.",
            "Put blanched leaves in a blender with garlic, coriander, dill and 1/4 cup milk. Blend until it forms a paste.",
            "Boil potatoes in salty water until tender, then begin mashing.",
            "Add finely chopped spring onion, blended greens, cheese and mix in.",
            "Add tender maize and fold in until distributed throughout.",
            "Let stay on heat for a minute or two then serve with spicy meat balls or chicken gravy."
        ],
        "region": "Central Kenya"
    })

    recipes.append({
        "name": "Raisin and Carrot Fried Rice",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "dinner, lunch",
        "description": "A speedy and delicious fried rice with raisins, carrots and groundnuts. Perfect for weeknight dinners.",
        "preparationTime": 5,
        "cookingTime": 20,
        "servings": 5,
        "tags": ["Quick", "Modern Adaptation", "Rice"],
        "ingredients": [
            {"name": "Pishori Rice", "amount": "1 cup"},
            {"name": "Ground Nuts", "amount": "a handful"},
            {"name": "Carrots", "amount": "a handful, finely diced"},
            {"name": "Raisins", "amount": "1/2 handful"},
            {"name": "Red Onion", "amount": "1, finely chopped"},
            {"name": "Soy Sauce", "amount": "2 tbsp"},
            {"name": "Ginger Root", "amount": "1/2 thumb-sized, minced"},
            {"name": "Garam Masala", "amount": "1 tbsp"},
            {"name": "Coriander Spice", "amount": "1 tbsp"},
            {"name": "Black Pepper", "amount": "1 tsp"},
            {"name": "Salt", "amount": "to taste"},
            {"name": "Vegetable Oil", "amount": "for frying"}
        ],
        "instructions": [
            "Cook rice until just done. Remove from heat and set aside.",
            "In a separate sufuria, add red onion, carrots, minced ginger, garam masala, coriander powder and ground nuts.",
            "Cook for about 5 minutes, retaining some texture.",
            "Add cooked rice, soy sauce and raisins. Toss until everything is evenly distributed.",
            "Let stay on heat for a minute, garnish with fresh coriander and serve."
        ],
        "region": "Modern Adaptation"
    })

    recipes.append({
        "name": "Coconut Milk and Cumin Bean Stew",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "lunch, dinner",
        "description": "Beans cooked with cumin seeds and coconut milk for a full-flavored stew. A modified family recipe with an inviting depth of flavor.",
        "preparationTime": 120,
        "cookingTime": 35,
        "servings": 5,
        "tags": ["Traditional", "Vegetarian", "High Protein", "Budget-Friendly"],
        "ingredients": [
            {"name": "Cumin Seeds", "amount": "2 tbsp"},
            {"name": "Coconut Milk", "amount": "125ml"},
            {"name": "Beans", "amount": "1 cup"},
            {"name": "Red Onion", "amount": "1, finely chopped"},
            {"name": "Tomatoes", "amount": "2, grated"},
            {"name": "Tomato Paste", "amount": "1 tsp"},
            {"name": "Green Bell Pepper", "amount": "1, finely chopped"},
            {"name": "Carrot", "amount": "1, finely diced"},
            {"name": "Black Pepper", "amount": "1 tbsp"},
            {"name": "Royco", "amount": "1 tbsp"}
        ],
        "instructions": [
            "Soak beans for 1-2 hours or preferably overnight.",
            "Boil beans together with cumin seeds until tender. Drain excess liquid.",
            "In a sufuria, add red onion and finely chopped garlic. Saute until fragrant.",
            "Add tomatoes and tomato paste, simmer for 5-10 minutes.",
            "Add carrots, beans, half the green bell pepper and coconut milk.",
            "Simmer for 10-20 minutes, stirring occasionally.",
            "Serve with rice or chapati."
        ],
        "region": "Modern Adaptation"
    })

    recipes.append({
        "name": "Cumin Bhajia with Tzatziki",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "snack",
        "description": "A global twist on the beloved Kenyan street food bhajia, served with homemade tzatziki sauce.",
        "preparationTime": 15,
        "cookingTime": 35,
        "servings": 3,
        "tags": ["Snack", "Street Food", "Modern Adaptation", "Vegetarian"],
        "ingredients": [
            {"name": "Large Potatoes", "amount": "3"},
            {"name": "Gram (Chickpea) Flour", "amount": "1 cup"},
            {"name": "Green Bell Pepper", "amount": "1/2"},
            {"name": "Ground Cumin", "amount": "1 tbsp"},
            {"name": "Ground Coriander", "amount": "1 tbsp"},
            {"name": "Turmeric", "amount": "1/2 tsp"},
            {"name": "Salt", "amount": "to taste"},
            {"name": "Thick Plain Yogurt", "amount": "120g (for tzatziki)"},
            {"name": "Cucumber", "amount": "1/2, seeded (for tzatziki)"},
            {"name": "Garlic", "amount": "2 cloves, crushed (for tzatziki)"},
            {"name": "Lemon", "amount": "1/2, squeezed (for tzatziki)"},
            {"name": "Black Pepper", "amount": "1/2 tsp (for tzatziki)"},
            {"name": "Vegetable Oil", "amount": "for deep frying"}
        ],
        "instructions": [
            "Mix the dry ingredients (ground cumin, salt, ground coriander, turmeric, gram flour) together.",
            "Add water bit by bit until the mixture has the consistency of yogurt. Add grated bell pepper and mix.",
            "Boil potatoes until just done. Slice into pieces 1/2 inch thick.",
            "Dip potato slices in the batter and fry until crispy and golden.",
            "For the tzatziki: Grate cucumber and drain excess liquid. Mix yogurt, salt, minced garlic, black pepper and lemon juice. Add drained cucumber.",
            "Serve bhajia with tzatziki."
        ],
        "region": "Urban Kenya"
    })

    recipes.append({
        "name": "Chicken Pilau with Garlic Sauce",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "dinner, lunch",
        "description": "A pilau with chicken and a rich garlic cream sauce. Strongly mirrors the flavors of the Kenyan coast.",
        "preparationTime": 20,
        "cookingTime": 30,
        "servings": 6,
        "tags": ["Traditional", "Spiced", "Coastal", "Protein"],
        "ingredients": [
            {"name": "Pishori Rice", "amount": "2 cups"},
            {"name": "Pilau Masala", "amount": "2 1/2 tbsp"},
            {"name": "Black Pepper Seeds", "amount": "1 tsp, whole (optional)"},
            {"name": "Tomato Paste", "amount": "2 tbsp"},
            {"name": "Chicken Breast", "amount": "palm-sized, diced"},
            {"name": "Red Onion", "amount": "1, diced"},
            {"name": "Garlic", "amount": "6 cloves, minced"},
            {"name": "Heavy Cream", "amount": "1/2 cup (for sauce)"},
            {"name": "Hot Water", "amount": "1/4 cup (for sauce)"},
            {"name": "Ground Mustard", "amount": "1/4 tsp (for sauce)"},
            {"name": "White Pepper", "amount": "1/8 tsp (for sauce)"},
            {"name": "Salt", "amount": "to taste"},
            {"name": "Vegetable Oil", "amount": "1 tbsp (for sauce)"}
        ],
        "instructions": [
            "In a sufuria, add onion, garlic and diced chicken breast. Cook until chicken has just turned white (3-5 minutes).",
            "Add tomato paste, pilau masala and black pepper seeds. Cook for about 5 minutes.",
            "Add 2 cups of rice followed by 4 cups of hot water. Cover and let cook until done.",
            "For the sauce: Add minced garlic in a sufuria with heated vegetable oil until softened.",
            "Add heavy cream, salt, mustard and hot water. Simmer on low heat until thickened.",
            "Serve pilau with the garlic sauce."
        ],
        "region": "Coastal Kenya"
    })

    recipes.append({
        "name": "Wali wa Nazi with Whole Cumin Seeds",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "dinner, lunch",
        "description": "Coconut rice with toasted whole cumin seeds that strongly mirrors flavors of the Kenyan coast. Simple yet impressive.",
        "preparationTime": 2,
        "cookingTime": 15,
        "servings": 5,
        "tags": ["Traditional", "Coastal", "Quick", "Vegetarian"],
        "ingredients": [
            {"name": "Basmati Rice", "amount": "1 1/2 cups"},
            {"name": "Desiccated Coconut", "amount": "50g"},
            {"name": "Coconut Milk", "amount": "2 cups"},
            {"name": "Water", "amount": "1 cup"},
            {"name": "Cumin Seeds", "amount": "1 tbsp"},
            {"name": "Red Onion", "amount": "1/2, finely diced"},
            {"name": "Salt", "amount": "to taste"}
        ],
        "instructions": [
            "Toast cumin seeds in a frying pan until fragrant. Set aside.",
            "In a sufuria, add toasted cumin seeds, finely chopped red onion, coconut milk, water and salt. Bring to a boil.",
            "Add rice once it boils.",
            "After a minute, add desiccated coconut and mix in.",
            "Turn down the heat, cover with a lid and allow the rice to cook.",
            "Garnish with fresh coriander and serve."
        ],
        "region": "Coastal Kenya"
    })

    recipes.append({
        "name": "Chili and Sage Githeri",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "lunch, dinner",
        "description": "A recipe that transforms the infamous Kenyan boarding school meal into a delicious culinary experience with chili, sage and curry.",
        "preparationTime": 15,
        "cookingTime": 40,
        "servings": 5,
        "tags": ["Traditional", "Vegetarian", "High Protein", "Budget-Friendly"],
        "ingredients": [
            {"name": "Black Pepper Seeds", "amount": "1 tsp"},
            {"name": "Birds Eye Chili", "amount": "1 medium"},
            {"name": "Dried Sage", "amount": "1/2 tsp"},
            {"name": "Curry Powder", "amount": "1/2 tsp"},
            {"name": "Garlic", "amount": "4 cloves"},
            {"name": "Boiled Githeri (Mixed Maize and Beans)", "amount": "900g"},
            {"name": "Red Onion", "amount": "1, finely diced"},
            {"name": "Royco All Spice Mix", "amount": "3/4 tbsp"},
            {"name": "Tomatoes", "amount": "2, grated"},
            {"name": "Tomato Paste", "amount": "1 tsp"},
            {"name": "Salt", "amount": "to taste"},
            {"name": "Fresh Coriander", "amount": "for garnish"}
        ],
        "instructions": [
            "Put garlic, black pepper seeds, diced chili and sage in a kinu and grind into a paste.",
            "In a sufuria, heat vegetable oil and add red onion and the garlic-chili paste. Simmer until onions soften.",
            "Add tomatoes, tomato paste and 1/4 cup of hot water. Simmer for about 5 minutes.",
            "Add the boiled githeri to the tomatoes and mix in.",
            "Mix royco and curry powder with some water to form a paste. Add with 1/2 a cup of hot water.",
            "Turn down heat and simmer for 10-15 minutes.",
            "Chop up fresh coriander, mix in, and serve."
        ],
        "region": "Central Kenya"
    })

    recipes.append({
        "name": "Garlic and Red Onion Infused Chapati",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "dinner, lunch",
        "description": "Savory chapati infused with garlic and red onion that brings out this flat bread's savoriness beautifully. A must-have from the food baskets from home.",
        "preparationTime": 60,
        "cookingTime": 40,
        "servings": 12,
        "tags": ["Bread", "Modern Adaptation", "Vegetarian"],
        "ingredients": [
            {"name": "Hot Water", "amount": "1 cup"},
            {"name": "All Purpose Flour", "amount": "as needed"},
            {"name": "Sugar", "amount": "2 tbsp"},
            {"name": "Salt", "amount": "1 tsp"},
            {"name": "Margarine", "amount": "1 tbsp"},
            {"name": "Red Onion", "amount": "1"},
            {"name": "Garlic", "amount": "4 cloves"}
        ],
        "instructions": [
            "Roughly chop red onion and garlic cloves. Put in a food processor until crushed and blended.",
            "In a bowl, add hot water, sugar, salt and vegetable oil. Mix until dissolved.",
            "Add flour bit by bit while stirring. Once the dough has come together, remove and start kneading.",
            "Spread dough and put margarine at the center. Fold in and distribute evenly.",
            "Cover with cling film and rest for 30 minutes.",
            "Pinch tangerine-sized dough balls and roll them out. Cut from center outwards and fold into a cone shape.",
            "Roll out again to a thin circular shape and fry on a hot pan until browned on each side.",
            "Serve warm."
        ],
        "region": "Nationwide"
    })

    recipes.append({
        "name": "Mayai ya Kukaanga with Oregano and Cheddar",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "breakfast, lunch",
        "description": "Kenyan scrambled eggs fried in tomatoes and onion, elevated with oregano and cheddar cheese. A gourmet twist on a bachelor and family favorite.",
        "preparationTime": 5,
        "cookingTime": 15,
        "servings": 2,
        "tags": ["Breakfast", "Quick", "Modern Adaptation", "Protein"],
        "ingredients": [
            {"name": "Eggs", "amount": "4"},
            {"name": "Tomato", "amount": "1, diced"},
            {"name": "Spring Onion", "amount": "diced"},
            {"name": "Red Onion", "amount": "finely chopped"},
            {"name": "Dried Oregano", "amount": "1/2 tsp"},
            {"name": "Cheddar Cheese", "amount": "1 tbsp"},
            {"name": "Salt and Pepper", "amount": "to taste"},
            {"name": "Vegetable Oil", "amount": "for frying"}
        ],
        "instructions": [
            "Crack eggs in a bowl and whisk with salt and pepper.",
            "Heat vegetable oil in a pan. Add spring onion and red onion. Saute until softened.",
            "Add diced tomatoes and cover until they have reduced.",
            "Pour the whisked egg over this and mix in. Add the cheddar cheese.",
            "Turn down heat to low. Scramble the egg and allow it to set and cheese to melt.",
            "Serve immediately."
        ],
        "region": "Nationwide"
    })

    recipes.append({
        "name": "Thyme and Lemon Masala Fries",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "snack, lunch",
        "description": "Masala fries taken to level 100 with fresh thyme, lemon zest and a spicy tomato sauce. A Kenyan street food indulgence elevated.",
        "preparationTime": 15,
        "cookingTime": 30,
        "servings": 2,
        "tags": ["Street Food", "Snack", "Modern Adaptation", "Spicy"],
        "ingredients": [
            {"name": "Large Potatoes", "amount": "5"},
            {"name": "Fresh Thyme", "amount": "1 sprig"},
            {"name": "Garlic", "amount": "3 cloves, chopped"},
            {"name": "Lemon Zest", "amount": "1/2 tbsp"},
            {"name": "Red Onion", "amount": "1, finely chopped"},
            {"name": "Tomato Paste", "amount": "1 tbsp"},
            {"name": "Black Pepper Seeds", "amount": "1/2 tsp, crushed"},
            {"name": "Cayenne Pepper", "amount": "1/2 tsp"},
            {"name": "Coriander", "amount": "finely chopped"},
            {"name": "Vegetable Oil", "amount": "for frying"}
        ],
        "instructions": [
            "Peel potatoes and chop into fries. Fry in hot oil until done. Set aside.",
            "In a frying pan, heat oil and add finely chopped onions and garlic. Saute until fragrant.",
            "Add tomato paste, lemon zest, black pepper and cayenne with 1/4 cup of hot water.",
            "Allow to cook down for 5-7 minutes on low heat.",
            "Add fries and finely chopped thyme. Toss in the sauce until evenly coated.",
            "Garnish with thyme sprigs and serve."
        ],
        "region": "Urban Kenya"
    })

    recipes.append({
        "name": "Rosemary and Garlic Viazi Karai",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "snack",
        "description": "A gourmet twist on the classic Kenyan viazi karai (fried potato wedges in batter). Infused with rosemary and cumin flavors.",
        "preparationTime": 15,
        "cookingTime": 30,
        "servings": 2,
        "tags": ["Street Food", "Snack", "Vegetarian", "Modern Adaptation"],
        "ingredients": [
            {"name": "Potatoes", "amount": "7"},
            {"name": "All Purpose Flour", "amount": "1 cup"},
            {"name": "Turmeric", "amount": "1/4 tsp"},
            {"name": "Cumin Seeds", "amount": "1 tbsp"},
            {"name": "Fresh Rosemary", "amount": "1 sprig"},
            {"name": "Salt", "amount": "1/2 tsp"},
            {"name": "Garlic", "amount": "3 cloves"},
            {"name": "Vegetable Oil", "amount": "for frying"}
        ],
        "instructions": [
            "Peel potatoes and boil with salt, rosemary and cumin seeds until just tender.",
            "Remove from heat and slice into quarters.",
            "Crush garlic into a paste. Mix all purpose flour, garlic paste and turmeric with water to form a batter (consistency of yogurt).",
            "Dip boiled potato quarters in batter and fry until crispy and golden.",
            "Remove and drain on paper towels. Serve with your favorite dip."
        ],
        "region": "Urban Kenya"
    })

    recipes.append({
        "name": "Okra and Rosemary Fried Rice",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "lunch, dinner",
        "description": "A healthy yet far from boring fried rice with okra and rosemary. Light yet filling.",
        "preparationTime": 15,
        "cookingTime": 20,
        "servings": 3,
        "tags": ["Healthy", "Quick", "Modern Adaptation"],
        "ingredients": [
            {"name": "Basmati Rice", "amount": "1 cup"},
            {"name": "Red Onion", "amount": "1, finely diced"},
            {"name": "Garlic", "amount": "5 cloves, minced"},
            {"name": "Okra", "amount": "7, thinly sliced"},
            {"name": "Dark Mushroom Soy Sauce", "amount": "1 tbsp"},
            {"name": "Carrot", "amount": "1 small, finely chopped"},
            {"name": "Rosemary", "amount": "1 tsp, finely chopped"},
            {"name": "Garam Masala", "amount": "1 tbsp"},
            {"name": "Black Pepper", "amount": "1/2 tbsp"},
            {"name": "Vegetable Oil", "amount": "for frying"}
        ],
        "instructions": [
            "Cook rice until almost done. Turn off heat and set aside.",
            "In a sufuria with heated vegetable oil, add red onion, garlic, garam masala, black pepper, chopped rosemary and carrots.",
            "Saute for about 4 minutes then add okra. Cook for not longer than 4-5 minutes to maintain texture.",
            "Add pre-cooked rice and toss together for about a minute.",
            "Add soy sauce and mix until evenly distributed.",
            "Remove from heat and serve."
        ],
        "region": "Modern Adaptation"
    })

    # Drinks
    recipes.append({
        "name": "Coconut and Iliki Milkshake",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "drink, snack",
        "description": "A milkshake infused with Kenyan coastal flavors - coconut milk, toasted cardamom and dark chocolate shavings.",
        "preparationTime": 10,
        "cookingTime": 3,
        "servings": 2,
        "tags": ["Drink", "Sweet", "Coastal", "Modern Adaptation"],
        "ingredients": [
            {"name": "Vanilla Ice Cream", "amount": "6 scoops"},
            {"name": "Coconut Milk", "amount": "50ml"},
            {"name": "Cardamom Seeds", "amount": "1/2 tbsp, freshly crushed"},
            {"name": "Dark Chocolate Shavings", "amount": "3 tbsp"}
        ],
        "instructions": [
            "Toast cardamom seeds in an ungreased pan for a minute or two. Crush until completely pulverized.",
            "Put ice cream, coconut milk and cardamom powder in a blender. Blitz until smooth.",
            "Pour into a glass and mix in the chocolate shavings.",
            "Serve immediately."
        ],
        "region": "Coastal Kenya"
    })

    recipes.append({
        "name": "Mango and Lime Dawa",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "drink",
        "description": "A sweet twist on the signature Kenyan vodka cocktail, channeling the flavors of Lamu with mango and lime.",
        "preparationTime": 7,
        "cookingTime": 25,
        "servings": 2,
        "tags": ["Drink", "Cocktail", "Modern Adaptation", "Coastal"],
        "ingredients": [
            {"name": "Vodka", "amount": "1/4 cup"},
            {"name": "Limes", "amount": "2, squeezed"},
            {"name": "Mango", "amount": "1/2, blended"},
            {"name": "Grated Ginger", "amount": "1/4 tsp"},
            {"name": "Rosemary Sprigs", "amount": "3"},
            {"name": "Water", "amount": "1 cup"},
            {"name": "Sparkling Water", "amount": "1/2 cup"}
        ],
        "instructions": [
            "Combine lime juice, ginger, mango juice and 1 cup of water in a sufuria over medium heat. Bring to a simmer for 10-12 minutes.",
            "Sieve the mixture and allow it to cool to room temperature.",
            "Fill two glasses with ice and 4-6 rosemary leaves. Muddle with a wooden spoon.",
            "Pour the cooled mango-lime juice to half the glass.",
            "In a cocktail mixer, add vodka, a sprig of rosemary and sparkling water. Shake and strain into the glasses.",
            "Garnish with remaining rosemary sprigs and serve."
        ],
        "region": "Coastal Kenya"
    })

    recipes.append({
        "name": "Vanilla Bean Chai Masala",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "drink, breakfast",
        "description": "An upgraded masala chai with vanilla beans, cardamom seeds and clove. Slow-brewed to allow all flavors to infuse deeply.",
        "preparationTime": 3,
        "cookingTime": 20,
        "servings": 5,
        "tags": ["Drink", "Traditional", "Spiced", "Breakfast"],
        "ingredients": [
            {"name": "Milk", "amount": "500ml"},
            {"name": "Hot Water", "amount": "1/2 cup"},
            {"name": "Tea Leaves", "amount": "1 tbsp"},
            {"name": "Clove", "amount": "1, roughly crushed"},
            {"name": "Vanilla Bean Pod", "amount": "1, seeded (optional)"},
            {"name": "Cardamom Seeds", "amount": "6, split"},
            {"name": "Freshly Grated Ginger", "amount": "1/2 tsp"}
        ],
        "instructions": [
            "Put milk and water in a sufuria with the clove, vanilla beans, cardamom seeds and ginger powder.",
            "Bring to a boil at low heat. Slow brewing allows the flavors to really infuse.",
            "Once the milk has come to a boil, add the tea leaves and stir in.",
            "Let simmer on low heat until it comes to a boil again.",
            "Sieve your tea and serve."
        ],
        "region": "Nationwide"
    })

    # Snacks
    recipes.append({
        "name": "Cheesy Mahindi Choma",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "snack",
        "description": "A cheesy upgrade to the classic Kenyan roasted maize street snack with chili, garam masala, cumin and melted cheddar cheese.",
        "preparationTime": 5,
        "cookingTime": 12,
        "servings": 3,
        "tags": ["Snack", "Street Food", "Modern Adaptation"],
        "ingredients": [
            {"name": "Tender Maize on the Cob", "amount": "1"},
            {"name": "Chili Powder", "amount": "2 tbsp"},
            {"name": "Garam Masala", "amount": "1/2 tsp"},
            {"name": "Coriander Powder", "amount": "1/2 tsp"},
            {"name": "Cumin Powder", "amount": "1/4 tsp"},
            {"name": "Cheddar Cheese", "amount": "1/2 cup"},
            {"name": "Coriander", "amount": "finely chopped"}
        ],
        "instructions": [
            "Heat coal and place corn cobs over hot embers. Turn every 4 minutes until golden brown.",
            "Mix all dry spices together in a bowl.",
            "Once maize is done, toss it in the spices.",
            "Add grated cheese and microwave for about 30 seconds until melted.",
            "Add finely chopped coriander over the molten cheese and serve."
        ],
        "region": "Nationwide"
    })

    recipes.append({
        "name": "Dates and Sesame Seed Bites",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "snack",
        "description": "Healthy no-bake bites made with dates, coconut, cinnamon and sesame seeds. A sweet treat inspired by childhood break time snacks.",
        "preparationTime": 20,
        "cookingTime": 20,
        "servings": 5,
        "tags": ["Snack", "Healthy", "Sweet", "No-Cook"],
        "ingredients": [
            {"name": "Dates", "amount": "1 cup, seeded"},
            {"name": "Coconut Flakes", "amount": "1/2 cup"},
            {"name": "Cinnamon", "amount": "1/2 tsp"},
            {"name": "Nutmeg", "amount": "1/4 tsp"},
            {"name": "Sesame Seeds", "amount": "1 cup"}
        ],
        "instructions": [
            "Soak dates in warm water to dislodge the skin.",
            "Put dates in a food processor with cinnamon and nutmeg. Process until it forms a paste.",
            "Pinch plum-sized pieces of the crushed dates and form a ball.",
            "Make a hollow and add fresh desiccated coconut. Roll up until the center is covered.",
            "Roll in sesame seeds or desiccated coconut.",
            "Serve as a snack."
        ],
        "region": "Coastal Kenya"
    })

    recipes.append({
        "name": "Nutmeg Kashata",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "snack",
        "description": "Homemade coconut candy bars with nutmeg, cardamom and clove. A nutty and fragrant version of the popular coastal sweet.",
        "preparationTime": 3,
        "cookingTime": 20,
        "servings": 10,
        "tags": ["Snack", "Sweet", "Coastal", "Traditional"],
        "ingredients": [
            {"name": "Fresh Desiccated Coconut", "amount": "1 1/2 cups"},
            {"name": "Cloves", "amount": "2, crushed"},
            {"name": "Cardamom Spice", "amount": "1/2 tsp"},
            {"name": "Nutmeg", "amount": "1/4 tsp"},
            {"name": "Brown Sugar", "amount": "1 cup"},
            {"name": "Water", "amount": "1/4 cup"},
            {"name": "Food Color", "amount": "of your choice"}
        ],
        "instructions": [
            "In a sufuria combine the sugar, food coloring and cup of water. Swirl around until sugar has dissolved. Do not stir as this will cause crystallization.",
            "Once dissolved and thickened, add the fresh coconut, nutmeg, cardamom and crushed cloves. Mix until it forms a lump and pulls away from the sides (3-6 minutes).",
            "Remove from heat and spread on a cookie sheet or greased pan at 1/2 inch thickness.",
            "Allow to completely cool down and firm up.",
            "Divide into rectangular bars. Store in an airtight container."
        ],
        "region": "Coastal Kenya"
    })

    recipes.append({
        "name": "Mango and Dark Chocolate Parfait",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "snack, dessert",
        "description": "A tasty layered dessert with fresh mango, dark chocolate, yogurt, raisins and oats. Packed with antioxidants and vitamins.",
        "preparationTime": 7,
        "cookingTime": 8,
        "servings": 2,
        "tags": ["Dessert", "Healthy", "Sweet", "Quick"],
        "ingredients": [
            {"name": "Apple Mango Cheeks", "amount": "2"},
            {"name": "Dark Chocolate", "amount": "150g"},
            {"name": "Raisins", "amount": "1 handful"},
            {"name": "Oats", "amount": "1 handful"},
            {"name": "Plain Yogurt", "amount": "50ml"}
        ],
        "instructions": [
            "Cube mango cheeks into bite-sized pieces.",
            "Roughly chop dark chocolate.",
            "Begin adding each component layer by layer, beginning with yogurt.",
            "Garnish with raisins and oats, then serve."
        ],
        "region": "Modern Adaptation"
    })

    recipes.append({
        "name": "Green Mango Posset",
        "source": "IN MY KITCHEN by Kaluhi Adagala",
        "type": "dessert",
        "description": "A creamy posset made with green mangoes common in East Africa with a distinctive sweet taste and bright orange pulp. A little indulgence that is sheer perfection.",
        "preparationTime": 10,
        "cookingTime": 60,
        "servings": 2,
        "tags": ["Dessert", "Sweet", "Modern Adaptation"],
        "ingredients": [
            {"name": "Green Mango", "amount": "1"},
            {"name": "Heavy Cream / Double Cream", "amount": "1 1/2 cups"},
            {"name": "Granulated Sugar", "amount": "3 tbsp"},
            {"name": "Lemon Slices", "amount": "for garnish"}
        ],
        "instructions": [
            "Peel mango and slice it up. Put slices into a blender and blend until smooth. Set aside.",
            "In a sufuria, add double cream and sugar. Bring to a boil while stirring continuously.",
            "Once it begins to simmer, take from heat and pour in fresh mango pulp. Mix.",
            "Pour into bowls and let cool for about an hour in the fridge until set.",
            "Serve and enjoy."
        ],
        "region": "Modern Adaptation"
    })

    print(f"  IN MY KITCHEN by Kaluhi Adagala: {len(recipes)} recipes")
    return recipes


# ============================================================
# 3. SMART FOOD RECIPE BOOK KENYA  
# ============================================================
def extract_smart_food():
    """Extract recipes from Smart Food Recipe Book Kenya."""
    recipes = []
    pdf_path = os.path.join(BASE, "Smart-Food-Recipe-Book-Kenya-edited.pdf")
    
    with pdfplumber.open(pdf_path) as pdf:
        all_text = []
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                all_text.append(t)

    # Parse from known structure
    smart_recipes = [
        {
            "name": "Finger Millet Porridge",
            "type": "breakfast",
            "description": "Traditional finger millet porridge. Can be fermented two days before use for added nutrition.",
            "servings": 4,
            "preparationTime": 10,
            "cookingTime": 30,
            "ingredients": [
                {"name": "Finger Millet Flour", "amount": "45g"},
                {"name": "Sugar", "amount": "to taste (optional)"},
                {"name": "Water", "amount": "1 litre"},
                {"name": "Milk", "amount": "250ml"},
                {"name": "Lemon/Tamarind Juice", "amount": "2 tbsp (optional)"}
            ],
            "instructions": [
                "Bring 750ml of water to the boil.",
                "Mix the flour with the remaining 250ml water to make a smooth paste.",
                "Gradually pour the paste into the boiling water while stirring vigorously to prevent lumps.",
                "Allow the porridge to simmer for 20 minutes until cooked.",
                "Add the sugar and simmer for a further 5 minutes.",
                "Add milk and simmer for a further 5 minutes.",
                "Remove from heat and add lemon/tamarind juice.",
                "Serve hot."
            ]
        },
        {
            "name": "Refreshing Sorghum Milk Drink",
            "type": "drink, breakfast",
            "description": "A traditional sorghum-based hot drink served with accompaniments like arrowroots or sweet potatoes.",
            "servings": 4,
            "preparationTime": 15,
            "cookingTime": 10,
            "ingredients": [
                {"name": "Sorghum Drinking Powder", "amount": "15g"},
                {"name": "Sugar", "amount": "40g"},
                {"name": "Milk", "amount": "1 litre"},
                {"name": "Water", "amount": "1/4 litre"}
            ],
            "instructions": [
                "Roast the sorghum grains on a pan until dark brown in color.",
                "Cool, grind into very fine flour using a pestle and mortar or grinding stone.",
                "Store in a tightly covered container.",
                "Bring the water to the boil.",
                "Make a paste from the sorghum powder using cold water.",
                "Add the paste to the boiling water and stir until the mixture cooks to a light consistency.",
                "Add the milk and allow it to boil.",
                "Serve hot with sweet potatoes or arrowroots."
            ]
        },
        {
            "name": "Pearl Millet Milk Paste",
            "type": "drink, snack",
            "description": "A cold drink made with fermented milk and roasted pearl millet flour. Simple and refreshing.",
            "servings": 4,
            "preparationTime": 5,
            "cookingTime": 0,
            "ingredients": [
                {"name": "Fermented Milk or Mala", "amount": "1 litre"},
                {"name": "Roasted Pearl Millet Flour", "amount": "250g"},
                {"name": "Sugar", "amount": "to taste (optional)"}
            ],
            "instructions": [
                "Pour the fermented milk in a clean jug.",
                "Add the flour and stir vigorously to the desired consistency.",
                "Serve cold."
            ]
        },
        {
            "name": "Stewed Cowpeas",
            "type": "lunch, dinner",
            "description": "A nutritious cowpea stew rich in protein and fiber.",
            "servings": 10,
            "preparationTime": 480,
            "cookingTime": 90,
            "ingredients": [
                {"name": "Cowpeas (dry)", "amount": "500g, soaked overnight"},
                {"name": "Onions", "amount": "2 medium, chopped"},
                {"name": "Tomatoes", "amount": "3, chopped"},
                {"name": "Cooking Oil", "amount": "50ml"},
                {"name": "Salt", "amount": "to taste"},
                {"name": "Water", "amount": "as needed"}
            ],
            "instructions": [
                "Soak cowpeas overnight in plenty of water.",
                "Drain and rinse. Boil in fresh water until tender (about 1 hour).",
                "Heat oil and saute onions until golden.",
                "Add tomatoes and cook until soft.",
                "Add the cooked cowpeas with some cooking liquid.",
                "Simmer for 20-30 minutes. Season with salt.",
                "Serve with rice, ugali or chapati."
            ]
        },
        {
            "name": "Creamy Pigeonpea and Sweet Potato Mash",
            "type": "lunch, dinner",
            "description": "A creamy mash combining pigeonpeas and sweet potatoes. Smart food that is good for you and the planet.",
            "servings": 6,
            "preparationTime": 20,
            "cookingTime": 45,
            "ingredients": [
                {"name": "Pigeonpeas", "amount": "250g, soaked overnight"},
                {"name": "Sweet Potatoes", "amount": "500g, peeled and cubed"},
                {"name": "Onion", "amount": "1, chopped"},
                {"name": "Salt", "amount": "to taste"},
                {"name": "Cooking Oil", "amount": "2 tbsp"}
            ],
            "instructions": [
                "Cook soaked pigeonpeas until tender.",
                "Boil sweet potatoes until soft.",
                "Mash the sweet potatoes and mix with the cooked pigeonpeas.",
                "Saute onion in oil until golden, add to the mash.",
                "Season with salt and mix well.",
                "Serve hot."
            ]
        },
        {
            "name": "Finger Millet Ugali",
            "type": "lunch, dinner",
            "description": "Ugali made with nutritious finger millet flour. Rich in calcium and iron.",
            "servings": 4,
            "preparationTime": 5,
            "cookingTime": 20,
            "ingredients": [
                {"name": "Finger Millet Flour", "amount": "500g"},
                {"name": "Water", "amount": "1 litre"}
            ],
            "instructions": [
                "Bring water to a boil.",
                "Gradually add finger millet flour while stirring continuously.",
                "Continue stirring until the mixture is thick and pulls away from the sides of the pot.",
                "Cover and let cook on low heat for 5-10 minutes.",
                "Serve with vegetables or stew."
            ]
        },
        {
            "name": "Sorghum Pilau",
            "type": "lunch, dinner",
            "description": "A pilau made with sorghum instead of rice. Nutritious and full of flavor.",
            "servings": 10,
            "preparationTime": 480,
            "cookingTime": 60,
            "ingredients": [
                {"name": "Pre-boiled Sorghum", "amount": "500g"},
                {"name": "Onions", "amount": "2 medium, chopped"},
                {"name": "Cooking Oil", "amount": "50ml"},
                {"name": "Pilau Masala", "amount": "15g"},
                {"name": "Fresh Ginger", "amount": "1 medium, crushed"},
                {"name": "Garlic", "amount": "1 clove, crushed"},
                {"name": "Coriander", "amount": "1 bunch, chopped"},
                {"name": "Capsicum", "amount": "1 large, chopped"},
                {"name": "Tomatoes", "amount": "2, chopped"},
                {"name": "Cumin Seeds", "amount": "1 tsp"},
                {"name": "Salt", "amount": "to taste"}
            ],
            "instructions": [
                "Wash and soak the sorghum overnight. Drain and boil until tender.",
                "Fry onions to golden brown.",
                "Add garlic and ginger, fry until brown.",
                "Add pilau masala and cumin seeds, cook evenly.",
                "Add capsicum and cook until tender.",
                "Add tomatoes and cook until tender.",
                "Add the sorghum, mix and simmer for 10 minutes.",
                "Add chopped coriander and serve hot with vegetable."
            ]
        },
        {
            "name": "Sorghum Chapati",
            "type": "lunch, dinner",
            "description": "Chapati made with a mix of sorghum and wheat flour. Adds nutrition and a nutty flavor.",
            "servings": 15,
            "preparationTime": 40,
            "cookingTime": 30,
            "ingredients": [
                {"name": "Sorghum Flour", "amount": "500g"},
                {"name": "Wheat Flour", "amount": "500g"},
                {"name": "Salt", "amount": "10g"},
                {"name": "Cooking Fat", "amount": "as needed"},
                {"name": "Warm Water", "amount": "as needed"}
            ],
            "instructions": [
                "Sift the sorghum and wheat flour and salt together.",
                "Rub in the fat using fingertips until well mixed.",
                "Using warm water, knead the flour into a stiff dough.",
                "Allow the dough to rest for 30 minutes.",
                "Divide the dough into balls.",
                "Roll each ball into a circle and apply melted fat then fold into a wheel.",
                "Allow to rest for 10 minutes.",
                "Roll each ball into a circle and shallow fry each side to golden brown.",
                "Serve hot with a stew, vegetable or beverage."
            ]
        },
        {
            "name": "Pearl Millet Mahamri",
            "type": "breakfast, snack",
            "description": "Mahamri made with pearl millet flour for added nutrition. A smart food version of the classic coastal pastry.",
            "servings": 12,
            "preparationTime": 120,
            "cookingTime": 20,
            "ingredients": [
                {"name": "Pearl Millet Flour", "amount": "250g"},
                {"name": "Wheat Flour", "amount": "250g"},
                {"name": "Sugar", "amount": "100g"},
                {"name": "Yeast", "amount": "1 tbsp"},
                {"name": "Cardamom", "amount": "1 tsp"},
                {"name": "Coconut Milk", "amount": "250ml"},
                {"name": "Cooking Oil", "amount": "for deep frying"}
            ],
            "instructions": [
                "Mix dry ingredients together.",
                "Add warm coconut milk and knead into a soft dough.",
                "Cover and let rise for 1-2 hours.",
                "Roll out and cut into triangular shapes.",
                "Deep fry until golden brown.",
                "Serve with tea."
            ]
        },
        {
            "name": "Flaky Finger Millet Chapati",
            "type": "lunch, dinner",
            "description": "A flaky chapati made with pearl millet and wheat flour blend.",
            "servings": 15,
            "preparationTime": 40,
            "cookingTime": 30,
            "ingredients": [
                {"name": "Pearl Millet Flour", "amount": "500g"},
                {"name": "Wheat Flour", "amount": "500g"},
                {"name": "Salt", "amount": "10g"},
                {"name": "Cooking Fat", "amount": "as needed"},
                {"name": "Warm Water", "amount": "as needed"}
            ],
            "instructions": [
                "Sift the flour and salt together.",
                "Rub in the fat using fingertips until well mixed.",
                "Using warm water, knead into a stiff dough.",
                "Allow to rest for 30 minutes.",
                "Divide into 20 balls. Roll each into a circle and apply melted fat then fold into a wheel.",
                "Allow to rest for 10 minutes.",
                "Roll each ball into a circle and shallow fry each side to golden brown.",
                "Serve hot with a stew, vegetable or beverage."
            ]
        },
        {
            "name": "Pigeonpea Chapati",
            "type": "lunch, dinner",
            "description": "A protein-enriched chapati made with pigeonpea flour and wheat flour.",
            "servings": 12,
            "preparationTime": 40,
            "cookingTime": 30,
            "ingredients": [
                {"name": "Pigeonpea Flour", "amount": "250g"},
                {"name": "Wheat Flour", "amount": "500g"},
                {"name": "Salt", "amount": "to taste"},
                {"name": "Cooking Oil", "amount": "as needed"},
                {"name": "Warm Water", "amount": "as needed"}
            ],
            "instructions": [
                "Mix the flours and salt together.",
                "Add oil and rub in until well mixed.",
                "Add warm water gradually and knead into a stiff dough.",
                "Rest for 30 minutes.",
                "Divide into balls, roll out and shallow fry until golden brown.",
                "Serve with stew or vegetables."
            ]
        },
        {
            "name": "Pearl Millet Steamed Cake",
            "type": "snack, dessert",
            "description": "A steamed cake made with pearl millet flour. A healthier alternative to regular cake.",
            "servings": 8,
            "preparationTime": 15,
            "cookingTime": 45,
            "ingredients": [
                {"name": "Pearl Millet Flour", "amount": "400g"},
                {"name": "Sugar", "amount": "200g"},
                {"name": "Margarine", "amount": "200g"},
                {"name": "Eggs", "amount": "4"},
                {"name": "Baking Powder", "amount": "2 tsp"},
                {"name": "Milk", "amount": "as needed"},
                {"name": "Vanilla Extract", "amount": "1 tsp"}
            ],
            "instructions": [
                "Cream sugar and margarine until fluffy.",
                "Add eggs one at a time, beating well.",
                "Fold in flour and baking powder.",
                "Add milk to reach dropping consistency.",
                "Steam for 45 minutes until a skewer comes out clean.",
                "Cool and serve."
            ]
        },
        {
            "name": "Pearl Millet Half Cake",
            "type": "snack, dessert",
            "description": "A quick half cake made with pearl millet flour. Perfect for tea time.",
            "servings": 6,
            "preparationTime": 10,
            "cookingTime": 30,
            "ingredients": [
                {"name": "Pearl Millet Flour", "amount": "300g"},
                {"name": "Sugar", "amount": "150g"},
                {"name": "Margarine", "amount": "150g"},
                {"name": "Eggs", "amount": "3"},
                {"name": "Baking Powder", "amount": "1 1/2 tsp"},
                {"name": "Milk", "amount": "as needed"}
            ],
            "instructions": [
                "Cream sugar and margarine until light and fluffy.",
                "Add eggs and beat well.",
                "Fold in flour and baking powder.",
                "Add milk to get a smooth batter.",
                "Bake at 180 degrees for 30 minutes.",
                "Cool and serve."
            ]
        },
        {
            "name": "Finger Millet Cupcakes",
            "type": "snack, dessert",
            "description": "Nutritious cupcakes made with finger millet flour. Rich in calcium and iron.",
            "servings": 12,
            "preparationTime": 15,
            "cookingTime": 20,
            "ingredients": [
                {"name": "Finger Millet Flour", "amount": "300g"},
                {"name": "Sugar", "amount": "200g"},
                {"name": "Margarine", "amount": "200g"},
                {"name": "Eggs", "amount": "4"},
                {"name": "Baking Powder", "amount": "2 tsp"},
                {"name": "Milk", "amount": "as needed"},
                {"name": "Vanilla Extract", "amount": "1 tsp"}
            ],
            "instructions": [
                "Preheat oven to 180 degrees.",
                "Cream sugar and margarine until fluffy.",
                "Add eggs one at a time, beating well.",
                "Fold in finger millet flour and baking powder.",
                "Add milk to dropping consistency.",
                "Pour into cupcake cases and bake for 15-20 minutes.",
                "Cool on a wire rack and serve."
            ]
        },
        {
            "name": "Sorghum Cupcakes",
            "type": "snack, dessert",
            "description": "Cupcakes made with sorghum flour and cardamom. A healthy and delicious treat.",
            "servings": 14,
            "preparationTime": 15,
            "cookingTime": 15,
            "ingredients": [
                {"name": "Sorghum Flour", "amount": "400g"},
                {"name": "Margarine", "amount": "200g"},
                {"name": "Sugar", "amount": "200g"},
                {"name": "Eggs", "amount": "8"},
                {"name": "Baking Powder", "amount": "8 level tsp"},
                {"name": "Ground Cardamom", "amount": "1 tsp"},
                {"name": "Milk", "amount": "as needed"}
            ],
            "instructions": [
                "Preheat oven to 250 degrees.",
                "Sift flour, cardamom and baking powder into a bowl.",
                "Cream sugar and margarine to a fluffy texture.",
                "Whisk eggs in a separate bowl.",
                "Gradually add eggs and continue creaming.",
                "Fold in the flour using a metal spoon.",
                "Gradually add milk to a dropping consistency.",
                "Grease cupcake tins, pour mixture to 3/4 full.",
                "Bake at 220 degrees for 15 minutes.",
                "Remove, cool and serve with a beverage."
            ]
        },
        {
            "name": "Pearl Millet Muffins",
            "type": "snack, dessert",
            "description": "Muffins made with pearl millet flour for a nutritious twist on classic muffins.",
            "servings": 12,
            "preparationTime": 15,
            "cookingTime": 25,
            "ingredients": [
                {"name": "Pearl Millet Flour", "amount": "300g"},
                {"name": "Sugar", "amount": "150g"},
                {"name": "Butter", "amount": "100g, melted"},
                {"name": "Eggs", "amount": "2"},
                {"name": "Baking Powder", "amount": "2 tsp"},
                {"name": "Milk", "amount": "200ml"},
                {"name": "Vanilla Extract", "amount": "1 tsp"}
            ],
            "instructions": [
                "Preheat oven to 180 degrees.",
                "Mix dry ingredients together.",
                "In a separate bowl, whisk eggs, melted butter, milk and vanilla.",
                "Combine wet and dry ingredients. Do not overmix.",
                "Pour into muffin tins and bake for 20-25 minutes.",
                "Cool and serve."
            ]
        },
        {
            "name": "Pearl Millet and Groundnut Muffins",
            "type": "snack, dessert",
            "description": "Muffins combining pearl millet flour and groundnuts for extra protein and flavor.",
            "servings": 12,
            "preparationTime": 15,
            "cookingTime": 25,
            "ingredients": [
                {"name": "Pearl Millet Flour", "amount": "250g"},
                {"name": "Ground Groundnuts", "amount": "100g"},
                {"name": "Sugar", "amount": "150g"},
                {"name": "Butter", "amount": "100g, melted"},
                {"name": "Eggs", "amount": "2"},
                {"name": "Baking Powder", "amount": "2 tsp"},
                {"name": "Milk", "amount": "200ml"}
            ],
            "instructions": [
                "Preheat oven to 180 degrees.",
                "Mix pearl millet flour, groundnuts, sugar and baking powder.",
                "Whisk eggs, melted butter and milk separately.",
                "Combine wet and dry ingredients gently.",
                "Pour into muffin tins and bake for 20-25 minutes.",
                "Cool and serve."
            ]
        },
        {
            "name": "Finger Millet Biscuits",
            "type": "snack",
            "description": "Crunchy biscuits made with finger millet and plain flour. Can be decorated with icing.",
            "servings": 30,
            "preparationTime": 40,
            "cookingTime": 15,
            "ingredients": [
                {"name": "Plain Flour", "amount": "250g"},
                {"name": "Finger Millet Flour", "amount": "250g"},
                {"name": "Butter or Margarine", "amount": "125g"},
                {"name": "Icing Sugar", "amount": "125g"},
                {"name": "Vanilla Extract", "amount": "2 tsp"},
                {"name": "Eggs", "amount": "2"},
                {"name": "Milk", "amount": "1 tbsp (optional)"}
            ],
            "instructions": [
                "Preheat oven to 220 degrees.",
                "Place flour, butter and sugar in a bowl. Rub together into fine breadcrumbs.",
                "Add eggs, vanilla extract and a little milk until mixture sticks together to form a dough.",
                "Allow dough to rest for 30 minutes in a cool place.",
                "Roll out to about 5mm thick on a floured surface. Cut out shapes.",
                "Bake for 12-15 minutes.",
                "Place on a wire rack to cool and harden.",
                "Decorate with icing and serve."
            ]
        },
        {
            "name": "Finger Millet Sugarfree Biscuits",
            "type": "snack",
            "description": "Sugar-free biscuits made with finger millet flour. A healthier snacking option.",
            "servings": 30,
            "preparationTime": 40,
            "cookingTime": 15,
            "ingredients": [
                {"name": "Plain Flour", "amount": "150g"},
                {"name": "Finger Millet Flour", "amount": "350g"},
                {"name": "Butter or Margarine", "amount": "250g"},
                {"name": "Vanilla Extract", "amount": "2 tsp"},
                {"name": "Eggs", "amount": "2"}
            ],
            "instructions": [
                "Preheat oven to 220 degrees.",
                "Place sifted flour and butter in a bowl. Rub together into fine breadcrumbs.",
                "Gradually add eggs and vanilla extract. Knead until mixture sticks together.",
                "Allow dough to relax for 30 minutes, preferably in a refrigerator.",
                "Roll out to 5mm thick on a floured surface. Cut out shapes.",
                "Bake for 12-15 minutes.",
                "Place on a wire rack to cool. Store in an airtight container."
            ]
        },
    ]

    for r in smart_recipes:
        r["source"] = "Smart Food Recipe Book Kenya"
        r["tags"] = r.get("tags", ["Smart Food", "Nutritious"])
        if "Smart Food" not in r.get("tags", []):
            r["tags"] = ["Smart Food", "Nutritious"] + r.get("tags", [])
        r["region"] = r.get("region", "Nationwide")

    recipes.extend(smart_recipes)
    print(f"  Smart Food Recipe Book Kenya: {len(recipes)} recipes")
    return recipes


# ============================================================
# 4. KFM COOKBOOK
# ============================================================
def extract_kfm():
    """Extract recipes from KFM CookBook."""
    recipes = []

    kfm_recipes = [
        {
            "name": "Dola Butternut Dhania Chapati",
            "type": "lunch, dinner",
            "description": "A creative chapati made with blended butternut squash and dhania (coriander). The butternut adds natural sweetness and a beautiful golden color.",
            "preparationTime": 30,
            "cookingTime": 20,
            "servings": 8,
            "tags": ["Bread", "Creative", "KFM"],
            "ingredients": [
                {"name": "Butternut Pumpkin", "amount": "1 medium"},
                {"name": "All-Purpose Flour", "amount": "4 cups"},
                {"name": "Sugar", "amount": "2 tbsp"},
                {"name": "Salt", "amount": "1 tbsp"},
                {"name": "Dhania (Coriander)", "amount": "1 bunch, chopped"},
                {"name": "Melted Butter/Margarine", "amount": "as needed"},
                {"name": "Cooking Oil", "amount": "for frying"}
            ],
            "instructions": [
                "Cut the butternut squash into small pieces and boil until soft.",
                "In a blender, blend the butternut until smooth.",
                "Add sugar, salt, chopped dhania, and flour. Knead to form a dough.",
                "Cover to rest for 15-20 minutes.",
                "Flatten the dough on a flat surface and apply oil. Cut into strips.",
                "Roll the strips one by one and flatten each strip into a flatbread.",
                "Fry the flatbread on a pan, adding oil evenly as you flip. Cook until golden brown.",
                "Serve with a stew of your choice."
            ]
        },
        {
            "name": "Dola Cinnamon Rolls",
            "type": "breakfast, snack",
            "description": "Soft and fluffy cinnamon rolls with a sweet icing glaze. Perfect for breakfast or tea time.",
            "preparationTime": 60,
            "cookingTime": 22,
            "servings": 12,
            "tags": ["Baking", "Sweet", "Breakfast", "KFM"],
            "ingredients": [
                {"name": "Warm Milk", "amount": "1 1/2 cups"},
                {"name": "Yeast", "amount": "2 1/2 tbsp"},
                {"name": "Eggs", "amount": "2"},
                {"name": "Sugar", "amount": "1/2 cup"},
                {"name": "Melted Butter/Margarine", "amount": "1/3 cup"},
                {"name": "Salt", "amount": "1 tbsp"},
                {"name": "All-Purpose Flour", "amount": "4 cups"},
                {"name": "Icing Sugar", "amount": "1 cup"},
                {"name": "Cinnamon Powder", "amount": "as needed"},
                {"name": "Vanilla Essence", "amount": "2 tbsp"}
            ],
            "instructions": [
                "In a bowl mix warm milk, 1/2 cup sugar, and yeast. Mix well.",
                "Add 1/3 cup melted butter/margarine and whisk. Add salt and flour, then knead to a sticky dough.",
                "Let the dough rest for 30 minutes.",
                "For the cinnamon filling: In a bowl, add 1/2 cup sugar and 1 tbsp cinnamon powder. Mix.",
                "Roll out dough, spread cinnamon filling, roll into a log.",
                "Cut into smaller sizes using string. Place on a greased baking pan.",
                "Cover for 30 minutes to allow to rise.",
                "Bake at 180 degrees for 20-22 minutes.",
                "For glaze: Mix icing sugar, milk, vanilla essence and melted butter. Drizzle over warm rolls."
            ]
        },
        {
            "name": "Dola T-Bone Steak with Ugali",
            "type": "dinner",
            "description": "A perfectly pan-seared T-bone steak served with Dola ugali. Seasoned with garlic, rosemary and thyme.",
            "preparationTime": 10,
            "cookingTime": 20,
            "servings": 2,
            "tags": ["Protein", "Special Occasion", "KFM"],
            "ingredients": [
                {"name": "T-Bone Steak Meat", "amount": "2 pieces"},
                {"name": "Dola Maize Flour", "amount": "2 cups"},
                {"name": "Salt", "amount": "to taste"},
                {"name": "Pepper", "amount": "to taste"},
                {"name": "Butter", "amount": "3 tbsp"},
                {"name": "Garlic", "amount": "3 cloves"},
                {"name": "Fresh Rosemary", "amount": "2 sprigs"},
                {"name": "Thyme", "amount": "2 sprigs"},
                {"name": "Cherry Tomatoes", "amount": "a handful"},
                {"name": "Water", "amount": "4 cups (for ugali)"}
            ],
            "instructions": [
                "Rub the steak with salt and pepper to taste.",
                "Melt 3 tablespoons of butter in a pan, and place the steak to brown.",
                "Add garlic, fresh rosemary, thyme and cherry tomatoes into the pan.",
                "Remember to flip the steak when brown on one side.",
                "For ugali: Bring 4 cups of water to boil. Add 2 cups of maize flour to the boiling water.",
                "Add flour in bits as you mix until firm.",
                "Reduce heat and continue to cook and turn the ugali.",
                "Serve steak alongside the ugali."
            ]
        },
        {
            "name": "Dola Whole Meal Choco Cookies",
            "type": "snack, dessert",
            "description": "Rich chocolate cookies made with Dola All-Purpose Flour, brown sugar, and chocolate chips. Perfect for tea time.",
            "preparationTime": 20,
            "cookingTime": 10,
            "servings": 24,
            "tags": ["Baking", "Sweet", "Snack", "KFM"],
            "ingredients": [
                {"name": "Dola All-Purpose Flour", "amount": "2 1/4 cups"},
                {"name": "Salt", "amount": "1 tbsp"},
                {"name": "Baking Soda", "amount": "1 tbsp"},
                {"name": "Margarine/Butter", "amount": "1 cup"},
                {"name": "Sugar", "amount": "1/4 cup"},
                {"name": "Brown Sugar", "amount": "1 cup"},
                {"name": "Eggs", "amount": "2"},
                {"name": "Vanilla Essence", "amount": "1 tbsp"},
                {"name": "Chocolate Chips", "amount": "1 cup"}
            ],
            "instructions": [
                "Mix flour, salt and baking soda. Sift the flour mixture.",
                "Add margarine, sugar, brown sugar and mix until smooth.",
                "Add eggs and vanilla essence, mix well.",
                "Add chocolate chips and fold in.",
                "Mix until even.",
                "Add the flour mixture gradually and mix.",
                "Roll the dough into little balls and put on a baking tray.",
                "Bake the dough balls at 180 degrees for 10 minutes.",
                "Serve with a beverage."
            ]
        },
        {
            "name": "Dola Coconut Fish with Ugali",
            "type": "lunch, dinner",
            "description": "Fish fillets in a rich coconut sauce with turmeric, paprika and black pepper, served with Dola ugali.",
            "preparationTime": 15,
            "cookingTime": 25,
            "servings": 4,
            "tags": ["Seafood", "Coastal", "KFM"],
            "ingredients": [
                {"name": "Fish Fillet", "amount": "500g"},
                {"name": "Onion", "amount": "1 mid-sized"},
                {"name": "Garlic", "amount": "1 tbsp"},
                {"name": "Blended Tomato", "amount": "1 large"},
                {"name": "Black Pepper", "amount": "1 tbsp"},
                {"name": "Paprika", "amount": "1 tbsp"},
                {"name": "Turmeric", "amount": "1/4 tsp"},
                {"name": "Tomato Paste", "amount": "1 tbsp"},
                {"name": "Coconut Milk", "amount": "1 cup"},
                {"name": "Lemon Juice", "amount": "1 tbsp"},
                {"name": "Coriander", "amount": "for garnish"},
                {"name": "Red Pepper", "amount": "1"},
                {"name": "Salt", "amount": "to taste"},
                {"name": "Dola Maize Flour", "amount": "for ugali"}
            ],
            "instructions": [
                "Shallow fry each side of the fish fillet for 3 minutes.",
                "Add oil to a pan on medium heat, add grated onion and cook till sauteed.",
                "Add the garlic, blended tomato, black pepper, paprika, turmeric, tomato paste and salt.",
                "Add red pepper, coconut milk, lemon juice and coriander. Cook until sauce thickens.",
                "Cook until the fish is ready and the sauce has thickened.",
                "For ugali: bring water to boil, add maize flour in bits while stirring.",
                "Cook until firm and serve with the coconut fish."
            ]
        },
        {
            "name": "Dola Savoury Crepes",
            "type": "breakfast, snack",
            "description": "Savory crepes made with Dola All-Purpose Flour, eggs and fresh coriander. Simple and delicious.",
            "preparationTime": 10,
            "cookingTime": 15,
            "servings": 6,
            "tags": ["Breakfast", "Quick", "KFM"],
            "ingredients": [
                {"name": "Dola All-Purpose Flour", "amount": "2 cups"},
                {"name": "Salt", "amount": "1/2 tbsp"},
                {"name": "Black Pepper", "amount": "1/2 tbsp"},
                {"name": "Water", "amount": "2 cups"},
                {"name": "Eggs", "amount": "3"},
                {"name": "Onion", "amount": "1 small, chopped"},
                {"name": "Coriander", "amount": "1 bunch, chopped"}
            ],
            "instructions": [
                "In a bowl, mix flour, salt, black pepper, and water until smooth consistency.",
                "Add a small chopped onion and coriander and mix.",
                "Using a scooping spoon, pour sizeable amounts of the batter into a medium heated pan.",
                "Cook both sides till golden brown.",
                "Serve and enjoy."
            ]
        },
        {
            "name": "Dola Atta Veggie Foldovers",
            "type": "snack, lunch",
            "description": "Vegetable-filled foldovers made with Dola atta flour. Stuffed with peas, carrots, potatoes and tandoori masala.",
            "preparationTime": 30,
            "cookingTime": 25,
            "servings": 8,
            "tags": ["Vegetarian", "Snack", "KFM"],
            "ingredients": [
                {"name": "Onion", "amount": "1 mid-sized"},
                {"name": "Mustard Seeds", "amount": "1 tbsp"},
                {"name": "Garlic", "amount": "1 tbsp"},
                {"name": "Green Peas", "amount": "1/4 cup"},
                {"name": "Carrots", "amount": "1/4 cup, diced"},
                {"name": "Tomato Puree", "amount": "1 cup"},
                {"name": "Tandoori Masala", "amount": "1 tbsp"},
                {"name": "Cumin Powder", "amount": "1/2 tsp"},
                {"name": "Salt", "amount": "to taste"},
                {"name": "Turmeric", "amount": "1/4 tsp"},
                {"name": "Potatoes", "amount": "4 large"},
                {"name": "Lemon Juice", "amount": "1 1/2 tbsp"},
                {"name": "Coriander", "amount": "1 bunch"},
                {"name": "Dola Atta Flour", "amount": "2 cups"},
                {"name": "Oil", "amount": "for frying"}
            ],
            "instructions": [
                "Put a pan on low heat and add onion, mustard seeds, garlic, peas, carrots, tomato puree, tandoori masala, cumin, salt, turmeric, potatoes, lemon juice and coriander. Mix well.",
                "In another bowl mix atta flour, salt and water. Knead into a dough.",
                "Roll out the dough into circles.",
                "Fill with the vegetable mixture and fold over.",
                "Seal edges and fry until golden brown.",
                "Serve hot."
            ]
        },
        {
            "name": "Dola Maru Bhajia",
            "type": "snack",
            "description": "Crispy potato bhajia made with gram flour, Dola All-Purpose Flour and aromatic spices. Served with a tamarind dipping sauce.",
            "preparationTime": 15,
            "cookingTime": 20,
            "servings": 6,
            "tags": ["Street Food", "Snack", "Vegetarian", "KFM"],
            "ingredients": [
                {"name": "Potatoes", "amount": "4 large"},
                {"name": "Gram Flour", "amount": "1 cup"},
                {"name": "Dola All-Purpose Flour", "amount": "1/2 cup"},
                {"name": "Salt", "amount": "to taste"},
                {"name": "Carom Seeds", "amount": "1 tbsp (optional)"},
                {"name": "Turmeric Powder", "amount": "1/4 tsp"},
                {"name": "Red Chilies", "amount": "1 tbsp"},
                {"name": "Paprika", "amount": "1 tbsp"},
                {"name": "Garlic", "amount": "1 tbsp"},
                {"name": "Coriander", "amount": "2 tbsp"},
                {"name": "Oil", "amount": "for frying"}
            ],
            "instructions": [
                "Peel the potatoes and slice them.",
                "Coat the sliced potatoes with gram flour, Dola flour, salt, carom seeds, turmeric, red chilies, paprika, garlic and coriander.",
                "Fry the potato slices in hot oil until golden brown.",
                "Prepare a dipping sauce with tamarind, sugar and water.",
                "Serve bhajia with the dipping sauce."
            ]
        },
        {
            "name": "Dola Apple Crumble Cake",
            "type": "dessert, snack",
            "description": "A delicious apple crumble cake with cinnamon and a buttery crumble topping.",
            "preparationTime": 20,
            "cookingTime": 35,
            "servings": 8,
            "tags": ["Baking", "Dessert", "Sweet", "KFM"],
            "ingredients": [
                {"name": "Dola All-Purpose Flour", "amount": "1 1/2 cups"},
                {"name": "Sugar", "amount": "2/3 cup"},
                {"name": "Salt", "amount": "1/2 tbsp"},
                {"name": "Cinnamon Powder", "amount": "1 tbsp"},
                {"name": "Melted Butter/Margarine", "amount": "1/2 cup"},
                {"name": "Apples", "amount": "3"},
                {"name": "Vinegar", "amount": "1 tbsp"},
                {"name": "Eggs", "amount": "2"},
                {"name": "Baking Powder", "amount": "1 tsp"},
                {"name": "Milk", "amount": "1/4 cup"},
                {"name": "Vanilla Essence", "amount": "1 tsp"}
            ],
            "instructions": [
                "In a bowl add flour, sugar, salt, cinnamon and melted butter. Crumble with a fork.",
                "In another bowl, peel and cut apples into cubes. Add vinegar, cinnamon, sugar and mix until coated.",
                "In another bowl, add eggs, baking powder, milk, vanilla and mix until well combined.",
                "Pour the liquid mixture into a baking pan, add apples, and top with the crumble mixture.",
                "Bake at 180 degrees for 30-35 minutes.",
                "Serve warm."
            ]
        },
        {
            "name": "Dola Mini Pizza",
            "type": "snack, lunch",
            "description": "Homemade mini pizzas with Dola flour base and a rich tomato sauce topped with cheese and vegetables.",
            "preparationTime": 45,
            "cookingTime": 15,
            "servings": 8,
            "tags": ["Snack", "Baking", "Modern Adaptation", "KFM"],
            "ingredients": [
                {"name": "Dola All-Purpose Flour", "amount": "1 1/2 cups"},
                {"name": "Yeast", "amount": "1 tbsp"},
                {"name": "Sugar", "amount": "1 tbsp"},
                {"name": "Olive Oil", "amount": "1 tbsp"},
                {"name": "Warm Water", "amount": "1/2 cup"},
                {"name": "Blended Tomatoes", "amount": "2"},
                {"name": "Tomato Paste", "amount": "2 tbsp"},
                {"name": "Garlic", "amount": "1 tbsp"},
                {"name": "Salt", "amount": "1/2 tbsp"},
                {"name": "Paprika", "amount": "1/2 tbsp"},
                {"name": "Oregano", "amount": "1/2 tbsp"},
                {"name": "Mixed Herbs", "amount": "1/2 tbsp"},
                {"name": "Black Pepper", "amount": "1/4 tbsp"},
                {"name": "Mozzarella Cheese", "amount": "1 cup"}
            ],
            "instructions": [
                "For pizza sauce: In a pan add oil, garlic, blended tomatoes, tomato paste, salt, sugar, paprika, oregano, mixed herbs and black pepper. Stir and simmer.",
                "For base: Mix flour, yeast, sugar, salt and warm water. Knead into a dough.",
                "Let the dough rest for 30 minutes.",
                "Divide into small balls and roll into mini pizza bases.",
                "Spread pizza sauce on each base, add toppings and cheese.",
                "Bake at 200 degrees for 10-15 minutes until golden.",
                "Serve hot."
            ]
        },
        {
            "name": "Dola Stuffed Donuts",
            "type": "snack, breakfast",
            "description": "Fluffy stuffed donuts made with Dola All-Purpose Flour, filled with jam or cream.",
            "preparationTime": 75,
            "cookingTime": 15,
            "servings": 12,
            "tags": ["Sweet", "Baking", "Snack", "KFM"],
            "ingredients": [
                {"name": "Warm Milk", "amount": "1 cup"},
                {"name": "Yeast", "amount": "1 1/2 tbsp"},
                {"name": "Dola All-Purpose Flour", "amount": "3 cups"},
                {"name": "Sugar", "amount": "1/2 cup"},
                {"name": "Butter/Margarine", "amount": "3 tbsp"},
                {"name": "Egg", "amount": "1"},
                {"name": "Vanilla Essence", "amount": "1 tbsp"},
                {"name": "Jam or Cream", "amount": "for filling"},
                {"name": "Oil", "amount": "for deep frying"},
                {"name": "Icing Sugar", "amount": "for dusting"}
            ],
            "instructions": [
                "In a bowl mix warm milk, yeast, flour, sugar, butter, egg and vanilla essence.",
                "Add in the milk mixture and knead the dough.",
                "Cover and let the dough rest for 1 hour.",
                "Roll the dough to 1/2 inch thickness. Use a cookie cutter to cut sizeable shapes.",
                "Deep fry in hot oil until golden brown.",
                "Fill with jam or cream using a piping bag.",
                "Dust with icing sugar and serve."
            ]
        },
        {
            "name": "Dola Somali Anjero",
            "type": "breakfast, lunch",
            "description": "A traditional Somali pancake (Anjero/Canjeero) made with a fermented batter of Dola flour. Light, spongy and full of flavor.",
            "preparationTime": 180,
            "cookingTime": 15,
            "servings": 6,
            "tags": ["Traditional", "Somali", "Breakfast", "KFM"],
            "ingredients": [
                {"name": "Dola All-Purpose Flour", "amount": "1 1/2 cups"},
                {"name": "Dola Maize Flour", "amount": "1/4 cup"},
                {"name": "Sugar", "amount": "1 tbsp"},
                {"name": "Salt", "amount": "3/4 tbsp"},
                {"name": "Yeast", "amount": "1 tbsp"},
                {"name": "Warm Water", "amount": "1 1/2 cups"}
            ],
            "instructions": [
                "In a bowl, mix All-Purpose Flour, Maize Flour, sugar, salt, and yeast. Add warm water and mix till it forms a batter.",
                "Cover the mixture and put it in a warm place for 3 hours to ferment.",
                "Using a scooping spoon, take ample portions of the batter, spread on a low heated pan.",
                "Cover and let it cook on low heat. Do not flip.",
                "Serve with stew or tea."
            ]
        },
        {
            "name": "Mashujaa Day Cookies",
            "type": "snack",
            "description": "Festive cookies decorated in Kenyan flag colors. Perfect for celebrating national holidays.",
            "preparationTime": 30,
            "cookingTime": 9,
            "servings": 20,
            "tags": ["Baking", "Sweet", "Festive", "KFM"],
            "ingredients": [
                {"name": "Dola All-Purpose Flour", "amount": "2 cups"},
                {"name": "Butter", "amount": "1/2 cup"},
                {"name": "Sugar", "amount": "1 cup"},
                {"name": "Egg", "amount": "1"},
                {"name": "Vanilla Essence", "amount": "1 tbsp"},
                {"name": "Icing Sugar", "amount": "2 cups"},
                {"name": "Food Coloring (Red, Green, Black)", "amount": "as needed"}
            ],
            "instructions": [
                "In a bowl, mix the butter and sugar and beat until creamy.",
                "Add egg, vanilla essence, and flour. Knead the dough.",
                "Cover with cling film and chill for 15 minutes.",
                "Flatten the dough and use a cookie cutter to cut shapes.",
                "Bake the cookies for 9 minutes at 180 degrees.",
                "For icing: Mix icing sugar with water, divide and color with food coloring.",
                "Decorate cookies in Kenyan flag colors and serve."
            ]
        },
        {
            "name": "Dola Ugali Beef Fry",
            "type": "lunch, dinner",
            "description": "Tender beef dry fry served with Dola ugali and a fresh tomato and green pepper relish.",
            "preparationTime": 15,
            "cookingTime": 40,
            "servings": 4,
            "tags": ["Traditional", "Protein", "KFM"],
            "ingredients": [
                {"name": "Cubed Beef", "amount": "500g"},
                {"name": "Hot Water", "amount": "2 cups"},
                {"name": "Oil", "amount": "2 tbsp"},
                {"name": "Onion", "amount": "1 large, chopped"},
                {"name": "Garlic and Ginger Paste", "amount": "1 tsp"},
                {"name": "Salt", "amount": "to taste"},
                {"name": "Tomatoes", "amount": "2 large, chopped"},
                {"name": "Green Pepper", "amount": "1, chopped"},
                {"name": "Dola Maize Flour", "amount": "2 cups"},
                {"name": "Water", "amount": "4 cups (for ugali)"}
            ],
            "instructions": [
                "Put beef in a sufuria with hot water, cover and cook until tender.",
                "Add oil, onion, garlic and ginger paste, and salt. Stir and cook until brown.",
                "Add tomatoes, green pepper and cook until soft.",
                "For ugali: Add 4 cups of water to boil. Add maize flour in bits while mixing.",
                "Reduce heat, continue turning until firm.",
                "Serve beef fry with ugali."
            ]
        },
        {
            "name": "Dola Gizzards Dry Fry",
            "type": "lunch, dinner",
            "description": "Crunchy and flavorful gizzards dry fry with fried onions and coriander. Served with ugali.",
            "preparationTime": 10,
            "cookingTime": 25,
            "servings": 4,
            "tags": ["Traditional", "Protein", "Budget-Friendly", "KFM"],
            "ingredients": [
                {"name": "Gizzards", "amount": "500g"},
                {"name": "Salt", "amount": "1 tbsp"},
                {"name": "Garlic", "amount": "1 tbsp"},
                {"name": "Oil", "amount": "for frying"},
                {"name": "Onions", "amount": "2 large"},
                {"name": "Coriander", "amount": "for garnish"},
                {"name": "Dola Maize Flour", "amount": "for ugali"}
            ],
            "instructions": [
                "Add the gizzards to a pan with 1 cup of water, salt and garlic.",
                "Cook till dry.",
                "In a different pan, fry two large onions till brown.",
                "Once brown, remove onions and fry the gizzards in the same oil.",
                "Add the fried onions and coriander.",
                "Serve with ugali."
            ]
        },
        {
            "name": "Dola Steam Cake",
            "type": "snack, dessert",
            "description": "A light and fluffy steamed cake made with Dola All-Purpose Flour. No oven needed!",
            "preparationTime": 10,
            "cookingTime": 30,
            "servings": 8,
            "tags": ["Baking", "Sweet", "Budget-Friendly", "KFM"],
            "ingredients": [
                {"name": "Eggs", "amount": "4"},
                {"name": "Sugar", "amount": "1/2 cup"},
                {"name": "Baking Powder", "amount": "1 1/2 tsp"},
                {"name": "Milk", "amount": "1/2 cup"},
                {"name": "Oil", "amount": "1/4 cup"},
                {"name": "Dola All-Purpose Flour", "amount": "4 cups"},
                {"name": "Vanilla Essence", "amount": "1 tbsp"}
            ],
            "instructions": [
                "In a bowl, beat eggs. Add sugar and baking powder, mix till frothy.",
                "Add milk and oil, mix well.",
                "Add flour gradually and whisk the batter.",
                "Add vanilla essence. Cover with a clean cloth and let it rest for 5 minutes.",
                "Pour into a greased steaming pot.",
                "Steam for about 30 minutes until a skewer comes out clean.",
                "Cool and serve."
            ]
        },
        {
            "name": "Dola Spicy Wings",
            "type": "snack, dinner",
            "description": "Crispy fried chicken wings with a spicy sauce. The chicken is coated in a mixture of corn flour and all-purpose flour.",
            "preparationTime": 15,
            "cookingTime": 25,
            "servings": 4,
            "tags": ["Snack", "Spicy", "Protein", "KFM"],
            "ingredients": [
                {"name": "Chicken Wings", "amount": "1 kg"},
                {"name": "Dola All-Purpose Flour", "amount": "1/4 cup"},
                {"name": "Corn Flour", "amount": "1 cup"},
                {"name": "Salt", "amount": "1 tbsp"},
                {"name": "Garlic Powder", "amount": "1 tbsp"},
                {"name": "Paprika Powder", "amount": "1 tbsp"},
                {"name": "Baking Powder", "amount": "1 tbsp"},
                {"name": "Onion", "amount": "1 mid-sized, grated"},
                {"name": "Ginger and Garlic Paste", "amount": "1 tbsp"},
                {"name": "Tomato Ketchup", "amount": "2 tbsp"},
                {"name": "Soy Sauce", "amount": "1 tbsp"},
                {"name": "Honey", "amount": "1 tbsp"},
                {"name": "Oil", "amount": "for frying"}
            ],
            "instructions": [
                "Mix flour, corn flour, salt, garlic powder, paprika and baking powder. Coat the chicken wings.",
                "Carefully place the chicken in hot oil and fry till golden brown.",
                "In a different pan, fry grated onion. Add ginger and garlic paste.",
                "Add tomato ketchup, soy sauce and honey. Mix to make a spicy sauce.",
                "Toss the fried wings in the sauce.",
                "Serve with ugali."
            ]
        },
        {
            "name": "Kuku wa Kupaka na Mahamri ya Dola",
            "type": "dinner, lunch",
            "description": "Coastal-style chicken in coconut sauce (Kuku wa Kupaka) served with Dola Mahamri. A true taste of Swahili cuisine.",
            "preparationTime": 30,
            "cookingTime": 40,
            "servings": 6,
            "tags": ["Coastal", "Traditional", "Protein", "KFM"],
            "ingredients": [
                {"name": "Dola Flour", "amount": "3 cups"},
                {"name": "Yeast", "amount": "1 tbsp"},
                {"name": "Warm Coconut Milk", "amount": "1 1/4 cups"},
                {"name": "Sugar", "amount": "1/2 cup"},
                {"name": "Oil", "amount": "1 tbsp"},
                {"name": "Cardamom Powder", "amount": "1 tsp"},
                {"name": "Onion", "amount": "1 large, grated"},
                {"name": "Ginger/Garlic Paste", "amount": "1 tbsp"},
                {"name": "Chicken", "amount": "1, cut into pieces"},
                {"name": "Salt", "amount": "to taste"},
                {"name": "Coconut Milk", "amount": "1 cup (for sauce)"},
                {"name": "Tomato", "amount": "1 large, grated"}
            ],
            "instructions": [
                "For mahamri: Mix flour and cardamom powder. In a separate bowl add warm coconut milk, sugar, oil and yeast. Let rest for 5 minutes.",
                "Pour milk mixture into flour and knead. Cover and let rest for 1 hour.",
                "Roll out and cut into triangular shapes. Deep fry until golden brown.",
                "For kuku wa kupaka: Saute onion, add ginger/garlic paste.",
                "Add chicken and salt, saute till dry.",
                "Add grated tomato and cook until thick.",
                "Add coconut milk and simmer until chicken is cooked through and sauce is rich.",
                "Serve chicken with mahamri."
            ]
        },
        {
            "name": "Visheti",
            "type": "snack, dessert",
            "description": "Traditional Kenyan twisted doughnuts coated in cardamom sugar syrup. Crispy on the outside, soft on the inside.",
            "preparationTime": 30,
            "cookingTime": 20,
            "servings": 15,
            "tags": ["Sweet", "Traditional", "Snack", "KFM"],
            "ingredients": [
                {"name": "Flour", "amount": "1 1/4 cups"},
                {"name": "Baking Powder", "amount": "1 tsp"},
                {"name": "Salt", "amount": "1/2 tsp"},
                {"name": "Eggs", "amount": "4"},
                {"name": "Sugar", "amount": "1/2 tbsp"},
                {"name": "Melted Butter/Margarine", "amount": "1 cup"},
                {"name": "Natural Yoghurt", "amount": "4 tsp"},
                {"name": "Warm Milk", "amount": "1 3/4 cups"},
                {"name": "Sugar (for syrup)", "amount": "1 cup"},
                {"name": "Water (for syrup)", "amount": "1/2 cup"},
                {"name": "Whole Cardamom", "amount": "for syrup"},
                {"name": "Oil", "amount": "for frying"}
            ],
            "instructions": [
                "In a bowl mix flour, baking powder, cardamom powder, vanilla essence, and melted butter with warm milk. Knead.",
                "Cover the dough and let it rest for 30 minutes.",
                "Roll into strips and twist them.",
                "Deep fry until golden brown.",
                "In another cooking pot add sugar, water, and whole cardamoms. Stir to make syrup.",
                "Coat the visheti in the sugar syrup.",
                "Serve."
            ]
        },
        {
            "name": "Dola Lamb Chops with Ugali",
            "type": "dinner",
            "description": "Succulent lamb chops glazed with soy sauce, ketchup and lemon juice, served with Dola ugali.",
            "preparationTime": 15,
            "cookingTime": 30,
            "servings": 4,
            "tags": ["Protein", "Special Occasion", "KFM"],
            "ingredients": [
                {"name": "Oil", "amount": "2 tsp"},
                {"name": "Onion", "amount": "1 large"},
                {"name": "Lamb Loin Chops", "amount": "1 kg"},
                {"name": "Light Soy Sauce", "amount": "1/2 cup"},
                {"name": "Ketchup", "amount": "3 tbsp"},
                {"name": "Sugar", "amount": "1 tsp"},
                {"name": "Lemon Juice", "amount": "from 1 lemon"},
                {"name": "Black Pepper", "amount": "to taste"},
                {"name": "Salt", "amount": "to taste"},
                {"name": "Sesame Seeds", "amount": "for garnish"},
                {"name": "Bell Peppers", "amount": "for garnish"},
                {"name": "Dola Maize Flour", "amount": "for ugali"}
            ],
            "instructions": [
                "Clean and bloat the lamb chops with kitchen towel to dry up excess water.",
                "Season with black pepper and a dash of salt.",
                "Add oil to a pan. Fry the onion until soft.",
                "Add the lamb chops and sear until browned.",
                "Add soy sauce, ketchup, sugar and lemon juice.",
                "Let simmer on medium heat till the sauce thickens. Keep turning the chops.",
                "Sprinkle sesame seeds and chopped bell peppers.",
                "Serve with ugali."
            ]
        },
        {
            "name": "Dola Ugali and Omena in Groundnut Sauce",
            "type": "lunch, dinner",
            "description": "Omena (silver fish) cooked in a rich groundnut (peanut) sauce. A nutritious and budget-friendly meal from the Lake Victoria region.",
            "preparationTime": 10,
            "cookingTime": 25,
            "servings": 4,
            "tags": ["Traditional", "Budget-Friendly", "Lake Region", "KFM"],
            "ingredients": [
                {"name": "Washed Omena", "amount": "1 cup"},
                {"name": "Tomatoes", "amount": "2 medium-sized"},
                {"name": "Onions", "amount": "1, chopped"},
                {"name": "Cooking Oil", "amount": "3 tbsp"},
                {"name": "Garlic Ginger Paste", "amount": "1 tsp"},
                {"name": "Tomato Paste", "amount": "1 tbsp"},
                {"name": "Curry Powder", "amount": "1 tsp"},
                {"name": "Paprika", "amount": "1 tsp"},
                {"name": "Groundnut Paste", "amount": "3 tbsp"},
                {"name": "Salt", "amount": "to taste"},
                {"name": "Dola Maize Flour", "amount": "for ugali"}
            ],
            "instructions": [
                "Boil the omena for 10 minutes.",
                "In a pan, fry the onions, ginger paste, tomatoes, tomato paste, curry powder, paprika and groundnut paste.",
                "Add the boiled omena and mix well.",
                "Simmer until the sauce thickens.",
                "Prepare ugali: Bring water to boil, add maize flour in bits while stirring.",
                "Serve omena in groundnut sauce with ugali."
            ]
        },
        {
            "name": "Dola Uji (Porridge)",
            "type": "breakfast, drink",
            "description": "Traditional Kenyan porridge made with Dola Maize Flour, sweetened with sugar and flavored with cardamom.",
            "preparationTime": 5,
            "cookingTime": 10,
            "servings": 4,
            "tags": ["Breakfast", "Traditional", "Budget-Friendly", "Quick", "KFM"],
            "ingredients": [
                {"name": "Dola Maize Flour", "amount": "3 cups"},
                {"name": "Water", "amount": "1 1/2 cups"},
                {"name": "Sugar", "amount": "3 tbsp"},
                {"name": "Cardamom", "amount": "1/2 tsp"},
                {"name": "Milk", "amount": "1 cup"}
            ],
            "instructions": [
                "In a bowl mix the maize flour and water.",
                "In a sufuria, add the mixture and more water. Stir continuously.",
                "Add sugar, cardamom powder, and milk. Stir continuously.",
                "Serve while still hot."
            ]
        },
        {
            "name": "Dola Style Omelette with Ugali",
            "type": "breakfast",
            "description": "A creative omelette using leftover ugali pieces mixed with eggs, tomatoes and onion. Zero waste cooking!",
            "preparationTime": 5,
            "cookingTime": 10,
            "servings": 2,
            "tags": ["Breakfast", "Quick", "Budget-Friendly", "KFM"],
            "ingredients": [
                {"name": "Leftover Ugali", "amount": "1/4 cup"},
                {"name": "Eggs", "amount": "3"},
                {"name": "Tomato", "amount": "1/2, chopped"},
                {"name": "Onion", "amount": "1/4, chopped"},
                {"name": "Coriander Leaves", "amount": "chopped"},
                {"name": "Milk", "amount": "1 tbsp"},
                {"name": "Salt", "amount": "to taste"},
                {"name": "Pepper", "amount": "to taste"},
                {"name": "Butter", "amount": "for frying"}
            ],
            "instructions": [
                "In a bowl, tear leftover ugali into pieces.",
                "Add eggs, tomatoes, onion, coriander, salt, pepper and milk. Whisk well.",
                "Heat butter in a pan. Scoop half the mixture and swirl it around.",
                "Let cook for 1.5 minutes on each side. Fold and serve.",
                "Serve with toast, sausages and bacon for a full breakfast."
            ]
        },
        {
            "name": "Dola Ugali and Kienyeji Chicken",
            "type": "lunch, dinner",
            "description": "Traditional free-range chicken (kienyeji) cooked with sukuma wiki and peanut butter, served with Dola ugali.",
            "preparationTime": 15,
            "cookingTime": 45,
            "servings": 6,
            "tags": ["Traditional", "Protein", "KFM"],
            "ingredients": [
                {"name": "Oil", "amount": "3 tbsp"},
                {"name": "Onion", "amount": "1 large, chopped"},
                {"name": "Garlic", "amount": "4 cloves, minced"},
                {"name": "Ginger", "amount": "1 tbsp, minced"},
                {"name": "Kienyeji Chicken", "amount": "1, cut into pieces"},
                {"name": "Salt", "amount": "to taste"},
                {"name": "Tomatoes", "amount": "3 large, chopped"},
                {"name": "Peanut Butter", "amount": "2 tbsp"},
                {"name": "Sukuma Wiki (Kale)", "amount": "1 bunch"},
                {"name": "Dola Maize Flour", "amount": "for ugali"}
            ],
            "instructions": [
                "Heat oil in a heavy bottomed pan and add the onions. Cook until translucent.",
                "Add the ginger and garlic followed by kienyeji chicken and salt. Stir, cover and simmer until cooked.",
                "Add tomatoes and cook until soft.",
                "In another pan, heat oil and add sliced onions. Once translucent, add peanut butter and stir.",
                "Stir in the sukuma wiki, cook for 2-3 minutes.",
                "Prepare ugali and serve with chicken and sukuma wiki."
            ]
        },
        {
            "name": "Dola Chicken Koroga",
            "type": "dinner",
            "description": "A rich Kenyan curry-style chicken dish with aromatic whole spices, fenugreek leaves and spinach.",
            "preparationTime": 15,
            "cookingTime": 40,
            "servings": 6,
            "tags": ["Traditional", "Spiced", "Protein", "KFM"],
            "ingredients": [
                {"name": "Oil", "amount": "1/4 cup"},
                {"name": "Cinnamon Sticks", "amount": "2-3"},
                {"name": "Cloves", "amount": "10-12"},
                {"name": "Black Peppercorns", "amount": "12-15"},
                {"name": "Cumin Seeds", "amount": "1 tbsp"},
                {"name": "Onions", "amount": "2, finely sliced"},
                {"name": "Garlic", "amount": "6 cloves"},
                {"name": "Ginger", "amount": "1 tbsp"},
                {"name": "Chicken", "amount": "1, cut into pieces"},
                {"name": "Fenugreek Leaves", "amount": "1/2 cup"},
                {"name": "Coriander Leaves", "amount": "1 bunch"},
                {"name": "Spinach", "amount": "1 cup"},
                {"name": "Tomatoes", "amount": "3, chopped"},
                {"name": "Salt", "amount": "to taste"},
                {"name": "Dola Maize Flour", "amount": "for ugali"}
            ],
            "instructions": [
                "Heat oil in a pot and add cinnamon sticks, cloves, black peppercorns and cumin seeds.",
                "Once cumin seeds start to turn dark, add the onions. Cook for 6-8 minutes until translucent.",
                "Add garlic and ginger, cook for 2 minutes.",
                "Add the chicken and sear until browned.",
                "Add fenugreek leaves, coriander, spinach, tomatoes and salt. Cook for 4-5 minutes.",
                "Pour in water and simmer until chicken is tender and sauce has thickened.",
                "Serve with ugali."
            ]
        },
        {
            "name": "Dola Ugali Fries",
            "type": "snack",
            "description": "Crispy fried ugali sticks coated in breadcrumbs and egg. A creative way to use leftover ugali.",
            "preparationTime": 20,
            "cookingTime": 15,
            "servings": 4,
            "tags": ["Snack", "Creative", "Budget-Friendly", "KFM"],
            "ingredients": [
                {"name": "Dola Maize Meal", "amount": "1 1/2 cups"},
                {"name": "Boiling Water", "amount": "3 cups"},
                {"name": "Eggs", "amount": "2"},
                {"name": "Bread Crumbs", "amount": "1 cup"},
                {"name": "Salt", "amount": "to taste"},
                {"name": "Oil", "amount": "for frying"},
                {"name": "Ketchup", "amount": "for dipping"}
            ],
            "instructions": [
                "For ugali: Bring water to boil. Add maize meal gradually while stirring.",
                "Cook until firm. Layer on a baking tray and spread evenly. Let cool.",
                "Cut the cooled ugali into fry-shaped strips.",
                "Dip each strip in beaten egg, then coat in bread crumbs.",
                "Deep fry in hot oil until golden brown.",
                "Serve with ketchup."
            ]
        },
        {
            "name": "Strawberry Jam and Coconut Cake",
            "type": "dessert, snack",
            "description": "A layered cake with strawberry jam filling and desiccated coconut coating.",
            "preparationTime": 15,
            "cookingTime": 35,
            "servings": 8,
            "tags": ["Baking", "Sweet", "Dessert", "KFM"],
            "ingredients": [
                {"name": "Flour", "amount": "1 1/4 cups"},
                {"name": "Baking Powder", "amount": "1 tsp"},
                {"name": "Salt", "amount": "1/2 tsp"},
                {"name": "Eggs", "amount": "4"},
                {"name": "Sugar", "amount": "1/2 tbsp"},
                {"name": "Melted Butter/Margarine", "amount": "1 cup"},
                {"name": "Strawberry Jam", "amount": "as needed"},
                {"name": "Desiccated Coconut", "amount": "1 cup"}
            ],
            "instructions": [
                "In a bowl mix flour, baking powder, and a pinch of salt.",
                "In a different bowl mix eggs, sugar and beat until fluffy.",
                "Add melted butter and mix well.",
                "Grease baking tin and pour in cake batter.",
                "Bake at 180 degrees for 30-35 minutes.",
                "Apply a coat of fruit jam to the cake.",
                "Spread desiccated coconut on top of the jam.",
                "Serve."
            ]
        },
        {
            "name": "Pojo wa Nazi kwa Sima",
            "type": "lunch, dinner",
            "description": "Green grams cooked in coconut milk with turmeric and curry powder. A coastal classic served with ugali (sima).",
            "preparationTime": 10,
            "cookingTime": 30,
            "servings": 4,
            "tags": ["Coastal", "Traditional", "Vegetarian", "KFM"],
            "ingredients": [
                {"name": "Oil", "amount": "2 tsp"},
                {"name": "Onion", "amount": "1 large"},
                {"name": "Tomato", "amount": "1 large"},
                {"name": "Turmeric Powder", "amount": "1/2 tsp"},
                {"name": "Crushed Garlic", "amount": "1 tsp"},
                {"name": "Tomato Paste", "amount": "1 tsp"},
                {"name": "Curry Powder", "amount": "1 tsp"},
                {"name": "Salt", "amount": "to taste"},
                {"name": "Green Grams", "amount": "2 cups, boiled"},
                {"name": "Coconut Milk", "amount": "1 cup"},
                {"name": "Dola Maize Flour", "amount": "for ugali"}
            ],
            "instructions": [
                "In a pan brown the onions then add chopped tomato, turmeric, garlic, tomato paste, curry powder and salt. Stir.",
                "Add the green grams and coconut milk with 1/2 cup of water.",
                "Simmer until the sauce thickens.",
                "Prepare ugali: Bring water and salt to a boil. Reduce heat and add maize flour gradually, stirring continuously.",
                "Serve green grams with ugali."
            ]
        },
    ]

    for r in kfm_recipes:
        r["source"] = "KFM CookBook"
        r["region"] = r.get("region", "Nationwide")

    recipes.extend(kfm_recipes)
    print(f"  KFM CookBook: {len(recipes)} recipes")
    return recipes


# ============================================================
# 5. KENYA RECIPE BOOK 2018 (FAO/GOK)
# ============================================================
def extract_kenya2018():
    """Extract recipes from Kenya Recipe Book 2018 using column-based extraction.
    
    The PDF has a two-column layout:
    - Left column: recipe name, description, ingredients (with bullet points)
    - Right column: KFCT code, swahili name, timing info, instructions (with bullet points)
    - Bottom: nutrition data spanning full width
    
    We use pdfplumber's crop() to extract left and right columns separately.
    """
    recipes = []
    pdf_path = os.path.join(BASE, "Kenya Recipe Book 2018.pdf")

    # Regex to detect ingredient-like text: starts with number/fraction + optional unit
    ING_RE = re.compile(
        r'^([\d\u00bd\u00bc\u00be\u2153\u2154/]+(?:\s*[\d\u00bd\u00bc\u00be\u2153\u2154/]*)*'
        r'\s*(?:cups?|tbsp?\.?|tsp\.?|g\b|kg\b|ml\b|litres?|pieces?|medium|large|small|whole|'
        r'stems?|cloves?|bunch|handful|heads?|slices?|sticks?|pinch)?'
        r'(?:\s*\([^)]+\))?)\s+(.+)',
        re.I
    )

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        
        # Parse nutrition data from the back of the book (pages 340+)
        nutrition_map = {}
        for i in range(339, total_pages):
            page = pdf.pages[i]
            text = page.extract_text()
            if not text:
                continue
            for line in text.split("\n"):
                code_match = re.match(r"(\d{5})\s+(.+?)\s+(\d+)\s+(\d+)\s+[\d.]+\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", line)
                if code_match:
                    code = code_match.group(1)
                    nutrition_map[code] = {
                        "calories": int(code_match.group(4)),
                        "protein": float(code_match.group(5)),
                        "fat": float(code_match.group(6)),
                        "carbs": float(code_match.group(7)),
                        "fiber": float(code_match.group(8))
                    }

        # Process recipe pages (pages 22-340)
        for i in range(21, min(340, total_pages)):
            page = pdf.pages[i]
            full_text = page.extract_text()
            if not full_text:
                continue
            
            # Only process pages with recipe content
            if "KFCT Code" not in full_text and not ("Ingredients" in full_text and "Preparation" in full_text):
                continue

            # Find dynamic column boundary using word positions
            # Look for the "Ingredients" header word to find the y-position of the recipe body
            words = page.extract_words()
            
            ing_y = None
            for w in words:
                # Match standalone "Ingredients" that starts a section (x position near left margin)
                if w["text"] == "Ingredients" and w["x0"] < 100:
                    ing_y = w["top"]
                    break
            
            if ing_y is None:
                # Fallback: try any "Ingredients" word
                for w in words:
                    if w["text"] == "Ingredients":
                        ing_y = w["top"]
                        break
            
            if ing_y is None:
                continue
            
            # Find right-column bullet positions (bullets with x > 200)
            right_bullet_xs = [w["x0"] for w in words if w["top"] > ing_y and w["text"] == "\u2022" and w["x0"] > 200]
            
            if right_bullet_xs:
                # Split 10px to the left of the rightmost cluster of bullets
                split_x = min(right_bullet_xs) - 10
            else:
                # Fallback: try "Preparation" word position
                prep_xs = [w["x0"] for w in words if w["top"] > ing_y and "Preparation" in w["text"] and w["x0"] > 150]
                if prep_xs:
                    split_x = min(prep_xs) - 10
                else:
                    split_x = page.width / 2 - 10

            # Extract columns: crop from Ingredients line downward
            left_text = page.crop((0, 0, split_x, page.height)).extract_text() or ""
            right_text = page.crop((split_x, 0, page.width, page.height)).extract_text() or ""
            
            # Also get full-width text for name/description (above Ingredients)
            full_top_text = page.crop((0, 0, page.width, ing_y)).extract_text() or ""

            # === EXTRACT NAME & DESCRIPTION from full-width text above Ingredients ===
            top_lines = full_top_text.split("\n")
            name = None
            swahili_name = None
            desc_lines = []
            found_name = False
            kfct_code = None
            
            for line in top_lines:
                line_s = line.strip()
                if not line_s:
                    continue
                if "Recipe Book" in line_s:
                    continue
                # Extract KFCT code
                kfct_m = re.search(r"KFCT Code\s+(\d+)", line_s)
                if kfct_m:
                    kfct_code = kfct_m.group(1)
                    continue
                if "KFCT Code" in line_s:
                    continue
                
                if not found_name and len(line_s) > 2 and not line_s.startswith("("):
                    name = line_s
                    found_name = True
                    continue
                
                if found_name:
                    if line_s.startswith("(") and line_s.endswith(")"):
                        swahili_name = line_s.strip("()")
                    elif len(line_s) > 15:
                        desc_lines.append(line_s)

            if not name or len(name) < 3:
                continue

            name = clean(name)
            description = " ".join(desc_lines) if desc_lines else ""
            # Clean up description: remove leaked timing/header info
            description = re.sub(r'\s*Ingredients\s+Preparation\s+.*$', '', description)
            description = re.sub(r'\s*Ingredients\s+Pre\s*$', '', description)
            description = re.sub(r'\s*Ingredients\s*$', '', description)
            description = description.strip()

            # === EXTRACT TIMING from right column ===
            time_match = re.search(
                r"Preparation\s+([\d]+\s*(?:hours?\s*(?:\d+\s*)?)?(?:min\w*)?[\w\s-]*?)\s*\|\s*Cooking\s*(?:Time\s*)?([\d]+\s*(?:hours?\s*(?:\d+\s*)?)?(?:min\w*)?[\w\s-]*?)\s*\|\s*(?:Serves?|Makes)\s+(\d+)",
                right_text, re.I
            )
            if time_match:
                prep_time = parse_time_str(time_match.group(1))
                cook_time = parse_time_str(time_match.group(2))
                servings = int(time_match.group(3))
            else:
                # Try extracting components separately from right column
                prep_full = re.search(r"Preparation\s+([\d]+\s*hours?\s*(?:\d+\s*min\w*)?|[\d]+\s*(?:-\s*\d+\s*)?min\w*)", right_text, re.I)
                cook_full = re.search(r"Cooking\s*(?:Time\s*)?([\d]+\s*hours?\s*(?:\d+\s*min\w*)?|[\d]+\s*(?:-\s*\d+\s*)?min\w*)", right_text, re.I)
                serves_m = re.search(r"(?:Serves?|Makes)\s+(\d+)", right_text, re.I)
                
                prep_time = parse_time_str(prep_full.group(1)) if prep_full else 15
                cook_time = parse_time_str(cook_full.group(1)) if cook_full else 30
                servings = int(serves_m.group(1)) if serves_m else 4

            # === EXTRACT INGREDIENTS from left column ===
            ingredients = []
            in_ingredients = False
            left_lines = left_text.split("\n")
            
            for line in left_lines:
                line_s = line.strip()
                if "Ingredients" in line_s:
                    in_ingredients = True
                    continue
                if not in_ingredients:
                    continue
                if not line_s:
                    continue
                # Stop at nutrition or energy line
                if re.match(r'^(Energy|Nutrition data)', line_s):
                    break
                
                # Remove bullet characters
                segments = re.split(r'\u2022\s*', line_s)
                for seg in segments:
                    seg = seg.strip()
                    if not seg or len(seg) < 3:
                        continue
                    # Skip page numbers
                    if re.match(r'^\d+$', seg):
                        continue
                    # Skip if it starts with a bullet from right column that leaked
                    if re.match(r'^(P$|S$|S\s|P\s)', seg):
                        continue
                    
                    # Try ingredient pattern
                    ing_m = ING_RE.match(seg)
                    if ing_m:
                        amount = ing_m.group(1).strip()
                        ing_name = ing_m.group(2).strip()
                        # Clean truncated text from column boundary
                        # Remove fragments that are clearly truncated words (end with single letter + space pattern)
                        if len(ing_name) > 2:
                            ingredients.append({"name": clean(ing_name), "amount": clean(amount)})

            # === EXTRACT INSTRUCTIONS from right column ===
            instructions = []
            in_instructions = False
            right_lines = right_text.split("\n")
            
            for line in right_lines:
                line_s = line.strip()
                # Start collecting after timing line or "Preparation:" label
                if re.search(r'Serves?\s+\d|Makes\s+\d', line_s):
                    in_instructions = True
                    continue
                # Handle "Serves" on one line and number on next line
                if re.search(r'Serves?\s*$|Makes\s*$', line_s):
                    in_instructions = True
                    continue
                # Start on standalone serving count (e.g. "4" after "Serves")
                if not in_instructions and re.match(r'^\d{1,2}$', line_s):
                    in_instructions = True
                    continue
                if line_s in ("Preparation:", "Method:", "Frying:", "Cooking:"):
                    in_instructions = True
                    continue
                # Also start on first bullet point if we haven't started yet
                if not in_instructions and '\u2022' in line_s:
                    in_instructions = True
                    # Don't continue — process this line below
                if not in_instructions:
                    continue
                if not line_s:
                    continue
                # Stop at nutrition data
                if re.match(r'^(Nutrition data|Energy|\d+\s*kcal|Vitamin)', line_s):
                    break
                # Skip page numbers
                if re.match(r'^\d+$', line_s):
                    continue
                
                # Remove bullet characters and process
                segments = re.split(r'\u2022\s*', line_s)
                for seg in segments:
                    seg = seg.strip()
                    if not seg or len(seg) < 3:
                        continue
                    if re.match(r'^\d+$', seg):
                        continue
                    # Skip nutrition fragments
                    if re.match(r'^(Energy|Fat\s+\d|Carbohydrate|Protein\s+\d|Fibre|Vitamin|Iron\s+\d|Zinc\s+\d)', seg):
                        continue
                    
                    seg_clean = clean(seg)
                    if seg_clean and len(seg_clean) > 3:
                        # Merge continuation lines
                        if instructions and not seg_clean[0].isupper() and seg_clean[0].isalpha():
                            prev = instructions[-1]
                            if prev.endswith("-"):
                                instructions[-1] = prev[:-1] + seg_clean
                            else:
                                instructions[-1] = prev + " " + seg_clean
                        else:
                            instructions.append(seg_clean)

            # === EXTRACT INLINE NUTRITION from full text ===
            nutrition = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0}
            if kfct_code and kfct_code in nutrition_map:
                nutrition = nutrition_map[kfct_code]
            
            nut_match = re.search(r"Energy\s+\d+\s*kJ/?\s*(\d+)\s*kcal.*?Fat\s+([\d.]+)\s*g.*?Carbohydrate\s+([\d.]+)\s*g.*?Protein\s+([\d.]+)\s*g.*?Fibre\s+([\d.]+)\s*g", full_text, re.S|re.I)
            if nut_match and nutrition["calories"] == 0:
                nutrition = {
                    "calories": int(nut_match.group(1)),
                    "protein": float(nut_match.group(4)),
                    "carbs": float(nut_match.group(3)),
                    "fat": float(nut_match.group(2)),
                    "fiber": float(nut_match.group(5))
                }

            # === DETERMINE MEAL TYPE ===
            name_lower = name.lower()
            meal_type = "lunch, dinner"
            if any(w in name_lower for w in ["porridge", "chai", "tea", "mandazi", "oat", "uji", "scone", "pancake"]):
                meal_type = "breakfast"
            elif any(w in name_lower for w in ["bhajia", "samosa", "chips", "snack", "kaimati"]):
                meal_type = "snack"
            elif any(w in name_lower for w in ["chaas", "juice", "drink", "beverage"]):
                meal_type = "drink"

            if not description:
                description = "Traditional Kenyan recipe from the FAO/Government of Kenya Recipe Book."
            
            recipe = {
                "name": name,
                "source": "Kenya Recipe Book 2018 (FAO/GOK)",
                "type": meal_type,
                "description": description,
                "preparationTime": prep_time,
                "cookingTime": cook_time,
                "servings": servings,
                "tags": ["Traditional", "FAO", "Community Recipe"],
                "ingredients": ingredients if ingredients else [{"name": "See original recipe", "amount": ""}],
                "instructions": instructions if instructions else ["See original recipe for detailed instructions."],
                "region": "Nationwide",
                "nutritionFacts": nutrition
            }
            if swahili_name:
                recipe["swahiliName"] = swahili_name
            if kfct_code:
                recipe["kfctCode"] = kfct_code
            recipes.append(recipe)

    # Deduplicate by name (some recipes appear on consecutive pages)
    seen = set()
    unique_recipes = []
    for r in recipes:
        key = r["name"].lower().strip()
        if key not in seen:
            seen.add(key)
            unique_recipes.append(r)
    
    recipes = unique_recipes
    print(f"  Kenya Recipe Book 2018: {len(recipes)} recipes")
    return recipes


# ============================================================
# MAIN: Combine all recipes into JSON
# ============================================================
def main():
    print("=" * 60)
    print("KENYAN RECIPE EXTRACTION")
    print("=" * 60)
    print()

    all_recipes = []

    # Extract from each PDF
    all_recipes.extend(extract_global_giveback())
    all_recipes.extend(extract_kaluhi())
    all_recipes.extend(extract_smart_food())
    all_recipes.extend(extract_kfm())
    all_recipes.extend(extract_kenya2018())

    print(f"\n{'=' * 60}")
    print(f"TOTAL RECIPES EXTRACTED: {len(all_recipes)}")
    print(f"{'=' * 60}")

    # Assign IDs starting from ke-046 (since kenyanMeals.js goes to ke-045)
    id_counter = 46
    for recipe in all_recipes:
        recipe["id"] = f"ke-{id_counter:03d}"
        recipe["image"] = None
        recipe["calories"] = recipe.get("calories", 0)
        recipe["totalCost"] = recipe.get("totalCost", 0)
        recipe["nutritionFacts"] = recipe.get("nutritionFacts", {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0
        })
        id_counter += 1

    # Save to JSON
    output_path = os.path.join(BASE, "extracted_recipes.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_recipes, f, indent=2, ensure_ascii=False)
    print(f"\nRecipes saved to: {output_path}")

    # Print summary by source
    sources = {}
    for r in all_recipes:
        src = r.get("source", "Unknown")
        sources[src] = sources.get(src, 0) + 1
    
    print(f"\nBreakdown by source:")
    for src, count in sorted(sources.items()):
        print(f"  {src}: {count}")


if __name__ == "__main__":
    main()
