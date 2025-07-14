import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_data():
    df = pd.read_csv("Supermart Grocery Sales - Retail Analytics Dataset.csv", parse_dates=["Order Date"])
    return df

df = load_data()
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Year"] = df["Order Date"].dt.year  
df["Month"] = df["Order Date"].dt.month_name()  
df["Day"] = df["Order Date"].dt.day  
df["Year-Month"] = df["Order Date"].dt.strftime("%Y-%m")  


st.sidebar.header("Filters")
categories = df["Category"].unique()
category_filter = st.sidebar.multiselect("Select Categories", categories, default=categories)

sub_categories = df["Sub Category"].unique()
sub_category_filter = st.sidebar.multiselect("Select Sub-Categories", sub_categories, default=sub_categories)

cities = df["City"].unique()
city_filter = st.sidebar.multiselect("Select Cities", cities, default=cities)

years = sorted(df["Year"].dropna().unique())
year_filter = st.sidebar.multiselect("Select Year(s)", years, default=years)

months = df["Month"].dropna().unique()
month_filter = st.sidebar.multiselect("Select Month(s)", months, default=months)


min_date = df["Order Date"].min()
max_date = df["Order Date"].max()
start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
end_date = pd.to_datetime(end_date, format='%Y-%m-%d')


df_filtered = df[
    (df["Category"].isin(category_filter)) & 
    (df["Sub Category"].isin(sub_category_filter)) & 
    (df["City"].isin(city_filter)) & 
    (df["Year"].isin(year_filter)) & 
    (df["Month"].isin(month_filter)) & 
    (df["Order Date"] >= start_date) & 
    (df["Order Date"] <= end_date)
]


st.subheader("Filtered Data")
st.dataframe(df_filtered)


st.header("📊 Data Visualizations")
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📈 Sales Over Time", 
    "📊 Sales by Category", 
    "🏙 Sales by City", 
    "🔻 Sales vs Discount", 
    "👤 Customer Orders", 
    "📅 Sales by Month", 
    "📂 Sales by Sub-Category", 
    "🌍 Sales by Region",
    "💰 Profit by Customer"
])


def display_max_min(df, column, value_column, tab_title):
    if not df.empty:
        max_value = df.loc[df[value_column].idxmax()]
        min_value = df.loc[df[value_column].idxmin()]

        st.write(f"### {tab_title} - Maximum {value_column}")
        st.table(pd.DataFrame([max_value]))

        st.write(f"### {tab_title} - Minimum {value_column}")
        st.table(pd.DataFrame([min_value]))

# 📈 Sales Over Time
with tab1:
    st.subheader("Sales Over Time")
    sales_over_time = df_filtered.groupby("Order Date")["Sales"].sum().reset_index()
    fig_time = px.line(sales_over_time, x="Order Date", y="Sales", title="Sales Trend Over Time")
    st.plotly_chart(fig_time)
    display_max_min(sales_over_time, "Order Date", "Sales", "Sales Over Time")

# 📊 Sales by Category
with tab2:
    st.subheader("Sales by Category")
    sales_by_category = df_filtered.groupby("Category")["Sales"].sum().reset_index()
    fig_category = px.bar(sales_by_category, x="Category", y="Sales", title="Total Sales by Category", color="Category")
    st.plotly_chart(fig_category)
    display_max_min(sales_by_category, "Category", "Sales", "Sales by Category")

# 🏙 Sales by City
with tab3:
    st.subheader("Sales by City")
    sales_by_city = df_filtered.groupby("City")["Sales"].sum().reset_index()
    fig_city = px.bar(sales_by_city, x="City", y="Sales", title="Total Sales by City", color="City")
    st.plotly_chart(fig_city)
    display_max_min(sales_by_city, "City", "Sales", "Sales by City")

# 🔻 Sales vs Discount
with tab4:
    st.subheader("Sales vs Discount")
    fig_discount = px.scatter(df_filtered, x="Discount", y="Sales", color="Category", title="Sales vs Discount")
    st.plotly_chart(fig_discount)
    display_max_min(df_filtered, "Discount", "Sales", "Sales vs Discount")

# 👤 Customer Orders
with tab5:
    st.subheader("Highest & Lowest Orders by Customers")
    customer_orders = df_filtered.groupby(["Customer Name", "Year", "Category"])["Sales"].sum().reset_index()
    fig_customer = px.bar(customer_orders, x="Customer Name", y="Sales", color="Category", title="Customer Orders")
    st.plotly_chart(fig_customer)
    display_max_min(customer_orders, "Customer Name", "Sales", "Customer Orders")

# 📅 Sales by Month
with tab6:
    st.subheader("Sales by Month")
    sales_by_month = df_filtered.groupby("Month")["Sales"].sum().reset_index()
    fig_month = px.bar(sales_by_month, x="Month", y="Sales", title="Total Sales by Month", color="Month")
    st.plotly_chart(fig_month)
    display_max_min(sales_by_month, "Month", "Sales", "Sales by Month")

# 📂 Sales by Sub-Category
with tab7:
    st.subheader("Sales by Sub-Category")
    sales_by_subcat = df_filtered.groupby("Sub Category")["Sales"].sum().reset_index()
    fig_subcat = px.bar(sales_by_subcat, x="Sub Category", y="Sales", title="Total Sales by Sub-Category", color="Sub Category")
    st.plotly_chart(fig_subcat)
    display_max_min(sales_by_subcat, "Sub Category", "Sales", "Sales by Sub-Category")

# 🌍 Sales by Region
with tab8:
    st.subheader("Sales by Region")
    sales_by_region = df_filtered.groupby("Region")["Sales"].sum().reset_index()
    fig_region = px.bar(sales_by_region, x="Region", y="Sales", title="Total Sales by Region", color="Region")
    st.plotly_chart(fig_region)
    display_max_min(sales_by_region, "Region", "Sales", "Sales by Region")

# 💰 Profit by Customer
with tab9:
    st.subheader("Profit by Customer")
    profit_by_customer = df_filtered.groupby("Customer Name")["Profit"].sum().reset_index()
    fig_profit = px.bar(profit_by_customer, x="Customer Name", y="Profit", title="Total Profit by Customer", color="Profit")
    st.plotly_chart(fig_profit)
    display_max_min(profit_by_customer, "Customer Name", "Profit", "Profit by Customer")
