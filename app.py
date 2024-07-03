import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from scipy.signal import find_peaks

# Function to identify accelerating downward slopes
def find_accelerating_slopes(df):
    slopes = np.diff(df['Values'])
    accel_slopes = []
    for i in range(1, len(slopes)):
        if slopes[i] < slopes[i - 1] < 0:
            accel_slopes.append(df['Timestamp'].iloc[i + 1])
    return accel_slopes

# Load the data
@st.cache
def load_data():
    df = pd.read_csv('Sample_Data.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d-%m-%Y %H:%M:%S')
    return df

df = load_data()

# Calculate 5-day moving average
df['5-day MA'] = df['Values'].rolling(window=5).mean()

# Find local peaks and lows
peaks, _ = find_peaks(df['Values'])
lows, _ = find_peaks(-df['Values'])

# Find instances where voltage went below 20
below_20 = df[df['Values'] < 20]

# Find instances where the downward slope accelerates
accelerating_slopes = find_accelerating_slopes(df)

# Plot the data
fig = px.line(df, x='Timestamp', y='Values', title='Voltage over Time')
fig.add_scatter(x=df['Timestamp'], y=df['5-day MA'], mode='lines', name='5-day MA')
fig.add_scatter(x=df.iloc[peaks]['Timestamp'], y=df.iloc[peaks]['Values'], mode='markers', name='Peaks')
fig.add_scatter(x=df.iloc[lows]['Timestamp'], y=df.iloc[lows]['Values'], mode='markers', name='Lows')

# Streamlit interface
st.title("Voltage Data Analysis")
st.plotly_chart(fig)

st.subheader("Local Peaks")
st.write(df.iloc[peaks][['Timestamp', 'Values']])

st.subheader("Local Lows")
st.write(df.iloc[lows][['Timestamp', 'Values']])

st.subheader("Voltage Below 20")
st.write(below_20)

st.subheader("Accelerating Downward Slopes")
st.write(pd.DataFrame({'Timestamp': accelerating_slopes}))

