import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db

# Firebase initialization
firebase_url = "https://pollutiondata-3ba48-default-rtdb.firebaseio.com/"
cred = credentials.Certificate("your-service-account-key.json")  # Upload this file too
firebase_admin.initialize_app(cred, {
    'databaseURL': firebase_url
})

# Title
st.title("🚗 Pollution Monitoring Dashboard")
st.markdown("Displays high-severity filtered pollution data pushed from Edge to Firebase.")

# Firebase path
data_ref = db.reference('/filtered_pollution_data')

# Fetch and display data
def fetch_data():
    data = data_ref.get()
    if data:
        df = pd.DataFrame.from_dict(data, orient='index')
        df.reset_index(drop=True, inplace=True)
        return df
    else:
        return pd.DataFrame()

df = fetch_data()

if not df.empty:
    st.success("High severity data loaded from Firebase!")
    st.dataframe(df)

    pollutant_cols = ['CO2 Emissions', 'NOx Emissions', 'PM2.5 Emissions', 'VOC Emissions', 'SO2 Emissions']
    st.line_chart(df[pollutant_cols])
else:
    st.warning("No high-severity pollution data found in Firebase.")
