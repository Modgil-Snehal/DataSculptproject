import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page Setup ---
st.set_page_config(page_title="India EV Market: Category vs Year", layout="wide")

st.title("🔋 India EV Sales Dashboard (2001–2024)")
st.markdown("""
This app combines two datasets:  
- **Vehicle Class - All.csv** for selecting EV categories  
- **ev_cat_01-24.csv** for selecting year range  

Explore India's EV journey across classes, filtered by the years you care about.
""")

# --- Load Data ---
df_class = pd.read_csv("Vehicle Class - All.csv")
df_years = pd.read_csv("ev_cat_01-24.csv")

# Clean and format
df_class['Year'] = pd.to_numeric(df_class['Year'])
df_years['Year'] = pd.to_numeric(df_years['Year'])

# --- Sidebar Filters ---
st.sidebar.header("Filters")

# Vehicle Class Selector (from Vehicle Class - All.csv)
available_classes = sorted(df_class['Vehicle_Class'].unique())
selected_classes = st.sidebar.multiselect("Select Vehicle Classes", available_classes, default=available_classes)

# Year Range Selector (based on ev_cat_01-24.csv)
year_min = int(df_years['Year'].min())
year_max = int(df_years['Year'].max())
year_range = st.sidebar.slider("Select Year Range", year_min, year_max, (year_min, year_max))

# Filter df_class with both year and class selections
filtered_df = df_class[
    (df_class['Vehicle_Class'].isin(selected_classes)) &
    (df_class['Year'] >= year_range[0]) &
    (df_class['Year'] <= year_range[1])
]

# --- Line Chart: Class-wise EV Sales ---
st.subheader(f"📈 EV Sales by Vehicle Class ({year_range[0]}–{year_range[1]})")
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.lineplot(data=filtered_df, x='Year', y='EV_Sales', hue='Vehicle_Class', marker='o', ax=ax1)
ax1.set_ylabel("EV Units Sold")
ax1.set_xlabel("Year")
ax1.set_title("EV Sales Trend by Vehicle Class")
ax1.legend(title="Vehicle Class", bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig1)

# --- Bar Chart: Total EV Sales Per Year ---
st.subheader(f"📊 Total EV Sales in Selected Years ({year_range[0]}–{year_range[1]})")
fig2, ax2 = plt.subplots(figsize=(10, 4))
yearly_sales = filtered_df.groupby("Year")["EV_Sales"].sum().reset_index()
sns.barplot(x='Year', y='EV_Sales', data=yearly_sales, palette="crest", ax=ax2)
ax2.set_ylabel("Total EVs Sold")
ax2.set_xlabel("Year")
st.pyplot(fig2)