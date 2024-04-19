import tkinter as tk
from tkinter import ttk
from events_handler import EventsHandler
from json_handler import JsonHandler

import datetime
from dateutil.relativedelta import relativedelta

import calendar


class CalendarHandler:
    def __init__(self) -> None:
        self.__w_constants = JsonHandler("const/window.json", False)
        self.__c_constants = JsonHandler("const/calendar.json", False)

        self.__main_window: tk.Tk = tk.Tk()
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
        actual_month_first_day: int
        actual_month_num_of_days: int
        actual_month_first_day, actual_month_num_of_days = calendar.monthrange(self.__actual_day.year, self.__actual_day.month)

        previous_month: datetime = self.__actual_day - relativedelta(months=1)
        previous_month_num_of_days: int = calendar.monthrange(previous_month.year, previous_month.month)[1]

        labels_days_consts = self.__c_constants.getElement("calendar_main", "labels_days")
        box_day_consts = self.__c_constants.getElement("calendar_main", "box_day")

        k: int = 0
        for i in range(previous_month_num_of_days - actual_month_first_day + 1, previous_month_num_of_days + 1):
            button_day: ttk.Button = ttk.Button(self.__main_window,
                                                text=f"{i}",
                                                padding=(0, box_day_consts["height"]),
                                                width=box_day_consts["width"],
                                                command=None)
            button_day.place(x=labels_days_consts["x"] + (k * labels_days_consts["width"]),
                             y=box_day_consts["y"])
            k += 1

    def __placeDaysNames(self):
        labels_days_names_consts = self.__c_constants.getElement("calendar_main", "labels_days")
        box_day_consts = self.__c_constants.getElement("calendar_main", "box_day")

        for i, day_name in enumerate(calendar.day_abbr):
            if i == 5:
                foreground_color: str = labels_days_names_consts["saturday_color"]
            elif i == 6:
                foreground_color: str = labels_days_names_consts["sunday_color"]
            else:
                foreground_color: str = "black"

            day_label = ttk.Label(self.__main_window,
                                  text=day_name,
                                  font=labels_days_names_consts["font"],
                                  background=self.__main_window["bg"],
                                  foreground=foreground_color,
                                  justify=tk.CENTER)
            day_label.place(x=labels_days_names_consts["x"] + (i * labels_days_names_consts["width"]),
                            y=labels_days_names_consts["y"])

    def __placeCalendarHeader(self):
        today_button = ttk.Button(self.__main_window,
                                  command=self.__setToday,
                                  text="Today")
        today_button.place(x=(self.__main_window.winfo_width() - today_button.winfo_reqwidth()) / 2,
                           y=self.__c_constants.getElement("header", "button_today", "y"))

        button_left = ttk.Button(self.__main_window,
                                 command=self.__nextMonth,
                                 text='left',
                                 padding=(0, self.__c_constants.getElement("header", "arrow_month_left", "height")))
        button_left.place(x=self.__c_constants.getElement("header", "arrow_month_left", "x"),
                          y=self.__c_constants.getElement("header", "arrow_month_left", "y"))

        button_right = ttk.Button(self.__main_window,
                                  command=self.__prevMonth,
                                  text='right',
                                  padding=(0, self.__c_constants.getElement("header", "arrow_month_right", "height")))
        button_right.place(x=self.__c_constants.getElement("header", "arrow_month_right", "x"),
                           y=self.__c_constants.getElement("header", "arrow_month_right", "y"))

        month_label = ttk.Label(self.__main_window,
                                text=f"{calendar.month_name[self.__actual_day.month].capitalize()}",
                                font=self.__c_constants.getElement("header", "label_month", "font"),
                                background=self.__main_window["bg"])
        month_label.place(x=(self.__main_window.winfo_width() - month_label.winfo_reqwidth()) / 2,
                          y=self.__c_constants.getElement("header", "label_month", "y"))

        year_label = ttk.Label(self.__main_window,
                               text=f"{self.__actual_day.year}",
                               font=self.__c_constants.getElement("header", "label_year", "font"),
                               background=self.__main_window["bg"])
        year_label.place(x=(self.__main_window.winfo_width() - year_label.winfo_reqwidth()) / 2,
                         y=self.__c_constants.getElement("header", "label_year", "y"))

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
