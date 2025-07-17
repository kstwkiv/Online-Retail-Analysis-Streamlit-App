import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

@st.cache_resource
def load_data_and_create_db():
    try:
        df = pd.read_csv("OnlineRetail.csv", encoding='ISO-8859-1')

       
        df.dropna(subset=['CustomerID', 'Description'], inplace=True)
        df = df[df['Quantity'] > 0]
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate']) 
        
        conn = sqlite3.connect(':memory:', check_same_thread=False)
        df.to_sql('onlineretail', conn, if_exists='replace', index=False)
        return conn
    except FileNotFoundError:
        st.error("OnlineRetail.csv not found. Please make sure the file is in the same directory.")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred while loading data or setting up the database: {e}")
        st.stop()

conn = load_data_and_create_db()

if conn is None: 
    st.stop()


@st.cache_data
def load_sql_queries(filepath='queries.sql'):
    queries = {}
    current_query_name = None
    current_query_lines = []

    try:
        with open(filepath, 'r') as f:
            for line in f:
                stripped_line = line.strip()
                if stripped_line.startswith('-- '): 
                    if current_query_name and current_query_lines:
                        queries[current_query_name] = "\n".join(current_query_lines).strip()
                    current_query_name = stripped_line[3:].strip().replace(" ", "_").upper() # Extract name
                    current_query_lines = []
                elif stripped_line:
                    current_query_lines.append(stripped_line)
            # last query
            if current_query_name and current_query_lines:
                queries[current_query_name] = "\n".join(current_query_lines).strip()
        return queries
    except FileNotFoundError:
        st.error(f"SQL queries file not found at {filepath}. Please ensure it exists.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading SQL queries from {filepath}: {e}")
        st.stop()

SQL_QUERIES = load_sql_queries()

if not SQL_QUERIES: # Stop 
    st.error("No SQL queries were loaded. Check 'queries.sql' file content and format.")
    st.stop()

# --- SQL Query ex---

def run_query(query_name, **kwargs):
    query_template = SQL_QUERIES.get(query_name)
    if not query_template:
        st.error(f"SQL query '{query_name}' not found in queries.sql.")
        return pd.DataFrame()

   
    try:
        final_query = query_template.format(**kwargs)
    except KeyError as e:
        st.error(f"Missing parameter for query '{query_name}': {e}")
        return pd.DataFrame()

    try:
        return pd.read_sql_query(final_query, conn)
    except Exception as e:
        st.error(f"Error executing query '{query_name}': {e}")
        st.error(f"Query: {final_query}")
        return pd.DataFrame() 

# --- Streamlit Layout ---
st.set_page_config(layout="wide", page_title="Online Retail Analytics")

st.title("Online Retail Data Analysis")

# Sidebar 
st.sidebar.header("Navigation")
analysis_options = [
    "Overview & Top Products",
    "Customer Insights",
    "Product Recommendations"
]
selected_analysis = st.sidebar.radio("Go to", analysis_options)

if selected_analysis == "Overview & Top Products":
    st.header("Top 10 Most Purchased Products")
    top_products = run_query("TOP_10_MOST_PURCHASED_PRODUCTS")
    st.dataframe(top_products)
    if not top_products.empty:
        fig_products = px.bar(top_products, x='Description', y='TotalSold',
                              title='Top 10 Products by Quantity Sold',
                              labels={'Description': 'Product', 'TotalSold': 'Total Quantity Sold'})
        st.plotly_chart(fig_products)

    st.header("Top 10 Products by Revenue")
    top_revenue_products = run_query("TOTAL_REVENUE_PER_PRODUCT")
    st.dataframe(top_revenue_products)
    if not top_revenue_products.empty:
        fig_revenue = px.bar(top_revenue_products, x='Description', y='Revenue',
                             title='Top 10 Products by Revenue',
                             labels={'Description': 'Product', 'Revenue': 'Total Revenue'})
        st.plotly_chart(fig_revenue)

elif selected_analysis == "Customer Insights":
    st.header("Top 10 Customers by Purchase Volume")
    top_customers = run_query("TOP_CUSTOMERS_BY_PURCHASE_VOLUME")
    st.dataframe(top_customers)
    if not top_customers.empty:
        fig_customers = px.bar(top_customers, x='CustomerID', y='TotalUnits',
                               title='Top 10 Customers by Total Units Purchased',
                               labels={'CustomerID': 'Customer ID', 'TotalUnits': 'Total Units Purchased'})
        st.plotly_chart(fig_customers)

elif selected_analysis == "Product Recommendations":
    st.header("Product Recommendation Engine")

    
    cursor = conn.cursor()
    cursor.execute("DROP VIEW IF EXISTS FrequentlyBoughtTogether;")
    try:
        cursor.execute(SQL_QUERIES["CREATE_FREQUENTLY_BOUGHT_TOGETHER_VIEW"])
        conn.commit()
    except sqlite3.OperationalError as e:
        st.error(f"Error creating view: {e}. Check CREATE_FREQUENTLY_BOUGHT_TOGETHER_VIEW query.")


    st.subheader("Frequently Bought Together (by Product)")

    all_products_df = run_query("GET_ALL_PRODUCT_DESCRIPTIONS")
    if not all_products_df.empty:
        product_list = all_products_df['Description'].tolist()
        selected_product_for_fbt = st.selectbox(
            "Select a Product to see what's frequently bought with it:",
            options=product_list,
            index=0 
        )
        if selected_product_for_fbt:
            fbt_results = run_query("GET_FREQUENTLY_BOUGHT_TOGETHER_FOR_PRODUCT",
                                    product_description=selected_product_for_fbt)
            if not fbt_results.empty:
                st.write(f"Products frequently bought with **{selected_product_for_fbt}**:")
                st.dataframe(fbt_results)
                fig_fbt = px.bar(fbt_results, x='ProductB', y='Frequency',
                                 title=f'Products Frequently Bought with {selected_product_for_fbt}',
                                 labels={'ProductB': 'Frequently Bought Product', 'Frequency': 'Frequency'})
                st.plotly_chart(fig_fbt)
            else:
                st.info(f"No frequently bought together products found for '{selected_product_for_fbt}' (frequency > 50).")
    else:
        st.warning("No product descriptions available for selection.")


    st.subheader("Product Recommendations for a Specific Customer")

    all_customer_ids_df = run_query("GET_ALL_CUSTOMER_IDS")
    if not all_customer_ids_df.empty:
        customer_id_list = all_customer_ids_df['CustomerID'].tolist()
        selected_customer_id = st.selectbox(
            "Select a Customer ID to get recommendations:",
            options=customer_id_list,
            index=0 
        )

        if selected_customer_id:

            customer_recommendations = run_query("GET_PRODUCT_RECOMMENDATIONS_FOR_CUSTOMER",
                                                customer_id=selected_customer_id)
            if not customer_recommendations.empty:
                st.write(f"Recommended products for Customer ID **{selected_customer_id}**:")
                st.dataframe(customer_recommendations)
                fig_cust_rec = px.bar(customer_recommendations, x='RecommendedProduct', y='Strength',
                                      title=f'Recommended Products for Customer {selected_customer_id}',
                                      labels={'RecommendedProduct': 'Recommended Product', 'Strength': 'Recommendation Strength'})
                st.plotly_chart(fig_cust_rec)
            else:
                st.info(f"No recommendations found for Customer ID {selected_customer_id}. This might be because the customer hasn't purchased products that frequently appear with others above the frequency threshold, or the customer hasn't made any purchases.")
    else:
        st.warning("No customer IDs available for selection.")