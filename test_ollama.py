from ollama import chat

# AI Business Assistant using FREE local Ollama
def ask_ai_business_assistant(user_question, business_data):
    prompt = f"""
You are an AI Business Assistant and Business Data Analyst.

You are analyzing the following business data:

{business_data}

Answer the user's question using the data provided.

User question:
{user_question}

Rules:
1. Give a clear and accurate answer.
2. Use numbers from the data when available.
3. Do not invent information.
4. Keep the answer business-friendly.
5. If the data does not contain enough information, clearly say so.
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


# Test the AI Business Assistant
business_data = """
Total Sales: 100000
Total Orders: 5000
Average Order Value: 20
Top Product: Product A
Top Customer: Customer A
"""

question = "Give me a short summary of the business performance."

answer = ask_ai_business_assistant(question, business_data)

print("\nAI BUSINESS ASSISTANT")
print("--------------------")
print(answer)