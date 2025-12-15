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
    """
        Returns a filtered entity dataframe
        Arguments: entity dataframe, filters
        Returns: filtered entity dataframe
    """

    filtered_df = df.copy()

    for col, search_text in filters.items():
        if search_text and search_text.strip():
            filtered_df = filtered_df[
                filtered_df[col].astype(str).str.contains(search_text, case = False, na = False)
            ]

    return filtered_df

"""
CRUD Service Class

Originally, CRUD operations for each entity was going to be handled individually, however, it makes more sense to do 
them via a service class that can handle it for any entity. This is due to the database design
"""

class CRUDService:
    def __init__(self, entity_name, df, repo, id_column, table_widget):
        """
            initalises the CRUD service by defining self to the applicable entity
            Arguments: self, entity name, entity df, entity repo, entity id_column, relevant table_widget
            Returns: filtered entity dataframe
        """
        self.entity_name = entity_name
        self.df = df
        self.repo = repo
        self.id_column = id_column
        self.table_widget = table_widget
        self.dropdown_widgets = []

    def get_df(self):
        """
            Helper function to get the current entity dataframe
            Arguments: self
            Returns: current entity dataframe
        """
        return self.df

    def set_df(self, df):
        """
            Helper function to set the current entity dataframe
            Arguments: self, entity dataframe
            Returns: current entity dataframe
        """
        self.df = df

    def register_dropdown(self, dropdown):
        """
            Helper function to set the dropdown options
            Arguments: self, relevant dropdown
            Returns: addition to dropdown options
        """
        self.dropdown_widgets.append(dropdown)

    def refresh_dropdowns(self):
        """
            Helper function to refresh dropdowns after an event
            Arguments: self
            Returns: Refreshes dropdowns
        """
        updated_options = sorted(self.df[self.id_column].astype(str).tolist())
        for dropdown in self.dropdown_widgets:
            dropdown.options = updated_options
            dropdown.update()

    def create(self, data):
        """
            Creates a new entity based on provided data
            Arguments: self, entity data
            Returns: entity
        """
        entity = self.repo.create(**data)
        api.commit()

        self.df = pd.concat([self.df, pd.DataFrame([entity.as_dict])], ignore_index=True)
        self.update_table()
        self.refresh_dropdowns()

        ui.notify(f'{self.entity_name} created', type = 'positive')

        return entity

    def update(self, id_value, data):
        """
            Updates an entity based on provided data
            Arguments: self, entity id_value, entity data
            Returns: entity
        """
        entity = self.repo.update(id_value, **data)
        api.commit()

        idx = self.df[self.df[self.id_column] == id_value].index[0]
        for col, value in data.items():
            self.df.at[idx, col] = value
        self.update_table()
        ui.notify(f'{self.entity_name} updated', type = 'positive')

        return entity

    def update_table(self):
        """
            Updates an entity's table
            Arguments: self
            Returns: entity
        """
        self.table_widget.rows = self.df.to_dict('records')
        self.table_widget.update()

    def delete(self, id_value):
        """
        Deletes an entity based on provided id_value
        Arguments: self, entity id_value
        Returns: None, the entity is deleted
        """
        self.repo.delete(id_value)
        api.commit()

        self.df = self.df[self.df[self.id_column] != id_value]
        self.df.reset_index(drop=True, inplace=True)

        self.update_table()
        self.refresh_dropdowns()
        ui.notify(f'{self.entity_name} deleted', type = 'positive')

"""
Dialog Factory

Rather than have Create, Edit, Delete dialog boxes for each entity, it makes more sense to have a factory that can be
called on for each entity configuration
"""

def create_add_dialog(service):
    """
        Creates a dialog box for adding a new entity
        Arguments: service, aka for which entity
        Returns: Appropriate Dialog box
    """

    dialog = ui.dialog()

    with dialog, ui.card().classes('w-[400px]'):
        ui.label(f'Add {service.entity_name}').classes('text-lg font-bold')

        inputs = {}
        df = service.get_df()

        #Create input fields:
        for col in df.columns:
            if col == service.id_column:
                next_id = get_next_id(df, service.id_column)
                inputs[col] = ui.input(
                    label = col.replace('_',' ').title(),
                    value = str(next_id)
                ).props('readonly')
            else:
                inputs[col] = ui.input(label=col.replace('_',' ').title())

        def save():
            """
                Called by the Dialogue box for adding a new entity to save inputted data into data source
                Arguments: None
                Returns: Saved entity in data source
            """
            data = {col: inp.value for col, inp in inputs.items()}

            #Validate fields using helper function:
            is_valid, invalid_col = validate_fields(data, service.id_column)
            if not is_valid:
                ui.notify(f'{invalid_col.replace("_"," ").title()} cannot be blank', type = 'negative')
                return
            service.create(data)
            dialog.close()

            #Update ID for the next entry for the entity
            next_id = get_next_id(service.get_df(), service.id_column)
            inputs[service.id_column].value = str(next_id)
            inputs[service.id_column].update()

        with ui.row().classes('gap-2 mt-4'):
            ui.button('Cancel', on_click = dialog.close)
            ui.button('Save', on_click = save)

    return dialog