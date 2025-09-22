
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
load_dotenv()

model = OpenAIChat(id="gpt-4o-mini")

def agno_tavily():
    agent = Agent(tools=[TavilyTools()])
    agent.model = model
    agent.print_response("Search tavily for 'Higienopolis'", markdown=True)

    # Adicionar esta parte para executar a função
if __name__ == "__main__":
    print("🚀 Executando teste agno_tavily...")
    agno_tavily()
    print("✅ Teste concluído!")