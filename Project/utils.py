import logging
import os
from dotenv import load_dotenv
from twilio.rest import Client
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.agents.agent_toolkits import O365Toolkit
from langchain.agents import Tool
from typing import Optional, Type
import json
from langchain.utilities import SerpAPIWrapper
from langchain.tools import YouTubeSearchTool
from langchain.utilities import TextRequestsWrapper
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)


# Set environment variables
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_number = os.getenv("TWILIO_NUMBER")
serpapi_api_key = os.getenv("SERPAPI_API_KEY")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Sending message logic through Twilio Messaging API
def send_message(to_number, body_text):
    try:
        message = client.messages.create(
            from_=f"whatsapp:{twilio_number}",
            body=body_text,
            to=f"whatsapp:{to_number}",
        )
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")


def query_office_365(query):
    """Search Wikipedia through the LangChain API
    and use the OpenAI LLM wrapper and retrieve
    the agent result based on the received query
    """
    llm = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

    toolkit = O365Toolkit()
    tools = toolkit.get_tools()

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
    )
    return agent.run(query)
