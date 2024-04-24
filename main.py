


# importing packages
import pandas as pd
from ydata_profiling import ProfileReport
import streamlit as st
import plotly.express as px


# Set page configuration
st.set_page_config(
    page_title="Suicides In India",
    page_icon=":bar_chart:",
    layout="wide"
)

# Read data
@st.cache
def load_data():
    df = pd.read_csv("Suicides_in_India.csv")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")
state = st.sidebar.multiselect("Select State", options=df['State'].unique())
year = st.sidebar.multiselect("Select Year", options=df['Year'].unique())
type = st.sidebar.multiselect("Select Type", options=df['Type'].unique())
age_group = st.sidebar.multiselect("Select Age Group", options=df['Age_group'].unique())
gender = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique())

# Apply filters
filtered_df = df.query("State == @state and Year == @year and Type == @type and Age_group == @age_group and Gender == @gender")

# Display filtered data
st.dataframe(filtered_df)

# Main page
st.title(":bar_chart: Suicides In India Dashboard")

# Line chart for suicide rate per year
suicide_rate_per_year = df.groupby("Year").sum()["Total"].reset_index()
fig = px.line(suicide_rate_per_year, x="Year", y="Total", title="Suicide Rate Per Year")
st.plotly_chart(fig)

# Bar chart for state-wise deaths
state_wise_deaths = df.groupby("State").sum()["Total"].sort_values(ascending=False)
fig_deaths = px.bar(
    x=state_wise_deaths.values,
    y=state_wise_deaths.index,
    orientation="h",
    title="State Wise Deaths",
    color=state_wise_deaths.values,
    color_continuous_scale='blues'
)
st.plotly_chart(fig_deaths)

# Pie chart for top N states
top_n = st.sidebar.number_input("Top N states", min_value=1, max_value=len(df['State'].unique()), value=10)
top_states = df.groupby("State").sum()["Total"].nlargest(top_n).reset_index()
fig_pie = px.pie(top_states, values="Total", names="State", title="Top States by Total Suicides")
st.plotly_chart(fig_pie)

# Bar chart for deaths by different age groups
age_group_deaths = df.groupby("Age_group").sum()["Total"].reset_index().sort_values(by="Total", ascending=False)
fig_age_group_deaths = px.bar(age_group_deaths, x="Age_group", y="Total", color="Age_group", title="Deaths by Age Groups")
st.plotly_chart(fig_age_group_deaths)

# Statistics Report
st.title("Statistics Report")
st.header("Data Summary")
data = pd.read_csv("Suicides_in_India.csv")
profile = ProfileReport(data)
profile
#profile.to_file(output_file='report.html')
