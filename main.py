
import streamlit as st

import plotly.express  as px

import pandas as pd


from streamlit_pandas_profiling import st_profile_report

from pandas_profiling import ProfileReport
st.set_page_config(page_title="Suicides In India",
                   page_icon=":bar_chart:",
                   layout="wide")
df = pd.read_csv("Suicides_in_India.csv")
df

#---sidebar
st.sidebar.header("Please Filter Here:")
State= st.sidebar.multiselect(
    "Select the State:-",
    options=df['State'].unique(),

)

Year= st.sidebar.multiselect(
    "Select the Year:-",
    options=df['Year'].unique(),

)

Type= st.sidebar.multiselect(
    "Select the Type:-",
    options=df['Type'].unique(),

)



Age_group= st.sidebar.multiselect(
    "Select the Age_group:-",
    options=df['Age_group'].unique()


)


Gender= st.sidebar.multiselect(
    "Select the Gender:-",
  options=df['Gender'].unique()
    )





df_selection = df.query(
    "State==@State & Year==@Year & Type==@Type & Age_group==@Age_group & Gender==@Gender "
)

st.dataframe(df_selection)


# Main page
st.title(":bar_chart: Suicides In India Dashboard")
st.markdown("##")


s_t=df.groupby(["Year"]).sum()["Total"].reset_index()

fig = px.line(s_t, x=s_t["Year"], y=s_t["Total"],title="Suicide Rate Per Year")
fig.show()



state_wise_deaths=((df.groupby(["State"]).sum())[["Total"]].sort_values(by="Total"))
fig_deaths=px.bar(
    state_wise_deaths,
    x="Total",
    y=state_wise_deaths.index,
    orientation="h",
    title="<b> State Wise Deaths</b>",
    color_discrete_sequence=["#0083B8"]* len(state_wise_deaths),
    template="plotly_white",

)


fig_deaths.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_deaths)

input_col,pie_col=st.columns(2)
data=df.groupby(["State"])
pf=data["Total"].sum().reset_index()
pf.columns=["State","Total"]
jf=pf.sort_values(by="Total",ascending=False)
top_n=input_col.text_input("How many of the states would you like to see?",10)
top_n=int(top_n)
jf=jf.head(top_n)
jf=jf.head(top_n)



print(jf)
fig=px.pie(jf,values="Total",names="State")
pie_col.write(fig)

x=df.groupby("Age_group")
y=x["Total"].sum().reset_index().sort_values(by="Total",ascending=False)


y.columns= ["Age_group","Total"]
ax = px.bar(y,x = 'Age_group', y = "Total", color = 'Age_group', title='Deaths By different Age Groups')
ax

st.title("Statistics Report")
st.header("Data")
#profile = ProfileReport(df)
profile = ProfileReport(df)
profile



st.dataframe(df)

st_profile_report(profile)
