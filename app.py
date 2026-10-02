import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

data_path = Path(__file__).parent / "Sales_Data.zip"
df = pd.read_csv(data_path, encoding="latin1")

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: wheat;
        }
    </style>
    """,
    unsafe_allow_html=True
)

selected_page = st.sidebar.radio(
    "Select a page",
    [
        "Dashboard",
        "Dataset",
        "Visualization",
        "KPI Report"
    ]
)

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()

if selected_page == "Dashboard":
    st.markdown("<h1 style='text-align: center;'>Retail Sales Analysis Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("------")
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #fff8e8, #f4e5c7);
            border-left: 6px solid #b7791f;
            border-radius: 12px;
            padding: 20px 24px;
            margin: 8px 0 24px;
            box-shadow: 0 4px 14px rgba(90, 60, 20, 0.10);
        ">
            <p style="margin: 0 0 8px; color: #5b3a13; font-size: 1.25rem; font-weight: 700;">
                Welcome to <span style="color: #9a5b0a;">Retail Sales Analysis Dashboard</span>
            </p>
            <p style="margin: 0; color: #655744; font-size: 1rem; line-height: 1.6;">
                Explore your sales data and uncover meaningful business insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Profit", f"₹{total_profit:,.2f}")

    with col2:
        st.metric("Total Sales", f"₹{total_sales:,.2f}")

    st.bar_chart({
        'Total Sales': total_sales,
        'Total Profit': total_profit
    })

if selected_page == "Dataset":
    st.subheader("Dataset Preview")
    x=st.slider("Data",min_value=0,max_value=len(df),value = 5)
    st.dataframe(df.head(x))

    
    st.subheader("NUll values")
    st.write(df.isnull().sum())
    st.success("No null values")
    st.subheader("Summary of Data")
    st.write(df.describe())

if selected_page == "Visualization":
    st.markdown("<h2 style='text-align: center;'>Visualization</h2>", unsafe_allow_html=True)
    st.markdown("------")

    df['Order Date'] = pd.to_datetime(df['Order Date'])
    monthly_sales = df.groupby(df['Order Date'].dt.month)['Sales'].sum().sort_values(ascending= False)

    st.header("Sales by Month")
    st.bar_chart(monthly_sales)
    st.success("Sales peak during festive months.")

    Category_Profit = df.groupby("Category")["Profit"].sum().sort_values(ascending= False)
    st.header("Profit by Category")
    st.bar_chart(Category_Profit)
    st.success(f"Most Profitable Category: {Category_Profit.index[0]}")
    st.success(f"Least Profitable Category: {Category_Profit.index[-1]}")

    Sub_category =df.groupby("Sub-Category")["Profit"].sum().sort_values(ascending= False)
    st.header("Profit by Sub-Category")
    st.bar_chart(Sub_category)
    st.success(f"Most Profitable Sub-Category: {Sub_category.index[0]}")
    st.success(f"Least Profitable Sub-Category: {Sub_category.index[-1]}")

    top_products = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10)
    st.header("Top Products by Sales")
    st.bar_chart(top_products)
    st.success(f"Top Products: \n{top_products.index[0]}, \n{top_products.index[1]}, \n{top_products.index[2]}")

    segment_sales = df.groupby("Segment")["Sales"].sum()
    st.header("Sales by Segment")
    st.bar_chart(segment_sales)
    st.success(f"Top Segment: {segment_sales.index[0]}")

    region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    st.header("Sales by Region")
    st.bar_chart(region_sales)
    st.success(f"Region with Highest Sales: {region_sales.index[0]}")

    region_sales = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
    st.header("Profit by Region")
    st.bar_chart(region_sales)
    st.success(f"Region with Highest Profit: {region_sales.index[0]}")

    region_sales = df.groupby("Discount")["Profit"].sum().sort_values()
    st.header("Profit by Discount")
    st.bar_chart(region_sales)
    st.success("Discount above 20% reduces profitability.")

    st.header("Correlation Heatmap")
    corr = df[["Sales", "Profit", "Quantity", "Discount"]].corr()
    fig,ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

if selected_page == "KPI Report":
    # KPI Cards
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order ID"].nunique()
    total_customers = df["Customer ID"].nunique()
    average_sales = df["Sales"].mean()
    profit_margin = (total_profit / total_sales) * 100

    st.markdown("<h2 style='text-align: center;'>KPI Report Card</h2>", unsafe_allow_html=True)
    st.markdown("------")
    
    st.write("Total Sales       :", total_sales)
    st.write("Total Profit      :", total_profit)
    st.write("Total Orders      :", total_orders)
    st.write("Total Customers   :", total_customers)
    st.write("Average Sale      :", average_sales)

    top_category = df.groupby("Category")["Sales"].sum().idxmax()
    top_product = df.groupby("Product Name")["Sales"].sum().idxmax()
    top_customer = df.groupby("Customer Name")["Sales"].sum().idxmax()
    top_state = df.groupby("State")["Sales"].sum().idxmax()

    st.write("Top Category       :",top_category)
    st.write("Top Product        :", top_product)
    st.write("Top Customer       :", top_customer)
    st.write("Top State          :", top_state)
    st.write("Profit Margin      :", profit_margin)
