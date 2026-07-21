from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db" # Tells sqlalchemy where to connect, . inside after /// represents the current directory and blog.db is a file and will generated automatically

engine = create_engine( # This represents the connection to our database
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}, # check same thread is something sqllite specific, sql lite normally allows only one thread but fastapi can handle multiple requests across threads so we disabled that restriction here and this isnt needed in postgres or mysql
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # This can be called as a factory that creates database sessions. A session is transaction with the database and each request gets its own session. Here autocommit and autoflush are designated false as we want to control when changes are committed  


class Base(DeclarativeBase): # Inheriting from DeclarativeBase is the modern approach with better type checking support 
    pass

# fastapi's dependancy injection calls this function for each request and handles that clean up automatically. dependency injection here is a way of saying that this route needs a database session to work so go ahead adn give it one. Instead of creating a session inside the route we declare that we need one and fastapi just provides one to us   
def get_db(): # This is a dependency function that provide sessions to a route, its a generator using yield db and with statement (with SessionLocal() as db) as a context manager like opening a file. This ensures a clean up even if a error occurs. 
    with SessionLocal() as db:
        yield db




