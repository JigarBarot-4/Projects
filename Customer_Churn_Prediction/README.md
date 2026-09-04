# Telco Customer Churn Prediction

## Approach

The main aim of this project is to predict whether a customer will churn or not. I used the Telco Customer Churn dataset and performed data cleaning, exploratory data analysis and machine learning.

I used Logistic Regression and Decision Tree Classifier for prediction. Logistic Regression was used as the main model because it is simple and good for binary classification. Decision Tree was used for comparison.

## Steps

1. Loaded the Telco Customer Churn dataset using Pandas.
2. Checked the shape, columns, data types and missing values.
3. Converted `TotalCharges` into numeric values.
4. Handled the blank values in `TotalCharges` by replacing them with 0.
5. Removed `customerID` because it is only an identification column.
6. Separated the features and target variable (`Churn`).
7. Converted categorical variables into numerical values using one-hot encoding.
8. Converted Churn values into 0 and 1.
9. Performed EDA using bar chart, boxplot and correlation heatmap.
10. Split the data into training and testing sets.
11. Applied StandardScaler to scale the data.
12. Trained a Logistic Regression model.
13. Trained a Decision Tree model.
14. Evaluated both models using Accuracy, Precision, Recall and F1 Score.
15. Compared the results and selected the better model.
16. Created a prediction function to predict customer churn.

## Results

| Model | Accuracy | Precision | Recall | F1 Score |
|---|---:|---:|---:|---:|
| Logistic Regression | 80.7% | 65.8% | 56.7% | 60.9% |
| Decision Tree | 72.5% | 48.2% | 47.9% | 48.1% |

Logistic Regression performed better than Decision Tree on all four evaluation metrics. Therefore, Logistic Regression was selected as the better model for this project.

## Key Insights

- Customers with month-to-month contracts had more churn compared to customers with one year or two year contracts.
- Customers who churned generally had higher monthly charges.
- Tenure and TotalCharges have a strong relation because customers who stay longer usually have higher total charges.
- The churned customers are less in number compared to the non-churned customers, so the dataset is slightly imbalenced.