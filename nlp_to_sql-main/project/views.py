#NLP - SQL
from django.http import JsonResponse
from django.shortcuts import render
from crewai import Agent, Task, Process, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
import json
from django.http import JsonResponse
api_key = "your api key"
def chatbot_ui(request):  
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        message = data.get('message', '') 
        # Here you can add your logic for NLP to SQL query conversion
        nlp = message
        print(nlp,"Hello")

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

        #print(op)
        # For now, let's just respond with a static message
        response = op
        print(response)
        print(type(response))
        return JsonResponse({'response': response})
    return render(request, 'project/chatbot_ui.html')
