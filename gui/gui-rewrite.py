from nicegui import ui
import pandas as pd

from src.database import get_engine
from src.models import Base
from src.services import APIService

def init_database():
    engine = get_engine()
    Base.metadata.create_all(engine)

if  __name__ == '__main__':
    init_database()
