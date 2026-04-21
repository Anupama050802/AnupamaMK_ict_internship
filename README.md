# 🍽️ Swiggy Restaurant Data Collection and Restaurant Success Prediction System

---

# 📌 Project Overview

This project focuses on **data collection, analysis, machine learning model building, and GenAI-powered web deployment** for predicting restaurant success.

The system uses Swiggy restaurant data collected from multiple cities using location-based API requests (latitude & longitude). The collected data is cleaned, analyzed, and used to build a machine learning model which is then deployed as a **Flask web application integrated with Google Gemini AI**.

---

# Week 1 — Data Collection

- Collected restaurant data using Swiggy API
- Used latitude and longitude for location-based scraping
- Implemented pagination using offset values
- Extracted restaurant-level features
- Stored data into CSV format
- Performed basic data cleaning
- Conducted exploratory data analysis (EDA)
- Added more data which helped increase the model performance

---

# Week 2 — Data Cleaning & Preprocessing

- Removed duplicate restaurants using `restaurant_id`
- Cleaned rating, votes, and price columns
- Dropped the unnecessary and pre-existing columns after feature creation
- Applied preprocessing using **ColumnTransformer**
- Performed:
  - Standardization of numerical features
  - One-hot encoding of categorical variables
  - Binary feature passthrough
  - Ordinal encoding of columns with order
- Saved machine-learning-ready dataset
---

# Week 3 — Model Building, Evaluation & Optimization

Model Development

Built and compared multiple models using **pipeline**:

- Logistic Regression
- K-Nearest Neighbors (KNN)
- Support Vector Classifier (SVC)
- Decision Tree
- Random Forest
- Gradient Boosting
- XGBoost (Best performing model)

Hyperparameter Tuning

Applied RandomizedSearchCV for optimization with tuned parameters and identified best-performing configuration for XGBoost

Model Evaluation

Models were evaluated using:Accuracy,Precision,Recall,F1-score,ROC-AUC

Key Results

XGBoost achieved the best classification performance
- Accuracy ≈ 93%
- Precision ≈ 94%
- Recall ≈ 98%
- F1-score ≈ 0.96


---

# Week 4 — Flask App + GenAI Deployment


The trained model is deployed using **Flask web framework** and hosted on **Render Cloud Platform**.

The system is enhanced with **Google Gemini (Generative AI)** to provide business improvement suggestions.

---

# 🌐 Flask Web Application

## 🔹 Features

- Takes restaurant input from user:
  - City
  - Area
  - Cuisine
  - Price for two
  - Online delivery availability
  - Votes

- Performs feature engineering:
  - City tier classification
  - Cuisine encoding
  - Price bucket creation
  - Log transformation of votes

- Predicts restaurant success using ML model
- Displays prediction result in real-time
- Sends data to Gemini AI for suggestions

---

## 🔹 Frontend

- Simple HTML form-based UI
- Clean and responsive design
- Displays:
  - Prediction result
  - AI suggestions
  - GenAI prompt used

---

# 🧠 GenAI Prompt Design (Google Gemini)

```text
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

```

### Example 1
### City-Bangalore,Area- Jayanagar

🧠 GenAI Prompt Used:

        
You are an expert restaurant business consultant.

Restaurant Details:

Prediction Result: Successful Restaurant
Price Category: Medium
Votes Received: 5000.0
Online Delivery: 1
Restaurant Density: High
Number of Cuisines: 6

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

### Example 2
### City-Kochi,Area-MG Road

🧠 GenAI Prompt Used:


        
You are an expert restaurant business consultant.

Restaurant Details:

Prediction Result: Not Successful
Price Category: Medium
Votes Received: 200.0
Online Delivery: 1
Restaurant Density: Low
Number of Cuisines: 4

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

### Refer the sample screenshots of app in the sample_outputs folder
---

## 📊 Dataset Description

The dataset contains restaurant-level information collected from Swiggy listings.

### Dataset Files

UPDATED
- swiggy_raw_dataset_final.csv
- swiggy_clean_dataset_final.csv


### Features Included

| Column Name | Description |
|-------------|-------------|
| name | Restaurant name |
| link | Restaurant menu link |
| city | City where the restaurant is located |
| area | Restaurant locality |
| cuisine | Types of cuisines served |
| rating | Average customer rating |
| votes | Total number of ratings received |
| has_online_delivery | Delivery availability (1 = Yes, 0 = No) |
| has_table_booking | Table booking availability (0 for delivery restaurants) |
| price_for_two | Cost for two people |
| cuisine_count | Number of cuisines offered by the restaurant |
| success | Derived feature indicating restaurant success based on rating thresholds |
| votes_log | Log-transformed votes |
| price_bucket | Price category (Low, Medium, High, Luxury) |
| city_tier | Tier classification of city |
| restaurant_density | Density level of restaurants in area |


### Characteristics

- Data collected from multiple cities and areas
- Pagination handled using offset values
- Duplicate restaurants may occur across nearby areas
- Duplicate records can be identified using restaurant_id,restaurants whose name,city and area is same are removed
- Basic data cleaning performed on rating, votes, and price fields
- Missing values handled during cleaning
- Outliers handled and log transformation applied where necessary
- Feature engineering applied to improve model performance
- Dataset transformed using preprocessing pipeline
- Dataset exploratory data analysis, preprocessing will prepare for modeling
- Machine learning models built and evaluated using multiple algorithms in pipeline with confusion metric
- Hyperparameter tuning applied to optimize model performance
- Evaluation using multiple metrics (Accuracy, Precision, Recall, F1-score, ROC-AUC) to assess performance comprehensively
- Feature Importance analysis helped understand the how and which are the features that are most important and influenced the most in success prediction.
- Generated pickle file of xgboost model pipeline and area counts for flask app
- Flask web application developed for real-time restaurant success prediction
- User inputs processed and converted into model-ready features
- Google Gemini (GenAI) integrated for generating business improvement suggestions
- Custom prompt designed to produce structured AI recommendations
- Full-stack deployment completed using Flask backend and HTML frontend
- Application deployed on Render cloud platform for live access

---

## Success Metric

A restaurant is considered **successful** based on customer engagement
and satisfaction indicators available in the dataset.

The **success** (target)column is created using the following conditions:

- Restaurant rating ≥ 4.1   

If the condition is satisfied:

success = 1 (Successful Restaurant)

Otherwise:

success = 0 (Not Successful)

This metric helps identify high-performing restaurants based on
customer popularity and feedback.

## ⚙️ Setup Instructions

Follow the notebooks to run the project after downloading the dataset and project from GitHub

1️⃣ Clone the Repository

git clone https://github.com/Anupama050802/AnupamaMK_ict_internship.git

2️⃣ Install Required Libraries

Install the necessary Python libraries if required:

pip install requests
pip install pandas
pip install numpy
pip install matplotlib
pip install seaborn
pip install scikit-learn

3️⃣ Run the Notebooks

4️⃣ Run Flask App

python app.py

Deployment (Render)

🔗 Live Link

https://restaurant-success-prediction-app.onrender.com/


###
