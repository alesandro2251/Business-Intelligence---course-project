import plotly.express as px

def sales_by_month(df):
    df['month'] = df['date'].dt.to_period('M').astype(str)
    return px.bar(df.groupby('month')['sales_amount'].sum().reset_index(), 
                  x='month', y='sales_amount', title="Monthly Sales")

def product_sales_pie(df):
    return px.pie(df, names='product', values='sales_amount', title="Sales by Product")

def inventory_bar(df):
    return px.bar(df, x='product', y='stock', title="Stock per Product")

def performance_bar(df):
    return px.bar(df, x='employee', y='sales', title="Employee Performance")
