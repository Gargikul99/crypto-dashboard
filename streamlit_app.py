import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from databricks import sql
from dotenv import load_dotenv
import os

load_dotenv()
st.title("📉 Real-Time Crypto Price Trend")

DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

conn = sql.connect(
    server_hostname=DATABRICKS_HOST,
    http_path=DATABRICKS_HTTP_PATH,
    access_token=DATABRICKS_TOKEN
 
)


@st.cache_data(ttl=60)
def load_data():
    query = "SELECT * FROM crypto_prices ORDER BY timestamp DESC LIMIT 200"
    return pd.read_sql(query, conn)

df = load_data()


df['timestamp'] = pd.to_datetime(df['timestamp'])


now = df['timestamp'].max()

minutes = st.slider(" Use the slider to get data from the last x minutes", 50, 200, 100)
st.markdown(f"x = {minutes}")
df = df[df['timestamp'] >= now - timedelta(minutes=minutes)]



df = df.sort_values('timestamp')
df.columns = df.columns.str.strip().str.lower()  


btc_col = 'bitcoin'
eth_col = 'ethereun'

btc_min = df[btc_col].min() * 0.995
btc_max = df[btc_col].max() * 1.005

eth_min = df[eth_col].min() * 0.995
eth_max = df[eth_col].max() * 1.005

latest = df.sort_values("timestamp").iloc[-1]

col1, col2 = st.columns(2)
with col1:
    st.metric("💰 Bitcoin (USD)", f"${latest['bitcoin']:.2f}")
with col2:
    st.metric("🪙 Ethereum (USD)", f"${latest['ethereun']:.2f}")

btc_chart = alt.Chart(df).mark_line().encode(
    x=alt.X('timestamp:T', title='Time (UTC)(HH:MM:SS)', axis=alt.Axis(format='%H:%M:%S')),
    y=alt.Y(f'{btc_col}:Q', title='BTC Price', scale=alt.Scale(domain=[btc_min, btc_max])),
    tooltip=[alt.Tooltip('timestamp:T', title='Timestamp (UTC)', format='%Y-%m-%d %H:%M:%S'),
             alt.Tooltip('bitcoin:Q', title='BTC Price')]
).properties(
    title="Bitcoin Price",
    width=800,
    height=300
)


eth_chart = alt.Chart(df).mark_line().encode(
    x=alt.X('timestamp:T', title='Time (UTC)(HH:MM:SS)', axis=alt.Axis(format='%H:%M:%S')),
    y=alt.Y(f'{eth_col}:Q', title='ETH Price', scale=alt.Scale(domain=[eth_min, eth_max])),
    tooltip=[alt.Tooltip('timestamp:T', title='Timestamp (UTC)', format='%Y-%m-%d %H:%M:%S'),
             alt.Tooltip('ethereun:Q', title='Ethereum Price')]
).properties(
    title="Ethereum Price",
    width=800,
    height=300
)

col1, col2 = st.columns(2)
with col1:
    st.altair_chart(btc_chart, use_container_width=True)
with col2:
    st.altair_chart(eth_chart, use_container_width=True)

