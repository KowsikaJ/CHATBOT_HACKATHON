#NLP - SQL
from crewai import Agent, Task, Process, Crew
from langchain_google_genai import ChatGoogleGenerativeAI


api_key = "AIzaSyDGp7zaOeZGQA_-rCHn9VrmK4lldJkdu24"

nlp = input("How can i help?: ")

agent_nlp_sql = Agent(
    role = 'NLP to SQL converter',
    goal = 'Generate Natural language to sql queries from the given input',
    backstory = 'You are a Database Engineer who is well versed in understanding natural languages and converting them into SQL queries.',
    verbose =False,
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",verbose=True,temperature=0.1, google_api_key=api_key
    )
)

nlp_task = Task(
    description = f"generate SQL query based on the input from the user and make sure the query is accurate, here's the query : {nlp}",
    expected_output="SQL query output based on the input.",
    agent = agent_nlp_sql
)

crew = Crew(
    agents = [agent_nlp_sql],
    tasks = [nlp_task],
    verbose = False,
)

op = crew.kickoff()

print(op)