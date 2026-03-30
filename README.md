# 🍽️ **Swiggy Restaurant Data Collection and Analysis for Restaurant Success Prediction**

## 📌 Project Overview

This project focuses on collecting restaurant data from **Swiggy** using location-based API requests.  
Restaurant data is gathered from multiple cities and areas using latitude and longitude coordinates.

The collected data is stored in a structured format and used for data cleaning, exploratory data analysis (EDA), preprocessing and machine learning tasks such as restaurant performance or success prediction.

Key tasks performed in this project:

- Collected restaurant data using Swiggy API
- Used latitude and longitude for location-based scraping
- Implemented pagination using offset values
- Extracted restaurant-level features
- Stored data into CSV format
- Performed basic data cleaning
- Conducted exploratory data analysis (EDA)

---

## 📊 Dataset Description

The dataset contains restaurant-level information collected from Swiggy listings.

### Dataset File

swiggy_clean_dataset.csv


### Features Included

| Column Name | Description |
|-------------|-------------|
| restaurant_id | Unique identifier for each restaurant |
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
| success | Derived feature indicating restaurant success based on rating and votes thresholds |


### Dataset Characteristics

- Data collected from multiple cities and areas
- Restaurants fetched using latitude and longitude coordinates
- Pagination handled using offset values
- Duplicate restaurants may occur across nearby areas
- Duplicate records can be identified using `restaurant_id`
- Basic data cleaning performed on rating, votes, and price fields
- Dataset exploratory data analysis, preprocessing and prepared for modeling

---

## Success Metric

A restaurant is considered **successful** based on customer engagement 
and satisfaction indicators available in the dataset.

The **success** column is created using the following conditions:

- Restaurant rating ≥ 4.0  
- Number of votes ≥ 1000  

If both conditions are satisfied:

success = 1 (Successful Restaurant)

Otherwise:

success = 0 (Not Successful)

This metric helps identify high-performing restaurants based on 
customer popularity and feedback.

## ⚙️ Setup Instructions

Follow these steps to run the project after downloading the project from GitHub

### Install Required Libraries

Install the necessary Python libraries:

```bash
pip install requests
pip install pandas
pip install numpy
pip install matplotlib
pip install seaborn
```

###
