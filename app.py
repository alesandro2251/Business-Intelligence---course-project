import streamlit as st
from utils.data_loader import *
from utils.charts import *

st.set_page_config(page_title="BI Dashboard", layout="wide")

st.title("📊 Business Intelligence Dashboard")

# Sidebar navigation
section = st.sidebar.selectbox("Select Section", ["Sales", "Inventory", "Performance"])

# Sales Section
if section == "Sales":
    st.header("📈 Sales Dashboard")
    sales_df = load_sales_data()
    st.dataframe(sales_df)

    st.plotly_chart(sales_by_month(sales_df))
    st.plotly_chart(product_sales_pie(sales_df))

# Inventory Section
elif section == "Inventory":
    st.header("📦 Inventory Overview")
    inv_df = load_inventory_data()
    st.dataframe(inv_df)

    st.plotly_chart(inventory_bar(inv_df))

    low_stock = inv_df[inv_df['stock'] < inv_df['reorder_point']]
    st.warning("🚨 Low Stock Items:")
    st.dataframe(low_stock)

# Performance Section
elif section == "Performance":
    st.header("🏆 Performance Reports")
    perf_df = load_performance_data()
    st.dataframe(perf_df)

    st.plotly_chart(performance_bar(perf_df))
