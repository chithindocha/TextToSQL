import gradio as gr
from db.database import Database
from nlp.query_processor import QueryProcessor

# Initialize Database and Query Processor
db = Database(db_name="chat_assistant.db")
query_processor = QueryProcessor(db)

def respond(message, history):
    """Processes user queries, fetches results from the database, and returns responses."""
    response = query_processor.process_query(message)
    return response 

# Gradio Chat UI
demo = gr.ChatInterface(
    respond,
    additional_inputs=[],
    title="SQL Chat Assistant",
    description="Ask any database-related question, and I will generate an SQL query and fetch the relevant data.",
)

if __name__ == "__main__":
    demo.launch()
