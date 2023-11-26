import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from babel.numbers import format_currency
# from pathlib import Path
from helper import create_byage_df, create_bygender_df, create_bystate_df, create_daily_order_df, create_rmf_df, create_sum_order_items_df
sns.set_style("dark")

# data_dir = Path("../Datasets/all_data.csv").parent.resolve() / "all_data.csv"

st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded"
)

all_df = pd.read_csv("all_data.csv")
datetime_columns = ["order_date", "delivery_date"]
all_df.sort_values(by="order_date", inplace=True)
all_df.reset_index(inplace=True)

for columns in datetime_columns:
    all_df[columns] = pd.to_datetime(all_df[columns])

min_date = all_df.order_date.min()
max_date = all_df.order_date.max()

st.header("Sales Performance Dashboard :chart_with_upwards_trend:")
st.subheader("Data Overview")

with st.sidebar:
    # Adds company logo to sidebar
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", width=200, use_column_width=True)
    
    start_date, end_date = st.date_input(
        label="Select Date Range",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    

col1, col2 = st.columns(2)

main_df = all_df[(all_df.order_date >= str(start_date)) & (all_df.order_date <= str(end_date))]
daily_order_df = create_daily_order_df(main_df)

with col1:
    total_order = daily_order_df.order_count.sum()
    st.metric("Total Orders", f"{total_order:,}")
    

with col2:
    total_revenue = format_currency(daily_order_df.total_sales.sum(), 'AUD', locale='es_CO')
    st.metric("Total Revenue", total_revenue)
    
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(daily_order_df["order_date"], daily_order_df["order_count"], marker="o", linewidth="2", color="#90CAF9")
ax.tick_params(axis="x", labelsize = 8, rotation=45)
ax.tick_params(axis="y", labelsize = 8)

st.pyplot(fig)

st.subheader("Best & Worst Products")

fig, ax = plt.subplots(figsize=(12, 6), nrows=1, ncols=2)

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sum_order_items_df = create_sum_order_items_df(main_df)

sns.barplot(
    x = "quantity_x",
    y = "product_name",
    data = sum_order_items_df.head(10),
    palette = colors,
    ax = ax[0]
)

ax[0].set_title("Top 10 Best Products", fontsize=12)
ax[0].set_xlabel("Quantity", fontsize=10)
ax[0].set_ylabel("Product Name", fontsize=10)
ax[0].tick_params(axis="x", labelsize = 8)
ax[0].tick_params(axis="y", labelsize = 8)

sns.barplot(
    x = "quantity_x",
    y = "product_name",
    data = sum_order_items_df.tail(10),
    palette = colors,
    ax = ax[1]
)

ax[1].set_title("Top 10 Worst Products", fontsize=12)
ax[1].set_xlabel("Quantity", fontsize=10)
ax[1].set_ylabel("Product Name", fontsize=10)
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis="x", labelsize = 8)
ax[1].tick_params(axis="y", labelsize = 8)

st.pyplot(fig)

st.subheader("Customer Demographic")

col1, col2 = st.columns(2)

bygender_df = create_bygender_df(main_df)
with col1:
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
    ax = sns.barplot(
        y = "customer_count",
        x = "gender",
        data = bygender_df.sort_values(by="customer_count", ascending=False),
        palette = colors,
        ax = ax
    )
    
    ax.set_title("Number of Customer by Gender", fontsize = 12)
    ax.set_xlabel("Gender", fontsize = 10)
    ax.set_ylabel("Number of Customer", fontsize = 10)
    ax.tick_params(axis="x", labelsize = 8)
    ax.tick_params(axis="y", labelsize = 8)
    st.pyplot(fig)
    
by_age_df = create_byage_df(main_df)    
with col2:
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = ["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"]
    
    ax = sns.barplot(
        y = "customer_count",
        x = "age_group",
        data = by_age_df.sort_values(by="age_group", ascending=False),
        palette = colors,
        ax = ax
    )
    
    ax.set_title("Number of Customer by Age", fontsize = 12)
    ax.set_xlabel("Age_Group", fontsize = 10)
    ax.set_ylabel("Number of Customer", fontsize = 10)
    ax.tick_params(axis="x", labelsize = 8)
    ax.tick_params(axis="y", labelsize = 8)
    st.pyplot(fig)

by_state_df = create_bystate_df(main_df)

fig, ax = plt.subplots(figsize=(12, 6))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

ax = sns.barplot(
    y = "customer_count",
    x = "state",
    data = by_state_df.sort_values(by="customer_count", ascending=False).head(10),
    palette = colors,
    ax = ax
)

ax.set_title("Number of Customer by State", fontsize = 12)
ax.set_xlabel("State", fontsize = 10)
ax.set_ylabel("Number of Customer", fontsize = 10)
ax.tick_params(axis="x", labelsize = 8)
ax.tick_params(axis="y", labelsize = 8)
st.pyplot(fig)

st.subheader("RFM Analysis")

col1, col2, col3 = st.columns(3)

rfm_df = create_rmf_df(main_df)
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

with col1:
    avg_recency = round(rfm_df.recency.mean(),1)
    st.metric("Average Recency", avg_recency)
    
with col2:
    avg_frequency = round(rfm_df.frequency.mean(),2)
    st.metric("Average Frequency", avg_frequency)

with col3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), 'AUD', locale='es_CO')
    st.metric("Average Monetary", avg_monetary)
    
fig, ax = plt.subplots(figsize=(12, 6), nrows=1, ncols=3)
sns.barplot(
            x = "recency",
            y = "customer_id",
            data = rfm_df.sort_values(by="recency", ascending=False).head(5),
            palette = colors,
            ax = ax[0],
            
)
ax[0].set_title("Top 5 Worst Customers by Recency", fontsize = 12)
ax[0].set_xlabel("Recency", fontsize = 10)
ax[0].set_ylabel("Customer ID", fontsize = 10)
ax[0].tick_params(axis="x", labelsize = 8)
ax[0].tick_params(axis="y", labelsize = 8)

sns.barplot(
            x = "frequency",
            y = "customer_id",
            data = rfm_df.sort_values(by="frequency", ascending=False).head(5),
            palette = colors,
            ax = ax[1]
)
ax[1].set_title("Top 5 Best Customers by Frequency", fontsize = 12)
ax[1].set_xlabel("Frequency", fontsize = 10)
ax[1].set_ylabel("Customer ID", fontsize = 10)
ax[1].tick_params(axis="x", labelsize = 8)
ax[1].tick_params(axis="y", labelsize = 8)

sns.barplot(
        x = "monetary",
        y = "customer_id",
        data = rfm_df.sort_values(by="monetary", ascending=False).head(5),
        palette = colors,
        ax = ax[2]
)
ax[2].set_title("Top 5 Best Customers by Monetary", fontsize = 12)
ax[2].set_xlabel("Monetary", fontsize = 10)
ax[2].set_ylabel("Customer ID", fontsize = 10)
ax[2].tick_params(axis="x", labelsize = 8)
ax[2].tick_params(axis="y", labelsize = 8)
    
st.pyplot(fig)

st.caption('Copyright (c) Dicoding 2023')
