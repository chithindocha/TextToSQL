import re
from huggingface_hub import InferenceClient

class SQLModel:
    def __init__(self, model_name="HuggingFaceH4/zephyr-7b-beta"):
        self.client = InferenceClient(model_name)

    def generate_sql(self, natural_language_query):
        prompt = (
            "You are a highly skilled SQL translator. Your task is to convert natural language descriptions of data queries "
            "into correct and optimized SQL statements.\n\n"
            "Here is the schema information for our database :\n\n"
            "Table: Employees\n"
            "- id (INT)\n"
            "- NAME (VARCHAR)\n"
            "- Department (VARCHAR)\n"
            "- Salary (INT)\n"
            "- Hire_Date (DATE)\n\n"
            "Table: Departments\n"
            "- ID (INT)\n"
            "- Name (VARCHAR)\n"
            "- Manager (VARCHAR)\n\n"
            "Here are a few examples:\n\n"
            "1. **Input**: \"Show me all employees in the Sales department.\"\n"
            "**Output**:\n\n"
            "        SELECT *\n"
            "        FROM Employees\n"
            "        WHERE Department = 'Sales';\n\n"
            "2. **Input**: \"Who is the manager of the Engineering department?\"\n"
            "**Output**:\n\n"
            "        SELECT Manager\n"
            "        FROM Departments\n"
            "        WHERE Name = 'Engineering';\n\n"
            "3. **Input**: \"List all employees hired after 2021-01-01.\"\n"
            "**Output**:\n\n"
            "        SELECT *\n"
            "        FROM Employees\n"
            "        WHERE Hire_Date > '2021-01-01';\n\n"
            "4. **Input**: \"What is the total salary expense for the Marketing department?\"\n"
            "**Output**:\n\n"
            "        SELECT SUM(Salary)\n"
            "        FROM Employees\n"
            "        WHERE Department = 'Marketing';\n\n"
            "5. **Input**: \"Find the average salary of employees in each department.\"\n"
            "**Output**:\n\n"
            "        SELECT Department, AVG(Salary) AS average_salary\n"
            "        FROM Employees\n"
            "        GROUP BY Department;\n\n"
            "Please do not return additional text besides query.\n"
            "Please only answer queries which makes sense for the given schema. Else just return - \"No information found\""
        )

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": natural_language_query}
        ]

        result = self.client.chat_completion(
            messages,
            max_tokens=150,
            stream=False,
            temperature=0.7,
            top_p=0.95,
        )

        # Initialize a variable to hold the extracted SQL text.
        sql_query = ""

        # Check if the result is a plain string.
        if isinstance(result, str):
            sql_query = result
        # If the result is a list, iterate over its tokens.
        elif isinstance(result, list):
            for token in result:
                if isinstance(token, str):
                    sql_query += token
                elif hasattr(token, "choices"):
                    # Extract from the structured object.
                    sql_query += token.choices[0].delta.content
                else:
                    sql_query += str(token)
        # Otherwise, if it's an object with choices, extract its content.
        elif hasattr(result, "choices"):
            sql_query = result.choices[0].message.content
        else:
            sql_query = str(result)

        # Optional: If the model output is in a markdown code block, extract only that content.
        match = re.search(r"```sql(.*?)```", sql_query, re.DOTALL | re.IGNORECASE)
        if match:
            sql_query = match.group(1).strip()

        # Remove both literal "\n" substrings and actual newline characters.
        sql_query = sql_query.replace("\\n", " ").replace("\n", " ")
        # Remove extra spaces.
        sql_query = " ".join(sql_query.split())

        # Extract only the SQL command: starting from the first occurrence of "select" to the first semicolon.
        extraction_pattern = r"(?i)(select\s.*?;)"
        extraction_match = re.search(extraction_pattern, sql_query, re.DOTALL)
        if extraction_match:
            sql_query = " ".join(extraction_match.group(1).split())

        print(sql_query)
        return sql_query
