# PyCal Task Manager App

PyCal is a simple, yet powerful desktop application with a beautiful UI that helps you manage your daily tasks and make notes.

## Features

* Easily add, edit, and delete tasks.
* Schedule tasks with a calendar interface.
* Preview the week ahead with convenient lists of upcoming events.
* Keep track of done and active tasks.
* Add notifications to important to-dos.
* Make and edit notes with a single click.
* Save tasks and notes in a database.

## Usage

1. Clone the repository or download the source code.
2. Make sure you have Python 3.11 installed on your system.
3. Activate your virtual environment.
4. Run pip install -r requirements.txt to install all dependencies.
5. Run main.py to start the application.

## Design
The GUI design is created using [Qt Designer](https://doc.qt.io/qt-5/qtdesigner-manual.html) and [PyQtDarkTheme Stylesheet](https://pypi.org/project/pyqtdarktheme/), providing an intuitive and visually appealing user interface.

## Technologies Used

- **PyQt6**: The main Python library for creating desktop applications with Qt.
- **SQLite**: Used for storing and retrieving tasks and notes in a lightweight local database.

## Application Structure

* **MainWindow.py** and **MainWindow.ui**: Contain logic and GUI of the main window of the application, which includes the sidebar with navigation buttons and StackedWidget as a placeholder for pages.
* **HomePage.py** and **HomePage.ui**: Contain logic and GUI of the home page, which includes a custom calendar widget (**CustomCalendarWidget.py**) and a task list (**TasksWidget.py** and **TasksWidget.ui**) for the selected day.
* **TaskListsPage.py** and **TaskListsPage.ui**: Contain logic and GUI of the task lists page, which includes task lists (**TasksWidget.py** and **TasksWidget.ui**) for today, tomorrow and next seven days. Changes in one list reflect in the others.
* **NotesWidget.py** and **NotesWidget.ui**: Contain logic and GUI of the notes page, which includes notes from the database and interface for changing them and creating new ones.
* **Task.py** and **Note.py**:Contain classes for saving entities in the database.
* **DB.py**: Sets connection between Python program and SQLite database with the use of SQLAlchemy library.
* **TasksFormTemplate.py** and based on it **TaskCreationWidget.py**, **TasksEditionWidget.py**, **TasksViewingWidget.py**: Serve task creation, edition and viewing processes.
* **style.qss**: Applies a custom stylesheet to some GUI elements.
* **resource.qrc** and **resource_rc.py**: Help insert icons saved in icon directory into the interface.

## Screenshots

Home page:

![Home page](screenshots/main_page.png?raw=true "Tasks Tab")

New task dialog window:

![Add New Task Dialog](screenshots/task_creation_dialog.png?raw=true "Add New Task")

Page with task lists:

![Task lists page](screenshots/task_lists_page.png?raw=true "Tasks Tab")

Page with notes:

![Notes page](screenshots/notes_page.png?raw=true "Notes Tab")
