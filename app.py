import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase connection
cred = credentials.Certificate("firebase-key.json")  # 🔁 Updated key filename
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pollutiondata-3ba48-default-rtdb.firebaseio.com/'  # 🔁 Replace with your actual Firebase DB URL
})

st.title("Vehicle Pollution Monitoring Dashboard")

# Fetch data from Firebase
ref = db.reference('/')
data = ref.get()

if data:
    df = pd.DataFrame(data).T  # Convert dict to DataFrame

    st.subheader("Raw Pollution Data")
    st.dataframe(df)

    # Convert relevant columns to numeric if needed
    for col in ['CO2 Emissions', 'NOx Emissions', 'PM2.5 Emissions', 'VOC Emissions', 'SO2 Emissions']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Plot each pollutant
    st.subheader("Pollution Visualizations")
    for pollutant in ['CO2 Emissions', 'NOx Emissions', 'PM2.5 Emissions', 'VOC Emissions', 'SO2 Emissions']:
        st.write(f"### {pollutant} Over Time")
        fig, ax = plt.subplots()
        df[pollutant].plot(kind='line', ax=ax)
        st.pyplot(fig)

    # Heatmap for correlation
    st.subheader("Pollutant Correlation Heatmap")
    fig, ax = plt.subplots()
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
else:
    st.warning("No data found in Firebase.")
