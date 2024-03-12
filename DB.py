from typing import Tuple
from Task import Task, BaseClass
from Note import Note
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime


class DB:
    """Access to database."""

    def __init__(self):
        self._db_name = "tasks.db"
        self._db_path = f"sqlite:///{self._db_name}"
        self._engine = create_engine(
        self._db_path, echo=False, connect_args={'check_same_thread': False}
        )
        self._session = sessionmaker(bind=self._engine)()
        metadata = BaseClass.metadata
        metadata.create_all(self._engine)


    def get_one_day_tasks(self, date_filter: date, state_filter: bool) -> Tuple[Task, ...]:
        """Returns tuple of tasks from given day."""
        date_filtered_query = self._session.query(Task).filter(Task.scheduled_date == date_filter).order_by(desc(Task.id))
        if state_filter is not None:
            state_filtered_query = date_filtered_query.filter(
                Task.done == state_filter)
            print(state_filtered_query.all())
            return state_filtered_query.all()
        return date_filtered_query.all()
        # except InvalidRequestError:
        #     sleep(0.1)

    def get_several_days_tasks(self, date_filter: list, state_filter: bool) -> Tuple[Task, ...]:
        """Returns tuple of tasks from given day."""
        date_filtered_query = self._session.query(Task).filter(Task.scheduled_date >= date_filter[0]).filter(Task.scheduled_date <= date_filter[1]).order_by(Task.scheduled_date)
        if state_filter is not None:
            state_filtered_query = date_filtered_query.filter(
                Task.done == state_filter)
            print(state_filtered_query.all())
            return state_filtered_query.all()
        return date_filtered_query.all()

    def get_all_dates(self):
        scheduled_dates = []
        query = self._session.query(Task).all()
        for task in query:
            scheduled_dates.append(task.scheduled_date)
        return scheduled_dates

    def save_task(self, task: Task):
        """Saves task in database."""
        self._session.add(task)
        self._session.commit()

    def delete_task(self, task: Task):
        """Deletes task from database."""
        self._session.delete(task)
        self._session.commit()


    def save_note(self, note: Note):
        """Saves task in database."""
        self._session.add(note)
        self._session.commit()

    def get_notes(self):
        notes_query = self._session.query(Note).order_by(desc(Note.id))
        return notes_query.all()