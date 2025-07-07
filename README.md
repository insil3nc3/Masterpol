Masterpol CRUD App
Overview

Masterpol is a fictional company that specializes in transferring other companies' products into its own system. These other companies are referred to as partners.
To facilitate efficient accounting and management of both partners and product supplies, the Masterpol application was developed.

This project serves as a practical exercise in building a Python application with full offline support, using tools such as SQLite, SQLAlchemy, and PyQt6.
Features

    ORM-based database with SQLAlchemy and SQLite

    Full CRUD functionality for managing partner data

    PyQt6 GUI with multiple windows:

        Main Window: Displays an interactive table of all partners

        Add Partner Window: Allows adding new partners

        Edit Partner Window: Accessible by double-clicking a partner in the list; allows editing partner information

        Product History Window: View and manage the history of products associated with each partner

Project Structure

    database/ – Contains the database initialization script and SQLAlchemy models

    Backend/ – Implements CRUD operations and business logic

    Frontend/ – Contains the main PyQt6 interface code

    database/excel_to_table.py – Script to import existing data from Excel into the database

    Frontend/main.py – Entry point to launch the application

Getting Started
1. Install Dependencies

Before running the application, make sure you have the required Python packages installed:

pip install sqlalchemy pyqt6

2. Initialize the Database

Run the following script to create the database and tables:

python database/models.py

3. (Optional) Import Existing Data

If you have existing data in Excel format, you can import it into the application by running:

python excel_to_table.py

4. Run the Application

Start the GUI application using:

python Frontend/main.py

Purpose

This project was developed as a training exercise to build a full-fledged desktop application without the use of internet resources. It demonstrates core principles of:

    GUI development with PyQt6

    Database management using SQLAlchemy ORM

    Working with Excel data

    Structuring and organizing medium-scale Python applications
