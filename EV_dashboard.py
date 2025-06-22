import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
import requests

# Page config
st.set_page_config(page_title="India EV Market Dashboard", layout="wide")

# Inject anchor links and smooth scrolling CSS
st.markdown("""
    <style>
    html {
        scroll-behavior: smooth;
    }
    .anchor-link {
        display: inline-block;
        margin-bottom: 5px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar: Navigation jump menu
with st.sidebar.expander("📌 Jump to Section"):
    st.markdown("""
    - [📊 Vehicle Category Distribution](#vehicle-category-distribution-bar-chart)
    - [📈 Category Trends](#compare-trends-of-selected-vehicle-categories)
    - [📉 All Vehicle Comparison](#total-vehicles-sold-by-category-20012024)
    - [🗺️ EVs on India Map](#state-wise-electric-vehicle-distribution)
    - [🔍 Vehicle Class Table](#vehicle-class-insights)
    """, unsafe_allow_html=True)

# Sidebar: Theme selector
mode = st.sidebar.radio("Select Theme Mode", ["Light", "Dark"])

# Define dark mode style
if mode == "Dark":
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #0E1117 !important;
            color: #FFFFFF !important;
        }
        .css-1d391kg, .css-1v0mbdj, .css-1cpxqw2, .css-ffhzg2, .css-1x8cf1d, .css-1rs6os {
            background-color: #1E1E1E !important;
            color: white !important;
        }
        .css-1rs6os, .css-1v0mbdj {
            border-color: #333 !important;
        }
        .markdown-text-container, .stTextInput>div>div>input {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Title
st.title("Explore India's EV Market (2001 - 2024)")

# Intro Paragraph
st.markdown("""
Welcome to the India EV Market Dashboard! 🚗🔋

This dashboard provides an interactive overview of electric vehicle registration trends across India from **2001 to 2024**. 
Using real-world data from government transport records:
- `ev_cat_01-24.csv`: Category-wise yearly vehicle registrations.
- `Vehicle Class - All.csv`: Supplementary classification data for vehicle categories.
- `EV_Maker.csv`: State-wise EV manufacturer data for map visualization.

Use the tools below to explore how different vehicle types have evolved over the years and gain insight into EV adoption.
""")

# Load datasets
ev_data = pd.read_csv("ev_cat_01-24.csv")
vehicle_class_data = pd.read_csv("Vehicle Class - All.csv")
ev_maker = pd.read_csv("EV_Maker.csv")

# Clean ev_data (remove placeholder rows)
ev_data = ev_data[ev_data['Year'] != 0]

# Sidebar filters
min_year, max_year = ev_data['Year'].min(), ev_data['Year'].max()
year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

# Sidebar: Vehicle class toggle
show_vehicle_class = st.sidebar.checkbox("Show Vehicle Class Table", value=True)

# Sidebar: Useful links
with st.sidebar.expander("🔗 Links"):
    st.markdown("- [Official Vehicle Data Source](https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml)")
    st.markdown("- [GitHub Repository](https://github.com/yourusername/ev-market-dashboard)")
    st.markdown("- [Streamlit Documentation](https://docs.streamlit.io)")

st.sidebar.markdown("---")

# Filtered data by year range
range_data = ev_data[(ev_data['Year'] >= year_range[0]) & (ev_data['Year'] <= year_range[1])]

# Plot: Animated Vehicle Category Distribution
st.subheader("📊 Vehicle Category Distribution (Bar Chart)", anchor="vehicle-category-distribution-bar-chart")
ev_melted = range_data.melt(id_vars='Year', var_name='Category', value_name='Count')
fig1 = px.bar(ev_melted, x='Count', y='Category', color='Category', animation_frame='Year', orientation='h', 
              range_x=[0, ev_melted['Count'].max() + 500], title="Category-wise EV Registrations Over Time")
fig1.update_layout(paper_bgcolor='#0E1117' if mode == "Dark" else 'white', font_color='white' if mode == "Dark" else 'black')
st.plotly_chart(fig1, use_container_width=True)

# Plot: Category-wise Trends (lineplot)
st.subheader("📈 Compare Trends of Selected Vehicle Categories", anchor="compare-trends-of-selected-vehicle-categories")
ev_trend = range_data.groupby('Year').sum(numeric_only=True).reset_index()
selected_categories = st.multiselect("Select Categories to Compare", ev_trend.columns[1:], default=['TWO WHEELER(NT)', 'LIGHT GOODS VEHICLE'])

fig2 = px.line(ev_trend, x='Year', y=selected_categories, title='EV Category Trends Over Time')
fig2.update_layout(paper_bgcolor='#0E1117' if mode == "Dark" else 'white', font_color='white' if mode == "Dark" else 'black')
st.plotly_chart(fig2, use_container_width=True)

# Plot: All categories comparison
st.subheader("📉 Total Vehicles Sold by Category (2001–2024)", anchor="total-vehicles-sold-by-category-20012024")
fig3 = px.line(ev_melted.groupby(['Year', 'Category']).sum().reset_index(), x='Year', y='Count', color='Category',
               title='Comparison of All Vehicle Categories Over Time')
fig3.update_layout(paper_bgcolor='#0E1117' if mode == "Dark" else 'white', font_color='white' if mode == "Dark" else 'black')
st.plotly_chart(fig3, use_container_width=True)

# Plot: EV Makers on India Map
# Fixing the Geo Map Display for India with Markers
st.subheader("🗺️ EV Manufacturers Across Indian States", anchor="state-wise-electric-vehicle-distribution")

ev_maker = ev_maker.iloc[:, :2]
ev_maker.columns = ['State', 'EV_Maker']
ev_maker['State'] = ev_maker['State'].str.title()

state_coords = {
    'Maharashtra': [19.7515, 75.7139],
    'Tamil Nadu': [11.1271, 78.6569],
    'Karnataka': [15.3173, 75.7139],
    'Delhi': [28.7041, 77.1025],
    'Gujarat': [22.2587, 71.1924],
    'Haryana': [29.0588, 76.0856],
    'Telangana': [18.1124, 79.0193],
    'Uttar Pradesh': [26.8467, 80.9462],
    'West Bengal': [22.9868, 87.8550],
    'Rajasthan': [27.0238, 74.2179],
    'Andhra Pradesh': [15.9129, 79.7400]
}

coords_df = pd.DataFrame(state_coords.items(), columns=['State', 'Coords'])
coords_df[['Lat', 'Lon']] = pd.DataFrame(coords_df['Coords'].tolist(), index=coords_df.index)
ev_map_data = pd.merge(ev_maker, coords_df[['State', 'Lat', 'Lon']], on='State', how='inner')

fig_map = px.scatter_geo(
    ev_map_data,
    lat='Lat',
    lon='Lon',
    text='EV_Maker',
    scope='asia',
    projection='natural earth',
    title='EV Manufacturers by Indian State',
    template='plotly_dark' if mode == "Dark" else 'plotly_white',
)

fig_map.update_geos(
    visible=False,
    fitbounds="locations",
    lataxis_range=[6, 37],
    lonaxis_range=[68, 98],
    resolution=50,
    showcountries=True,
    showland=True,
    landcolor="#EAEAEA" if mode == "Light" else "#333"
)

fig_map.update_layout(
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    paper_bgcolor='#0E1117' if mode == "Dark" else 'white'
)

st.plotly_chart(fig_map, use_container_width=True)
# Comparison with Vehicle Class Data
if show_vehicle_class:
    st.subheader("🔍 Vehicle Class Insights", anchor="vehicle-class-insights")
    st.dataframe(vehicle_class_data.head(10), use_container_width=True)
    st.markdown("*Explore vehicle classification details from the supplementary dataset.*")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: gray;'>Created By - Snehal Modgil</p>", unsafe_allow_html=True)
