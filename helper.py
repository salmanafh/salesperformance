import pandas as pd

def create_daily_order_df(df):
    """
    Create a daily order DataFrame from the given DataFrame.
    
    Parameters:
    df (pandas.DataFrame): The input DataFrame containing order data.
    
    Returns:
    pandas.DataFrame: The daily order DataFrame with columns 'order_date', 'order_count', and 'total_sales'.
    """
    daily_order_df = df.resample(rule="D", on="order_date").agg({
        "order_id": "nunique",
        "total_price": "sum"
        })
    
    daily_order_df = daily_order_df.reset_index()
    daily_order_df.rename(columns={
        "order_id": "order_count",
        "total_price": "total_sales"
    }, inplace=True)
    return daily_order_df

def create_sum_order_items_df(df):
    """
    Create a DataFrame that calculates the sum of order items for each product.

    Args:
        df (pandas.DataFrame): The input DataFrame containing order items.

    Returns:
        pandas.DataFrame: A DataFrame with the sum of order items for each product, sorted in descending order.

    """
    sum_of_order_items_df = df.groupby("product_name").quantity_x.sum().sort_values(ascending=False).reset_index()
    return sum_of_order_items_df

def create_bygender_df(df):
    """
    Create a dataframe that counts the number of unique customers by gender.

    Parameters:
    df (pandas.DataFrame): The input dataframe containing customer data.

    Returns:
    pandas.DataFrame: A dataframe with two columns - 'gender' and 'customer_count',
                      where 'gender' represents the gender category and 'customer_count'
                      represents the count of unique customers for each gender.
    """
    bygender_df = df.groupby("gender").customer_id.nunique().reset_index()
    bygender_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
    return bygender_df

def create_byage_df(df):
    """
    Create a dataframe that groups the input dataframe by age and calculates the number of unique customer IDs for each age group.

    Parameters:
    df (pandas.DataFrame): The input dataframe containing customer data.

    Returns:
    pandas.DataFrame: The resulting dataframe with the following columns:
        - age (int): The age group.
        - customer_count (int): The number of unique customer IDs for each age group.
        - age_group (str): The age group category, categorized as "Youth", "Adults", or "Seniors".
    """
    byage_df = df.groupby("age_group").customer_id.nunique().reset_index()
    byage_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
    byage_df["age_group"] = pd.Categorical(byage_df["age_group"], ["Youth", "Adults", "Seniors"])
    return byage_df

def create_bystate_df(df):
    """
    Create a dataframe that counts the number of unique customers by state.

    Parameters:
    df (pandas.DataFrame): The input dataframe containing customer data.

    Returns:
    pandas.DataFrame: A dataframe with two columns: 'state' and 'customer_count'.
                      'state' represents the state name, and 'customer_count' represents
                      the number of unique customers in that state.
    """
    by_state_df = df.groupby("state").customer_id.nunique().reset_index()
    by_state_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
    return by_state_df

def create_rmf_df(df):
    """
    Create an RFM (Recency, Frequency, Monetary) DataFrame from the given DataFrame.
    
    Parameters:
    df (pandas.DataFrame): The input DataFrame containing customer order information.
    
    Returns:
    pandas.DataFrame: The RFM DataFrame with columns for customer ID, recency, frequency, and monetary value.
    """
    rmf_df = df.groupby("customer_id", as_index=False).agg({
        "order_date": "max",
        "order_id": "nunique",
        "total_price": "sum"
    })
    
    rmf_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    
    rmf_df["max_order_timestamp"] = rmf_df["max_order_timestamp"].dt.date
    recent_date = df["order_date"].dt.date.max()
    rmf_df["recency"] = rmf_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rmf_df.drop(columns=["max_order_timestamp"], inplace=True)
    
    return rmf_df