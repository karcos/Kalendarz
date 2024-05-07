import json
import os
from tkinter import messagebox


class JsonHandler:
    def __init__(self, json_path: str, editing: bool = True) -> None:
        if not os.path.isfile(json_path):
            messagebox.showerror("Cannot find file!", f"No such file {json_path}")
            exit(-1)

        self.__json_file_path: str = json_path

        with open(json_path, 'r') as json_file:
            self.__json_data: dict = json.load(json_file)

        self.__editing: bool = editing

    def addNewRecord(self, record: dict) -> bool:
        if not self.__editing:
            return False

        for key in record:
            if key in self.__json_data:
                return False

        self.__json_data.update(record)
        self.__updateFile()

        return True

    def getElement(self, *args) -> dict | str | list | int | bool:
        actual = self.__json_data
        for arg in args:
            if arg in actual:
                actual = actual[arg]
            else:
                messagebox.showerror("Cannot find element!", f"Cannot find \"{arg}\"")
                exit(-1)

        return actual

    def __updateFile(self) -> None:
        if not os.path.isfile(self.__json_file_path):
            messagebox.showerror("Cannot find file!", f"No such file {self.__json_file_path}")
            exit(-1)

        with open(self.__json_file_path, 'w') as json_file:
            json.dump(self.__json_data, json_file, ensure_ascii=True, indent=4)

    @property
    def data(self) -> dict:
        return self.__json_data
