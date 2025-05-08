# Dashboard page
elif st.session_state.page == "Dashboard":
    st.title("Customer Insights Dashboard")
    st.write("This dashboard provides insights into customer data and churn prediction.")

    # Load default dataset from GitHub
    @st.cache_data
    def load_default_data():
        url = "https://raw.githubusercontent.com/ajaykumarjaganathan/Telecom_prediction-chunk/main/churn_dataset.csv"
        try:
            df = pd.read_csv(url)
            # Basic cleaning if needed
            df = df.dropna()  # Remove rows with missing values
            return df
        except Exception as e:
            st.error(f"Error loading default dataset: {e}")
            # Fallback to sample data if URL fails
            data = {
                'MonthlyRevenue': [50.0, 75.0, 100.0, 45.0, 80.0],
                'MonthlyMinutes': [300, 450, 600, 250, 500],
                'CustomerCareCalls': [2, 5, 8, 1, 4],
                'OverageMinutes': [10, 45, 80, 5, 30],
                'RoamingCalls': [1, 3, 5, 0, 2],
                'MonthsInService': [12, 24, 6, 36, 18],
                'Churn': [0, 1, 1, 0, 0]
            }
            return pd.DataFrame(data)

    # File uploader with default dataset
    uploaded_file = st.file_uploader("Upload your dataset (CSV file) or use our sample data", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("Uploaded Dataset:")
    else:
        df = load_default_data()
        st.info("Using Default Dataset (you can upload your own data above):")
    
    # Show basic info
    st.write(f"Dataset contains {len(df)} rows and {len(df.columns)} columns")
    
    # Interactive filters for the dashboard
    st.write("### Customer Data Preview")
    selected_columns = st.multiselect(
        "Select columns to display", 
        df.columns.tolist(), 
        default=df.columns.tolist()[:6]  # Show first 6 columns by default
    )
    st.dataframe(df[selected_columns].head(20))

    # Add a section for churn analysis
    st.write("### Churn Analysis")
    if 'Churn' in df.columns:
        churn_counts = df['Churn'].value_counts().reset_index()
        churn_counts.columns = ['Churn', 'Count']
        fig = px.pie(churn_counts, values='Count', names='Churn', 
                     title='Churn Distribution (0 = No, 1 = Yes)')
        st.plotly_chart(fig)
    else:
        st.warning("No 'Churn' column found in the dataset")

    # Variables for comparison
    st.write("### Compare Variables")
    col1, col2 = st.columns(2)
    with col1:
        x_var = st.selectbox("Select X-axis variable", options=df.columns.tolist(), index=0)
    with col2:
        y_var = st.selectbox("Select Y-axis variable", options=df.columns.tolist(), 
                            index=1 if 'Churn' in df.columns else 2)

    # Generate and display the plot
    st.write(f"### {x_var} vs {y_var}")
    if df[x_var].dtype == 'object' or df[y_var].dtype == 'object':
        plot = px.histogram(df, x=x_var, color=y_var, barmode='group', 
                           title=f'{x_var} vs {y_var}')
    else:
        plot = px.scatter(df, x=x_var, y=y_var, title=f'{x_var} vs {y_var}', 
                         labels={x_var: x_var, y_var: y_var}, 
                         color='Churn' if 'Churn' in df.columns else None,
                         trendline='ols')
    st.plotly_chart(plot)

    st.sidebar.button("Home", on_click=set_page, args=("Home",))
    st.sidebar.button("Predict Churn", on_click=set_page, args=("Predict Churn",))
    st.sidebar.button("Results", on_click=set_page, args=("Results",))
    st.sidebar.button("Dashboard", on_click=set_page, args=("Dashboard",))
