import streamlit as st
import pandas as pd 
import plotly.express as px 
import matplotlib.pyplot as plt
import numpy as np

st.title("SuperMarketSales Explodatory Data Analysis")
st.header("Dataset of supermarkes sales")
df=pd.read_csv('supermarkt_sales.csv')
st.dataframe(df)
# Add 'hour' column to dataframe
df["hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour
t = df['Payment'].value_counts()
# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")


st.title("Bar Chart")
# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
#st.plotly_chart(fig_product_sales)

# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)
#st.plotly_chart(fig_hourly_sales)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#pie chart
# Create labels for the pie chart
labels = ['Cash', 'Ewallet', 'Credit card']
# Create pie chart
fig1, ax1 = plt.subplots()
ax1.pie(t,labels=labels,autopct='%1.1f%%')
# Add title
ax1.set_title('Payment')
# Show plot
#st.pyplot(fig1)
#
# SALES BY PRODUCT LINE [BAR CHART]
st.header("Total Sales City wise")
sales_by_City = (
    df_selection.groupby(by=["City"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_City,
    x="Total",
    y=sales_by_City.index,
    orientation="h",
    title="<b>Sales by City</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_City),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_product_sales)
st.text("Toatal sales is a bit higher in Napyitaw City. ")

#Heatmap
import seaborn as sns
import matplotlib.pyplot as plt
st.title("HeatMap")
st.header("Correlation Of Variables")
fig, ax = plt.subplots()
sns.heatmap(df.corr(), ax=ax)
st.write(fig)
#snow effect
#st.snow()

#custmores per city 
city_count=df["City"].value_counts()
# Create labels for the pie chart
labels = ['Mandalay', 'Naypyitaw', 'Yangon']
# Create pie chart
fig2, ax1 = plt.subplots()
ax1.pie(city_count,labels=labels,autopct='%1.1f%%')
ax1.set_title('customers per city')
#st.pyplot(fig2)

col1,col2=st.columns(2)
with col1:
    labels = ['Cash', 'Ewallet', 'Credit card']
    # Create pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(t,labels=labels,autopct='%1.1f%%')
    # Add title
    ax1.set_title('Payment')
    st.pyplot(fig1)
    st.text("""The most popular payment method is
              E-wallet and Cash.""")
with col2:
    labels1=['Mandalay', 'Naypyitaw', 'Yangon']
    fig2, ax1 = plt.subplots()
    ax1.pie(city_count,labels=labels1,autopct='%1.1f%%')
    ax1.set_title('customers per city')
    st.pyplot(fig2)
    st.text("""There is not much difference in sales 
     across the 3 branches.The sales in
     branch Yangon is a bit higher than
     the rest of the branches.""")


#st.line_chart(data=df,  x="Quantity", y="Time")
st.title('Area Chart')
st.header('Rating and Gross Income')
st.area_chart(data=df,x="Rating",y="gross income")
st.text('There is no relationship between gross income of a customer and his rating.')
#boxplot
st.write("***********************************************************************")
st.header('Box Plot')
import streamlit as st
import pandas as pd
import altair as alt
chart = alt.Chart(df).mark_boxplot().encode(
    x='City',
    y='gross income'
)
#st.header('boxplot')
st.header("City and Gross Income")
st.altair_chart(chart, use_container_width=True)
st.text("""There is not much difference in gross income by branches at an average level. 
        Napityaw has a slightly higher income than other 2 cities ,
        i.e. Naypyitaw is the most profitable branch in terms of gross income.""")

st.header("Product line and Quantity")
chart1 = alt.Chart(df).mark_boxplot().encode(
    x='Product line',
    y='Quantity'
)
# Show the chart in Streamlit
st.altair_chart(chart1, use_container_width=True)
st.text("Food and beverages sold more in supermaket.")

#barplot
st.header('Barchart of Products and Gross income')
st.bar_chart(data=df,  x="Product line", y="gross income", width=0, height=0, use_container_width=True)
st.text("Gross income is highest in Food and beverages.")
