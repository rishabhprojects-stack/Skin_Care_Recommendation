from collections import OrderedDict

# Typical skincare application order
APPLICATION_ORDER = [
    "cleanser",
    "toner",
    "serum",
    "hydrator",
    "moisturizer",
    "cream",
    "balm",
    "mattifier",
    "sunscreen",
    "treatment",
    "other"
]

def group_and_sort_products(products_list, products_db):
    """
    Group products by category and sort categories by APPLICATION_ORDER.
    Returns OrderedDict of category -> list of products.
    """
    grouped = {}
    for p in products_list:
        product_row = products_db[products_db["name"] == p]
        if not product_row.empty:
            category = product_row.iloc[0]["category"]
        else:
            category = "other"
        grouped.setdefault(category, []).append(p)

    ordered_grouped = OrderedDict()
    for cat in APPLICATION_ORDER:
        if cat in grouped:
            ordered_grouped[cat] = grouped[cat]
    for cat in grouped:
        if cat not in ordered_grouped:
            ordered_grouped[cat] = grouped[cat]

    return ordered_grouped


def recommend_products(user_row, daily_with_score, products_db):
    """
    Generate personalized recommendations based on weather, skin type, and concerns,
    and split into smarter AM/PM routines.
    """
    owned_names = set(user_row["owned_products"])
    owned_products = products_db[products_db["name"].isin(owned_names)]

    today = daily_with_score.iloc[0]
    recs_from_weather = today["skincare_recs"].lower()

    owned_recs = []
    new_recs = []

    # --- Weather-driven recs ---
    if "moisturizer" in recs_from_weather or "cream" in recs_from_weather:
        owned_recs.extend(owned_products[owned_products["category"].isin(["moisturizer", "cream"])]["name"].tolist())
        new_recs.extend(products_db[(products_db["category"].isin(["moisturizer", "cream"])) & (~products_db["name"].isin(owned_names))]["name"].tolist())

    if "spf" in recs_from_weather:
        owned_recs.extend(owned_products[owned_products["category"] == "sunscreen"]["name"].tolist())
        new_recs.extend(products_db[(products_db["category"] == "sunscreen") & (~products_db["name"].isin(owned_names))]["name"].tolist())

    if "serum" in recs_from_weather:
        owned_recs.extend(owned_products[owned_products["category"] == "serum"]["name"].tolist())
        new_recs.extend(products_db[(products_db["category"] == "serum") & (~products_db["name"].isin(owned_names))]["name"].tolist())

    if "balm" in recs_from_weather:
        owned_recs.extend(owned_products[owned_products["category"] == "balm"]["name"].tolist())
        new_recs.extend(products_db[(products_db["category"] == "balm") & (~products_db["name"].isin(owned_names))]["name"].tolist())

    # --- Skin type baseline needs ---
    skin_type = user_row["skin_type"].lower()
    if skin_type == "dry":
        new_recs.extend(products_db[(products_db["category"].isin(["hydrator", "serum"])) & (~products_db["name"].isin(owned_names))]["name"].tolist())
    elif skin_type == "oily":
        new_recs.extend(products_db[(products_db["category"].isin(["gel cleanser", "mattifier"])) & (~products_db["name"].isin(owned_names))]["name"].tolist())
    elif skin_type == "sensitive":
        new_recs.extend(products_db[(products_db["category"].isin(["soothing cream", "balm"])) & (~products_db["name"].isin(owned_names))]["name"].tolist())

    # --- Skin concerns targeted boosters ---
    for concern in user_row["skin_concerns"]:
        concern = concern.lower()
        if "acne" in concern:
            new_recs.extend(products_db[(products_db["category"] == "anti-acne") & (~products_db["name"].isin(owned_names))]["name"].tolist())
        if "fine lines" in concern or "wrinkles" in concern:
            new_recs.extend(products_db[(products_db["category"] == "anti-aging") & (~products_db["name"].isin(owned_names))]["name"].tolist())
        if "dullness" in concern:
            new_recs.extend(products_db[(products_db["category"] == "brightening") & (~products_db["name"].isin(owned_names))]["name"].tolist())

    # Deduplicate
    owned_recs = list(set(owned_recs))
    new_recs = list(set(new_recs))

    # --- Smart AM/PM routines ---
    routine = {"AM": [], "PM": []}

    all_products = owned_recs + new_recs

    for p in all_products:
        p_lower = p.lower()

        # AM routine logic
        if ("spf" in p_lower) or ("day" in p_lower) or ("hydrating serum" in p_lower) or ("light" in p_lower):
            routine["AM"].append(p)
        # PM routine logic
        elif ("night" in p_lower) or ("repair" in p_lower) or ("cream" in p_lower) or ("serum" in p_lower):
            routine["PM"].append(p)

        # Add products based on skin type/concerns
        if skin_type == "oily" and "mattifier" in p_lower:
            routine["AM"].append(p)
        if skin_type == "dry" and ("rich" in p_lower or "hydrator" in p_lower):
            routine["PM"].append(p)
        if "anti-aging" in p_lower or "brightening" in p_lower:
            routine["PM"].append(p)
        if "anti-acne" in p_lower:
            routine["AM"].append(p)

    # Deduplicate routines
    routine["AM"] = list(set(routine["AM"]))
    routine["PM"] = list(set(routine["PM"]))

    return today["skincare_recs"], owned_recs, new_recs, routine
