
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

staff = api.staff_repo.get_all()
all_staff_df = pd.DataFrame([staff.as_dict for staff in staff])

courses = api.course_repo.get_all()
all_courses_df = pd.DataFrame([course.as_dict for course in courses])

departments = api.department_repo.get_all()
all_departments_df = pd.DataFrame([department.as_dict for department in departments])

research_projects = api.research_project_repo.get_all()
all_projects_df = pd.DataFrame([rp.as_dict for rp in research_projects])

ui.add_css('''
    @layer utilities {
       .standard-btn {
           background-color: black !important; height: 50% !important; width: 500px !important;
        }
    }
''')

with ui.column().classes('w-full'):
    with ui.tabs().classes('w-full') as main_tabs:
        tab_students = ui.tab('Students')
        tab_lecturers = ui.tab('Lecturers')
        tab_staff = ui.tab('Non-Academic Staff')
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

                    def refresh_student_dropdowns():
                        updated_options = sorted(all_students_df['student_id'].astype(str).tolist())
                        edit_student_inputs['student_id_selector'].options = updated_options
                        edit_student_inputs['student_id_selector'].update()
                        delete_student_inputs['student_id_selector'].options = updated_options
                        delete_student_inputs['student_id_selector'].update()

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
 #                               all_students_df = pd.concat([all_students_df, pd.DataFrame([student_data])],
 #                                                           ignore_index=True)

                                all_students_df = pd.concat([all_students_df, pd.DataFrame([student.as_dict])],
                                                            ignore_index=True)

                                add_student_dialog.close()
                                ui.notify('Student added successfully', type='positive')

                                tbl_view_students.rows[:] = all_students_df.to_dict('records')
                                tbl_view_students.update()

                                refresh_student_dropdowns()

                                next_student_id = get_next_student_id(all_students_df)
                                new_student_inputs['student_id'].value = int(next_student_id)
                                new_student_inputs['student_id'].update()

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
                                api.commit()

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
                                    api.commit()
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

                                refresh_student_dropdowns()

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

                    def refresh_lecturer_dropdowns():
                        updated_options = sorted(all_lecturers_df['lecturer_id'].astype(str).tolist())
                        edit_lecturer_inputs['lecturer_id_selector'].options = updated_options
                        edit_lecturer_inputs['lecturer_id_selector'].update()
                        delete_lecturer_inputs['lecturer_id_selector'].options = updated_options
                        delete_lecturer_inputs['lecturer_id_selector'].update()

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

                                refresh_lecturer_dropdowns()

                                next_lecturer_id = get_next_student_id(all_lecturers_df)
                                new_lecturer_inputs['lecturer_id'].value = int(next_lecturer_id)
                                new_lecturer_inputs['lecturer_id'].update()

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
                                api.commit()

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
                                    api.commit()
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

                                refresh_lecturer_dropdowns()

                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=delete_lecturer_dialog.close)
                                ui.button('Delete', on_click=delete_lecturer, color='red')
                    with ui.row().classes('gap-4'):
                        ui.button('Add', on_click=lambda: add_lecturer_dialog.open())
                        ui.button('Edit', on_click=lambda: edit_lecturer_dialog.open())
                        ui.button('Delete', on_click=lambda: delete_lecturer_dialog.open(), color='red')
    with ui.tab_panels(main_tabs, value = tab_staff).classes('w-full'):
        with ui.tab_panel(tab_staff):
            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Non-Academic Staff Records').classes('text-xl')
            with ui.tabs().classes('w-full') as staff_ops:
                tab_staff_view = ui.tab('View Non-Academic Staff Records')
                tab_staff_manage = ui.tab('Manage Non-Academic Staff Records')
            with ui.tab_panels(staff_ops).classes('w-full'):
                with ui.tab_panel(tab_staff_view).classes('w-full'):
                    columns = [
                        {
                            'name': col,
                            'label': col.replace('_', ' ').title(),  # nicer column titles
                            'field': col,
                            'sortable': True,
                        }
                        for col in all_staff_df.columns
                    ]

                    rows = all_staff_df.to_dict(orient='records')

                    tbl_view_staff = ui.table(
                        columns=columns,
                        rows=rows,
                        row_key='staff_id',
                    ).classes('w-full border border-black text-black bg-white')
                with ui.tab_panel(tab_staff_manage).classes('w-full'):
                    with ui.dialog() as add_staff_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Add staff').classes('text-lg font-bold')


                            def get_next_staff_id(df):
                                if df.empty:
                                    return 1
                                return int(df['staff_id'].max()) + 1


                            new_staff_inputs = {}

                            # Create input fields for all columns
                            for col in all_staff_df.columns:
                                if col == 'staff_id':
                                    # Show the auto-generated student_id as read-only
                                    new_staff_id = get_next_staff_id(all_staff_df)
                                    new_staff_inputs[col] = ui.input(
                                        label=f'Staff ID',
                                        value=str(new_staff_id)
                                    ).props('readonly')
                                else:
                                    # Create editable input for other columns
                                    new_staff_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    )


                            def save_staff():
                                staff_data = {col: inp.value for col, inp in new_staff_inputs.items()}

                                for col, value in staff_data.items():
                                    if col != 'staff_id' and not value.strip():
                                        ui.notify(f'{col.replace("_", " ").title()} cannot be blank', type='negative')
                                        return

                                # print(staff_data)

                                staff = api.staff_repo.create(**staff_data)
                                api.commit()

                                global all_staff_df
                                all_staff_df = pd.concat([all_staff_df, pd.DataFrame([staff_data])],
                                                             ignore_index=True)

                                add_staff_dialog.close()
                                ui.notify('Staff added successfully', type='positive')

                                tbl_view_staff.rows[:] = all_staff_df.to_dict('records')
                                tbl_view_staff.update()

                                next_staff_id = get_next_staff_id(all_staff_df)
                                new_staff_inputs['staff_id'].value = int(next_staff_id)
                                new_staff_inputs['staff_id'].update()

                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=add_staff_dialog.close)
                                ui.button('Save', on_click=save_staff)
                    with ui.dialog() as edit_staff_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Edit Staff').classes('text-lg font-bold')

                            edit_staff_inputs = {}
                            selected_staff_id = {'value': None}  # Store selected ID


                            # Staff ID selector
                            def validate_and_load_staff():
                                staff_id_value = edit_staff_inputs['staff_id_selector'].value

                                if not staff_id_value or not staff_id_value.strip():
                                    ui.notify('Please enter a Staff ID', type='negative')
                                    return

                                # Check if staff exists
                                try:
                                    staff_id_int = int(staff_id_value)
                                except ValueError:
                                    ui.notify('Staff ID must be a number', type='negative')
                                    return

                                if staff_id_int not in all_staff_df['staff_id'].values:
                                    ui.notify(f'Staff ID {staff_id_int} does not exist', type='negative')
                                    return

                                # Load staff data
                                selected_staff_id['value'] = staff_id_int
                                staff_row = \
                                all_staff_df[all_staff_df['staff_id'] == staff_id_int].iloc[0]

                                # Populate input fields
                                for col in all_staff_df.columns:
                                    if col != 'staff_id':
                                        edit_staff_inputs[col].value = str(staff_row[col])

                                ui.notify(f'Loaded Staff {staff_id_int}', type='positive')


                            # staff ID input with dropdown
                            with ui.row().classes('w-full items-end gap-2'):
                                edit_staff_inputs['staff_id_selector'] = ui.select(
                                    label='staff ID',
                                    options=sorted(all_staff_df['staff_id'].astype(str).tolist()),
                                    with_input=True
                                ).classes('flex-grow')
                                ui.button('Load', on_click=validate_and_load_staff)

                            ui.separator()

                            # Create input fields for all other columns
                            for col in all_staff_df.columns:
                                if col != 'staff_id':
                                    edit_staff_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    ).props('readonly')  # Start as readonly until staff is loaded


                            def enable_staff_editing():
                                if selected_staff_id['value'] is None:
                                    ui.notify('Please load Staff first', type='negative')
                                    return

                                # Enable all fields for editing
                                for col in all_staff_df.columns:
                                    if col != 'staff_id':
                                        edit_staff_inputs[col].props(remove='readonly')


                            def save_edited_staff():
                                if selected_staff_id['value'] is None:
                                    ui.notify('Please load Staff first', type='negative')
                                    return

                                # Get the updated values
                                updated_data = {col: inp.value for col, inp in edit_staff_inputs.items() if
                                                col != 'staff_id_selector'}

                                # Validate that no fields are blank
                                for col, value in updated_data.items():
                                    if col != 'staff_id_selector' and (not value or not str(value).strip()):
                                        ui.notify(f'{col.replace("_", " ").title()} cannot be blank', type='negative')
                                        return

                                # Update in API
                                staff = api.staff_repo.update(selected_staff_id['value'], **updated_data)
                                api.commit()

                                # Update the dataframe
                                global all_staff_df
                                idx = \
                                    all_staff_df[
                                        all_staff_df['staff_id'] == selected_staff_id['value']].index[0]
                                for col, value in updated_data.items():
                                    all_staff_df.at[idx, col] = value

                                # Update the table
                                tbl_view_staff.rows = all_staff_df.to_dict('records')
                                tbl_view_staff.update()

                                edit_staff_dialog.close()
                                ui.notify('staff updated successfully', type='positive')


                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=edit_staff_dialog.close)
                                ui.button('Edit', on_click=enable_staff_editing)
                                ui.button('Save', on_click=save_edited_staff)
                    with ui.dialog() as delete_staff_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Delete Staff').classes('text-lg font-bold')

                            delete_staff_inputs = {}
                            delete_selected_staff_id = {'value': None}


                            # staff ID selector
                            def validate_and_load_staff_for_delete():
                                delete_staff_id_value = delete_staff_inputs['staff_id_selector'].value

                                if not delete_staff_id_value or not delete_staff_id_value.strip():
                                    ui.notify('Please enter Staff ID', type='negative')
                                    return

                                # Check if staff exists
                                try:
                                    delete_staff_id_int = int(delete_staff_id_value)
                                except ValueError:
                                    ui.notify('Staff ID must be a number', type='negative')
                                    return

                                if delete_staff_id_int not in all_staff_df['staff_id'].values:
                                    ui.notify(f'Staff ID {delete_staff_id_int} does not exist', type='negative')
                                    return

                                # Load staff data
                                delete_selected_staff_id['value'] = delete_staff_id_int
                                staff_row = \
                                all_staff_df[all_staff_df['staff_id'] == delete_staff_id_int].iloc[
                                    0]

                                # Populate input fields
                                for col in all_staff_df.columns:
                                    if col != 'staff_id':
                                        delete_staff_inputs[col].value = str(staff_row[col])

                                ui.notify(f'Loaded Staff {delete_staff_id_int}', type='positive')


                            # staff ID input with dropdown
                            with ui.row().classes('w-full items-end gap-2'):
                                delete_staff_inputs['staff_id_selector'] = ui.select(
                                    label='Staff ID',
                                    options=sorted(all_staff_df['staff_id'].astype(str).tolist()),
                                    with_input=True
                                ).classes('flex-grow')
                                ui.button('Load', on_click=validate_and_load_staff_for_delete)

                            ui.separator()

                            # Create input fields for all other columns (read-only)
                            for col in all_staff_df.columns:
                                if col != 'staff_id':
                                    delete_staff_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    ).props('readonly')

                            ui.separator()

                            ui.label('Warning: This action cannot be undone!').classes('text-red-600 font-semibold')


                            def delete_staff():
                                if delete_selected_staff_id['value'] is None:
                                    ui.notify('Please load a Staff first', type='negative')
                                    return

                                # Delete from API
                                try:
                                    api.staff_repo.delete(delete_selected_staff_id['value'])
                                    api.commit()
                                except Exception as e:
                                    ui.notify(f'Error deleting Staff: {str(e)}', type='negative')
                                    return

                                # Delete from dataframe
                                global all_staff_df
                                all_staff_df = all_staff_df[
                                    all_staff_df['staff_id'] != delete_selected_staff_id['value']]
                                all_staff_df.reset_index(drop=True, inplace=True)

                                # Update the table
                                tbl_view_staff.rows = all_staff_df.to_dict('records')
                                tbl_view_staff.update()

                                # Reset dialog state
                                delete_selected_staff_id['value'] = None
                                for col in all_staff_df.columns:
                                    if col != 'staff_id':
                                        delete_staff_inputs[col].value = ''
                                delete_staff_inputs['staff_id_selector'].value = None

                                delete_staff_dialog.close()
                                ui.notify('staff deleted successfully', type='positive')


                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=delete_staff_dialog.close)
                                ui.button('Delete', on_click=delete_staff, color='red')

                        with ui.row().classes('gap-4'):
                            ui.button('Add', on_click=lambda: add_staff_dialog.open())
                            ui.button('Edit', on_click=lambda: edit_staff_dialog.open())
                            ui.button('Delete', on_click=lambda: delete_staff_dialog.open(), color='red')
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
                    with ui.dialog() as add_course_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Add Course').classes('text-lg font-bold')

                            def get_next_course_id(df):
                                if df.empty:
                                    return 1
                                return int(df['course_id'].max()) + 1


                            new_course_inputs = {}

                            # Create input fields for all columns
                            for col in all_courses_df.columns:
                                if col == 'course_id':
                                    # Show the auto-generated student_id as read-only
                                    new_course_id = get_next_course_id(all_courses_df)
                                    new_course_inputs[col] = ui.input(
                                        label=f'Course ID',
                                        value=str(new_course_id)
                                    ).props('readonly')
                                else:
                                    # Create editable input for other columns
                                    new_course_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    )


                            def save_course():
                                course_data = {col: inp.value for col, inp in new_course_inputs.items()}

                                for col, value in course_data.items():
                                    if col != 'course_id' and not value.strip():
                                        ui.notify(f'{col.replace("_", " ").title()} cannot be blank', type='negative')
                                        return

                                #print(course_data)

                                course = api.course_repo.create(**course_data)
                                api.commit()

                                global all_courses_df
                                all_courses_df = pd.concat([all_courses_df, pd.DataFrame([course_data])],
                                                            ignore_index=True)

                                add_course_dialog.close()
                                ui.notify('Course added successfully', type='positive')

                                tbl_view_courses.rows[:] = all_courses_df.to_dict('records')
                                tbl_view_courses.update()

                                next_course_id = get_next_course_id(all_courses_df)
                                new_course_inputs['course_id'].value = int(next_course_id)
                                new_course_inputs['course_id'].update()

                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=add_course_dialog.close)
                                ui.button('Save', on_click=save_course)
                    with ui.dialog() as edit_course_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Edit Course').classes('text-lg font-bold')

                            edit_course_inputs = {}
                            selected_course_id = {'value': None}  # Store selected ID


                            # course ID selector
                            def validate_and_load_course():
                                course_id_value = edit_course_inputs['course_id_selector'].value

                                if not course_id_value or not course_id_value.strip():
                                    ui.notify('Please enter a course ID', type='negative')
                                    return

                                # Check if course exists
                                try:
                                    course_id_int = int(course_id_value)
                                except ValueError:
                                    ui.notify('Course ID must be a number', type='negative')
                                    return

                                if course_id_int not in all_courses_df['course_id'].values:
                                    ui.notify(f'course ID {course_id_int} does not exist', type='negative')
                                    return

                                # Load course data
                                selected_course_id['value'] = course_id_int
                                course_row = all_courses_df[all_courses_df['course_id'] == course_id_int].iloc[0]

                                # Populate input fields
                                for col in all_courses_df.columns:
                                    if col != 'course_id':
                                        edit_course_inputs[col].value = str(course_row[col])

                                ui.notify(f'Loaded course {course_id_int}', type='positive')


                            # course ID input with dropdown
                            with ui.row().classes('w-full items-end gap-2'):
                                edit_course_inputs['course_id_selector'] = ui.select(
                                    label='Course ID',
                                    options=sorted(all_courses_df['course_id'].astype(str).tolist()),
                                    with_input=True
                                ).classes('flex-grow')
                                ui.button('Load', on_click=validate_and_load_course)

                            ui.separator()

                            # Create input fields for all other columns
                            for col in all_courses_df.columns:
                                if col != 'course_id':
                                    edit_course_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    ).props('readonly')  # Start as readonly until course is loaded


                            def enable_course_editing():
                                if selected_course_id['value'] is None:
                                    ui.notify('Please load a course first', type='negative')
                                    return

                                # Enable all fields for editing
                                for col in all_courses_df.columns:
                                    if col != 'course_id':
                                        edit_course_inputs[col].props(remove='readonly')


                            def save_edited_course():
                                if selected_course_id['value'] is None:
                                    ui.notify('Please load a course first', type='negative')
                                    return

                                # Get the updated values
                                updated_data = {col: inp.value for col, inp in edit_course_inputs.items() if
                                                col != 'course_id_selector'}

                                # Validate that no fields are blank
                                for col, value in updated_data.items():
                                    if col != 'course_id' and (not value or not str(value).strip()):
                                        ui.notify(f'{col.replace("_", " ").title()} cannot be blank', type='negative')
                                        return

                                # Update in API
                                course = api.course_repo.update(selected_course_id['value'], **updated_data)
                                api.commit()

                                # Update the dataframe
                                global all_courses_df
                                idx = \
                                    all_courses_df[
                                        all_courses_df['course_id'] == selected_course_id['value']].index[0]
                                for col, value in updated_data.items():
                                    all_courses_df.at[idx, col] = value

                                # Update the table
                                tbl_view_courses.rows = all_courses_df.to_dict('records')
                                tbl_view_courses.update()

                                edit_course_dialog.close()
                                ui.notify('Course updated successfully', type='positive')


                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=edit_course_dialog.close)
                                ui.button('Edit', on_click=enable_course_editing)
                                ui.button('Save', on_click=save_edited_course)
                    with ui.dialog() as delete_course_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Delete Course').classes('text-lg font-bold')

                            delete_course_inputs = {}
                            delete_selected_course_id = {'value': None}


                            # course ID selector
                            def validate_and_load_course_for_delete():
                                delete_course_id_value = delete_course_inputs['course_id_selector'].value

                                if not delete_course_id_value or not delete_course_id_value.strip():
                                    ui.notify('Please enter a course ID', type='negative')
                                    return

                                # Check if course exists
                                try:
                                    delete_course_id_int = int(delete_course_id_value)
                                except ValueError:
                                    ui.notify('course ID must be a number', type='negative')
                                    return

                                if delete_course_id_int not in all_courses_df['course_id'].values:
                                    ui.notify(f'course ID {delete_course_id_int} does not exist', type='negative')
                                    return

                                # Load course data
                                delete_selected_course_id['value'] = delete_course_id_int
                                course_row = all_courses_df[all_courses_df['course_id'] == delete_course_id_int].iloc[
                                    0]

                                # Populate input fields
                                for col in all_courses_df.columns:
                                    if col != 'course_id':
                                        delete_course_inputs[col].value = str(course_row[col])

                                ui.notify(f'Loaded course {delete_course_id_int}', type='positive')


                            # course ID input with dropdown
                            with ui.row().classes('w-full items-end gap-2'):
                                delete_course_inputs['course_id_selector'] = ui.select(
                                    label='course ID',
                                    options=sorted(all_courses_df['course_id'].astype(str).tolist()),
                                    with_input=True
                                ).classes('flex-grow')
                                ui.button('Load', on_click=validate_and_load_course_for_delete)

                            ui.separator()

                            # Create input fields for all other columns (read-only)
                            for col in all_courses_df.columns:
                                if col != 'course_id':
                                    delete_course_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    ).props('readonly')

                            ui.separator()

                            ui.label('Warning: This action cannot be undone!').classes('text-red-600 font-semibold')


                            def delete_course():
                                if delete_selected_course_id['value'] is None:
                                    ui.notify('Please load a course first', type='negative')
                                    return

                                # Delete from API
                                try:
                                    api.course_repo.delete(delete_selected_course_id['value'])
                                    api.commit()
                                except Exception as e:
                                    ui.notify(f'Error deleting course: {str(e)}', type='negative')
                                    return

                                # Delete from dataframe
                                global all_courses_df
                                all_courses_df = all_courses_df[
                                    all_courses_df['course_id'] != delete_selected_course_id['value']]
                                all_courses_df.reset_index(drop=True, inplace=True)

                                # Update the table
                                tbl_view_courses.rows = all_courses_df.to_dict('records')
                                tbl_view_courses.update()

                                # Reset dialog state
                                delete_selected_course_id['value'] = None
                                for col in all_courses_df.columns:
                                    if col != 'course_id':
                                        delete_course_inputs[col].value = ''
                                delete_course_inputs['course_id_selector'].value = None

                                delete_course_dialog.close()
                                ui.notify('course deleted successfully', type='positive')


                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=delete_course_dialog.close)
                                ui.button('Delete', on_click=delete_course, color='red')
                    with ui.row().classes('gap-4'):
                        ui.button('Add', on_click=lambda: add_course_dialog.open())
                        ui.button('Edit', on_click=lambda: edit_course_dialog.open())
                        ui.button('Delete', on_click=lambda: delete_course_dialog.open(), color='red')
    with ui.tab_panels(main_tabs, value = tab_departments).classes('w-full'):
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
                    with ui.dialog() as add_department_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Add Department').classes('text-lg font-bold')

                            def get_next_dept_id(df):
                                if df.empty:
                                    return 1
                                return int(df['dept_id'].max()) + 1


                            new_department_inputs = {}

                            # Create input fields for all columns
                            for col in all_departments_df.columns:
                                if col == 'dept_id':
                                    # Show the auto-generated student_id as read-only
                                    new_dept_id = get_next_dept_id(all_departments_df)
                                    new_department_inputs[col] = ui.input(
                                        label=f'Department ID',
                                        value=str(new_dept_id)
                                    ).props('readonly')
                                else:
                                    # Create editable input for other columns
                                    new_department_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    )


                            def save_department():
                                department_data = {col: inp.value for col, inp in new_department_inputs.items()}

                                for col, value in department_data.items():
                                    if col != 'dept_id' and not value.strip():
                                        ui.notify(f'{col.replace("_", " ").title()} cannot be blank', type='negative')
                                        return

                                #print(department_data)

                                department = api.department_repo.create(**department_data)
                                api.commit()

                                global all_departments_df
                                all_departments_df = pd.concat([all_departments_df, pd.DataFrame([department_data])],
                                                            ignore_index=True)

                                add_department_dialog.close()
                                ui.notify('Department added successfully', type='positive')

                                tbl_view_departments.rows[:] = all_departments_df.to_dict('records')
                                tbl_view_departments.update()

                                next_dept_id = get_next_dept_id(all_departments_df)
                                new_department_inputs['dept_id'].value = int(next_dept_id)
                                new_department_inputs['dept_id'].update()

                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=add_department_dialog.close)
                                ui.button('Save', on_click=save_department)
                    with ui.dialog() as edit_department_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Edit Department').classes('text-lg font-bold')

                            edit_department_inputs = {}
                            selected_dept_id = {'value': None}  # Store selected ID


                            # department ID selector
                            def validate_and_load_department():
                                dept_id_value = edit_department_inputs['dept_id_selector'].value

                                if not dept_id_value or not dept_id_value.strip():
                                    ui.notify('Please enter a department ID', type='negative')
                                    return

                                # Check if department exists
                                try:
                                    dept_id_int = int(dept_id_value)
                                except ValueError:
                                    ui.notify('Department ID must be a number', type='negative')
                                    return

                                if dept_id_int not in all_departments_df['dept_id'].values:
                                    ui.notify(f'department ID {dept_id_int} does not exist', type='negative')
                                    return

                                # Load department data
                                selected_dept_id['value'] = dept_id_int
                                department_row = all_departments_df[all_departments_df['dept_id'] == dept_id_int].iloc[0]

                                # Populate input fields
                                for col in all_departments_df.columns:
                                    if col != 'dept_id':
                                        edit_department_inputs[col].value = str(department_row[col])

                                ui.notify(f'Loaded department {dept_id_int}', type='positive')


                            # department ID input with dropdown
                            with ui.row().classes('w-full items-end gap-2'):
                                edit_department_inputs['dept_id_selector'] = ui.select(
                                    label='Department ID',
                                    options=sorted(all_departments_df['dept_id'].astype(str).tolist()),
                                    with_input=True
                                ).classes('flex-grow')
                                ui.button('Load', on_click=validate_and_load_department)

                            ui.separator()

                            # Create input fields for all other columns
                            for col in all_departments_df.columns:
                                if col != 'dept_id':
                                    edit_department_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    ).props('readonly')  # Start as readonly until department is loaded


                            def enable_department_editing():
                                if selected_dept_id['value'] is None:
                                    ui.notify('Please load a department first', type='negative')
                                    return

                                # Enable all fields for editing
                                for col in all_departments_df.columns:
                                    if col != 'dept_id':
                                        edit_department_inputs[col].props(remove='readonly')


                            def save_edited_department():
                                if selected_dept_id['value'] is None:
                                    ui.notify('Please load a department first', type='negative')
                                    return

                                # Get the updated values
                                updated_data = {col: inp.value for col, inp in edit_department_inputs.items() if
                                                col != 'dept_id_selector'}

                                # Validate that no fields are blank
                                for col, value in updated_data.items():
                                    if col != 'dept_id' and (not value or not str(value).strip()):
                                        ui.notify(f'{col.replace("_", " ").title()} cannot be blank', type='negative')
                                        return

                                # Update in API
                                department = api.department_repo.update(selected_dept_id['value'], **updated_data)
                                api.commit()

                                # Update the dataframe
                                global all_departments_df
                                idx = \
                                    all_departments_df[
                                        all_departments_df['dept_id'] == selected_dept_id['value']].index[0]
                                for col, value in updated_data.items():
                                    all_departments_df.at[idx, col] = value

                                # Update the table
                                tbl_view_departments.rows = all_departments_df.to_dict('records')
                                tbl_view_departments.update()

                                edit_department_dialog.close()
                                ui.notify('Department updated successfully', type='positive')


                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=edit_department_dialog.close)
                                ui.button('Edit', on_click=enable_department_editing)
                                ui.button('Save', on_click=save_edited_department)
                    with ui.dialog() as delete_department_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Delete Department').classes('text-lg font-bold')

                            delete_department_inputs = {}
                            delete_selected_dept_id = {'value': None}


                            # department ID selector
                            def validate_and_load_department_for_delete():
                                delete_dept_id_value = delete_department_inputs['dept_id_selector'].value

                                if not delete_dept_id_value or not delete_dept_id_value.strip():
                                    ui.notify('Please enter a department ID', type='negative')
                                    return

                                # Check if department exists
                                try:
                                    delete_dept_id_int = int(delete_dept_id_value)
                                except ValueError:
                                    ui.notify('department ID must be a number', type='negative')
                                    return

                                if delete_dept_id_int not in all_departments_df['dept_id'].values:
                                    ui.notify(f'department ID {delete_dept_id_int} does not exist', type='negative')
                                    return

                                # Load department data
                                delete_selected_dept_id['value'] = delete_dept_id_int
                                department_row = all_departments_df[all_departments_df['dept_id'] == delete_dept_id_int].iloc[
                                    0]

                                # Populate input fields
                                for col in all_departments_df.columns:
                                    if col != 'dept_id':
                                        delete_department_inputs[col].value = str(department_row[col])

                                ui.notify(f'Loaded department {delete_dept_id_int}', type='positive')


                            # department ID input with dropdown
                            with ui.row().classes('w-full items-end gap-2'):
                                delete_department_inputs['dept_id_selector'] = ui.select(
                                    label='department ID',
                                    options=sorted(all_departments_df['dept_id'].astype(str).tolist()),
                                    with_input=True
                                ).classes('flex-grow')
                                ui.button('Load', on_click=validate_and_load_department_for_delete)

                            ui.separator()

                            # Create input fields for all other columns (read-only)
                            for col in all_departments_df.columns:
                                if col != 'dept_id':
                                    delete_department_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    ).props('readonly')

                            ui.separator()

                            ui.label('Warning: This action cannot be undone!').classes('text-red-600 font-semibold')


                            def delete_department():
                                if delete_selected_dept_id['value'] is None:
                                    ui.notify('Please load a department first', type='negative')
                                    return

                                # Delete from API
                                try:
                                    api.department_repo.delete(delete_selected_dept_id['value'])
                                    api.commit()
                                except Exception as e:
                                    ui.notify(f'Error deleting department: {str(e)}', type='negative')
                                    return

                                # Delete from dataframe
                                global all_departments_df
                                all_departments_df = all_departments_df[
                                    all_departments_df['dept_id'] != delete_selected_dept_id['value']]
                                all_departments_df.reset_index(drop=True, inplace=True)

                                # Update the table
                                tbl_view_departments.rows = all_departments_df.to_dict('records')
                                tbl_view_departments.update()

                                # Reset dialog state
                                delete_selected_dept_id['value'] = None
                                for col in all_departments_df.columns:
                                    if col != 'dept_id':
                                        delete_department_inputs[col].value = ''
                                delete_department_inputs['dept_id_selector'].value = None

                                delete_department_dialog.close()
                                ui.notify('department deleted successfully', type='positive')


                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=delete_department_dialog.close)
                                ui.button('Delete', on_click=delete_department, color='red')
                    with ui.row().classes('gap-4'):
                        ui.button('Add', on_click=lambda: add_department_dialog.open())
                        ui.button('Edit', on_click=lambda: edit_department_dialog.open())
                        ui.button('Delete', on_click=lambda: delete_department_dialog.open(), color='red')
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
                        for col in all_projects_df.columns
                    ]

                    rows = all_projects_df.to_dict(orient='records')

                    tbl_view_projects = ui.table(
                        columns=columns,
                        rows=rows,
                        row_key='project_id',
                    ).classes('w-full border border-black text-black bg-white')
                with ui.tab_panel(tab_rp_manage).classes('w-full'):
                    with ui.dialog() as add_project_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Add Project').classes('text-lg font-bold')

                            def get_next_project_id(df):
                                if df.empty:
                                    return 1
                                return int(df['project_id'].max()) + 1


                            new_project_inputs = {}

                            # Create input fields for all columns
                            for col in all_projects_df.columns:
                                if col == 'project_id':
                                    # Show the auto-generated student_id as read-only
                                    new_project_id = get_next_project_id(all_projects_df)
                                    new_project_inputs[col] = ui.input(
                                        label=f'Project ID',
                                        value=str(new_project_id)
                                    ).props('readonly')
                                else:
                                    # Create editable input for other columns
                                    new_project_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    )


                            def save_project():
                                project_data = {col: inp.value for col, inp in new_project_inputs.items()}

                                for col, value in project_data.items():
                                    if col != 'project_id' and not value.strip():
                                        ui.notify(f'{col.replace("_", " ").title()} cannot be blank', type='negative')
                                        return

                                #print(project_data)

                                project = api.research_project_repo.create(**project_data)
                                api.commit()

                                global all_projects_df
                                all_projects_df = pd.concat([all_projects_df, pd.DataFrame([project_data])],
                                                            ignore_index=True)

                                add_project_dialog.close()
                                ui.notify('Project added successfully', type='positive')

                                tbl_view_projects.rows[:] = all_projects_df.to_dict('records')
                                tbl_view_projects.update()

                                next_project_id = get_next_project_id(all_projects_df)
                                new_project_inputs['project_id'].value = int(next_project_id)
                                new_project_inputs['project_id'].update()

                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=add_project_dialog.close)
                                ui.button('Save', on_click=save_project)
                    with ui.dialog() as edit_project_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Edit Project').classes('text-lg font-bold')

                            edit_project_inputs = {}
                            selected_project_id = {'value': None}  # Store selected ID


                            # project ID selector
                            def validate_and_load_project():
                                project_id_value = edit_project_inputs['project_id_selector'].value

                                if not project_id_value or not project_id_value.strip():
                                    ui.notify('Please enter a project ID', type='negative')
                                    return

                                # Check if project exists
                                try:
                                    project_id_int = int(project_id_value)
                                except ValueError:
                                    ui.notify('Project ID must be a number', type='negative')
                                    return

                                if project_id_int not in all_projects_df['project_id'].values:
                                    ui.notify(f'project ID {project_id_int} does not exist', type='negative')
                                    return

                                # Load project data
                                selected_project_id['value'] = project_id_int
                                project_row = all_projects_df[all_projects_df['project_id'] == project_id_int].iloc[0]

                                # Populate input fields
                                for col in all_projects_df.columns:
                                    if col != 'project_id':
                                        edit_project_inputs[col].value = str(project_row[col])

                                ui.notify(f'Loaded project {project_id_int}', type='positive')


                            # project ID input with dropdown
                            with ui.row().classes('w-full items-end gap-2'):
                                edit_project_inputs['project_id_selector'] = ui.select(
                                    label='Project ID',
                                    options=sorted(all_projects_df['project_id'].astype(str).tolist()),
                                    with_input=True
                                ).classes('flex-grow')
                                ui.button('Load', on_click=validate_and_load_project)

                            ui.separator()

                            # Create input fields for all other columns
                            for col in all_projects_df.columns:
                                if col != 'project_id':
                                    edit_project_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    ).props('readonly')  # Start as readonly until project is loaded


                            def enable_project_editing():
                                if selected_project_id['value'] is None:
                                    ui.notify('Please load a project first', type='negative')
                                    return

                                # Enable all fields for editing
                                for col in all_projects_df.columns:
                                    if col != 'project_id':
                                        edit_project_inputs[col].props(remove='readonly')


                            def save_edited_project():
                                if selected_project_id['value'] is None:
                                    ui.notify('Please load a project first', type='negative')
                                    return

                                # Get the updated values
                                updated_data = {col: inp.value for col, inp in edit_project_inputs.items() if
                                                col != 'project_id_selector'}

                                # Validate that no fields are blank
                                for col, value in updated_data.items():
                                    if col != 'project_id' and (not value or not str(value).strip()):
                                        ui.notify(f'{col.replace("_", " ").title()} cannot be blank', type='negative')
                                        return

                                # Update in API
                                project = api.research_project_repo.update(selected_project_id['value'], **updated_data)
                                api.commit()

                                # Update the dataframe
                                global all_projects_df
                                idx = \
                                    all_projects_df[
                                        all_projects_df['project_id'] == selected_project_id['value']].index[0]
                                for col, value in updated_data.items():
                                    all_projects_df.at[idx, col] = value

                                # Update the table
                                tbl_view_projects.rows = all_projects_df.to_dict('records')
                                tbl_view_projects.update()

                                edit_project_dialog.close()
                                ui.notify('Project updated successfully', type='positive')


                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=edit_project_dialog.close)
                                ui.button('Edit', on_click=enable_project_editing)
                                ui.button('Save', on_click=save_edited_project)
                    with ui.dialog() as delete_project_dialog:
                        with ui.card().classes('w-[400px]'):
                            ui.label('Delete Project').classes('text-lg font-bold')

                            delete_project_inputs = {}
                            delete_selected_project_id = {'value': None}


                            # project ID selector
                            def validate_and_load_project_for_delete():
                                delete_project_id_value = delete_project_inputs['project_id_selector'].value

                                if not delete_project_id_value or not delete_project_id_value.strip():
                                    ui.notify('Please enter a project ID', type='negative')
                                    return

                                # Check if project exists
                                try:
                                    delete_project_id_int = int(delete_project_id_value)
                                except ValueError:
                                    ui.notify('project ID must be a number', type='negative')
                                    return

                                if delete_project_id_int not in all_projects_df['project_id'].values:
                                    ui.notify(f'project ID {delete_project_id_int} does not exist', type='negative')
                                    return

                                # Load project data
                                delete_selected_project_id['value'] = delete_project_id_int
                                project_row = all_projects_df[all_projects_df['project_id'] == delete_project_id_int].iloc[
                                    0]

                                # Populate input fields
                                for col in all_projects_df.columns:
                                    if col != 'project_id':
                                        delete_project_inputs[col].value = str(project_row[col])

                                ui.notify(f'Loaded project {delete_project_id_int}', type='positive')


                            # project ID input with dropdown
                            with ui.row().classes('w-full items-end gap-2'):
                                delete_project_inputs['project_id_selector'] = ui.select(
                                    label='project ID',
                                    options=sorted(all_projects_df['project_id'].astype(str).tolist()),
                                    with_input=True
                                ).classes('flex-grow')
                                ui.button('Load', on_click=validate_and_load_project_for_delete)

                            ui.separator()

                            # Create input fields for all other columns (read-only)
                            for col in all_projects_df.columns:
                                if col != 'project_id':
                                    delete_project_inputs[col] = ui.input(
                                        label=col.replace('_', ' ').title()
                                    ).props('readonly')

                            ui.separator()

                            ui.label('Warning: This action cannot be undone!').classes('text-red-600 font-semibold')


                            def delete_project():
                                if delete_selected_project_id['value'] is None:
                                    ui.notify('Please load a project first', type='negative')
                                    return

                                # Delete from API
                                try:
                                    api.research_project_repo.delete(delete_selected_project_id['value'])
                                    api.commit()
                                except Exception as e:
                                    ui.notify(f'Error deleting project: {str(e)}', type='negative')
                                    return

                                # Delete from dataframe
                                global all_projects_df
                                all_projects_df = all_projects_df[
                                    all_projects_df['project_id'] != delete_selected_project_id['value']]
                                all_projects_df.reset_index(drop=True, inplace=True)

                                # Update the table
                                tbl_view_projects.rows = all_projects_df.to_dict('records')
                                tbl_view_projects.update()

                                # Reset dialog state
                                delete_selected_project_id['value'] = None
                                for col in all_projects_df.columns:
                                    if col != 'project_id':
                                        delete_project_inputs[col].value = ''
                                delete_project_inputs['project_id_selector'].value = None

                                delete_project_dialog.close()
                                ui.notify('project deleted successfully', type='positive')


                            with ui.row().classes('gap-2 mt-4'):
                                ui.button('Cancel', on_click=delete_project_dialog.close)
                                ui.button('Delete', on_click=delete_project, color='red')
                    with ui.row().classes('gap-4'):
                        ui.button('Add', on_click=lambda: add_project_dialog.open())
                        ui.button('Edit', on_click=lambda: edit_project_dialog.open())
                        ui.button('Delete', on_click=lambda: delete_project_dialog.open(), color='red')
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
