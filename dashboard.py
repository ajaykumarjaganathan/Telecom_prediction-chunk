@st.cache_data
def load_default_data():
    # Example loading from a URL
    url = "https://raw.githubusercontent.com/yourusername/yourrepo/main/yourdata.csv"
    try:
        return pd.read_csv(url)
    except:
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
