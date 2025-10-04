🌤️💧 Skincare & Environmental Recommendation App

Personalized skincare routines powered by real-time weather data 🌍✨
This app combines user skin profiles (type, concerns, owned products) with live weather conditions to generate:
🌡️ Daily skincare stress scores
💡 Personalized skincare recommendations
🕘 Step-by-step AM/PM skincare routines
Built with Python + Streamlit.

🚀 Features
✅ Fetches real-time weather via OpenWeather API (current + 48h forecast)
✅ Computes daily skin stress scores (humidity, UV, wind, cold, precipitation)
✅ Suggests owned vs. new skincare products
✅ Generates AM/PM routines tailored to user needs
✅ Interactive Streamlit dashboard

🛠️ Tech Stack
Python 3.9+
Streamlit – UI framework
Pandas – data handling
Requests – API calls
OpenWeather API – weather data

📦 Installation
Clone the repo
git clone https://github.com/YOUR_USERNAME/skincare-recommender.git
cd skincare-recommender
Set up a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
Install dependencies
pip install -r requirements.txt
Add your API key
Create a config.py (or .env) file
Add:
OPENWEATHER_API_KEY = "your_api_key_here"
▶️ Usage
Run the app for a specific user ID:
streamlit run app.py -- 1
Example:
User 1 (Alice, Dry Skin, Paris) → Gets hydrating/moisturizing recs.
User 2 (Ben, Oily Skin, Stockholm) → Gets oil-control & SPF recs.

📊 Example Output
🌤 Weather Summary + Skin Stress
Date	Min Temp	Max Temp	Humidity	Score	Recommendations
2025-10-04	12°C	18°C	45%	75	Low humidity – rich moisturizer ...
✅ Owned Products: Hydrating Serum, Day Moisturizer SPF 30
✨ Suggested New Products: Soothing Cream, SPF 50 Sunscreen
🕘 AM Routine: Cleanser → Hydrating Serum → SPF
🌙 PM Routine: Serum → Night Repair Cream
(Add a screenshot here from Streamlit UI – examples/sample_output.png)

📂 Project Structure
skincare-recommender/
│
├── app.py                     # Streamlit app
├── weather.py                 # Weather fetch + summary
├── skinscore.py               # Skincare stress scoring
├── products.py                # Dummy product DB
├── users.py                   # Dummy user DB
├── product_recommendation.py  # Recommendation engine
│
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── LICENSE                    # Open-source license
├── .gitignore                 # Ignore venv/__pycache__
│
├── docs/                      # Documentation
│   └── presentation.md
└── examples/                  # Example screenshots
    └── sample_output.png
    
📌 Roadmap / Future Enhancements
✅ Replace dummy data with a real product/user database
✅ Add UV Index API integration (currently placeholder = 0)
🔮 Deploy app online (Streamlit Cloud / HuggingFace Spaces)
🔮 Add machine learning for smarter recommendations
🔮 Mobile-responsive UI
