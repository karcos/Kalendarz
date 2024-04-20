from json_handler import JsonHandler


class EventsHandler:
    def __init__(self) -> None:
        self.__events_data_handler: JsonHandler = JsonHandler("events_data/tutoring.json")

    def addStudent(self, stud_data: dict) -> bool:
        raise NotImplementedError




    