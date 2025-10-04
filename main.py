# main.py – Full Step-by-Step Skincare Planner
import sys
from collections import OrderedDict
from users import get_dummy_users
from products import get_dummy_products
from weather import fetch_weather_data, summarize_daily_weather
from skinscore import add_skincare_score
from product_recommendation import recommend_products

# Define typical skincare application order
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <UserName>")
        sys.exit(1)

    user_name = sys.argv[1]

    # Load users and products
    users = get_dummy_users()
    products_db = get_dummy_products()

    # Find the user
    user_row = users[users["name"].str.lower() == user_name.lower()]
    if user_row.empty:
        print(f"User '{user_name}' not found in database.")
        sys.exit(1)
    user_row = user_row.iloc[0]

    print("=" * 50)
    print(f"👤 User: {user_row['name']} ({user_row['skin_type']} skin, concerns: {', '.join(user_row['skin_concerns'])})")
    print(f"📍 Location: {user_row['location']}")
    print(f"👜 Owned Products: {', '.join(user_row['owned_products'])}")
    print("=" * 50)

    # --- Weather & Skin Stress ---
    df_weather = fetch_weather_data(user_row["lat"], user_row["lon"])
    if df_weather.empty:
        print("⚠️ Could not fetch weather data. Using dummy values instead.")
        sys.exit(1)

    # --- Daily Summary ---
    daily_summary = summarize_daily_weather(df_weather)
    daily_with_score = add_skincare_score(daily_summary, user_row["skin_type"])

    print("\n🌤 Weather Summary + Skin Stress:")
    cols_to_show = ["date", "min_temp", "max_temp", "avg_humidity", "skincare_score", "skincare_recs"]
    print(daily_with_score[cols_to_show].head(2))

    # --- Product Recommendations ---
    recs_from_weather, owned_recs, new_recs, routine = recommend_products(user_row, daily_with_score, products_db)

    print("\n💡 Recommendations based on today’s conditions:")
    print(f"➡ Weather-driven needs: {recs_from_weather}")

    print("\n✅ Useful from owned products:")
    if owned_recs:
        for p in owned_recs:
            print(f"   - {p}")
    else:
        print("   None")

    print("\n✨ Suggested new products to consider:")
    if new_recs:
        for p in new_recs:
            print(f"   - {p}")
    else:
        print("   None")

    # --- Display AM/PM routines as step-by-step plan ---
    for time_of_day in ["AM", "PM"]:
        print(f"\n🕘 {time_of_day} Routine:")
        if routine.get(time_of_day):
            grouped = group_and_sort_products(routine[time_of_day], products_db)
            step_num = 1
            for cat, items in grouped.items():
                print(f"  {cat.capitalize()}:")
                for p in items:
                    print(f"    Step {step_num}: {p}")
                    step_num += 1
        else:
            print("  None")

if __name__ == "__main__":
    main()
