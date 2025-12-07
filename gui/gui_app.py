
from nicegui import ui

ui.add_head_html('''
    <style>
        .my-red-button {
            color: Crimson;
            font-weight: bold;
        }
    </style>
''')

ui.add_css('''
    @layer utilities {
       .standard-btn {
           background-color: black !important; height: 50% !important; width: 500px !important;
        }
    }
''')

def student_menu():
    ui.notify("Student")

def lecturer_menu():
    ui.notify("Lecturer")

def nas_menu():
    ui.notify("NAS")

def course_menu():
    ui.notify("Course")

def department_menu():
    ui.notify("Department")

def rp_menu():
    ui.notify("RP")

def qr_menu():
    ui.notify("Q&R")

#with ui.row().classes('w-full justify-center items-center min-h-screen'):
#    with ui.column().classes('items-center gap-4'):
#        with ui.column().classes('w-full items-center gap-4'):
#            ui.label('Record Management Service').classes('text-2xl font-bold')
#            ui.label('Welcome to your institutional records management service').classes('text-2xl font-bold')

#        ui.button("Students", on_click=student_menu()).classes('standard-btn')
#        ui.button("Lecturers", on_click=lecturer_menu()).classes('standard-btn')
#        ui.button("Non-Academic Staff", on_click=nas_menu()).classes('standard-btn')
#        ui.button("Courses", on_click=course_menu()).classes('standard-btn')
#        ui.button("Departments", on_click=department_menu()).classes('standard-btn')
#        ui.button("Research Projects", on_click=rp_menu()).classes('standard-btn')
#        ui.button("Queries and Reports", on_click=qr_menu()).classes('standard-btn')

with ui.column().classes('w-full'):
    with ui.tabs().classes('w-full') as main_tabs:
        tab_students = ui.tab('Students')
        tab_lecturers = ui.tab('Lecturers')
        tab_nas = ui.tab('Non-Academic Staff')
        tab_courses = ui.tab('Courses')
        tab_departments = ui.tab('Departments')
        tab_research_projects = ui.tab('Research Projects')
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
                    inputs = {}
                with ui.tab_panel(tab_students_view).classes('w-full'):
                    inputs1 = {}
    with ui.tab_panels(main_tabs, value = tab_lecturers).classes('w-full'):
        with ui.tab_panel(tab_lecturers):
            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Lecturer Records').classes('text-xl')
            with ui.tabs().classes('w-full') as lecturer_ops:
                tab_lecturers_view = ui.tab('View Lecturer Records')
                tab_lecturers_manage = ui.tab('Manage Lecturer Records')
            with ui.tab_panels(lecturer_ops).classes('w-full'):
                with ui.tab_panel(tab_lecturers_view).classes('w-full'):
                    inputs3 = {}
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
                    inputs5 = {}
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
                    inputs7 = {}
                with ui.tab_panel(tab_courses_manage).classes('w-full'):
                    inputs8 = {}
    with ui.tab_panels(main_tabs, value = tab_research_projects).classes('w-full'):
        with ui.tab_panel(tab_departments):
            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Departmental Records').classes('text-xl')
            with ui.tabs().classes('w-full') as department_ops:
                tab_departments_view = ui.tab('View Departmental Records')
                tab_departments_manage = ui.tab('Manage Departmental Records')
            with ui.tab_panels(department_ops).classes('w-full'):
                with ui.tab_panel(tab_departments_view).classes('w-full'):
                    inputs9 = {}
                with ui.tab_panel(tab_departments_manage).classes('w-full'):
                    inputs10 = {}
    with ui.tab_panels(main_tabs, value = tab_research_projects).classes('w-full'):
        with ui.tab_panel(tab_research_projects):
            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Research Projects Records').classes('text-xl')
            with ui.tabs().classes('w-full') as rp_ops:
                tab_research_projects_view = ui.tab('View Research Projects Records')
                tab_research_projects_manage = ui.tab('Manage Research Projects Records')
            with ui.tab_panels(rp_ops).classes('w-full'):
                with ui.tab_panel(tab_research_projects_view).classes('w-full'):
                    inputs11 = {}
                with ui.tab_panel(tab_research_projects_manage).classes('w-full'):
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
