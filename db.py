from sqlmodel import SQLModel,Session,create_engine

DATABASE_URL = "sqlite:///./rangmanch.db"

engine=create_engine(DATABASE_URL,echo=True)


def create_tables():
    """create tables in the database and all the tables are defined by sqlmodel"""
    SQLModel.metadata.create_all(engine)
    
def get_session():
    """create a session to the database"""
    with Session(engine) as session:
        yield session