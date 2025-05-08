import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import statsmodels.api as sm

# Load the trained model
model = joblib.load('xgb_model.pkl')

# Calculate the prediction function
def predict_churn(input_data):
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)
    prediction_proba = model.predict_proba(input_df)
    churn_rate = prediction_proba[0][1] * 100
    return churn_rate

# Generate recommendations based on input data
def generate_recommendations(input_data, churn_rate):
    recommendations = []
    
    # High churn rate (greater than 75%)
    if churn_rate > 75:
        recommendations.append("Customer is very likely to churn. Consider offering a significant discount or promotion to retain the customer.")
        if input_data['OverageMinutes'] > 100:
            recommendations.append("Provide a higher plan with more minutes to avoid overage charges.")
        if input_data['CustomerCareCalls'] > 10:
            recommendations.append("Investigate the reasons for frequent customer care calls and improve the service.")
        if input_data['RoamingCalls'] > 5:
            recommendations.append("Offer a special roaming plan to reduce costs for the customer.")
    
    # Moderate to high churn rate (between 50% and 75%)
    elif 50 < churn_rate <= 75:
        recommendations.append("Customer shows signs of dissatisfaction. Consider the following actions to improve satisfaction:")
        if input_data['MonthlyRevenue'] > 70:
            recommendations.append("Offer a discount or value-added services to increase perceived value.")
        if input_data['OverageMinutes'] > 50:
            recommendations.append("Review the current plan and suggest a plan with higher included minutes.")
        if input_data['CustomerCareCalls'] > 5:
            recommendations.append("Enhance customer care interactions to resolve issues more effectively.")
        if input_data['RoamingCalls'] > 3:
            recommendations.append("Provide information about roaming cost-saving options.")
    
    # Low to moderate churn rate (between 25% and 50%)
    elif 25 < churn_rate <= 50:
        recommendations.append("Customer satisfaction seems moderate. Consider the following to enhance their experience:")
        if input_data['MonthlyRevenue'] > 50:
            recommendations.append("Check if the current plan aligns with customer usage patterns and suggest adjustments if needed.")
        if input_data['OverageMinutes'] > 20:
            recommendations.append("Educate the customer on usage monitoring to avoid overage charges.")
        if input_data['CustomerCareCalls'] > 3:
            recommendations.append("Proactively follow up on past customer care interactions to ensure satisfaction.")
    
    # Low churn rate (less than 25%)
    else:
        recommendations.append("Customer seems satisfied based on current data. Continue monitoring their usage and feedback.")
        if input_data['MonthlyRevenue'] > 50:
            recommendations.append("Offer loyalty rewards or incentives to maintain their satisfaction.")
    
    return recommendations

# Set colour based on churn rate
def get_churn_color(churn_rate):
    # Define a gradient from green (low churn) to red (high churn)
    if churn_rate <= 50:
        green = 255
        red = int(255 * (churn_rate / 50))
        return f'rgb({red}, {green}, 0)'  # Green to Yellow
    else:
        red = 255
        green = int(255 * ((100 - churn_rate) / 50))
        return f'rgb({red}, {green}, 0)'  # Yellow to Red

# Set the custom theme and additional styles
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #f8f9fa;
        padding: 20px;
        color: #343a40;
    }
    .sidebar .sidebar-content {
        background-color: #343a40;
        color: white;
    }
    .stButton>button {
        background-color: #343a40;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 1em;
        width: 100%;
        margin: 5px 0;
    }
    .stButton>button:hover {
        background-color: #23272b;
    }
    .stSlider>div>div>div>div {
        background: #343a40;
    }
    .container {
        padding: 1.5em;
        background: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 2em;
        color: #343a40;
    }
    .header {
        font-size: 2.5em;
        font-weight: bold;
        color: #343a40;
        margin-bottom: 0.5em;
        text-align: center;
    }
    .subheader {
        font-size: 1.5em;
        font-weight: bold;
        color: #23272b;
        margin-bottom: 1em;
        text-align: center.
    }
    .card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        color: #343a40;
    }
    .card h4 {
        color: #343a40;
    }
    .card p {
        color: #343a40;
    }
    .tooltip {
        display: inline-block;
        position: relative;
        cursor: pointer;
        border-bottom: 1px dotted black.
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 5px;
        padding: 5px 0;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1.
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define the navigation
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'input_data' not in st.session_state:
    st.session_state.input_data = {}
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False

# Define the navigation
def set_page(page):
    st.session_state.page = page

# Sidebar header
st.sidebar.title("Navigation Bar")

# Home page
if st.session_state.page == "Home":
    st.image('https://miro.medium.com/v2/resize:fit:1400/0*8Iu_eymr6eR-YuQw', use_column_width=True)
    st.title("Telecom Customer Churn Prediction")
    st.write("""
        Welcome to the Telecom Customer Churn Prediction App. This application helps you predict whether a customer will churn based on their usage and other parameters.
             
             
    """)
    st.write("Let's get started by navigating to the 'Predict Churn' page!")

    st.sidebar.button("Home", on_click=set_page, args=("Home",))
    st.sidebar.button("Predict Churn", on_click=set_page, args=("Predict Churn",))
    st.sidebar.button("Results", on_click=set_page, args=("Results",))
    st.sidebar.button("Dashboard", on_click=set_page, args=("Dashboard",))

# Predict Churn page
elif st.session_state.page == "Predict Churn":
    st.title("Predict Customer Churn")
    st.write('<div class="subheader">Please input the customer details below</div>', unsafe_allow_html=True)

    with st.form("customer_data_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            MonthlyRevenue = st.number_input('Monthly Revenue', min_value=0.0, max_value=1000.0, value=0.0, step=0.1, help="Monthly revenue of the customer in dollars.")
            MonthlyMinutes = st.number_input('Monthly Minutes', min_value=0.0, max_value=5000.0, value=0.0, step=10.0, help="Total minutes used by the customer in a month.")
            DirectorAssistedCalls = st.slider('Director Assisted Calls', min_value=0, max_value=50, value=0, step=1, help="Number of calls assisted by a director.")
            OverageMinutes = st.number_input('Overage Minutes', min_value=0.0, max_value=1000.0, value=0.0, step=1.0, help="Minutes used over the allocated limit.")
            RoamingCalls = st.slider('Roaming Calls', min_value=0, max_value=50, value=0, step=1, help="Number of calls made while roaming.")

        with col2:
            PercChangeMinutes = st.number_input('Percentage Change Minutes', min_value=-100.0, max_value=100.0, value=0.0, step=0.1, help="Percentage change in minutes used from the previous month.")
            PercChangeRevenues = st.number_input('Percentage Change Revenues', min_value=-100.0, max_value=100.0, value=0.0, step=0.1, help="Percentage change in revenue from the previous month.")
            CustomerCareCalls = st.slider('Customer Care Calls', min_value=0, max_value=50, value=0, step=1, help="Number of calls made to customer care.")
            ReceivedCalls = st.slider('Received Calls', min_value=0, max_value=500, value=0, step=1, help="Total number of calls received by the customer.")
            OutboundCalls = st.slider('Outbound Calls', min_value=0, max_value=500, value=0, step=1, help="Total number of outbound calls made by the customer.")

        with col3:
            MonthsInService = st.slider('Months In Service', min_value=0, max_value=100, value=0, step=1, help="Total number of months the customer has been in service.")
            UniqueSubs = st.slider('Unique Subs', min_value=0, max_value=10, value=0, step=1, help="Number of unique subscriptions the customer has.")
            ActiveSubs = st.slider('Active Subs', min_value=0, max_value=10, value=0, step=1, help="Number of active subscriptions the customer has.")
            st.markdown("""
                <div class="tooltip">Income Group <span class="tooltiptext">0: Very Low Income<br>10: Very High Income</span></div>
            """, unsafe_allow_html=True)
            IncomeGroup = st.slider('Income Group', min_value=0, max_value=10, value=0, step=1, help="Income group of the customer on a scale of 0-10.")
            st.markdown("""
                <div class="tooltip">Credit Rating <span class="tooltiptext">0: Very Low Credit Rating<br>6: Very High Credit Rating</span></div>
            """, unsafe_allow_html=True)
            CreditRating = st.selectbox('Credit Rating', options=[0, 1, 2, 3, 4, 5, 6], help="Credit rating of the customer.")
            PrizmCode = st.selectbox('Prizm Code', options=['Suburban', 'Town', 'Rural', 'Other'], help="Prizm code representing the customer's location.")

        submitted = st.form_submit_button("Predict")

    if submitted:
        # Store inputs in session state
        st.session_state.input_data = {
            'MonthlyRevenue': MonthlyRevenue,
            'MonthlyMinutes': MonthlyMinutes,
            'DirectorAssistedCalls': DirectorAssistedCalls,
            'OverageMinutes': OverageMinutes,
            'RoamingCalls': RoamingCalls,
            'PercChangeMinutes': PercChangeMinutes,
            'PercChangeRevenues': PercChangeRevenues,
            'CustomerCareCalls': CustomerCareCalls,
            'ReceivedCalls': ReceivedCalls,
            'OutboundCalls': OutboundCalls,
            'MonthsInService': MonthsInService,
            'UniqueSubs': UniqueSubs,
            'ActiveSubs': ActiveSubs,
            'IncomeGroup': IncomeGroup,
            'CreditRating': CreditRating,
            'PrizmCode_Rural': 1 if PrizmCode == 'Rural' else 0,
            'PrizmCode_Suburban': 1 if PrizmCode == 'Suburban' else 0,
            'PrizmCode_Town': 1 if PrizmCode == 'Town' else 0
        }
        st.session_state.prediction_made = True
        st.session_state.page = "Results"
        st.rerun()

    st.sidebar.button("Home", on_click=set_page, args=("Home",))
    st.sidebar.button("Predict Churn", on_click=set_page, args=("Predict Churn",))
    st.sidebar.button("Results", on_click=set_page, args=("Results",))
    st.sidebar.button("Dashboard", on_click=set_page, args=("Dashboard",))

# Results page
elif st.session_state.page == "Results":
    st.title("Prediction Results")
    if st.session_state.get('prediction_made', False):
        input_data = st.session_state.input_data

        # Predict churn
        churn_rate = predict_churn(input_data)
        
        # Display results
        churn_color = get_churn_color(churn_rate)
        
        st.write('<div class="card">', unsafe_allow_html=True)
        st.write(f'<h4>Prediction Result</h4><p style="color:{churn_color};">Churn probability: <strong>{churn_rate:.2f}%</strong></p></div>', unsafe_allow_html=True)

        st.write('<div class="card">', unsafe_allow_html=True)
        st.subheader('Recommendations')
        recommendations = generate_recommendations(input_data, churn_rate)
        for recommendation in recommendations:
            st.write(f'<p>{recommendation}</p>', unsafe_allow_html=True)
        st.write('</div>', unsafe_allow_html=True)

        # Generate and display the report
        report_data = input_data.copy()
        report_data['Churn Probability (%)'] = churn_rate
        report = pd.DataFrame([report_data]).T
        report.columns = ['Value']
        report['Description'] = [
            'Monthly revenue of the customer in dollars.',
            'Total minutes used by the customer in a month.',
            'Number of calls assisted by a director.',
            'Minutes used over the allocated limit.',
            'Number of calls made while roaming.',
            'Percentage change in minutes used from the previous month.',
            'Percentage change in revenue from the previous month.',
            'Number of calls made to customer care.',
            'Total number of calls received by the customer.',
            'Total number of outbound calls made by the customer.',
            'Total number of months the customer has been in service.',
            'Number of unique subscriptions the customer has.',
            'Number of active subscriptions the customer has.',
            'Income group of the customer on a scale of 0-10.',
            'Credit rating of the customer.',
            '1 if the customer is located in a rural area, otherwise 0.',
            '1 if the customer is located in a suburban area, otherwise 0.',
            '1 if the customer is located in a town, otherwise 0.',
            'Probability that the customer will churn.'
        ]
        
        st.subheader('Report')
        st.dataframe(report)

        # Download report
        st.subheader('Download Report')
        st.download_button("Download Report", report.to_csv().encode('utf-8'), "report.csv", "text/csv", key='download-csv')
    else:
        st.write('<div class="card"><p>No predictions made, please make your prediction at the "Predict Churn" page.</p></div>', unsafe_allow_html=True)

    st.sidebar.button("Home", on_click=set_page, args=("Home",))
    st.sidebar.button("Predict Churn", on_click=set_page, args=("Predict Churn",))
    st.sidebar.button("Results", on_click=set_page, args=("Results",))
    st.sidebar.button("Dashboard", on_click=set_page, args=("Dashboard",))

# Dashboard page
elif st.session_state.page == "Dashboard":
    st.title("Customer Insights Dashboard")
    st.write("This dashboard provides insights into customer data and churn prediction.")

    # File uploader
    uploaded_file = st.file_uploader("Upload your dataset (CSV file)", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Dataset Uploaded Successfully!")
        
        # Interactive filters for the dashboard
        st.write("### Customer Data")
        selected_columns = st.multiselect("Select columns to display", df.columns.tolist(), default=df.columns.tolist())
        st.dataframe(df[selected_columns])

        # Variables for comparison
        st.write("### Compare Variables")
        col1, col2 = st.columns(2)
        with col1:
            x_var = st.selectbox("Select X-axis variable", options=df.columns.tolist(), index=0)
        with col2:
            y_var = st.selectbox("Select Y-axis variable", options=df.columns.tolist(), index=1)

        # Generate and display the plot
        st.write(f"### {x_var} vs {y_var}")
        if df[x_var].dtype == 'object' or df[y_var].dtype == 'object':
            plot = px.histogram(df, x=x_var, color=y_var, barmode='group', title=f'{x_var} vs {y_var}')
        else:
            plot = px.scatter(df, x=x_var, y=y_var, title=f'{x_var} vs {y_var}', labels={x_var: x_var, y_var: y_var}, trendline='ols')

        st.plotly_chart(plot)
    else:
        st.write("Please upload a dataset to visualize.")

    st.sidebar.button("Home", on_click=set_page, args=("Home",))
    st.sidebar.button("Predict Churn", on_click=set_page, args=("Predict Churn",))
    st.sidebar.button("Results", on_click=set_page, args=("Results",))
    st.sidebar.button("Dashboard", on_click=set_page, args=("Dashboard",))
