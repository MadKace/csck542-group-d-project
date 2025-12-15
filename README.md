# University Record Management System

Group Project Repository for **CSCK542 – Database and Information Systems**  
Due: **15 December 2025**

## 1. Overview

This project implements a **University Record Management System** that connects a relational database to a Python interface. The application allows users to run a set of predefined queries through a simple GUI.

The system allows users to **view, create, update, and query** university data including students, staff, courses, departments, programmes, research projects, and publications.

The solution consists of:
- A normalised relational database schema
- A Python backend using SQLAlchemy
- A GUI built with NiceGUI
- Pre-populated sample data
- Supporting documentation and video walkthrough

## 2. Project Structure
```text
database/
  schema.sql         # Database schema definition
  seed_data.sql      # Script used to populate the database
  university.db      # Local unencrypted database (generated)
  university.db.enc  # Encrypted database (generated / used by app)

docs/
  meeting_minutes/   # Project meeting records
  API_REFERENCE.md   # API documentation

gui/
  gui_app.py         # Main GUI application

scripts/
  generate_seed_data.py
  init_db.py

src/
  database/          # Engine and connection setup
  models/            # ORM models
  repositories/      # Data access layer
  services/          # Service / API layer
  exceptions.py

video/               # Video report

main.py
requirements.txt
README.md
.gitignore
```

## 3. Technologies Used

- Python 3.10+
- SQLite
- SQLAlchemy (ORM)
- NiceGUI (GUI framework)
- Pandas (data handling)
- AES-256 encryption (encryption at rest)
- GitHub (version control)

## 4. Team Members and Roles

- **Madiyah Khan** – Testing (UAT), Documentation, Project Coordination, Video Lead
- **Youna Kim** – Database Design and Schema
- **Jonathan Ross** – Layered Architecture Designer
- **Ismail Ghafoor** – GUI Design, Reporting Lead and Query Designer

## 5. How to Run the Project

1. Create and activate a virtual environment

**MacOS / Linux**

python -m venv venv

source venv/bin/activate

**Windows (CMD)**

python -m venv venv

venv\Scripts\activate

2. Install dependencies

pip install -r requirements.txt

3. Create a fresh database

Remove any existing DB files:

rm database/university.db

rm database/university.db.enc

Initialise a fresh database:

python scripts/init_db.py

Run the application and generate a new encryption key:

**MacOS / Linux**

DB_ENCRYPTION_KEY=your_new_key_here python main.py

**Windows (CMD)**

set DB_ENCRYPTION_KEY=your_new_key_here
python main.py

4. Run the GUI application
The database is encrypted using AES-256.
The required encryption key for this submission is:
csck542

**MacOS / Linux**

DB_ENCRYPTION_KEY=csck542 python main.py

**Windows (CMD)**

set DB_ENCRYPTION_KEY=csck542 && python main.py

The application will launch in a browser window using the encrypted SQLite database provided in the repository.
