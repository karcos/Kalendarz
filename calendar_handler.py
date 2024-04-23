import tkinter as tk
from tkinter import ttk
from events_handler import EventsHandler
from json_handler import JsonHandler
from styles import Styles

import datetime
from dateutil.relativedelta import relativedelta

import calendar


class CalendarHandler:
    def __init__(self) -> None:
        self.__w_constants = JsonHandler("const/window.json", False)
        self.__c_constants = JsonHandler("const/calendar.json", False)

        self.__main_window: tk.Tk = tk.Tk()
        self.__styles = Styles(self.__main_window)
        width: bool
        height: bool
        width, height = self.__w_constants.getElement("resize")
        self.__main_window.resizable(width, height)
        self.__main_window.title(self.__w_constants.getElement("title"))
        self.__main_window.geometry(self.__w_constants.getElement("size"))
        self.__main_window.configure(bg=self.__w_constants.getElement("bg_color"))
        self.__main_window.update()

        self.__today_day: datetime = datetime.date.today()
        self.__actual_day: datetime = self.__today_day

        self.__events_handler: EventsHandler = EventsHandler()

        self.__generateMonth()

    def __generateMonth(self):
        self.__clear()
        self.__placeCalendarHeader()
        self.__placeDaysNames()
        self.__placeCalendarMain()

    def __placeCalendarMain(self):
        labels_days_consts = self.__c_constants.getElement("labels_days")
        buttons_days_consts = self.__c_constants.getElement("button_day")

        list_of_month_days: list[list[tuple[int, str]]] = self.__prepareListOfMonthDays()

        for y, week in enumerate(list_of_month_days):
            for x, day in enumerate(week):
                button_day: ttk.Button = ttk.Button(self.__main_window,
                                                    text=f"{day[0]}",
                                                    style=self.__c_constants.getElement("button_day", "style", "name"),
                                                    command=None)
                button_day.place(x=labels_days_consts["x"] + (x * labels_days_consts["style"]["width"]),
                                 y=buttons_days_consts["y"] + (y * labels_days_consts["style"]["height"]))

    def __prepareListOfMonthDays(self) -> list[list[tuple[int, str]]]:
        actual_month_first_day: int
        actual_month_num_of_days: int
        actual_month_first_day, actual_month_num_of_days = calendar.monthrange(self.__actual_day.year,
                                                                               self.__actual_day.month)

        previous_month: datetime = self.__actual_day - relativedelta(months=1)
        previous_month_num_of_days: int = calendar.monthrange(previous_month.year, previous_month.month)[1]

        prepare_month_day_list: list[list[tuple[int, str]]] = [[]]

        for i in range(previous_month_num_of_days - actual_month_first_day + 1, previous_month_num_of_days + 1):
            prepare_month_day_list[0].append((i, "before"))

        for i in range(1, actual_month_num_of_days + 1):
            prepare_month_day_list[-1].append((i, "main"))
            if len(prepare_month_day_list[-1]) == 7:
                prepare_month_day_list.append([])

        i: int = 1
        while len(prepare_month_day_list[-1]) < 7:
            prepare_month_day_list[-1].append((i, "after"))
            i += 1

        return prepare_month_day_list

    def __placeDaysNames(self):
        labels_days_names_consts = self.__c_constants.getElement("labels_days")

        for i, day_name in enumerate(calendar.day_abbr):
            foreground_color: str = ""
            if i == 5:
                foreground_color = labels_days_names_consts["saturday_foreground"]
            elif i == 6:
                foreground_color = labels_days_names_consts["sunday_foreground"]

            day_label = ttk.Label(self.__main_window,
                                  text=day_name,
                                  background=self.__main_window["bg"],
                                  style=self.__c_constants.getElement("labels_days", "style", "name"),
                                  foreground=foreground_color)
            day_label.place(x=labels_days_names_consts["x"] + (i * labels_days_names_consts["style"]["width"]),
                            y=labels_days_names_consts["y"])

    def __placeCalendarHeader(self):
        today_button = ttk.Button(self.__main_window,
                                  command=self.__setToday,
                                  text="Today",
                                  style=self.__c_constants.getElement("button_today", "style", "name"))
        today_button.place(x=(self.__main_window.winfo_width() - today_button.winfo_reqwidth()) / 2,
                           y=self.__c_constants.getElement("button_today", "y"))

        button_left = ttk.Button(self.__main_window,
                                 command=self.__nextMonth,
                                 text='\u2190',
                                 style=self.__c_constants.getElement("arrow_month_left", "style", "name"))
        button_left.place(x=self.__c_constants.getElement("arrow_month_left", "x"),
                          y=self.__c_constants.getElement("arrow_month_left", "y"))

        button_right = ttk.Button(self.__main_window,
                                  command=self.__prevMonth,
                                  text='\u2192',
                                  style=self.__c_constants.getElement("arrow_month_left", "style", "name"))
        button_right.place(x=self.__c_constants.getElement("arrow_month_right", "x"),
                           y=self.__c_constants.getElement("arrow_month_right", "y"))

        month_label = ttk.Label(self.__main_window,
                                text=f"{calendar.month_name[self.__actual_day.month].capitalize()}",
                                background=self.__main_window["bg"],
                                style=self.__c_constants.getElement("label_month", "style", "name"))
        month_label.place(x=(self.__main_window.winfo_width() - month_label.winfo_reqwidth()) / 2,
                          y=self.__c_constants.getElement("label_month", "y"))

        year_label = ttk.Label(self.__main_window,
                               text=f"{self.__actual_day.year}",
                               background=self.__main_window["bg"],
                               style=self.__c_constants.getElement("label_year", "style", "name"))
        year_label.place(x=(self.__main_window.winfo_width() - year_label.winfo_reqwidth()) / 2,
                         y=self.__c_constants.getElement("label_year", "y"))

    def __nextMonth(self):
        self.__actual_day -= relativedelta(months=1)
        self.__generateMonth()

    def __prevMonth(self):
        self.__actual_day += relativedelta(months=1)
        self.__generateMonth()

    def __setToday(self):
        self.__today_day = datetime.date.today()
        self.__actual_day = self.__today_day
        self.__generateMonth()

    def __clear(self):
        for widget in self.__main_window.winfo_children():
            widget.destroy()

    @property
    def todayDayNumber(self) -> int:
        return self.__today_day.day

    @property
    def todayMonthNumber(self) -> int:
        return self.__today_day.month

    @property
    def todayYearNumber(self) -> int:
        return self.__today_day.year

    def loop(self) -> None:
        self.__main_window.mainloop()
