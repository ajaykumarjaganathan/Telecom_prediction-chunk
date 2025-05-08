# Telecom Customer Churn Prediction System
## Overview
The Telecom Customer Churn Prediction System is an advanced application designed to predict customer churn and provide actionable recommendations to help telecom companies retain their customers. The system utilizes a trained machine learning model and provides a user-friendly interface for inputting customer data, generating predictions, and visualizing results.

## Features
### Data Input and Prediction
Customer Data Form: A form where users can input customer details such as monthly revenue, monthly minutes, number of customer care calls, overage minutes, and more.

Prediction Engine: Utilizes a pre-trained XGBoost model to predict the likelihood of a customer churning. The prediction is displayed as a churn probability percentage.

Churn Color Indicator: Visual representation of the churn probability using a color gradient from green (low churn) to red (high churn).

## Recommendations
### Customized Recommendations:
Based on the churn probability and customer data, the system generates tailored recommendations to help reduce the likelihood of churn. Recommendations are categorized based on the churn probability range:

## Dashboard
### Customer Insights Dashboard: An interactive dashboard that provides insights into customer data and churn predictions.
Users can filter the displayed data, compare variables, and visualize relationships using histograms and scatter plots.

Data Visualization: Utilizes Plotly for dynamic and interactive data visualization, allowing users to gain insights into factors influencing customer churn.

### Report Generation
Detailed Report: After making a prediction, the system generates a detailed report displaying customer data, churn probability, and descriptive insights.

Downloadable Report: Users can download the report as a CSV file for further analysis and record-keeping.

## User Interface
### Custom Theme and Styles: The application features a custom theme with a clean and modern design. 
The sidebar and buttons are styled for easy navigation, and the main content area is designed for readability and user engagement.

Intuitive Navigation: The sidebar allows users to easily navigate between different sections of the application, including the Home, Predict Churn, Results, and Dashboard pages.
