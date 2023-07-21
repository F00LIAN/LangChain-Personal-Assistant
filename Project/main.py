from fastapi import FastAPI, Form, Depends, Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import openai
from models import Conversation, SessionLocal
from utils import send_message, logger, query_office_365
from custom_utils import agent_creation


app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/message")
async def reply(request: Request, Body: str = Form(), db: Session = Depends(get_db)):
    # Extract the phone number from the incoming webhook request
    form_data = await request.form()
    whatsapp_number = form_data["From"].split("whatsapp:")[-1]
    print(f"Sending the LangChain response to this number: {whatsapp_number}")

    # Get the generated text from the LangChain agent
    langchain_response = agent_creation(Body)

    # Store the conversation in the database
    try:
        conversation = Conversation(
            sender=whatsapp_number, message=Body, response=langchain_response
        )
        db.add(conversation)
        db.commit()
        logger.info(f"Conversation #{conversation.id} stored in database")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error storing conversation in database: {e}")
    send_message(whatsapp_number, langchain_response)
    return ""
