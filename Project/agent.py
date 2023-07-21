import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from dotenv import load_dotenv
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
from langchain.agents.agent_toolkits import O365Toolkit

load_dotenv()

############## Configure Azure ID and Secret to use email functionality #####################


# get access to main accounts
toolkit = O365Toolkit()
tools = toolkit.get_tools()
tools


# Initialize the LLM and Agent
llm = OpenAI(temperature=0)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    verbose=False,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
)

# Run the Email Task
agent.run(
    "Create an email draft for me for my brother with the email of 'sotel102@mail.chapman.edu' "
    "let him know that I plan on bringing the cooler to the beach on saturday."
    "Also highlight to him that I am using Artificial intelligence to send him this email."
)
