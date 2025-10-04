import sys
import streamlit as st
from users import get_dummy_users
from products import get_dummy_products
from weather import fetch_weather_data, summarize_daily_weather
from skinscore import add_skincare_score
from product_recommendation import recommend_products, group_and_sort_products, APPLICATION_ORDER

# --- Get user ID from command-line argument ---
if len(sys.argv) < 2:
    st.error("Usage: python -m streamlit run app.py <UserID>")
    st.stop()

try:
    user_id = int(sys.argv[1])
except ValueError:
    st.error("UserID must be an integer.")
    st.stop()

# --- Load users and products ---
users = get_dummy_users()
products_db = get_dummy_products()

# --- Find the user by ID ---
user_row = users[users["user_id"] == user_id]
if user_row.empty:
    st.error(f"User with ID '{user_id}' not found in database.")
    st.stop()
user_row = user_row.iloc[0]

# --- Welcome message ---
st.title(f"Welcome {user_row['name']}! Your Personalized Skincare Routine")

# --- User info ---
st.write(f"**Location:** {user_row['location']}")
st.write(f"**Skin type:** {user_row['skin_type']}")
st.write(f"**Concerns:** {', '.join(user_row['skin_concerns'])}")
st.write(f"**Owned products:** {', '.join(user_row['owned_products']) if user_row['owned_products'] else 'None'}")

# --- Weather & Skin Score ---
df_weather = fetch_weather_data(user_row["lat"], user_row["lon"])
daily_summary = summarize_daily_weather(df_weather)
daily_with_score = add_skincare_score(daily_summary, user_row["skin_type"])

st.subheader("🌤 Weather Summary + Skin Stress")
st.dataframe(
    daily_with_score[["date", "min_temp", "max_temp", "avg_humidity", "skincare_score", "skincare_recs"]]
)

# --- Product Recommendations ---
recs_from_weather, owned_recs, new_recs, routine = recommend_products(user_row, daily_with_score, products_db)

st.subheader("💡 Recommendations based on today’s conditions")

# Weather-driven needs
st.markdown("### 🌤 Weather-driven needs")
if recs_from_weather:
    st.info(recs_from_weather)
else:
    st.write("No special weather-driven needs today. Keep your routine consistent!")

# Owned products
st.markdown("### ✅ Useful from owned products")
if owned_recs:
    cols = st.columns(min(len(owned_recs), 4))  # max 4 per row for layout
    for idx, p in enumerate(owned_recs):
        with cols[idx % 4]:
            st.success(p)
else:
    st.write("No owned products match today’s needs.")

# New products
st.markdown("### ✨ Suggested new products")
if new_recs:
    cols = st.columns(min(len(new_recs), 4))
    for idx, p in enumerate(new_recs):
        with cols[idx % 4]:
            st.warning(p)
else:
    st.write("No new products needed today!")

# --- Step-by-step AM/PM routines as cards ---
for time_of_day in ["AM", "PM"]:
    st.subheader(f"🕘 {time_of_day} Routine")
    if routine.get(time_of_day):
        grouped = group_and_sort_products(routine[time_of_day], products_db)
        if grouped:
            for cat, items in grouped.items():
                with st.container():
                    st.markdown(f"### {cat.capitalize()}")
                    cols = st.columns(min(len(items), 4))  # max 4 per row
                    for idx, p in enumerate(items):
                        with cols[idx % 4]:
                            st.info(p)
        else:
            st.write("No steps required in this routine.")
    else:
        st.write("No routine suggested for this time of day.")
