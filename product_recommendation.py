# product_recommendation.py

# Mapping rules for product application order
APPLICATION_ORDER = {
    # AM essentials
    "SPF": "AM",
    "Sunscreen": "AM",
    "Day Moisturizer": "AM",
    "Vitamin C": "AM",

    # PM essentials
    "Night Repair": "PM",
    "Soothing Cream": "PM",
    "Barrier Protection Balm": "PM",
    "Retinol": "PM",
    "Sleeping Mask": "PM",

    # Flexible (defaults to AM if not specified elsewhere)
    "Moisturizer": "AM",
}


def assign_routine(products):
    """
    Assigns products into AM and PM skincare routines.
    Falls back gracefully if products are not found in APPLICATION_ORDER.
    """

    am_routine = []
    pm_routine = []

    for product in products:
        assigned = False
        for key, slot in APPLICATION_ORDER.items():
            if key.lower() in product.lower():
                if slot == "AM":
                    am_routine.append(product)
                else:
                    pm_routine.append(product)
                assigned = True
                break

        # fallback if product not explicitly in APPLICATION_ORDER
        if not assigned:
            if "cream" in product.lower():
                pm_routine.append(product)
            else:
                am_routine.append(product)

    # ensure routines are never empty
    if not am_routine:
        am_routine.append("Gentle Cleanser")
    if not pm_routine:
        pm_routine.append("Basic Moisturizer")

    return am_routine, pm_routine


def recommend_products(user_row, daily_with_score, products_db):
    """
    Recommend skincare products based on:
    - User’s skin type and concerns
    - Weather-driven needs (from skinscore)
    - Owned products vs new suggestions
    """

    # Take today’s weather-driven needs
    today = daily_with_score.iloc[0]
    weather_recs = today.get("skincare_recs", "")

    # Filter useful owned products
    owned_useful = []
    for p in user_row["owned_products"]:
        for keyword in ["SPF", "Moisturizer", "Cream", "Serum", "Balm"]:
            if keyword.lower() in p.lower() and keyword.lower() in weather_recs.lower():
                owned_useful.append(p)

    # Suggested new products (exclude already owned)
    suggested_new = [
        prod for prod in products_db["name"].tolist()
        if prod not in user_row["owned_products"]
    ]

    # Build AM/PM routines
    all_products = owned_useful + suggested_new
    am_routine, pm_routine = assign_routine(all_products)

    return weather_recs, owned_useful, suggested_new, {"AM": am_routine, "PM": pm_routine}


def group_and_sort_products(product_names, products_db):
    """
    Group a list of product names by their category.
    Returns a dict: {category: [product names]}
    """
    grouped = {}
    for name in product_names:
        row = products_db[products_db["name"] == name]
        if not row.empty:
            cat = row.iloc[0]["category"]
            grouped.setdefault(cat, []).append(name)
    return grouped
