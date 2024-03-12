from datetime import datetime, time, date
from sqlalchemy import Column, Integer, String, Date, Time, Boolean
from sqlalchemy.orm import declarative_base

BaseClass = declarative_base()


class Task(BaseClass):
    """Model of a task saved in database."""
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)

    summary = Column(String)
    description = Column(String)
    scheduled_date: Column[date] = Column(Date)
    notification_time = Column(Time, nullable=True)
    done = Column(Boolean)

    def __init__(
            self, summary: str, description: str, datetime: datetime,
            # with_notification,
            notification_time: time, done: int
    ):
        self.summary = summary
        self.description = description
        self.scheduled_date = datetime
        self.notification_time = notification_time
        self.done = done

    def __str__(self):
        string = f"{self.summary} scheduled at {self.scheduled_date}"
        if self.notification_time:
            return f"{string}, with notification at {self.notification_time}"
        return string

    def __repr__(self):
        return f"Task({self.summary}, {self.description}, {self.scheduled_date}, {self.notification_time})"
