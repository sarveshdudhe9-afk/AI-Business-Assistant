# AI Business Assistant

## 📌 Project Overview

AI Business Assistant is an interactive data analysis application that allows users to ask business-related questions in natural language and receive data-driven answers.

The application combines **Python, MySQL, Streamlit, and a local Large Language Model (LLM)** to convert natural-language business questions into useful insights and visualizations.

## 🎯 Project Objective

Business users often need to analyze sales data but may not have strong SQL or programming knowledge.

The objective of this project is to provide a simple interface where users can ask questions about business data in natural language and receive relevant answers, analysis, and visualizations.

## 🛠️ Tools & Technologies

* **Python** – Application development and data processing
* **MySQL** – Database and sales data storage
* **Streamlit** – Interactive web application
* **Ollama** – Local LLM execution
* **Llama 3.2** – Local language model
* **Pandas** – Data manipulation and analysis
* **Matplotlib** – Data visualization
* **Machine Learning / Logic** – Data analysis and prediction

## 🔄 Project Workflow

```text id="a3f1c9"
Sales Dataset
      ↓
Data Cleaning & Preprocessing
      ↓
MySQL Database
      ↓
User asks a question
      ↓
Local LLM + Python Logic
      ↓
Data Analysis
      ↓
Answer / Visualization
      ↓
Business Insight
```

## 🤖 Key Features

### 1. Natural Language Queries

Users can ask business questions using normal language instead of writing SQL queries.

Example:

> What were the monthly sales?

The application processes the question and provides a relevant business answer.

### 2. Data Analysis

The application analyzes sales data stored in MySQL and provides useful business insights.

### 3. Interactive Visualizations

The application can generate visual representations of business data, making trends and patterns easier to understand.

### 4. Local LLM

The project uses **Ollama with Llama 3.2** to run the language model locally.

Using a local model avoids depending on a paid external API for the core natural-language interaction.

### 5. Business Predictions

The application also includes logic for analyzing trends and generating future-oriented business insights.

## 📊 Dataset

The project uses sales data containing business-related information.

The dataset was cleaned and prepared before being stored in MySQL.

During data preparation:

* Duplicate records were identified
* The dataset was cleaned
* Data was standardized
* The final dataset was prepared for analysis
* Cleaned data was stored in the MySQL `sales_data` table

## 🗄️ MySQL Database

MySQL is used as the backend database for storing and querying the sales data.

The application connects to the database and retrieves relevant information based on the user's business question.

## 🖥️ Streamlit Application

Streamlit provides the user interface for the AI Business Assistant.

The application allows users to:

* Enter natural-language questions
* Analyze business data
* View generated answers
* Generate charts
* Explore business insights

## 💡 Business Use Cases

The AI Business Assistant can help business users:

* Analyze sales performance
* Understand monthly trends
* Explore business metrics
* Identify important patterns
* Generate visual reports
* Ask data-related questions without manually writing SQL queries

## 📁 Project Structure

```text id="z2rj8k"
ai-business-assistant/
│
├── README.md
├── app.py
├── data/
├── sql/
├── images/
├── requirements.txt
└── .gitignore
```

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Ollama

Make sure Ollama is installed and the required Llama model is available locally.

### 4. Configure MySQL

Create the required database and `sales_data` table and update the database connection settings.

### 5. Run the Streamlit application

```bash
streamlit run app.py
```

## 📌 Example Questions

Users can ask questions such as:

* What are the monthly sales?
* Which products generate the highest sales?
* What is the sales trend?
* Which category performs best?
* What are the expected sales for the next month?

## 🔮 Future Improvements

Possible future improvements include:

* More advanced forecasting
* Additional business KPIs
* More visualization types
* Improved natural-language query handling
* Role-based dashboards
* Support for larger datasets

## 👨‍💻 Author

**Sarvesh Dudhe**

Electronics Engineering | Data Analyst | Machine Learning | Generative AI

Skills: Python | SQL | MySQL | Excel | Streamlit | Machine Learning | Generative AI
