from flask import Flask, render_template, request, redirect, url_for
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI

app = Flask(__name__)

api_key = "AIzaSyBRzRrIKVRDmX7bApGo7OadHabT487kDk4"  # Your API key here

# Load the book text
try:
    with open(r"C:\Users\jothi\Downloads\BookHub-flask-app-20240410T145314Z-001\BookHub-flask-app\history_of_computers.txt", "r") as f:
        book = f.read()
except FileNotFoundError:
    print("Error: Could not find the text file.")
    exit()

# Initialize the AI agent
agent_nlp_sql = Agent(
    role="Book Information Agent",
    goal="Information Retrieval and answer questions from the book or text provided",
    backstory="You are an expert book reader and help others by answering the contents in the book",
    verbose=False,
    llm=ChatGoogleGenerativeAI(model="gemini-pro", verbose=True, temperature=0.1, google_api_key=api_key)
)

nlp_task = Task(
    description=f"Answer questions based on the content of the provided from this book\n.The contents of the book is\n{book}",
    agent=agent_nlp_sql,
    expected_output="Generated response based on the provided book text."
)

crew = Crew(
    agents=[agent_nlp_sql],
    tasks=[nlp_task],
    verbose=False,
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_question = request.form['question']
        if user_question:
            # Update task description with user's question
            nlp_task.description = f"Answer the question: {user_question}"
            try:
                # Run the crew
                op = crew.kickoff()
                response = op
            except Exception as e:
                response = f"Error: An error occurred while processing the question. ({e})"
            return render_template('index.html', response=response)
    return render_template('index.html', response=None)

if __name__ == '__main__':
    app.run(debug=True)
