
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
all_lecturer_df = pd.DataFrame([lecturer.as_dict for lecturer in lecturers])

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
                    inputs1 = {} #Edit Dialogue would go here
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
                        for col in all_lecturer_df.columns
                    ]

                    rows = all_lecturer_df.to_dict(orient='records')

                    tbl_view_lecturers = ui.table(
                        columns=columns,
                        rows=rows,
                        row_key='lecturer_id',
                    ).classes('w-full border border-black text-black bg-white')
                with ui.tab_panel(tab_lecturers_manage).classes('w-full'):
                    inputs4 = {}
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
