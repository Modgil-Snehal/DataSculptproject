import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page Configuration ---
st.set_page_config(page_title="India EV Market Dashboard", layout="wide")

# --- Header Image & Description ---
st.image(
    "https://www.grandviewresearch.com/static/img/research/india-electric-vehicle-market.png",
    use_column_width=True
)

st.title("🔋 India EV Market Dashboard (2001–2024)")
st.markdown("""
Welcome to the **India EV Market Dashboard**, your interactive window into the evolution of electric mobility in India.  
This dashboard visualizes EV sales trends across major manufacturers and tracks the industry's growth from 2015 to 2024.  
Use the sidebar to filter by year range and explore how different companies have contributed to India's electric revolution.
""")

# --- Load Data ---
df = pd.read_csv("EVIndia.csv")
df['Year'] = pd.to_numeric(df['Year'])
df['Company/Model'] = df['Company/Model'].astype(str)

# --- Sidebar Filters ---
st.sidebar.header("Filter by Year Range")
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

# --- Company-wise Sales Chart ---
st.subheader(f"📈 EV Sales by Company ({year_range[0]}–{year_range[1]})")
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.lineplot(data=filtered_df, x='Year', y='EVSales', hue='Company/Model', marker='o', ax=ax1)
ax1.set_ylabel("EVs Sold")
ax1.set_xlabel("Year")
ax1.set_title("Year-wise EV Sales by Company")
ax1.legend(title="Company/Model", bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig1)

# --- Total Yearly Sales Chart ---
st.subheader(f"📊 Total EV Sales ({year_range[0]}–{year_range[1]})")
fig2, ax2 = plt.subplots(figsize=(10, 4))
yearly_sales = filtered_df.groupby("Year")["EVSales"].sum().reset_index()
sns.barplot(x='Year', y='EVSales', data=yearly_sales, palette="viridis", ax=ax2)
ax2.set_ylabel("Total EVs Sold")
ax2.set_xlabel("Year")
st.pyplot(fig2)