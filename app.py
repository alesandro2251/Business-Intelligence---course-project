import streamlit as st
from utils.data_loader import *
from utils.charts import *
from prophet import Prophet
import matplotlib.pyplot as plt

st.set_page_config(page_title="BI Dashboard", layout="wide")

st.title("📊 Business Intelligence Dashboard")

section = st.sidebar.selectbox("Select Section", ["Sales", "Inventory", "Performance"])

if section == "Sales":
    st.header("📈 Sales Dashboard")

    sales_df = load_sales_data()

    with st.expander("➕ Add New Sale"):
        inventory_df = load_inventory_data()
        product_options = inventory_df["product"].unique().tolist()

        if product_options:
            new_product = st.selectbox("Product", product_options)
        else:
            new_product = st.text_input("Enter product name")

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

            sales_df = load_sales_data()

    table_placeholder = st.empty()
    table_placeholder.dataframe(sales_df)

    with st.expander("🗑️ Delete Sale"):
        if not sales_df.empty:
            selected_index = st.selectbox("Select Sale Entry to Delete", sales_df.index)
            selected_row = sales_df.loc[selected_index]
            st.write(selected_row)

            if st.button("Delete Sale"):
                sales_df = sales_df.drop(selected_index).reset_index(drop=True)
                sales_df.to_csv("data/sales_data.csv", index=False)
                st.success("Sale entry deleted!")

                sales_df = load_sales_data()
                table_placeholder.dataframe(sales_df)
        else:
            st.info("No sales data available to delete.")

    st.subheader("📊 Key Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Total Sales", f"${sales_df['sales_amount'].sum():,.0f}")
    if not sales_df.empty:
        col2.metric("Top Product", sales_df.groupby('product')['sales_amount'].sum().idxmax())
    else:
        col2.metric("Top Product", "N/A")

    st.subheader("📅 Filter by Date")
    if not sales_df.empty:
        min_date = sales_df["date"].min()
        max_date = sales_df["date"].max()
        date_range = st.date_input("Select date range", [min_date, max_date])

        if len(date_range) == 2:
            start_date, end_date = date_range
            sales_df = sales_df[
                (sales_df["date"] >= pd.to_datetime(start_date)) &
                (sales_df["date"] <= pd.to_datetime(end_date))
            ]

    st.plotly_chart(sales_by_month(sales_df))
    st.plotly_chart(product_sales_pie(sales_df))

    # 🔮 SALES FORECASTING
    st.subheader("🔮 Sales Forecast")
    if not sales_df.empty:
        forecast_period = st.slider("Forecast Days", 7, 90, 30)

        df_prophet = sales_df.groupby("date")["sales_amount"].sum().reset_index()
        df_prophet.columns = ['ds', 'y']

        model = Prophet()
        model.fit(df_prophet)

        future = model.make_future_dataframe(periods=forecast_period)
        forecast = model.predict(future)

        # Plot forecast
        fig1 = model.plot(forecast)
        st.pyplot(fig1)

        with st.expander("📊 Forecast Components"):
            fig2 = model.plot_components(forecast)
            st.pyplot(fig2)
    else:
        st.info("Not enough sales data to generate forecast.")

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

            inv_df = load_inventory_data()

    table_placeholder = st.empty()
    table_placeholder.dataframe(inv_df)

    with st.expander("🗑️ Delete Product"):
        if not inv_df.empty:
            selected_product = st.selectbox("Select Product to Delete", inv_df['product'].unique())
            if st.button("Delete Product"):
                inv_df = inv_df[inv_df['product'] != selected_product].reset_index(drop=True)
                inv_df.to_csv("data/inventory.csv", index=False)
                st.success(f"Product '{selected_product}' deleted!")

                inv_df = load_inventory_data()
                table_placeholder.dataframe(inv_df)
        else:
            st.info("No inventory data available to delete.")

    st.plotly_chart(inventory_bar(inv_df))

    low_stock = inv_df[inv_df['stock'] < inv_df['reorder_point']]
    st.warning("🚨 Low Stock Items:")
    st.dataframe(low_stock)

elif section == "Performance":
    st.header("🏆 Performance Reports")

    perf_df = load_performance_data()

    with st.expander("➕ Add Employee Performance"):
        employee = st.text_input("Employee Name")
        month = st.text_input("Month (YYYY-MM)")
        sales = st.number_input("Sales", min_value=0)
        if st.button("Add Performance"):
            new_perf = {
                "employee": employee,
                "month": month,
                "sales": sales
            }
            perf_df = pd.concat([perf_df, pd.DataFrame([new_perf])], ignore_index=True)
            perf_df.to_csv("data/performance.csv", index=False)
            st.success("Performance added!")

            perf_df = load_performance_data()

    table_placeholder = st.empty()
    table_placeholder.dataframe(perf_df)

    with st.expander("🗑️ Delete Performance Entry"):
        if not perf_df.empty:
            selected_index = st.selectbox("Select Entry to Delete", perf_df.index)
            selected_row = perf_df.loc[selected_index]
            st.write(selected_row)

            if st.button("Delete Performance"):
                perf_df = perf_df.drop(selected_index).reset_index(drop=True)
                perf_df.to_csv("data/performance.csv", index=False)
                st.success("Performance entry deleted!")

                perf_df = load_performance_data()
                table_placeholder.dataframe(perf_df)
        else:
            st.info("No performance data available to delete.")

    st.plotly_chart(performance_bar(perf_df))

