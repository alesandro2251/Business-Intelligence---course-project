import streamlit as st
from utils.data_loader import *
from utils.charts import *

st.set_page_config(page_title="BI Dashboard", layout="wide")

st.title("📊 Business Intelligence Dashboard")

# Test
# Sidebar navigation
section = st.sidebar.selectbox("Select Section", ["Sales", "Inventory", "Performance"])

# Sales Section
if section == "Sales":
    st.header("📈 Sales Dashboard")
    sales_df = load_sales_data()

    with st.expander("➕ Add New Sale"):
        inventory_df = load_inventory_data()
        existing_products = inventory_df["product"].unique().tolist()

        if existing_products:
            new_product = st.selectbox("Product", existing_products)

        new_region = st.text_input("Region")
        new_amount = st.number_input("Sales Amount", min_value=0)
        new_date = st.date_input("Date")
        
        if st.button("Add Sale"):
            new_entry = {
                "date": pd.to_datetime(new_date),
                "product": new_product,
                "region": new_region,
                "sales_amount": new_amount
            }
            sales_df = pd.concat([sales_df, pd.DataFrame([new_entry])], ignore_index=True)
            sales_df.to_csv("data/sales_data.csv", index=False)
            st.success("Sale added!")

    st.dataframe(sales_df)

    st.subheader("📊 Key Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Total Sales", f"${sales_df['sales_amount'].sum():,.0f}")
    col2.metric("Top Product", sales_df.groupby('product')['sales_amount'].sum().idxmax())

    st.subheader("📅 Filter by Date")
    date_range = st.date_input("Select date range", 
                               [sales_df["date"].min(), sales_df["date"].max()])

    if len(date_range) == 2:
        start_date, end_date = date_range
        sales_df = sales_df[(sales_df['date'] >= pd.to_datetime(start_date)) &
                            (sales_df['date'] <= pd.to_datetime(end_date))]


    st.plotly_chart(sales_by_month(sales_df))
    st.plotly_chart(product_sales_pie(sales_df))

# Inventory Section
elif section == "Inventory":
    st.header("📦 Inventory Overview")
    inv_df = load_inventory_data()

    with st.expander("➕ Add New Product"):
        product_name = st.text_input("Product Name")
        sku = st.text_input("SKU")
        stock = st.number_input("Stock", min_value=0)
        reorder_point = st.number_input("Reorder Point", min_value=0)
        if st.button("Add Product"):
            new_product = {
                "product": product_name,
                "sku": sku,
                "stock": stock,
                "reorder_point": reorder_point
            }
            inv_df = pd.concat([inv_df, pd.DataFrame([new_product])], ignore_index=True)
            inv_df.to_csv("data/inventory.csv", index=False)
            st.success("Product added!")

    st.dataframe(inv_df)

    with st.expander("🗑️ Delete Product"):
        if not inv_df.empty:
            selected_product = st.selectbox("Select Product to Delete", inv_df['product'].unique())
            if st.button("Delete Product"):
                inv_df = inv_df[inv_df['product'] != selected_product].reset_index(drop=True)
                inv_df.to_csv("data/inventory.csv", index=False)
                st.success(f"Product '{selected_product}' deleted!")
                inv_df = load_inventory_data()
        else:
            st.info("No inventory data available to delete.")

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
