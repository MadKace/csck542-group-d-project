
from nicegui import ui
import pandas as pd

from src.database import get_engine
from src.models import Base
from src.services import APIService

def init_database():
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("Tbl created")

if __name__ == "__main__":
    init_database()

api = APIService()

students = api.student_repo.get_all()
all_students_df = pd.DataFrame([student.as_dict for student in students])

lecturers = api.lecturer_repo.get_all()
all_lecturers_df = pd.DataFrame([lecturer.as_dict for lecturer in lecturers])

nas = api.staff_repo.get_all()
all_nas_df = pd.DataFrame([staff.as_dict for staff in nas])

courses = api.course_repo.get_all()
all_courses_df = pd.DataFrame([course.as_dict for course in courses])

departments = api.department_repo.get_all()
all_departments_df = pd.DataFrame([department.as_dict for department in departments])

research_projects = api.research_project_repo.get_all()
all_rp_df = pd.DataFrame([rp.as_dict for rp in research_projects])

#print(all_students_df)
#print(lecturers)
#print(courses)

ui.add_css('''
    @layer utilities {
       .standard-btn {
           background-color: black !important; height: 50% !important; width: 500px !important;
        }
    }
''')

#def build_view_students():
    #columns_view_students = [
    #    'student_id', 'programme_id', 'advisor_id', 'name', 'date_of_birth', 'contact_info', 'year_of_study',
    #    'graduation_status'
    #]

#def build_view_lectures():
    #tbl_view_lectures = [
    #    'lecturer_id', 'dept_id', 'name', 'course_load'
    #]

#def build_view_nas():
    #tbl_view_nas = [
    #    'staff_id', 'dept_id', 'name', 'job_title', 'employment_type', 'contract_details', 'salary', 'emergency_contact'
    #]

#def build_view_courses():
 #   tbl_view_courses = [
 #       'programme_id', 'course_id', 'is_required'
 #   ]

#def build_view_department():
 #   tbl_view_departments = [
 #       'dept_id', 'name', 'faculty'
 #   ]

with ui.column().classes('w-full'):
    with ui.tabs().classes('w-full') as main_tabs:
        tab_students = ui.tab('Students')
        tab_lecturers = ui.tab('Lecturers')
        tab_nas = ui.tab('Non-Academic Staff')
        tab_courses = ui.tab('Courses')
        tab_departments = ui.tab('Departments')
        tab_rp = ui.tab('Research Projects')
        tab_qr = ui.tab('Queries and Reports')
    with ui.tab_panels(main_tabs, value = tab_students).classes('w-full'):
        with ui.tab_panel(tab_students):
            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Student Records').classes('text-xl')
            with ui.tabs().classes('w-full') as student_ops:
                tab_students_view = ui.tab('View Student Records')
                tab_students_manage = ui.tab('Manage Student Records')
            with ui.tab_panels(student_ops).classes('w-full'):
                with ui.tab_panel(tab_students_view).classes('w-full'):
                    columns = [
                        {
                            'name': col,
                            'label': col.replace('_', ' ').title(),  # nicer column titles
                            'field': col,
                            'sortable': True,
                        }
                        for col in all_students_df.columns
                    ]

                    rows = all_students_df.to_dict(orient='records')

                    tbl_view_students = ui.table(
                        columns=columns,
                        rows=rows,
                        row_key='student_id',
                    ).classes('w-full border border-black text-black bg-white')
                with ui.tab_panel(tab_students_manage).classes('w-full'):
                    with ui.dialog() as add_student_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Add Student').classes('text-lg font-bold')
                            add_inputs = {}

                            def get_next_student_id(df):
                                if df.empty:
                                    return 1
                                return int(df['student_id'].max()) + 1


                            new_student_inputs = {}

                            # Create input fields for all columns
                            for col in all_students_df.columns:
                                if col == 'student_id':
                                    # Show the auto-generated student_id as read-only
                                    new_student_id = get_next_student_id(all_students_df)
                                    new_student_inputs[col] = ui.input(
                                        label=f'Student ID',
                                        value=str(new_student_id)
                                    ).props('readonly')
                                else:
                                    # Create editable input for other columns
                                    new_student_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    )


                            def save_student():
                                student_data = {col: inp.value for col, inp in new_student_inputs.items()}

                                for col, value in student_data.items():
                                    if col != 'student_id' and not value.strip():
                                        ui.notify(f'{col.replace("_", " ").title()} cannot be blank', type='negative')
                                        return

                                #print(student_data)

                                student = api.student_repo.create(**student_data)
                                api.commit()

                                global all_students_df
                                all_students_df = pd.concat([all_students_df, pd.DataFrame([student_data])],
                                                            ignore_index=True)

                                add_student_dialog.close()
                                ui.notify('Student added successfully', type='positive')

                                tbl_view_students.rows[:] = all_students_df.to_dict('records')
                                tbl_view_students.update()

                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=add_student_dialog.close)
                                ui.button('Save', on_click=save_student)
                    with ui.dialog() as edit_student_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Edit Student').classes('text-lg font-bold')

                            edit_student_inputs = {}
                            selected_student_id = {'value': None}  # Store selected ID


                            # Student ID selector
                            def validate_and_load_student():
                                student_id_value = edit_student_inputs['student_id_selector'].value

                                if not student_id_value or not student_id_value.strip():
                                    ui.notify('Please enter a Student ID', type='negative')
                                    return

                                # Check if student exists
                                try:
                                    student_id_int = int(student_id_value)
                                except ValueError:
                                    ui.notify('Student ID must be a number', type='negative')
                                    return

                                if student_id_int not in all_students_df['student_id'].values:
                                    ui.notify(f'Student ID {student_id_int} does not exist', type='negative')
                                    return

                                # Load student data
                                selected_student_id['value'] = student_id_int
                                student_row = all_students_df[all_students_df['student_id'] == student_id_int].iloc[0]

                                # Populate input fields
                                for col in all_students_df.columns:
                                    if col != 'student_id':
                                        edit_student_inputs[col].value = str(student_row[col])

                                ui.notify(f'Loaded student {student_id_int}', type='positive')


                            # Student ID input with dropdown
                            with ui.row().classes('w-full items-end gap-2'):
                                edit_student_inputs['student_id_selector'] = ui.select(
                                    label='Student ID',
                                    options=sorted(all_students_df['student_id'].astype(str).tolist()),
                                    with_input=True
                                ).classes('flex-grow')
                                ui.button('Load', on_click=validate_and_load_student)

                            ui.separator()

                            # Create input fields for all other columns
                            for col in all_students_df.columns:
                                if col != 'student_id':
                                    edit_student_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    ).props('readonly')  # Start as readonly until student is loaded


                            def enable_editing():
                                if selected_student_id['value'] is None:
                                    ui.notify('Please load a student first', type='negative')
                                    return

                                # Enable all fields for editing
                                for col in all_students_df.columns:
                                    if col != 'student_id':
                                        edit_student_inputs[col].props(remove='readonly')


                            def save_edited_student():
                                if selected_student_id['value'] is None:
                                    ui.notify('Please load a student first', type='negative')
                                    return

                                # Get the updated values
                                updated_data = {col: inp.value for col, inp in edit_student_inputs.items() if
                                                col != 'student_id_selector'}

                                # Validate that no fields are blank
                                for col, value in updated_data.items():
                                    if col != 'student_id' and (not value or not str(value).strip()):
                                        ui.notify(f'{col.replace("_", " ").title()} cannot be blank', type='negative')
                                        return

                                # Update in API
                                student = api.student_repo.update(selected_student_id['value'], **updated_data)

                                # Update the dataframe
                                global all_students_df
                                idx = \
                                all_students_df[all_students_df['student_id'] == selected_student_id['value']].index[0]
                                for col, value in updated_data.items():
                                    all_students_df.at[idx, col] = value

                                # Update the table
                                tbl_view_students.rows = all_students_df.to_dict('records')
                                tbl_view_students.update()

                                edit_student_dialog.close()
                                ui.notify('Student updated successfully', type='positive')


                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=edit_student_dialog.close)
                                ui.button('Edit', on_click=enable_editing)
                                ui.button('Save', on_click=save_edited_student)
                    with ui.dialog() as delete_student_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Delete Student').classes('text-lg font-bold')

                            delete_student_inputs = {}
                            delete_selected_student_id = {'value': None}


                            # Student ID selector
                            def validate_and_load_student_for_delete():
                                delete_student_id_value = delete_student_inputs['student_id_selector'].value

                                if not delete_student_id_value or not delete_student_id_value.strip():
                                    ui.notify('Please enter a Student ID', type='negative')
                                    return

                                # Check if student exists
                                try:
                                    delete_student_id_int = int(delete_student_id_value)
                                except ValueError:
                                    ui.notify('Student ID must be a number', type='negative')
                                    return

                                if delete_student_id_int not in all_students_df['student_id'].values:
                                    ui.notify(f'Student ID {delete_student_id_int} does not exist', type='negative')
                                    return

                                # Load student data
                                delete_selected_student_id['value'] = delete_student_id_int
                                student_row = all_students_df[all_students_df['student_id'] == delete_student_id_int].iloc[0]

                                # Populate input fields
                                for col in all_students_df.columns:
                                    if col != 'student_id':
                                        delete_student_inputs[col].value = str(student_row[col])

                                ui.notify(f'Loaded student {delete_student_id_int}', type='positive')


                            # Student ID input with dropdown
                            with ui.row().classes('w-full items-end gap-2'):
                                delete_student_inputs['student_id_selector'] = ui.select(
                                    label='Student ID',
                                    options=sorted(all_students_df['student_id'].astype(str).tolist()),
                                    with_input=True
                                ).classes('flex-grow')
                                ui.button('Load', on_click=validate_and_load_student_for_delete)

                            ui.separator()

                            # Create input fields for all other columns (read-only)
                            for col in all_students_df.columns:
                                if col != 'student_id':
                                    delete_student_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    ).props('readonly')

                            ui.separator()

                            ui.label('Warning: This action cannot be undone!').classes('text-red-600 font-semibold')


                            def delete_student():
                                if delete_selected_student_id['value'] is None:
                                    ui.notify('Please load a student first', type='negative')
                                    return

                                # Delete from API
                                try:
                                    api.student_repo.delete(delete_selected_student_id['value'])
                                except Exception as e:
                                    ui.notify(f'Error deleting student: {str(e)}', type='negative')
                                    return

                                # Delete from dataframe
                                global all_students_df
                                all_students_df = all_students_df[
                                    all_students_df['student_id'] != delete_selected_student_id['value']]
                                all_students_df.reset_index(drop=True, inplace=True)

                                # Update the table
                                tbl_view_students.rows = all_students_df.to_dict('records')
                                tbl_view_students.update()

                                # Reset dialog state
                                delete_selected_student_id['value'] = None
                                for col in all_students_df.columns:
                                    if col != 'student_id':
                                        delete_student_inputs[col].value = ''
                                delete_student_inputs['student_id_selector'].value = None

                                delete_student_dialog.close()
                                ui.notify('Student deleted successfully', type='positive')


                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=delete_student_dialog.close)
                                ui.button('Delete', on_click=delete_student, color='red')
                    with ui.row().classes('gap-4'):
                        ui.button('Add', on_click=lambda: add_student_dialog.open())
                        ui.button('Edit', on_click=lambda: edit_student_dialog.open())
                        ui.button('Delete', on_click=lambda: delete_student_dialog.open(), color = 'red')
    with ui.tab_panels(main_tabs, value = tab_lecturers).classes('w-full'):
        with ui.tab_panel(tab_lecturers):
            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Lecturer Records').classes('text-xl')
            with ui.tabs().classes('w-full') as lecturer_ops:
                tab_lecturers_view = ui.tab('View Lecturer Records')
                tab_lecturers_manage = ui.tab('Manage Lecturer Records')
            with ui.tab_panels(lecturer_ops).classes('w-full'):
                with ui.tab_panel(tab_lecturers_view).classes('w-full'):
                    columns = [
                        {
                            'name': col,
                            'label': col.replace('_', ' ').title(),  # nicer column titles
                            'field': col,
                            'sortable': True,
                        }
                        for col in all_lecturers_df.columns
                    ]

                    rows = all_lecturers_df.to_dict(orient='records')

                    tbl_view_lecturers = ui.table(
                        columns=columns,
                        rows=rows,
                        row_key='lecturer_id',
                    ).classes('w-full border border-black text-black bg-white')
                with ui.tab_panel(tab_lecturers_manage).classes('w-full'):
                    with ui.dialog() as add_lecturer_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Add Lecturer').classes('text-lg font-bold')

                            def get_next_lecturer_id(df):
                                if df.empty:
                                    return 1
                                return int(df['lecturer_id'].max()) + 1


                            new_lecturer_inputs = {}

                            # Create input fields for all columns
                            for col in all_lecturers_df.columns:
                                if col == 'lecturer_id':
                                    # Show the auto-generated student_id as read-only
                                    new_lecturer_id = get_next_lecturer_id(all_lecturers_df)
                                    new_lecturer_inputs[col] = ui.input(
                                        label=f'Lecturer ID',
                                        value=str(new_lecturer_id)
                                    ).props('readonly')
                                else:
                                    # Create editable input for other columns
                                    new_lecturer_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    )


                            def save_lecturer():
                                lecturer_data = {col: inp.value for col, inp in new_lecturer_inputs.items()}

                                for col, value in lecturer_data.items():
                                    if col != 'lecturer_id' and not value.strip():
                                        ui.notify(f'{col.replace("_", " ").title()} cannot be blank', type='negative')
                                        return

                                #print(lecturer_data)

                                lecturer = api.lecturer_repo.create(**lecturer_data)
                                api.commit()

                                global all_lecturers_df
                                all_lecturers_df = pd.concat([all_lecturers_df, pd.DataFrame([lecturer_data])],
                                                            ignore_index=True)

                                add_lecturer_dialog.close()
                                ui.notify('Lecturer added successfully', type='positive')

                                tbl_view_lecturers.rows[:] = all_lecturers_df.to_dict('records')
                                tbl_view_lecturers.update()

                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=add_lecturer_dialog.close)
                                ui.button('Save', on_click=save_lecturer)
                    with ui.dialog() as edit_lecturer_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Edit Lecturer').classes('text-lg font-bold')

                            edit_lecturer_inputs = {}
                            selected_lecturer_id = {'value': None}  # Store selected ID


                            # lecturer ID selector
                            def validate_and_load_lecturer():
                                lecturer_id_value = edit_lecturer_inputs['lecturer_id_selector'].value

                                if not lecturer_id_value or not lecturer_id_value.strip():
                                    ui.notify('Please enter a lecturer ID', type='negative')
                                    return

                                # Check if lecturer exists
                                try:
                                    lecturer_id_int = int(lecturer_id_value)
                                except ValueError:
                                    ui.notify('Lecturer ID must be a number', type='negative')
                                    return

                                if lecturer_id_int not in all_lecturers_df['lecturer_id'].values:
                                    ui.notify(f'lecturer ID {lecturer_id_int} does not exist', type='negative')
                                    return

                                # Load lecturer data
                                selected_lecturer_id['value'] = lecturer_id_int
                                lecturer_row = all_lecturers_df[all_lecturers_df['lecturer_id'] == lecturer_id_int].iloc[0]

                                # Populate input fields
                                for col in all_lecturers_df.columns:
                                    if col != 'lecturer_id':
                                        edit_lecturer_inputs[col].value = str(lecturer_row[col])

                                ui.notify(f'Loaded lecturer {lecturer_id_int}', type='positive')


                            # lecturer ID input with dropdown
                            with ui.row().classes('w-full items-end gap-2'):
                                edit_lecturer_inputs['lecturer_id_selector'] = ui.select(
                                    label='Lecturer ID',
                                    options=sorted(all_lecturers_df['lecturer_id'].astype(str).tolist()),
                                    with_input=True
                                ).classes('flex-grow')
                                ui.button('Load', on_click=validate_and_load_lecturer)

                            ui.separator()

                            # Create input fields for all other columns
                            for col in all_lecturers_df.columns:
                                if col != 'lecturer_id':
                                    edit_lecturer_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    ).props('readonly')  # Start as readonly until lecturer is loaded


                            def enable_lecturer_editing():
                                if selected_lecturer_id['value'] is None:
                                    ui.notify('Please load a lecturer first', type='negative')
                                    return

                                # Enable all fields for editing
                                for col in all_lecturers_df.columns:
                                    if col != 'lecturer_id':
                                        edit_lecturer_inputs[col].props(remove='readonly')


                            def save_edited_lecturer():
                                if selected_lecturer_id['value'] is None:
                                    ui.notify('Please load a lecturer first', type='negative')
                                    return

                                # Get the updated values
                                updated_data = {col: inp.value for col, inp in edit_lecturer_inputs.items() if
                                                col != 'lecturer_id_selector'}

                                # Validate that no fields are blank
                                for col, value in updated_data.items():
                                    if col != 'lecturer_id' and (not value or not str(value).strip()):
                                        ui.notify(f'{col.replace("_", " ").title()} cannot be blank', type='negative')
                                        return

                                # Update in API
                                lecturer = api.lecturer_repo.update(selected_lecturer_id['value'], **updated_data)

                                # Update the dataframe
                                global all_lecturers_df
                                idx = \
                                    all_lecturers_df[
                                        all_lecturers_df['lecturer_id'] == selected_lecturer_id['value']].index[0]
                                for col, value in updated_data.items():
                                    all_lecturers_df.at[idx, col] = value

                                # Update the table
                                tbl_view_lecturers.rows = all_lecturers_df.to_dict('records')
                                tbl_view_lecturers.update()

                                edit_lecturer_dialog.close()
                                ui.notify('Lecturer updated successfully', type='positive')


                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=edit_lecturer_dialog.close)
                                ui.button('Edit', on_click=enable_lecturer_editing)
                                ui.button('Save', on_click=save_edited_lecturer)
                    with ui.dialog() as delete_lecturer_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Delete Lecturer').classes('text-lg font-bold')

                        delete_lecturer_inputs = {}
                        delete_selected_lecturer_id = {'value': None}


                        # lecturer ID selector
                        def validate_and_load_lecturer_for_delete():
                            delete_lecturer_id_value = delete_lecturer_inputs['lecturer_id_selector'].value

                            if not delete_lecturer_id_value or not delete_lecturer_id_value.strip():
                                ui.notify('Please enter a lecturer ID', type='negative')
                                return

                            # Check if lecturer exists
                            try:
                                delete_lecturer_id_int = int(delete_lecturer_id_value)
                            except ValueError:
                                ui.notify('lecturer ID must be a number', type='negative')
                                return

                            if delete_lecturer_id_int not in all_lecturers_df['lecturer_id'].values:
                                ui.notify(f'lecturer ID {delete_lecturer_id_int} does not exist', type='negative')
                                return

                            # Load lecturer data
                            delete_selected_lecturer_id['value'] = delete_lecturer_id_int
                            lecturer_row = all_lecturers_df[all_lecturers_df['lecturer_id'] == delete_lecturer_id_int].iloc[
                                0]

                            # Populate input fields
                            for col in all_lecturers_df.columns:
                                if col != 'lecturer_id':
                                    delete_lecturer_inputs[col].value = str(lecturer_row[col])

                            ui.notify(f'Loaded lecturer {delete_lecturer_id_int}', type='positive')


                        # lecturer ID input with dropdown
                        with ui.row().classes('w-full items-end gap-2'):
                            delete_lecturer_inputs['lecturer_id_selector'] = ui.select(
                                label='lecturer ID',
                                options=sorted(all_lecturers_df['lecturer_id'].astype(str).tolist()),
                                with_input=True
                            ).classes('flex-grow')
                            ui.button('Load', on_click=validate_and_load_lecturer_for_delete)

                        ui.separator()

                        # Create input fields for all other columns (read-only)
                        for col in all_lecturers_df.columns:
                            if col != 'lecturer_id':
                                delete_lecturer_inputs[col] = ui.input(
                                    label=col.replace('_', ' ').title()
                                ).props('readonly')

                        ui.separator()

                        ui.label('Warning: This action cannot be undone!').classes('text-red-600 font-semibold')


                        def delete_lecturer():
                            if delete_selected_lecturer_id['value'] is None:
                                ui.notify('Please load a lecturer first', type='negative')
                                return

                            # Delete from API
                            try:
                                api.lecturer_repo.delete(delete_selected_lecturer_id['value'])
                            except Exception as e:
                                ui.notify(f'Error deleting lecturer: {str(e)}', type='negative')
                                return

                            # Delete from dataframe
                            global all_lecturers_df
                            all_lecturers_df = all_lecturers_df[
                                all_lecturers_df['lecturer_id'] != delete_selected_lecturer_id['value']]
                            all_lecturers_df.reset_index(drop=True, inplace=True)

                            # Update the table
                            tbl_view_lecturers.rows = all_lecturers_df.to_dict('records')
                            tbl_view_lecturers.update()

                            # Reset dialog state
                            delete_selected_lecturer_id['value'] = None
                            for col in all_lecturers_df.columns:
                                if col != 'lecturer_id':
                                    delete_lecturer_inputs[col].value = ''
                            delete_lecturer_inputs['lecturer_id_selector'].value = None

                            delete_lecturer_dialog.close()
                            ui.notify('lecturer deleted successfully', type='positive')


                        with ui.row().classes('gap-2 mt-4'):
                            ui.button('Cancel', on_click=delete_lecturer_dialog.close)
                            ui.button('Delete', on_click=delete_lecturer, color='red')

                    with ui.row().classes('gap-4'):
                        ui.button('Add', on_click=lambda: add_lecturer_dialog.open())
                        ui.button('Edit', on_click=lambda: edit_lecturer_dialog.open())
                        ui.button('Delete', on_click=lambda: delete_lecturer_dialog.open(), color='red')
    with ui.tab_panels(main_tabs, value = tab_nas).classes('w-full'):
        with ui.tab_panel(tab_nas):
            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Non-Academic Staff Records').classes('text-xl')
            with ui.tabs().classes('w-full') as nas_ops:
                tab_nas_view = ui.tab('View Non-Academic Staff Records')
                tab_nas_manage = ui.tab('Manage Non-Academic Staff Records')
            with ui.tab_panels(nas_ops).classes('w-full'):
                with ui.tab_panel(tab_nas_view).classes('w-full'):
                    columns = [
                        {
                            'name': col,
                            'label': col.replace('_', ' ').title(),  # nicer column titles
                            'field': col,
                            'sortable': True,
                        }
                        for col in all_nas_df.columns
                    ]

                    rows = all_nas_df.to_dict(orient='records')

                    tbl_view_nas = ui.table(
                        columns=columns,
                        rows=rows,
                        row_key='staff_id',
                    ).classes('w-full border border-black text-black bg-white')
                with ui.tab_panel(tab_nas_manage).classes('w-full'):
                    inputs6 = {}
    with ui.tab_panels(main_tabs, value = tab_courses).classes('w-full'):
        with ui.tab_panel(tab_courses):
            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Course Records').classes('text-xl')
            with ui.tabs().classes('w-full') as course_ops:
                tab_courses_view = ui.tab('View Course Records')
                tab_courses_manage = ui.tab('Manage Course Records')
            with ui.tab_panels(course_ops).classes('w-full'):
                with ui.tab_panel(tab_courses_view).classes('w-full'):
                    columns = [
                        {
                            'name': col,
                            'label': col.replace('_', ' ').title(),  # nicer column titles
                            'field': col,
                            'sortable': True,
                        }
                        for col in all_courses_df.columns
                    ]

                    rows = all_courses_df.to_dict(orient='records')

                    tbl_view_courses = ui.table(
                        columns=columns,
                        rows=rows,
                        row_key='course_id',
                    ).classes('w-full border border-black text-black bg-white')
                with ui.tab_panel(tab_courses_manage).classes('w-full'):
                    inputs8 = {}
    with ui.tab_panels(main_tabs, value = tab_rp).classes('w-full'):
        with ui.tab_panel(tab_departments):
            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Departmental Records').classes('text-xl')
            with ui.tabs().classes('w-full') as department_ops:
                tab_departments_view = ui.tab('View Departmental Records')
                tab_departments_manage = ui.tab('Manage Departmental Records')
            with ui.tab_panels(department_ops).classes('w-full'):
                with ui.tab_panel(tab_departments_view).classes('w-full'):
                    columns = [
                        {
                            'name': col,
                            'label': col.replace('_', ' ').title(),  # nicer column titles
                            'field': col,
                            'sortable': True,
                        }
                        for col in all_departments_df.columns
                    ]

                    rows = all_departments_df.to_dict(orient='records')

                    tbl_view_departments = ui.table(
                        columns=columns,
                        rows=rows,
                        row_key='departments_id',
                    ).classes('w-full border border-black text-black bg-white')
                with ui.tab_panel(tab_departments_manage).classes('w-full'):
                    inputs10 = {}
    with ui.tab_panels(main_tabs, value = tab_rp).classes('w-full'):
        with ui.tab_panel(tab_rp):
            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Research Projects Records').classes('text-xl')
            with ui.tabs().classes('w-full') as rp_ops:
                tab_rp_view = ui.tab('View Research Projects Records')
                tab_rp_manage = ui.tab('Manage Research Projects Records')
            with ui.tab_panels(rp_ops).classes('w-full'):
                with ui.tab_panel(tab_rp_view).classes('w-full'):
                    columns = [
                        {
                            'name': col,
                            'label': col.replace('_', ' ').title(),  # nicer column titles
                            'field': col,
                            'sortable': True,
                        }
                        for col in all_rp_df.columns
                    ]

                    rows = all_rp_df.to_dict(orient='records')

                    tbl_view_rp = ui.table(
                        columns=columns,
                        rows=rows,
                        row_key='project_id',
                    ).classes('w-full border border-black text-black bg-white')
                with ui.tab_panel(tab_rp_manage).classes('w-full'):
                    inputs12 = {}
    with ui.tab_panels(main_tabs, value = tab_qr).classes('w-full'):
        with ui.tab_panel(tab_qr):
            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Queries and Reports').classes('text-xl')
            with ui.tabs().classes('w-full') as qr_ops:
                tab_qr_view = ui.tab('View Queries and Reports')
            with ui.tab_panels(qr_ops).classes('w-full'):
                with ui.tab_panel(tab_qr_view).classes('w-full'):
                    inputs13 = {}

ui.run()
