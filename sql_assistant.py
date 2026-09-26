import mysql.connector
from ollama import chat
import re

# ============================================================
# NATURAL LANGUAGE → SQL → MYSQL → AI ANSWER
# ============================================================

print("=" * 60)
print("        AI BUSINESS SQL ASSISTANT")
print("=" * 60)


# ============================================================
# 1. MYSQL CONNECTION
# ============================================================

try:

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ai_business_assistant"
    )

    print("\n✅ MySQL connected successfully.")

except Exception as e:

    print("\n❌ MySQL connection failed.")
    print(e)
    exit()


# ============================================================
# 2. GET TABLE STRUCTURE
# ============================================================

cursor = connection.cursor()

cursor.execute("DESCRIBE sales_data")

columns = cursor.fetchall()

column_names = [column[0] for column in columns]

print("\nAvailable columns:")
print(column_names)


# ============================================================
# 3. CREATE DATABASE SCHEMA FOR OLLAMA
# ============================================================

schema = """
Table name: sales_data

Columns:
"""

for column in column_names:
    schema += f"- {column}\n"


# ============================================================
# 4. GENERATE SQL USING OLLAMA
# ============================================================

def generate_sql(user_question):

    prompt = f"""
You are an expert MySQL data analyst.

Convert the user's business question into ONE MySQL SELECT query.

DATABASE SCHEMA:

{schema}

USER QUESTION:

{user_question}

STRICT RULES:

1. Generate ONLY a SELECT query.
2. Use ONLY the sales_data table.
3. Do not use INSERT.
4. Do not use UPDATE.
5. Do not use DELETE.
6. Do not use DROP.
7. Do not use ALTER.
8. Do not use CREATE.
9. Do not use TRUNCATE.
10. Do not use multiple SQL statements.
11. Do not use markdown.
12. Return only the SQL query.

Example:

Question:
What is the total sales?

Answer:
SELECT SUM(total_amount) AS total_sales FROM sales_data;
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

    sql = response["message"]["content"].strip()

    # Remove markdown code fences if Ollama adds them
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)

    sql = sql.strip()

    return sql


# ============================================================
# 5. SQL SECURITY VALIDATION
# ============================================================

def validate_sql(sql):

    sql_clean = sql.strip().lower()

    # Must start with SELECT
    if not sql_clean.startswith("select"):
        return False

    # Only allow sales_data
    if "sales_data" not in sql_clean:
        return False

    # Block dangerous SQL commands
    forbidden_words = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "truncate",
        "replace",
        "grant",
        "revoke"
    ]

    for word in forbidden_words:

        if re.search(r"\b" + word + r"\b", sql_clean):
            return False

    # Block multiple statements
    if ";" in sql_clean[:-1]:
        return False

    return True


# ============================================================
# 6. EXECUTE SQL
# ============================================================

def execute_sql(sql):

    cursor = connection.cursor(dictionary=True)

    cursor.execute(sql)

    result = cursor.fetchall()

    cursor.close()

    return result


# ============================================================
# 7. CONVERT SQL RESULT INTO BUSINESS ANSWER
# ============================================================

def generate_business_answer(question, sql, result):

    prompt = f"""
You are a professional Business Analyst.

The user asked:

{question}

SQL query executed:

{sql}

SQL result:

{result}

Explain the result in simple business language.

Rules:
1. Use the actual result.
2. Do not invent information.
3. Mention important numbers.
4. Keep the answer concise.
5. If the result is empty, explain that no matching records were found.
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


# ============================================================
# 8. INTERACTIVE SQL ASSISTANT
# ============================================================

print("\n" + "=" * 60)
print("        ASK BUSINESS QUESTIONS")
print("=" * 60)

print("\nType 'exit' to stop.")

while True:

    question = input("\nYou: ").strip()

    if question.lower() == "exit":

        break

    if question == "":

        print("Please enter a question.")

        continue


    # --------------------------------------------------------
    # Generate SQL
    # --------------------------------------------------------

    print("\n🤖 Generating SQL...")

    try:

        sql = generate_sql(question)

    except Exception as e:

        print("\n❌ Ollama error:")
        print(e)

        continue


    print("\nGenerated SQL:")
    print(sql)


    # --------------------------------------------------------
    # Validate SQL
    # --------------------------------------------------------

    if not validate_sql(sql):

        print("\n❌ SQL query rejected for security reasons.")

        continue


    # --------------------------------------------------------
    # Execute SQL
    # --------------------------------------------------------

    try:

        result = execute_sql(sql)

    except Exception as e:

        print("\n❌ SQL execution error:")
        print(e)

        continue


    print("\nSQL Result:")
    print(result)


    # --------------------------------------------------------
    # Generate Business Answer
    # --------------------------------------------------------

    print("\n🤖 AI Business Answer:")

    try:

        answer = generate_business_answer(
            question,
            sql,
            result
        )

        print(answer)

    except Exception as e:

        print("\n❌ AI answer error:")
        print(e)


# ============================================================
# 9. CLOSE CONNECTION
# ============================================================

connection.close()

print("\n✅ MySQL connection closed.")
print("AI Business SQL Assistant stopped.")