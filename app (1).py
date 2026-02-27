import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Trader Dashboard", layout="wide")

# ---------------- TITLE ----------------
st.title("📊 Trader Performance vs Market Sentiment Dashboard")
st.markdown("Analyze trading behavior, sentiment impact, and trader performance 🚀")

# ---------------- LOAD DATA ----------------
# Change this to your Google Drive link OR local file
# url = "https://drive.google.com/uc?id=YOUR_FILE_ID"
df = pd.read_csv("/workspaces/Trader-Performance-vs-Market-Sentiment/final_data.csv")

# Convert date
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Filters")

# Coin filter
if 'coin' in df.columns:
    coin = st.sidebar.selectbox("Select Coin", ["All"] + list(df['coin'].dropna().unique()))
    if coin != "All":
        df = df[df['coin'] == coin]

# Sentiment filter
if 'classification' in df.columns:
    sentiment = st.sidebar.selectbox("Market Sentiment", ["All"] + list(df['classification'].dropna().unique()))
    if sentiment != "All":
        df = df[df['classification'] == sentiment]

# ---------------- METRICS ----------------
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total PnL", round(df['pnl'].sum(), 2))
col2.metric("Win Rate", round(df['win'].mean(), 2))
col3.metric("Total Trades", len(df))
col4.metric("Avg PnL", round(df['pnl'].mean(), 2))

# ---------------- PNL TREND ----------------
if 'date' in df.columns:
    st.subheader("📈 PnL Over Time")

    pnl_time = df.groupby('date')['pnl'].sum()

    st.line_chart(pnl_time)

# ---------------- CLUSTER PLOT ----------------
if 'cluster_name' in df.columns:
    st.subheader("🧠 Trader Segmentation")

    fig, ax = plt.subplots()

    sns.scatterplot(
        data=df,
        x='trade_count',
        y='pnl',
        hue='cluster_name',
        ax=ax
    )

    plt.title("Trader Segments")
    st.pyplot(fig)

# ---------------- PNL BY COIN ----------------
if 'coin' in df.columns:
    st.subheader("🪙 PnL by Coin")

    coin_pnl = df.groupby('coin')['pnl'].sum().sort_values(ascending=False)

    st.bar_chart(coin_pnl)

# ---------------- WIN / LOSS ----------------
if 'win' in df.columns:
    st.subheader("🎯 Win vs Loss Distribution")

    fig2, ax2 = plt.subplots()

    sns.countplot(x='win', data=df, ax=ax2)

    st.pyplot(fig2)

# ---------------- PNL DISTRIBUTION ----------------
st.subheader("📊 PnL Distribution")

fig3, ax3 = plt.subplots()

sns.histplot(df['pnl'], bins=30, kde=True, ax=ax3)

st.pyplot(fig3)

# ---------------- SENTIMENT ANALYSIS ----------------
if 'classification' in df.columns:
    st.subheader("📈 Sentiment vs PnL")

    sentiment_pnl = df.groupby('classification')['pnl'].mean().reset_index()

    fig4, ax4 = plt.subplots()

    sns.barplot(data=sentiment_pnl, x='classification', y='pnl', ax=ax4)

    st.pyplot(fig4)

# ---------------- TOP TRADERS ----------------
st.subheader("🏆 Top Traders")

top_traders = df.groupby('account')['pnl'].sum().sort_values(ascending=False).head(10)

st.dataframe(top_traders)

# ---------------- RISK ANALYSIS ----------------
st.subheader("⚠️ Risk Analysis")

max_loss = df['pnl'].min()
max_profit = df['pnl'].max()

st.write(f"🔻 Maximum Loss: {round(max_loss,2)}")
st.write(f"🔺 Maximum Profit: {round(max_profit,2)}")

# ---------------- INSIGHTS ----------------
st.subheader("💡 Insights")

if df['pnl'].mean() > 0:
    st.success("Overall traders are profitable 📈")
else:
    st.error("Overall traders are in loss 📉")

if 'classification' in df.columns:
    best_sentiment = df.groupby('classification')['pnl'].mean().idxmax()
    st.info(f"Best performance in **{best_sentiment}** market")

# ---------------- DOWNLOAD ----------------
st.subheader("⬇️ Download Data")

st.download_button(
    "Download Filtered Data",
    df.to_csv(index=False),
    file_name="filtered_data.csv"
)