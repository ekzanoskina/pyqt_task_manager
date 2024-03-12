from sqlalchemy import Column, Integer, String
from Task import BaseClass


class Note(BaseClass):
    """Model of a task saved in database."""
    __tablename__ = "note"
    id = Column(Integer, primary_key=True)
    summary = Column(String)

    def __init__(self, summary: str):
        self.summary = summary

    def __str__(self):
        string = f"{self.summary}"
        return string

    def __repr__(self):
        return f"Note({self.summary})"
