
## These are my projects:

### [Master's Thesis: ML and DL in MoCap](https://github.com/Mohammadbk93/projects/blob/main/PPG_Signal_Processing.ipynb)
Project Aim:
The goal of this project was to develop an advanced Human Activity Recognition (HAR) system using both traditional and deep learning models, with a focus on CNN-LSTM architecture. The system aimed to improve the accuracy and robustness of motion recognition in sports, rehabilitation, and ergonomics by addressing key challenges such as feature extraction, data imbalance, and noise in sensor data. Through the use of hybrid models like CNN-LSTM, the project successfully integrated temporal and spatial features, leading to significant performance improvements.

Results:
The CNN-LSTM model achieved a high accuracy of 94.78%, demonstrating its effectiveness in motion recognition tasks compared to traditional ML models. This approach significantly enhanced real-time motion recognition capabilities, particularly in complex scenarios involving diverse activities and sensor data.

<p align="center">
  <img src="https://github.com/user-attachments/assets/28f78d73-23f7-4e9e-bcec-85cbea27bf5c" width="300" height="300">
  <img src="https://github.com/user-attachments/assets/31470d3e-77f8-46f7-968f-427aeb2bbd6e" width="300" height="300">
  <img src="https://github.com/user-attachments/assets/76480683-5005-45ef-93af-6762c175d6ad" width="300" height="300">
</p>

____________________________________________________________________________________________________________
### [Biomedical Signal Processing: PPG-Based Heart Condition Detection](https://github.com/Mohammadbk93/projects/blob/main/PPG_Signal_Processing.ipynb)  

##  Overview  
This project analyzes **Photoplethysmogram (PPG) signals** to classify **Normal** vs **Myocardial Infarction (MI)** conditions using **Machine Learning (Random Forest)** and **Deep Learning (LSTM)**. The dataset comes from the **UCI Machine Learning Repository**.  

## 📊 Dataset  
- **Source**: [UCI Machine Learning Repository]  
- **Type**: Time-series PPG signals  
- **Features**: 2000 signal amplitudes per sample  
- **Labels**:  
  - **Normal** (Healthy)  
  - **MI (Heart Attack Risk)**  

##  Methods & Techniques  
✅ **Signal Processing**: Butterworth filter for noise removal  
✅ **Feature Engineering**: Extracted Mean, StdDev, Min, Max, Skewness, Kurtosis  
✅ **Machine Learning**: **Random Forest** 
✅ **Deep Learning**: **Bi-LSTM with Regularization** 

## 📌 Results & Insights  
- **Random Forest slightly outperformed LSTM** in accuracy.  
- **Filtering improved data quality**, enhancing model performance.  
- **LSTM is better suited for long-term sequence learning** but requires tuning.  
____________________________________________________________________________________________________________

## Data analysis
### [COVID_Pandas_Numpy](https://github.com/Mohammadbk93/projects/blob/main/COVID%20Pandas%2C%20Numpy.ipynb)
# 🦠 COVID-19 Data Analysis & Monte Carlo Integration  

## 📌 Project Overview  
This project analyzes a **large-scale COVID-19 dataset (327K+ rows)** using **Python, Pandas, NumPy, Dask, and PySpark**. It includes:  
- **Exploratory Data Analysis (EDA)**: Extracting trends, case growth, and country-wise infection patterns.  
- **Monte Carlo Integration**: Estimating function integrals using **Dask & PySpark** for parallel computing.  
- **Optimized Data Processing**: Leveraging distributed computing to handle large datasets efficiently.  

---

##  Features  
✅ **Data Preprocessing**: Cleaning and transforming large COVID-19 datasets.  
✅ **Exploratory Data Analysis (EDA)**: Identifying trends and patterns in case growth.  
✅ **Monte Carlo Integration**: Estimating integrals using **random sampling techniques**.  
✅ **Parallel Computing**: Using **Dask & PySpark** for scalable and faster computations.  
✅ **Data Visualization**: Plotting **Monte Carlo simulations** to illustrate results.  

---

##  Technologies Used  
- **Python** (Data analysis & scripting)  
- **Pandas & NumPy** (Data processing & statistical analysis)  
- **Dask & PySpark** (Parallel computing for large datasets)  
- **Matplotlib & Seaborn** (Data visualization)  

---

##  Dataset  
- The dataset contains **COVID-19 case records** across multiple countries.  
- It includes **dates, locations, cumulative cases, and recovery rates**.  

---

##  Methodology  
1. **Data Cleaning & Processing**  
   - Imported the dataset using **Pandas** and handled missing values.  
   - Filtered country-specific data for targeted analysis.  

2. **Exploratory Data Analysis (EDA)** 📊  
   - Identified **worst-case infection days** and **country-wise trends**.  
   - Analyzed seasonal patterns in case spikes.  

3. **Monte Carlo Integration**   
   - Used **random sampling techniques** to estimate function integrals.  
   - Parallelized computations using **Dask & PySpark** for scalability.  

4. **Visualization & Insights** 📉  
   - Created **scatter plots** to visualize Monte Carlo estimations.  
   - Plotted **COVID-19 case distribution trends** over time.  

____________________________________________________________________________________________________________
## Blockchain

### [Sha256 & RSA](https://github.com/Mohammadbk93/projects/blob/main/Project%20SHA256%20%26%20RSA-Copy1.ipynb)
In this project I used `sha256 and RSA`
This project involves the development of a Python program that combines two essential cryptographic functions: the implementation of the SHA-256 hashing algorithm and the creation of digital signatures using the RSA algorithm. These cryptographic functions are vital for securing data and ensuring the integrity of digital information.
____________________________________________________________________________________________________________
##Time_Series

### [TimeSeries_Forcasting](https://github.com/Mohammadbk93/projects/blob/main/time_series_forecasting_in_tensorflow.Project.ipynb)
Aim of the Project:
The aim of this project is to develop and compare various deep learning models for time series forecasting using TensorFlow. The focus is on predicting future values of a dataset by training models on historical data and evaluating their performance based on Mean Absolute Error (MAE).

<img width="484" alt="Screenshot 2024-08-06 130905" src="https://github.com/user-attachments/assets/32b84030-7d81-4e74-a4ef-53bf1e90887f">
____________________________________________________________________________________________________________
## API Integration and Automation

### [Stock_Market_and_News_API](https://github.com/Mohammadbk93/projects/blob/main/Stock_Market_and_News_API.ipynb)
This project integrates two APIs—Alpha Vantage (for stock market data) and News API (for retrieving related news articles) to monitor stock performance and fetch relevant news articles when certain thresholds are met.

Learning purposes:
- Combining multiple APIs in a single workflow to build a cohesive project.
- Handling API responses and parsing JSON data to extract actionable insights.
- Working with conditional logic to trigger specific actions based on data thresholds.
- The basics of working with external APIs for real-time data integration.

____________________________________________________________________________________________________________
## OAuth 2.0 Authentication and Automation

### [Google Sheets Integration with OAuth 2.0](https://github.com/Mohammadbk93/projects/blob/main/Google_Sheets_Automation_with_Python.ipynb)
This project focuses on automating calculations and updates in a Google Sheet using the Google Sheets API and Python. It demonstrates how to programmatically interact with Google Sheets to perform repetitive tasks efficiently. The project uses OAuth 2.0 for secure API authentication and showcases efficient, automated data processing workflows.

Learning purposes:
- Working with the Google Sheets API for data automation.
- Understanding and implementing OAuth 2.0 for secure authentication.
- Automating repetitive tasks using Python.
____________________________________________________________________________________________________________
## Product Matching and Price Comparison
### [Product Matching and Price Comparison](https://github.com/Mohammadbk93/projects/blob/main/Assignment_task%20(1).ipynb)

This project aims to streamline the process of detecting product overlaps between two datasets by combining **text similarity analysis** with **price comparison**.  
It is designed for scenarios such as e-commerce catalog cleaning, marketplace price monitoring, and duplicate product detection.

By comparing product names, brands, and prices, the system identifies items that are likely the same but may have **different listings or inconsistent prices**.

<img width="482" height="162" alt="Matching product" src="https://github.com/user-attachments/assets/856dff6b-ddc3-48ac-8b0c-fbee8d2727c0" />


## Objective

- Match products from two sources based on name similarity
- Calculate and analyze price differences
- Visualize matches and pricing trends
- Export results for further review

## Key Steps

1. Clean and preprocess product names
2. Compute similarity scores (e.g., fuzzy matching)
3. Filter matches above a similarity threshold (e.g., 70%)
4. Calculate absolute price differences
5. Visualize results with histograms and bar charts
6. Export matched results to CSV

## Output

- `all_matched_price_diff.csv` – full list of matched products with price differences
- Plots showing similarity and price distributions

This project was developed for an assignment involving product comparison and data analysis.

____________________________________________________________________________________________________________

### [Random Number Generator](https://github.com/Mohammadbk93/projects/blob/main/Project%20SHA256%20%26%20RSA-Copy1.ipynb)
### [Caffe machine](https://github.com/Mohammadbk93/projects/blob/main/Coffe%20machine/main.py)
### [Tip Calculator](https://github.com/Mohammadbk93/projects/blob/main/Tip%20Calculator%20Project%20-%20Copy.py)
### [Mail Merging](https://github.com/Mohammadbk93/projects/blob/main/Mail%20Merge%20Project%20Start/main.py)


## Gaming
### [Higher Lower Game](https://github.com/Mohammadbk93/projects/blob/main/Higher%20lower%20game/main.py)


```
print('hello')
```
____________________________________________________________________________________________________________
