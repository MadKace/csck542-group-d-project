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

api = APIService()

# Load all data from repositories

students = api.student_repo.get_all()
all_students_df = pd.DataFrame([student.as_dict for student in students])

lecturers = api.lecturer_repo.get_all()
all_lecturers_df = pd.DataFrame([lecturer.as_dict for lecturer in lecturers])

staff = api.staff_repo.get_all()
all_staff_df = pd.DataFrame([staff.as_dict for staff in staff])

courses = api.course_repo.get_all()
all_courses_df = pd.DataFrame([course.as_dict for course in courses])

departments = api.department_repo.get_all()
all_departments_df = pd.DataFrame([department.as_dict for department in departments])

research_projects = api.research_project_repo.get_all()
all_projects_df = pd.DataFrame([rp.as_dict for rp in research_projects])

"""
Helper Functions

These functions will be used to find next_id, handle validation and create table_colours for nicegui ui table
"""

def get_next_id(df, id_column):
    """
    Determines the next available ID for a given entity type
    Arguments: entity dataframe, entity id column
    Returns: maximum of entity id column + 1
    """
    if df.empty:
        return 1
    return int(df[id_column].max())+1

def validate_fields(data, id_column):
    """
        Validates that fields are not empty
        Arguments: data to validate, entity id column
        Returns: True/False depending on pass criteria
    """
    for col, value in data.items():
        if col != id_column and not str(value).strip:
            return False, col
    return True, None

def create_table_columns(df):
    """
        Creates table for ui.table based on columns in the supplied entity dataframe
        Arguments: entity dataframe
        Returns: Columns
    """
    return[
        {
            'name': col,
            'label': col.replace('_', ' ').title(),
            'field': col,
            'sortable': True,
            'align': 'left'
        }
        for col in df.columns
    ]

def filter_dataframe(df, filters):
    filtered_df = df.copy()

    for col, search_text in filters.items():
        if search_text and search_text.strip():
            filtered_df = filtered_df[
                filtered_df[col].astype(str).str.contains(search_text, case = False, na = False)
            ]

    return filtered_df