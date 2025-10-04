import pandas as pd

def get_dummy_products():
    data = [
        {
            "product_id": 101,
            "name": "Hydrating Serum",
            "category": "serum",
            "suitable_for": ["dry", "combination"],
            "concerns_targeted": ["dehydration", "fine lines"],
            "key_ingredients": ["hyaluronic acid", "glycerin"]
        },
        {
            "product_id": 102,
            "name": "Day Moisturizer SPF 30",
            "category": "moisturizer",
            "suitable_for": ["dry", "normal", "combination"],
            "concerns_targeted": ["sun damage", "dehydration"],
            "key_ingredients": ["niacinamide", "zinc oxide"]
        },
        {
            "product_id": 103,
            "name": "Oil-Control Gel",
            "category": "treatment",
            "suitable_for": ["oily", "combination"],
            "concerns_targeted": ["acne", "shine"],
            "key_ingredients": ["salicylic acid", "green tea"]
        },
        {
            "product_id": 104,
            "name": "Lightweight Moisturizer",
            "category": "moisturizer",
            "suitable_for": ["oily", "normal"],
            "concerns_targeted": ["shine", "acne"],
            "key_ingredients": ["aloe vera", "niacinamide"]
        },
        {
            "product_id": 105,
            "name": "SPF 50 Sunscreen",
            "category": "sunscreen",
            "suitable_for": ["all"],
            "concerns_targeted": ["sun damage"],
            "key_ingredients": ["titanium dioxide", "vitamin E"]
        },
        {
            "product_id": 106,
            "name": "Soothing Cream",
            "category": "cream",
            "suitable_for": ["sensitive", "dry"],
            "concerns_targeted": ["redness", "irritation"],
            "key_ingredients": ["ceramides", "aloe vera"]
        },
        {
            "product_id": 107,
            "name": "Vitamin C Serum",
            "category": "serum",
            "suitable_for": ["all"],
            "concerns_targeted": ["dullness", "uneven tone"],
            "key_ingredients": ["vitamin C", "ferulic acid"]
        },
        {
            "product_id": 108,
            "name": "Night Repair Cream",
            "category": "cream",
            "suitable_for": ["dry", "combination"],
            "concerns_targeted": ["fine lines", "dullness"],
            "key_ingredients": ["retinol", "peptides"]
        },
        {
            "product_id": 109,
            "name": "Barrier Protection Balm",
            "category": "balm",
            "suitable_for": ["sensitive", "dry"],
            "concerns_targeted": ["wind burn", "cold damage"],
            "key_ingredients": ["shea butter", "panthenol"]
        }
    ]
    return pd.DataFrame(data)
