import streamlit as st
import pandas as pd
import mysql.connector
from ollama import chat

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Business Assistant",
    page_icon="🤖",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("🤖 AI Business Assistant")
st.subheader("Business Analytics Dashboard")

st.markdown("---")

# =========================================================
# MYSQL CONNECTION
# =========================================================

@st.cache_data
def load_data():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ai_business_assistant"
    )

    query = "SELECT * FROM sales_data"

    df = pd.read_sql(query, connection)

    connection.close()

    return df


# =========================================================
# LOAD DATA
# =========================================================

try:

    df = load_data()

except Exception as e:

    st.error("Unable to connect to MySQL.")
    st.error(e)
    st.stop()


# =========================================================
# DATA PREPARATION
# =========================================================

df.columns = df.columns.str.strip().str.lower()

# Convert important columns to numeric

if "total_amount" in df.columns:
    df["total_amount"] = pd.to_numeric(
        df["total_amount"],
        errors="coerce"
    )

if "quantity" in df.columns:
    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = df["total_amount"].sum()

total_orders = len(df)

average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

total_quantity = (
    df["quantity"].sum()
    if "quantity" in df.columns
    else 0
)


# =========================================================
# KPI CARDS
# =========================================================

st.markdown("### 📊 Business Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Sales",
        f"₹{total_sales:,.2f}"
    )

with col2:
    st.metric(
        "🧾 Total Orders",
        f"{total_orders:,}"
    )

with col3:
    st.metric(
        "📦 Total Quantity",
        f"{total_quantity:,.0f}"
    )

with col4:
    st.metric(
        "💵 Average Order Value",
        f"₹{average_order_value:,.2f}"
    )


st.markdown("---")


# =========================================================
# PRODUCT ANALYSIS
# =========================================================

st.markdown("### 🛍️ Product Analysis")

if "product" in df.columns:

    product_sales = (
        df.groupby("product")["total_amount"]
        .sum()
        .sort_values(ascending=False)
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("#### Sales by Product")

        st.bar_chart(product_sales)

    with col2:

        top_product = product_sales.idxmax()

        st.markdown("#### 🏆 Top Product")

        st.success(
            f"**{top_product}**"
        )

        st.write(
            f"Sales generated: ₹{product_sales.max():,.2f}"
        )

else:

    st.warning("Product column not found.")


st.markdown("---")

# =========================================================
# SALES TREND ANALYSIS
# =========================================================

st.markdown("---")

st.markdown("### 📈 Sales Trend Analysis")

# Convert sale_date to datetime
if "sale_date" in df.columns:

    df["sale_date"] = pd.to_datetime(
        df["sale_date"],
        errors="coerce"
    )

    # Remove invalid dates
    trend_df = df.dropna(
        subset=["sale_date"]
    ).copy()

    # Monthly sales
    monthly_sales = (
        trend_df
        .groupby(
            trend_df["sale_date"].dt.to_period("M")
        )["total_amount"]
        .sum()
    )

    # Convert period to string for Streamlit
    monthly_sales.index = monthly_sales.index.astype(str)

    st.markdown("#### Monthly Sales")

    st.line_chart(monthly_sales)

    # Best month
    if len(monthly_sales) > 0:

        best_month = monthly_sales.idxmax()
        best_month_sales = monthly_sales.max()

        lowest_month = monthly_sales.idxmin()
        lowest_month_sales = monthly_sales.min()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🏆 Best Sales Month",
                best_month,
                f"₹{best_month_sales:,.2f}"
            )

        with col2:

            st.metric(
                "📉 Lowest Sales Month",
                lowest_month,
                f"₹{lowest_month_sales:,.2f}"
            )

else:

    st.warning(
        "The sale_date column was not found."
    )

# =========================================================
# AI SALES TREND INSIGHTS
# =========================================================

st.markdown("---")

st.markdown("### 🧠 AI Sales Trend Insights")

if "monthly_sales" in locals() and len(monthly_sales) > 0:

    # Convert monthly sales into text
    trend_information = monthly_sales.to_string()

    trend_prompt = f"""
You are a professional Business Data Analyst.

Analyze the following monthly sales data:

{trend_information}

Provide:

1. Overall sales trend
2. Best-performing month
3. Lowest-performing month
4. Important business insight
5. One practical recommendation

Rules:
- Use only the data provided.
- Do not invent numbers.
- Keep the explanation concise.
- Use clear business language.
"""

    if st.button("🧠 Generate AI Insights"):

        with st.spinner("AI is analyzing the sales trend..."):

            try:

                response = chat(
                    model="llama3.2",
                    messages=[
                        {
                            "role": "user",
                            "content": trend_prompt
                        }
                    ]
                )

                insight = response["message"]["content"]

                st.success(insight)

            except Exception as e:

                st.error(
                    "Unable to generate AI insights."
                )

                st.error(e)

else:

    st.info(
        "Monthly sales data is not available for AI analysis."
    )

# =========================================================
# AI BUSINESS ASSISTANT
# =========================================================

st.markdown("### 🤖 Ask Your Business Assistant")

st.write(
    "Ask questions about your sales data in natural language."
)

user_question = st.text_input(
    "Enter your business question:",
    placeholder="Example: What is the total sales amount?"
)


# =========================================================
# AI FUNCTION
# =========================================================

def ask_ai(question):

    # Create a compact business summary for Ollama

    business_summary = f"""
Business Dataset Summary:

Total Sales: ₹{total_sales:,.2f}

Total Orders: {total_orders}

Total Quantity: {total_quantity}

Average Order Value: ₹{average_order_value:,.2f}

Number of Products: {df["product"].nunique() if "product" in df.columns else "Unknown"}

Top Product: {df.groupby("product")["total_amount"].sum().idxmax() if "product" in df.columns else "Unknown"}

Top Product Sales:
₹{df.groupby("product")["total_amount"].sum().max():,.2f}

Product Sales:
{product_sales.to_string() if "product" in df.columns else "Not available"}
"""

    prompt = f"""
You are an AI Business Analyst.

Use ONLY the business information provided below.

{business_summary}

User Question:
{question}

Rules:

1. Give an accurate business answer.
2. Use numbers from the data.
3. Do not invent information.
4. Keep the answer clear and professional.
5. If the information is unavailable, say that clearly.
"""

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# =========================================================
# ASK QUESTION
# =========================================================

if user_question:

    with st.spinner("🤖 Analyzing your business data..."):

        try:

            answer = ask_ai(user_question)

            st.markdown("### 💡 AI Answer")

            st.info(answer)

        except Exception as e:

            st.error("Unable to communicate with Ollama.")

            st.error(e)


# =========================================================
# DATA PREVIEW
# =========================================================

with st.expander("🔍 View Sales Data"):

    st.dataframe(
        df,
        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "AI Business Assistant | Python + MySQL + Ollama + Streamlit"
)