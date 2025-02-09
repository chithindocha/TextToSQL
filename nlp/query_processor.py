import re
import sqlite3  # Added import for sqlite3
from datetime import datetime
from db.database import Database
from nlp.sql_model import SQLModel

class QueryProcessor:
    def __init__(self, db):
        self.db = db
        self.sql_model = SQLModel()

    def convert_date(self, date_str):
        formats = [
            '%d/%m/%Y',
            '%d %B %Y',
            '%B %Y',
            '%b %Y',
            '%Y-%m-%d'
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        raise ValueError('Invalid date format')

    def extract_and_convert_date(self, user_query):
        date_pattern = r'\b(\b[0-9]{1,2}[/-]?[0-9]{1,2}[/-]?[0-9]{2,4}\b|\b(?:\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b[- ]?[0-9]{1,2}[- ]?[0-9]{2,4}\b|\b[0-9]{2,4}[- ]?(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b)\b)'
        match = re.search(date_pattern, user_query, re.I)
        if match:
            date_str = match.group(0)
            try:
                return self.convert_date(date_str)
            except ValueError:
                return None
        return None


    def process_query(self, user_query):
        conn = self.db.connect()
        if not conn:
            return "Failed to connect to the database."

        response = ''
        try:
            # Generate SQL query using the LLM model
            sql_query = self.sql_model.generate_sql(user_query)
            # Execute generated SQL query against the database
            cursor = self.db.execute_query(sql_query)
            if cursor:
                results = cursor.fetchall()
                if results:
                    response = f'Results: {results}'
                else:
                    response = 'No results found.'
            else:
                response = 'Error executing query.'
        finally:
            self.db.close()
        return response