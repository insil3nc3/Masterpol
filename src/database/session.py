from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "Partners.db")
engine = create_engine(f"sqlite:///{db_path}", echo=True)
Session = sessionmaker(engine)
session = Session()