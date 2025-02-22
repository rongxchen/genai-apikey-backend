from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config.reader import config
from src.model.util import to_string


DATABASE_URL = config["sqlite3"]["url"]


engine = create_engine(DATABASE_URL)
Base = declarative_base()


@to_string
class User(Base):
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(String, nullable=False)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    status = Column(Integer, nullable=False, default=1)
    is_deleted = Column(Integer, nullable=False, default=0)
    created_at = Column(Integer)
    updated_at = Column(Integer)
    
    
@to_string
class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    api_key_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    key = Column(String, nullable=False)
    status = Column(Integer, nullable=False, default=1)
    is_default = Column(Integer, nullable=False, default=0)
    created_at = Column(Integer)
    updated_at = Column(Integer)
    
    
@to_string
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    chat_id = Column(String, nullable=False)
    message_id = Column(String, nullable=False)
    content = Column(String, nullable=False)
    role = Column(String, nullable=False)
    model = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    token_used = Column(Integer)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer)
    has_think = Column(Integer, nullable=False, default=0)
    think_content = Column(String)
    
    
@to_string
class Chat(Base):
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    chat_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    model = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    created_at = Column(Integer)
    updated_at = Column(Integer)


Base.metadata.create_all(engine)


session = None

def get_session():
    # global session, engine
    # if session is not None:
    #     return session
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
