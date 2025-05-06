import pandas as pd

def load_sales_data(path="data/sales_data.csv"):
    return pd.read_csv(path, parse_dates=["date"])

def load_inventory_data(path="data/inventory.csv"):
    return pd.read_csv(path)

def load_performance_data(path="data/performance.csv"):
    return pd.read_csv(path)
