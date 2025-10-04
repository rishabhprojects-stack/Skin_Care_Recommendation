import pandas as pd

def get_dummy_users():
    data = [
        {
            "user_id": 1,
            "name": "Alice",
            "location": "Paris, FR",
            "lat": 48.8566,
            "lon": 2.3522,
            "skin_type": "dry",
            "skin_concerns": ["dehydration", "fine lines"],
            "owned_products": ["Hydrating Serum", "Day Moisturizer SPF 30"]
        },
        {
            "user_id": 2,
            "name": "Ben",
            "location": "Stockholm, SE",
            "lat": 59.3293,
            "lon": 18.0686,
            "skin_type": "oily",
            "skin_concerns": ["acne", "shine"],
            "owned_products": ["Oil-Control Gel", "Lightweight Moisturizer"]
        },
        {
            "user_id": 3,
            "name": "Chloe",
            "location": "Dubai, AE",
            "lat": 25.276987,
            "lon": 55.296249,
            "skin_type": "sensitive",
            "skin_concerns": ["redness", "sun damage"],
            "owned_products": ["Soothing Cream", "SPF 50 Sunscreen"]
        },
        {
            "user_id": 4,
            "name": "David",
            "location": "Toronto, CA",
            "lat": 43.65107,
            "lon": -79.347015,
            "skin_type": "combination",
            "skin_concerns": ["dullness", "uneven tone"],
            "owned_products": ["Vitamin C Serum", "Night Repair Cream"]
        }
    ]
    return pd.DataFrame(data)
