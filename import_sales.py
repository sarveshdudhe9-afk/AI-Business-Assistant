import pandas as pd
import mysql.connector

df = pd.read_excel("Ai_Assistant_Dataset.xlsx")

print("CSV rows:", len(df))
print("Columns:")
print(df.columns.tolist())

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="ai_business_assistant"
)

cursor = conn.cursor()

sql = """
INSERT INTO sales_data
(sale_date, customer_name, product, quantity, unit_price,
total_amount, tax_rate, payment_method, sentence,
tax_amount, amount_with_tax, year, month)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

data = [tuple(row) for row in df.itertuples(index=False, name=None)]

cursor.executemany(sql, data)

conn.commit()

print("Rows imported:", cursor.rowcount)

cursor.close()
conn.close()

print("Import completed successfully!")