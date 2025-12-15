import atexit
from nicegui import ui
import pandas as pd

from src.database import get_engine, decrypt_database, encrypt_database
from src.models import Base
from src.services import APIService

# Decrypt database on startup, encrypt on exit
decrypt_database()
atexit.register(encrypt_database)

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

programmes = api.programme_repo.get_all()
all_programmes_df = pd.DataFrame([prog.as_dict for prog in programmes])

# Load publications data - special case as publication data is stored in parent repositories
all_publications = []
for lecturer in api.lecturer_repo.get_all():
    pubs = api.lecturer_repo.get_publications(lecturer.lecturer_id)
    all_publications.extend([pub.as_dict for pub in pubs])
all_publications_df = pd.DataFrame(all_publications) if all_publications else pd.DataFrame(columns=['publication_id', 'lecturer_id', 'title', 'journal', 'publication_date'])



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
            self.df.at[idx, col] = type(self.df[col].iloc[0])(value)
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
            elif col == 'head_lecturer_id':
                available = api.lecturer_repo.get_available_head_lecturers()
                inputs[col] = ui.select(
                    label='Head Lecturer',
                    options={l.lecturer_id: f"{l.lecturer_id}: {l.name}" for l in available},
                    with_input=True
                ).classes('w-full')
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

def create_edit_dialog(service):
    """
        Creates a dialog box for editing an existing entity
        Arguments: service, aka for which entity
        Returns: Appropriate Dialog box
    """
    dialog = ui.dialog()
    selected_id = {'value': None}

    with dialog, ui.card().classes('w-[400px]'):
        ui.label(f'Edit {service.entity_name}').classes('text-lg font-bold')

        inputs = {}
        df = service.get_df()

        def load_entity():
            """
                Loads the correct entity based on provided data from outside the scope of the function, not passed into
                function, for viewing and editing
                Arguments: None
                Returns: Loads entity
            """
            id_value = inputs['id_selector'].value

            if not id_value or not id_value.strip():
                ui.notify(f'Please enter a {service.entity_name} ID', type='negative')
                return

            try:
                id_int = int(id_value)
            except ValueError:
                ui.notify(f'{service.entity_name} ID must be a number', type='negative')
                return

            if id_int not in service.get_df()[service.id_column].values:
                ui.notify(f'{service.entity_name} ID {id_int} does not exist', type='negative')
                return

            selected_id['value'] = id_int
            entity_row = service.get_df()[service.get_df()[service.id_column] == id_int].iloc[0]

            for col in service.get_df().columns:
                if col == service.id_column:
                    continue
                if col == 'head_lecturer_id':
                    current_head = int(entity_row[col])
                    available = api.lecturer_repo.get_available_head_lecturers(exclude_lecturer_id=current_head)
                    inputs[col].options = {l.lecturer_id: f"{l.lecturer_id}: {l.name}" for l in available}
                    inputs[col].value = current_head
                else:
                    inputs[col].value = str(entity_row[col])

            ui.notify(f'Loaded {service.entity_name} {id_int}', type='positive')

        # ID selector
        with ui.row().classes('w-full items-end gap-2'):
            inputs['id_selector'] = ui.select(
                label=f'{service.entity_name} ID',
                options=sorted(df[service.id_column].astype(str).tolist()),
                with_input=True
            ).classes('flex-grow')
            service.register_dropdown(inputs['id_selector'])
            ui.button('Load', on_click=load_entity)

        ui.separator()

        # Create input fields for other columns
        for col in df.columns:
            if col == service.id_column:
                continue
            if col == 'head_lecturer_id':
                inputs[col] = ui.select(label='Head Lecturer', options={}, with_input=True).classes('w-full').props('disable')
            else:
                inputs[col] = ui.input(label=col.replace('_', ' ').title()).props('readonly')

        def enable_editing():
            """
                Enables editing once the data is loaded, preventing accidental editing.
                Arguments: None
                Returns: Unlocks fields of an entity for editing
            """
            if selected_id['value'] is None:
                ui.notify(f'Please load a {service.entity_name} first', type='negative')
                return

            for col in service.get_df().columns:
                if col == service.id_column:
                    continue
                if col == 'head_lecturer_id':
                    inputs[col].props(remove='disable')
                else:
                    inputs[col].props(remove='readonly')

        def save():
            """
                Saves the updated data for the entity, requiring positive affirmation before editing data
                Arguments: None
                Returns: Saves updates to entity
            """
            if selected_id['value'] is None:
                ui.notify(f'Please load a {service.entity_name} first', type='negative')
                return

            updated_data = {col: inp.value for col, inp in inputs.items()
                            if col != 'id_selector'}

            is_valid, invalid_col = validate_fields(updated_data, service.id_column)
            if not is_valid:
                ui.notify(f'{invalid_col.replace("_", " ").title()} cannot be blank', type='negative')
                return

            service.update(selected_id['value'], updated_data)
            dialog.close()

        with ui.row().classes('gap-2 mt-4'):
            ui.button('Cancel', on_click=dialog.close)
            ui.button('Edit', on_click=enable_editing)
            ui.button('Save', on_click=save)

    return dialog

def create_delete_dialog(service):
    """
        Creates a dialog box for deleting an existing entity
        Arguments: service, aka for which entity
        Returns: Appropriate Dialog box
    """
    dialog = ui.dialog()
    selected_id = {'value': None}

    with dialog, ui.card().classes('w-[400px]'):
        ui.label(f'Delete {service.entity_name}').classes('text-lg font-bold')

        inputs = {}
        df = service.get_df()

        def load_entity():
            """
                Loads the correct entity based on provided data from outside the scope of the function, not passed into
                function, for viewing and editing
                Arguments: None
                Returns: Loads entity
            """
            id_value = inputs['id_selector'].value

            if not id_value or not id_value.strip():
                ui.notify(f'Please enter a {service.entity_name} ID', type='negative')
                return

            try:
                id_int = int(id_value)
            except ValueError:
                ui.notify(f'{service.entity_name} ID must be a number', type='negative')
                return

            if id_int not in service.get_df()[service.id_column].values:
                ui.notify(f'{service.entity_name} ID {id_int} does not exist', type='negative')
                return

            selected_id['value'] = id_int
            entity_row = service.get_df()[service.get_df()[service.id_column] == id_int].iloc[0]

            for col in service.get_df().columns:
                if col != service.id_column:
                    inputs[col].value = str(entity_row[col])

            ui.notify(f'Loaded {service.entity_name} {id_int}', type='positive')

        # ID selector
        with ui.row().classes('w-full items-end gap-2'):
            inputs['id_selector'] = ui.select(
                label=f'{service.entity_name} ID',
                options=sorted(df[service.id_column].astype(str).tolist()),
                with_input=True
            ).classes('flex-grow')
            service.register_dropdown(inputs['id_selector'])
            ui.button('Load', on_click=load_entity)

        ui.separator()

        # Create readonly input fields
        for col in df.columns:
            if col != service.id_column:
                inputs[col] = ui.input(label=col.replace('_', ' ').title()).props('readonly')

        ui.separator()
        ui.label('Warning: This action cannot be undone!').classes('text-red-600 font-semibold')

        def delete():
            """
                Deletes the entity
                Arguments: None
                Returns: Deletes entity
            """
            if selected_id['value'] is None:
                ui.notify(f'Please load a {service.entity_name} first', type='negative')
                return

            try:
                service.delete(selected_id['value'])

                # Reset dialog
                selected_id['value'] = None
                for col in service.get_df().columns:
                    if col != service.id_column:
                        inputs[col].value = ''
                inputs['id_selector'].value = None

                dialog.close()
            except Exception as e:
                ui.notify(f'Error deleting {service.entity_name}: {str(e)}', type='negative')

        with ui.row().classes('gap-2 mt-4'):
            ui.button('Cancel', on_click=dialog.close)
            ui.button('Delete', on_click=delete, color='red')

    return dialog

"""
Entity Panel Factory

Rather than have separate panels defined, can instead define configurations that are then referenced by functions
to create panels identical in structure but variant in data based on desired entity
"""

def create_entity_panel(config):
    """
        Creates an entity panel
        Arguments: configuration aka for what entity
        Returns: Panel and sub-panel for respective entity
    """

    # Create view table with search/filter
    with ui.tab_panel(config['view_tab']).classes('w-full'):

        # Filter inputs container
        filter_inputs = {}
        current_filters = {}

        with ui.expansion('Search & Filter', icon='search').classes('w-full mb-4'):
            with ui.grid(columns=3).classes('w-full gap-4'):
                for col in config['df'].columns:
                    filter_inputs[col] = ui.input(
                        label=f'Search {col.replace("_", " ").title()}',
                        placeholder=f'Filter by {col.replace("_", " ")}...'
                    ).classes('w-full')

        # Table
        columns = create_table_columns(config['df'])
        rows = config['df'].to_dict(orient='records')

        table = ui.table(
            columns=columns,
            rows=rows,
            row_key=config['id_column'],
        ).classes('w-full border border-black text-black bg-white')

        # Add pagination
        table.add_slot('top-right', r'''
               <q-input dense debounce="300" v-model="props.filter" placeholder="Quick search">
                   <template v-slot:append>
                       <q-icon name="search" />
                   </template>
               </q-input>
           ''')
        table.props('dense')
        table.props('flat bordered')
        table.props(':rows-per-page-options="[10, 25, 50, 100, 0]"')

        config['table'] = table
        config['filter_inputs'] = filter_inputs


        # Filter function
        def apply_filters():
            """
                Applies filters
                Arguments: Uses previously set filters
                Returns: Filtered table
            """
            filters = {col: inp.value for col, inp in filter_inputs.items()}
            filtered_df = filter_dataframe(config['df'], filters)

            # Update table
            table.rows = filtered_df.to_dict('records')
            table.update()

            row_count = len(filtered_df)
            total_count = len(config['df'])
            ui.notify(f'Showing {row_count} of {total_count} records', type='info')


        def clear_filters():
            """
                Clears filters
                Arguments: Clears set filters
                Returns: Unfiltered table
            """
            for inp in filter_inputs.values():
                inp.value = ''

            # Reset table to show all data
            table.rows = config['df'].to_dict('records')
            table.update()
            ui.notify('Filters cleared', type='info')


        # Connect filter inputs to apply function
        for inp in filter_inputs.values():
            inp.on('keyup.enter', apply_filters)

        # Filter action buttons
        with ui.row().classes('gap-2 mt-2'):
            ui.button('Apply Filters', on_click=apply_filters, icon='filter_alt')
            ui.button('Clear Filters', on_click=clear_filters, icon='clear')

    # Create manage panel
    with ui.tab_panel(config['manage_tab']).classes('w-full'):
        # Initialize service
        service = CRUDService(
            entity_name=config['display_name'],
            df=config['df'],
            repo=config['repo'],
            id_column=config['id_column'],
            table_widget=table
        )

        # Create dialogs
        add_dialog = create_add_dialog(service)
        edit_dialog = create_edit_dialog(service)
        delete_dialog = create_delete_dialog(service)

        # Create action buttons
        with ui.row().classes('gap-4'):
            ui.button('Add', on_click=lambda: add_dialog.open())
            ui.button('Edit', on_click=lambda: edit_dialog.open())
            ui.button('Delete', on_click=lambda: delete_dialog.open(), color='red')

"""
Entity Configurations

Can now describe entities, thus modifying the behaviour of the panels and functions above
"""

entity_configs = [
    {
        'key': 'students',
        'display_name': 'Student',
        'df': all_students_df,
        'repo': api.student_repo,
        'id_column': 'student_id',
        'label': 'Student Records',
    },
    {
        'key': 'lecturers',
        'display_name': 'Lecturer',
        'df': all_lecturers_df,
        'repo': api.lecturer_repo,
        'id_column': 'lecturer_id',
        'label': 'Lecturer Records',
    },
    {
        'key': 'staff',
        'display_name': 'Non-Academic Staff',
        'df': all_staff_df,
        'repo': api.staff_repo,
        'id_column': 'staff_id',
        'label': 'Non-Academic Staff Records',
    },
    {
        'key': 'courses',
        'display_name': 'Course',
        'df': all_courses_df,
        'repo': api.course_repo,
        'id_column': 'course_id',
        'label': 'Course Records',
    },
    {
        'key': 'departments',
        'display_name': 'Department',
        'df': all_departments_df,
        'repo': api.department_repo,
        'id_column': 'dept_id',
        'label': 'Departmental Records',
    },
    {
        'key': 'programmes',
        'display_name': 'Programme',
        'df': all_programmes_df,
        'repo': api.programme_repo,
        'id_column': 'programme_id',
        'label': 'Programme Records',
    },
    {
        'key': 'research_projects',
        'display_name': 'Research Project',
        'df': all_projects_df,
        'repo': api.research_project_repo,
        'id_column': 'project_id',
        'label': 'Research Projects Records',
    },
    {
        'key': 'publications',
        'display_name': 'Publication',
        'df': all_publications_df,
        'repo': None,  # Publications are managed through lecturer repo
        'id_column': 'publication_id',
        'label': 'Publication Records',
        'is_readonly': True,
    },
]

"""
UI Build

Can now build UI by referencing entity configs and functions above
"""

with ui.column().classes('w-full'):
    # Create main tabs
    with ui.tabs().classes('w-full') as main_tabs:
        for config in entity_configs:
            config['main_tab'] = ui.tab(
                config['display_name'] + 's' if not config['key'] == 'staff' else config['display_name'])
        tab_qr = ui.tab('Queries and Reports')

    # Create entity panels
    with ui.tab_panels(main_tabs).classes('w-full'):
        for config in entity_configs:
            with ui.tab_panel(config['main_tab']):
                with ui.row().classes('w-full justify-center mb-4'):
                    ui.label(config['label']).classes('text-xl')

                # Create sub-tabs for view/manage
                with ui.tabs().classes('w-full') as entity_ops:
                    config['view_tab'] = ui.tab(f'View {config["label"]}')
                    config['manage_tab'] = ui.tab(f'Manage {config["label"]}')

                with ui.tab_panels(entity_ops).classes('w-full'):
                    create_entity_panel(config)

        # Queries and Reports panel
        with ui.tab_panel(tab_qr):
            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Queries and Reports').classes('text-xl')
            # Query 1: Students advised by a lecturer:
            with ui.expansion('Students Advised by Lecturer', icon='school').classes('w-full mb-4'):
                with ui.column().classes('w-full gap-4'):
                    lecturer_select = ui.select(
                        label='Select Lecturer',
                        options=[f"{l.lecturer_id}: {l.name}" for l in api.lecturer_repo.get_all()],
                        with_input=True
                    ).classes('w-full')

                    query_students_advised_by_lecturer_result = ui.table(
                        columns=[
                            {'name': 'student_id', 'label': 'Student ID', 'field': 'student_id', 'sortable': True},
                            {'name': 'name', 'label': 'Name', 'field': 'name', 'sortable': True},
                            {'name': 'programme_id', 'label': 'Programme ID', 'field': 'programme_id',
                             'sortable': True},
                            {'name': 'year_of_study', 'label': 'Year', 'field': 'year_of_study', 'sortable': True},
                        ],
                        rows=[],
                        row_key='student_id'
                    ).classes('w-full')


                    def run_query_students_advised_by_lecturer():
                        """
                            Runs query for students advised by selected lecturer
                            Arguments: None
                            Returns: Students advised by selected lecturer
                        """
                        if not lecturer_select.value:
                            ui.notify('Please select a lecturer', type='warning')
                            return

                        lecturer_id = int(lecturer_select.value.split(':')[0])
                        students = api.student_repo.get_by_advisor(lecturer_id)

                        query_students_advised_by_lecturer_result.rows = [s.as_dict for s in students]
                        query_students_advised_by_lecturer_result.update()
                        ui.notify(f'Found {len(students)} student(s)', type='positive')


                    ui.button('Run Query', on_click=run_query_students_advised_by_lecturer, icon='play_arrow')


            #Query 2: All courses taught by a lecturer
            with ui.expansion('Courses Taught by Departments', icon='class').classes('w-full mb-4'):
                with ui.column().classes('w-full gap-4'):
                    dept_select = ui.select(
                        label='Select Department',
                        options=[f"{d.dept_id}: {d.name}" for d in api.department_repo.get_all()],
                        with_input=True
                    ).classes('w-full')

                    query_courses_by_department_result = ui.table(
                        columns=[
                            {'name': 'course_id', 'label': 'Course ID', 'field': 'course_id', 'sortable': True},
                            {'name': 'course_code', 'label': 'Code', 'field': 'course_code', 'sortable': True},
                            {'name': 'name', 'label': 'Name', 'field': 'name', 'sortable': True},
                            {'name': 'level', 'label': 'Level', 'field': 'level', 'sortable': True},
                            {'name': 'credits', 'label': 'Credits', 'field': 'credits', 'sortable': True},
                        ],
                        rows=[],
                        row_key='course_id'
                    ).classes('w-full')


                    def query_courses_by_department():
                        """
                            Runs query for courses offered by selected department
                            Arguments: None
                            Returns: Students advised by selected lecturer
                        """
                        if not dept_select.value:
                            ui.notify('Please select a department', type='warning')
                            return

                        dept_id = int(dept_select.value.split(':')[0])
                        courses = api.course_repo.get_by_department_lecturers(dept_id)

                        query_courses_by_department_result.rows = [c.as_dict for c in courses]
                        query_courses_by_department_result.update()
                        ui.notify(f'Found {len(courses)} course(s)', type='positive')


                    ui.button('Run Query', on_click=query_courses_by_department, icon='play_arrow')

            # Query 3 - Complete Student Profile
            with ui.expansion('Complete Student Profile', icon='person_search').classes('w-full mb-4'):
                with ui.column().classes('w-full gap-4'):
                    student_select_profile = ui.select(
                        label = 'Select Student',
                        options=[f"{s.student_id}:{s.name}" for s in api.student_repo.get_all()],
                        with_input = True
                    ).classes('w-full')

                    # A container for student profile information

                    profile_container = ui.column().classes('w-full gap-4')

                    def run_query_student_profile():
                        """
                            Runs a series of queries to gather a complete picture of a student's performance
                            Arguments: None
                            Returns: All information relevant about a student
                        """
                        if not student_select_profile.value:
                            ui.notify('Please select a student', type='warning')
                            return

                        student_id = int(student_select_profile.value.split(':')[0])
                        student = api.student_repo.get_by_id(student_id)

                        # Clear previous profile
                        profile_container.clear()

                        with profile_container:
                            # Basic Information Card
                            with ui.card().classes('w-full'):
                                ui.label('Basic Information').classes('text-lg font-bold mb-2')
                                with ui.grid(columns=2).classes('w-full gap-2'):
                                    ui.label('Student ID:').classes('font-semibold')
                                    ui.label(str(student.student_id))

                                    ui.label('Name:').classes('font-semibold')
                                    ui.label(student.name)

                                    ui.label('Date of Birth:').classes('font-semibold')
                                    ui.label(student.date_of_birth or 'N/A')

                                    ui.label('Contact Info:').classes('font-semibold')
                                    ui.label(student.contact_info or 'N/A')

                                    ui.label('Year of Study:').classes('font-semibold')
                                    ui.label(str(student.year_of_study) if student.year_of_study else 'N/A')

                                    ui.label('Graduation Status:').classes('font-semibold')
                                    ui.label(student.graduation_status or 'N/A')

                            # Programme Information Card
                            with ui.card().classes('w-full'):
                                ui.label('Programme Information').classes('text-lg font-bold mb-2')
                                if student.programme_id:
                                    try:
                                        programme = api.programme_repo.get_by_id(student.programme_id)
                                        with ui.grid(columns=2).classes('w-full gap-2'):
                                            ui.label('Programme:').classes('font-semibold')
                                            ui.label(programme.name)

                                            ui.label('Degree Awarded:').classes('font-semibold')
                                            ui.label(programme.degree_awarded or 'N/A')

                                            ui.label('Duration:').classes('font-semibold')
                                            ui.label(
                                                f"{programme.duration_years} years" if programme.duration_years else 'N/A')

                                            ui.label('Enrolment Details:').classes('font-semibold')
                                            ui.label(programme.enrolment_details or 'N/A')
                                    except:
                                        ui.label('Programme information not available')
                                else:
                                    ui.label('No programme assigned')

                            # Advisor Information Card
                            with ui.card().classes('w-full'):
                                ui.label('Advisor Information').classes('text-lg font-bold mb-2')
                                if student.advisor_id:
                                    try:
                                        advisor = api.lecturer_repo.get_by_id(student.advisor_id)
                                        with ui.grid(columns=2).classes('w-full gap-2'):
                                            ui.label('Advisor:').classes('font-semibold')
                                            ui.label(advisor.name)

                                            if advisor.dept_id:
                                                try:
                                                    dept = api.department_repo.get_by_id(advisor.dept_id)
                                                    ui.label('Department:').classes('font-semibold')
                                                    ui.label(dept.name)
                                                except:
                                                    pass
                                    except:
                                        ui.label('Advisor information not available')
                                else:
                                    ui.label('No advisor assigned')

                            # Courses and Grades Card
                            with ui.card().classes('w-full'):
                                ui.label('Courses and Grades').classes('text-lg font-bold mb-2')

                                # Get all grades for the student
                                grades = api.student_repo.get_grades(student_id)

                                if grades:
                                    # Group grades by course
                                    course_grades = {}
                                    for grade in grades:
                                        if grade.course_id not in course_grades:
                                            course_grades[grade.course_id] = []
                                        course_grades[grade.course_id].append(grade)

                                    course_data = []
                                    overall_grades = []

                                    for course_id, grade_list in course_grades.items():
                                        try:
                                            course = api.course_repo.get_by_id(course_id)
                                            grade_values = [g.grade for g in grade_list if g.grade is not None]

                                            if grade_values:
                                                avg_grade = sum(grade_values) / len(grade_values)
                                                overall_grades.append(avg_grade)

                                                course_data.append({
                                                    'course_code': course.course_code,
                                                    'course_name': course.name,
                                                    'num_assessments': len(grade_values),
                                                    'average_grade': f"{avg_grade:.2f}%",
                                                    'credits': course.credits or 'N/A'
                                                })
                                        except:
                                            pass

                                    # Display overall average
                                    if overall_grades:
                                        overall_avg = sum(overall_grades) / len(overall_grades)
                                        ui.label(f'Overall Average Grade: {overall_avg:.2f}%').classes(
                                            'text-lg font-semibold text-blue-600 mb-3')

                                    # Display course table
                                    ui.table(
                                        columns=[
                                            {'name': 'course_code', 'label': 'Code', 'field': 'course_code',
                                             'sortable': True},
                                            {'name': 'course_name', 'label': 'Course', 'field': 'course_name',
                                             'sortable': True},
                                            {'name': 'num_assessments', 'label': 'Assessments',
                                             'field': 'num_assessments', 'sortable': True},
                                            {'name': 'average_grade', 'label': 'Average',
                                             'field': 'average_grade', 'sortable': True},
                                            {'name': 'credits', 'label': 'Credits', 'field': 'credits',
                                             'sortable': True},
                                        ],
                                        rows=course_data,
                                        row_key='course_code'
                                    ).classes('w-full')
                                else:
                                    ui.label('No grades recorded')

                            # Disciplinary Records Card
                            with ui.card().classes('w-full'):
                                ui.label('Disciplinary Records').classes('text-lg font-bold mb-2')

                                disciplinary_records = api.student_repo.get_disciplinary_records(student_id)

                                if disciplinary_records:
                                    records_data = [{
                                        'incident_date': r.incident_date or 'N/A',
                                        'description': r.description or 'N/A',
                                        'action_taken': r.action_taken or 'N/A'
                                    } for r in disciplinary_records]

                                    ui.table(
                                        columns=[
                                            {'name': 'incident_date', 'label': 'Date', 'field': 'incident_date',
                                             'sortable': True},
                                            {'name': 'description', 'label': 'Description',
                                             'field': 'description', 'sortable': True},
                                            {'name': 'action_taken', 'label': 'Action Taken',
                                             'field': 'action_taken', 'sortable': True},
                                        ],
                                        rows=records_data,
                                        row_key='incident_date'
                                    ).classes('w-full')
                                else:
                                    ui.label('No disciplinary records').classes('text-green-600')

                            # Research Projects Card
                            with ui.card().classes('w-full'):
                                ui.label('Research Projects').classes('text-lg font-bold mb-2')

                                # Get all projects and check if student is a member
                                all_projects = api.research_project_repo.get_all()
                                student_projects = []

                                for project in all_projects:
                                    # Check if student is in this project
                                    project_students = api.student_repo.get_by_research_project(
                                        project.project_id)
                                    if any(s.student_id == student_id for s in project_students):
                                        try:
                                            head_lecturer = api.lecturer_repo.get_by_id(
                                                project.head_lecturer_id)
                                            student_projects.append({
                                                'title': project.title,
                                                'head_lecturer': head_lecturer.name,
                                                'start_date': project.start_date or 'N/A',
                                                'end_date': project.end_date or 'N/A'
                                            })
                                        except:
                                            pass

                                if student_projects:
                                    ui.table(
                                        columns=[
                                            {'name': 'title', 'label': 'Project Title', 'field': 'title',
                                             'sortable': True},
                                            {'name': 'head_lecturer', 'label': 'Head Lecturer',
                                             'field': 'head_lecturer', 'sortable': True},
                                            {'name': 'start_date', 'label': 'Start Date', 'field': 'start_date',
                                             'sortable': True},
                                            {'name': 'end_date', 'label': 'End Date', 'field': 'end_date',
                                             'sortable': True},
                                        ],
                                        rows=student_projects,
                                        row_key='title'
                                    ).classes('w-full')
                                else:
                                    ui.label('Not involved in any research projects')

                        ui.notify('Student profile loaded', type='positive')

                    ui.button('Load Profile', on_click= run_query_student_profile, icon='person_search')

            # Query 4 - Lecturer Publications
            with ui.expansion('Lecturer Publications', icon='article').classes('w-full mb-4'):
                with ui.column().classes('w-full gap-4'):
                    lecturer_select_pubs = ui.select(
                        label='Select Lecturer',
                        options=[f"{l.lecturer_id}: {l.name}" for l in api.lecturer_repo.get_all()],
                        with_input=True
                    ).classes('w-full')

                    # Container for lecturer info and publications
                    publications_container = ui.column().classes('w-full gap-4')


                    def run_query_publications():
                        """
                            Runs a series of queries to gather a complete picture of a lecturer's publications.
                            Arguments: None
                            Returns: All information relevant about a lecturer's publications
                        """
                        if not lecturer_select_pubs.value:
                            ui.notify('Please select a lecturer', type='warning')
                            return

                        lecturer_id = int(lecturer_select_pubs.value.split(':')[0])
                        lecturer = api.lecturer_repo.get_by_id(lecturer_id)
                        publications = api.lecturer_repo.get_publications(lecturer_id)

                        # Clear previous content
                        publications_container.clear()

                        with publications_container:
                            # Lecturer Info Card
                            with ui.card().classes('w-full'):
                                ui.label(f'{lecturer.name}').classes('text-xl font-bold mb-2')
                                with ui.grid(columns=2).classes('w-full gap-2'):
                                    ui.label('Lecturer ID:').classes('font-semibold')
                                    ui.label(str(lecturer.lecturer_id))

                                    if lecturer.dept_id:
                                        try:
                                            dept = api.department_repo.get_by_id(lecturer.dept_id)
                                            ui.label('Department:').classes('font-semibold')
                                            ui.label(dept.name)
                                        except:
                                            pass

                                    ui.label('Course Load:').classes('font-semibold')
                                    ui.label(str(lecturer.course_load) if lecturer.course_load else 'N/A')

                                    ui.label('Total Publications:').classes('font-semibold')
                                    ui.label(str(len(publications))).classes('text-blue-600 font-bold')

                            # Publications Card
                            with ui.card().classes('w-full'):
                                ui.label('Publications').classes('text-lg font-bold mb-2')

                                if publications:
                                    # Create table data
                                    pubs_data = []
                                    for pub in publications:
                                        pubs_data.append({
                                            'title': pub.title,
                                            'journal': pub.journal or 'N/A',
                                            'publication_date': pub.publication_date or 'N/A',
                                            'publication_id': pub.publication_id
                                        })

                                    # Sort by date (most recent first)
                                    pubs_data.sort(
                                        key=lambda x: x['publication_date'] if x['publication_date'] != 'N/A' else '',
                                        reverse=True)

                                    ui.table(
                                        columns=[
                                            {'name': 'title', 'label': 'Title', 'field': 'title', 'sortable': True,
                                             'align': 'left'},
                                            {'name': 'journal', 'label': 'Journal', 'field': 'journal',
                                             'sortable': True, 'align': 'left'},
                                            {'name': 'publication_date', 'label': 'Publication Date',
                                             'field': 'publication_date', 'sortable': True, 'align': 'left'},
                                        ],
                                        rows=pubs_data,
                                        row_key='publication_id'
                                    ).classes('w-full').props('dense flat bordered')
                                else:
                                    ui.label('No publications recorded').classes('text-gray-500')

                        ui.notify(f'Found {len(publications)} publication(s)', type='positive')


                    ui.button('Load Publications', on_click=run_query_publications, icon='menu_book')

            # Query 5: Final year students with high grades
            with ui.expansion('High-Performing Final Year Students', icon='elevator').classes(
                    'w-full mb-4'):
                with ui.column().classes('w-full gap-4'):
                    threshold_input = ui.number(
                        label='Minimum Average Grade (%)',
                        value=70,
                        min=0,
                        max=100,
                        step=1
                    ).classes('w-64')

                    query4_result = ui.table(
                        columns=[
                            {'name': 'student_id', 'label': 'Student ID', 'field': 'student_id',
                             'sortable': True},
                            {'name': 'name', 'label': 'Name', 'field': 'name', 'sortable': True},
                            {'name': 'programme_id', 'label': 'Programme ID', 'field': 'programme_id',
                             'sortable': True},
                            {'name': 'year_of_study', 'label': 'Year', 'field': 'year_of_study',
                             'sortable': True},
                            {'name': 'average_grade', 'label': 'Average Grade', 'field': 'average_grade',
                             'sortable': True},
                        ],
                        rows=[],
                        row_key='student_id'
                    ).classes('w-full')


                    def run_query_high_performance():
                        threshold = threshold_input.value
                        all_students = api.student_repo.get_all()

                        # Get programmes to determine final year
                        programmes = {p.programme_id: p for p in api.programme_repo.get_all()}

                        results = []
                        for student in all_students:
                            # Check if student is in final year
                            if student.programme_id and student.year_of_study:
                                programme = programmes.get(student.programme_id)
                                if programme and programme.duration_years:
                                    is_final_year = student.year_of_study == programme.duration_years
                                else:
                                    # Assume 4 years if duration not specified
                                    is_final_year = student.year_of_study == 4

                                if is_final_year:
                                    # Calculate average grade
                                    grades = api.student_repo.get_grades(student.student_id)
                                    if grades:
                                        grade_values = [g.grade for g in grades if g.grade is not None]
                                        if grade_values:
                                            avg_grade = sum(grade_values) / len(grade_values)
                                            if avg_grade >= threshold:
                                                student_dict = student.as_dict
                                                student_dict['average_grade'] = f"{avg_grade:.2f}%"
                                                results.append(student_dict)

                        query4_result.rows = results
                        query4_result.update()
                        ui.notify(f'Found {len(results)} student(s)', type='positive')


                    ui.button('Run Query', on_click=run_query_high_performance, icon='play_arrow')

ui.run()