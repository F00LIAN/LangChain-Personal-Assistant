from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# Loading secret information like a treasure map
load_dotenv()


# Creating a special key to open the treasure chest (our database)
url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    database="wikipedia_ai",
    port=3306,
)

engine = create_engine(
    url
)  # We use the special key to be able to open the treasure chest
SessionLocal = sessionmaker(
    bind=engine
)  # Preparing a special room to put and take out treasures
Base = declarative_base()  # Drawing a blueprint of our treasures


class Conversation(Base):  # Each treasure is a conversation
    __tablename__ = "conversations"  # Our treasure is called 'conversations'

    id = Column(
        Integer, primary_key=True, index=True
    )  # Each treasure has a special number
    sender = Column(String(255))  # The name of the person who sent the treasure
    message = Column(String(1000))  # The message they sent as a treasure
    response = Column(String(1000))  # The response to the message as another treasure


# We create places for all our treasures in the chest
Base.metadata.create_all(engine)
