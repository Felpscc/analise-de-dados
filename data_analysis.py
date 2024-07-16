import pandas as pd

def analyze_sales(data):
    df = pd.DataFrame(data)
    sales_summary = df.groupby('produto')['valor'].sum().reset_index()
    return sales_summary
