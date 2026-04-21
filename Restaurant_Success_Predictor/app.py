import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request

# Gemini imports
from google import genai
from dotenv import load_dotenv
import os
import time

# ==============================
# Load API Key Safely (.env)
# ==============================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

client = genai.Client(api_key=api_key)

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = pickle.load(open(os.path.join(BASE_DIR, "restaurant.pkl"), "rb"))

area_counts = pd.read_pickle(os.path.join(BASE_DIR, "area_counts.pkl"))
# Convert dictionary keys to lowercase
area_counts = {k.lower(): v for k, v in area_counts.items()}

# Tier lists
tier_1_cities = [
    "mumbai","delhi","bangalore",
    "chennai","hyderabad","pune","kolkata"
]

tier_2_cities = [
    "ahmedabad","jaipur","kochi",
    "trivandrum","mysore","coimbatore"
]

top_cuisines=['Desserts', 'Beverages', 'Snacks', 'Chinese', 'North Indian', 'Biryani',
       'Fast Food', 'Bakery', 'Ice Cream', 'Burgers']


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():

    city = request.form['city'].lower()
    area = request.form['area'].lower()
    cuisine = request.form['cuisine']
    price = float(request.form['price'])
    online_delivery=request.form['online_delivery']
    votes = float(request.form['votes'])

    # City tier function
    def city_tier(city):
        if city in tier_1_cities:
            return 1
        elif city in tier_2_cities:
            return 2
        else:
            return 3

    tier = city_tier(city)


    # Clean input area
    area = area.strip().lower()

    count = area_counts.get(area, 0)
    if count >= 16:
        restaurant_density = "High"
    elif count > 8 and count<16:
        restaurant_density = "Medium"
    else:
        restaurant_density = "Low"
    
    print("Location:", area)
    print("Restaurant Count:",count)

    # Cuisine one-hot encoding
    cuisine_features = {}

    cuisine_list = [c.strip().title() for c in cuisine.split(",")]
    cuisine_count = len(cuisine_list)

    for cus in top_cuisines:
        cuisine_features[cus] = 1 if cus in cuisine_list else 0

    cuisine_other = 1 if any(
    c.strip() not in top_cuisines
    for c in cuisine_list
) else 0
    
    def price_buckets(price):
        if price <= 200:
            return "Low"
        elif (price>200 and price <= 600):
            return "Medium"
        elif (price>600 and price <= 1000):
            return "High"
        else:
            return "Luxury"
    price_bucket = price_buckets(price)

    if online_delivery.lower() == 'yes':
        has_online_delivery=1
    else:
        has_online_delivery=0
        

    votes_log = np.log1p(votes)


    # Create dataframe
    input_data = {
        'cuisine_count':cuisine_count,
        'cuisine_other': cuisine_other,
        'has_online_delivery':has_online_delivery,
        'price_bucket': price_bucket,
        'votes_log': votes_log,
        'city_tier': tier,
        'restaurant_density': restaurant_density
    }

    input_data.update(cuisine_features)

    input_df = pd.DataFrame([input_data])

    input_df = input_df.reindex(
    columns=model.feature_names_in_,
    fill_value=0
)
    
    # Predict
    prediction = model.predict(input_df)

    if prediction[0] == 1:
        result = "Successful Restaurant"
    else:
        result = "Not Successful"

    # ==============================
    # GENAI PROMPT DESIGN
    # ==============================

    prompt = f"""
You are an expert restaurant business consultant.

Restaurant Details:

Prediction Result: {result}
Price Category: {price_bucket}
Votes Received: {votes}
Online Delivery: {has_online_delivery}
Restaurant Density: {restaurant_density}
Number of Cuisines: {cuisine_count}

Task:
Suggest exactly 4 short business improvements.

Rules:
- Format each suggestion exactly like this:
  * Action: [10 words max]
  Reason: [10 words max]
- Ensure there is a NEW LINE between Action and Reason.
- Use clear business language
- Use only ONE bullet (*) per improvement
- Avoid long explanations
"""
    
    # ==============================
    # Generate AI Suggestions
    # ==============================

    try:
        ai_suggestions = ""
        for attempt in range(2):   # Try Gemini 2 times
                try:
                    response = client.models.generate_content(
                        model="gemini-flash-latest",
                        contents=prompt
                        )
                    # Get Gemini output
                    ai_suggestions = response.text.strip()
                    # Format AI output (fix alignment & spacing)
                    # # Remove markdown bold
                    if ai_suggestions:
                        break
                except Exception as e:
                    print("Gemini retry:", e)
                    time.sleep(2)   # wait before retry

        # If Gemini still fails → fallback suggestions
        if not ai_suggestions:
            ai_suggestions = (
                "* Action: Improve food presentation\n"
                "  Reason: Attracts more customers\n"
                "* Action: Offer promotional discounts\n"
                "  Reason: Encourages repeat visits\n"
                "* Action: Enhance online visibility\n"
                "  Reason: Expands customer reach\n"
                "* Action: Maintain consistent quality\n"
                "  Reason: Builds customer trust"
                )

        ai_suggestions = ai_suggestions.replace("**", "")
        lines = ai_suggestions.split("\n")
        
        formatted_lines = []
        
        for line in lines:
            clean_line = line.strip()
            if not clean_line:
                continue

            # Case 1: The line contains BOTH Action and Reason (fixes your current image)
            if "*" in clean_line and "Reason:" in clean_line:
                parts = clean_line.split("Reason:")
                action_part = parts[0].strip()
                reason_part = "Reason: " + parts[1].strip()
                formatted_lines.append(action_part)
                formatted_lines.append("  " + reason_part) # Indented on new line
            
            if clean_line.startswith("*"):
                formatted_lines.append(clean_line)
            
            elif clean_line.startswith("Reason:"):
                formatted_lines.append("  " + clean_line)
                           
            else:
                formatted_lines.append(clean_line)
                
        ai_suggestions = "\n".join(formatted_lines)
        
    except Exception as e:
        print("Gemini Error:", e)
        
        ai_suggestions = (
            "AI suggestions currently unavailable."
            )

    return render_template(
        "index.html",
        prediction_text=result,
        ai_text=ai_suggestions,
        prompt_text=prompt
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# if __name__ == "__main__":
#     app.run(debug=True)

