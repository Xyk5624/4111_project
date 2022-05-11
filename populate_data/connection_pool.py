from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

address = "postgresql+psycopg2://yx2622:3827@34.74.246.148/proj1part2"

engine = create_engine(address,connect_args={'connect_timeout': 30})

class Session:
    def __init__(self, engine):
        self.engine = engine
        self.session = None

    def __enter__(self) -> Session:
        session = sessionmaker(bind=self.engine)
        self.session = session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        del self.session
