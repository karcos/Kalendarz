import calendar

from json_handler import JsonHandler
import datetime
from datetime import datetime


class EventsHandler:
    def __init__(self) -> None:
        self.__events_data_handler: JsonHandler = JsonHandler("events_data/tutoring.json")

    def addEvent(self, stud_data: dict) -> bool:
        raise NotImplementedError

    def getEventsByDay(self, date: datetime) -> list[tuple[str, str]]:
        events: list[tuple[str, str]] = []

        return events
