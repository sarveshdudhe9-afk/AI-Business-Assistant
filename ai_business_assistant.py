import mysql.connector
from ollama import chat
from getpass import getpass

# ============================================================
# AI BUSINESS ASSISTANT
# MySQL + Python + FREE LOCAL OLLAMA
# ============================================================

print("=" * 60)
print("              AI BUSINESS ASSISTANT")
print("=" * 60)


# ============================================================
# 1. CONNECT TO MYSQL
# ============================================================

print("\nConnecting to MySQL...")

mysql_password = getpass("Enter your MySQL password: ")

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=mysql_password,
        database="ai_business_assistant"
    )

    print("MySQL connection successful!")

except Exception as e:
    print("\nMySQL connection failed.")
    print("Error:", e)
    exit()


# ============================================================
# 2. LOAD SALES DATA FROM MYSQL
# ============================================================

try:
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sales_data")

    rows = cursor.fetchall()

    print(f"Loaded {len(rows)} records from sales_data.")

except Exception as e:
    print("\nCould not load sales data.")
    print("Error:", e)

    connection.close()
    exit()


# ============================================================
# 3. CONVERT DATABASE DATA INTO TEXT
# ============================================================

business_data = ""

for row in rows:
    business_data += str(row) + "\n"


# ============================================================
# 4. AI BUSINESS ASSISTANT FUNCTION
# ============================================================

def ask_ai_business_assistant(user_question):

    prompt = f"""
You are an AI Business Assistant and Business Data Analyst.

You are analyzing real business sales data retrieved from a MySQL database.

DATABASE DATA:

{business_data}

USER QUESTION:

{user_question}

IMPORTANT RULES:

1. Answer using the database data provided above.
2. Do not invent numbers or information.
3. Use calculations when they can be derived from the data.
4. Give clear and business-friendly answers.
5. If the requested information is not available, clearly say:
   "The available database does not contain enough information to answer this."
6. When appropriate, mention the relevant numbers.
7. Keep answers concise but useful.
"""


    try:

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

    except Exception as e:

        return f"Error communicating with Ollama: {e}"


# ============================================================
# 5. START AI CHAT
# ============================================================

print("\n" + "=" * 60)
print("              AI BUSINESS ASSISTANT READY")
print("=" * 60)

print("\nYou can ask questions about your sales data.")
print("Type 'exit' to stop the assistant.")

while True:

    user_question = input("\nYou: ")

    if user_question.lower().strip() == "exit":
        print("\nAI Business Assistant stopped.")
        break

    if user_question.strip() == "":
        print("Please enter a question.")
        continue

    answer = ask_ai_business_assistant(user_question)

    print("\nAI Business Assistant:")
    print(answer)


# ============================================================
# 6. CLOSE MYSQL CONNECTION
# ============================================================

cursor.close()
connection.close()

print("\nMySQL connection closed.")