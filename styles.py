from tkinter import ttk
import tkinter as tk
from json_handler import JsonHandler


class Styles:
    def __init__(self, master: tk.Tk):
        json_data: JsonHandler = JsonHandler("const/calendar.json")
        self.style: ttk.Style = ttk.Style(master)

        style_data: dict = json_data.getElement("button_today", "style")
        self.style.configure(style_data.pop("name", None), **style_data)

        style_data = json_data.getElement("arrow_month_left", "style")
        self.style.configure(style_data.pop("name", None), **style_data)

        style_data = json_data.getElement("arrow_month_right", "style")
        self.style.configure(style_data.pop("name", None), **style_data)

        style_data = json_data.getElement("label_month", "style")
        self.style.configure(style_data.pop("name", None), **style_data)

        style_data = json_data.getElement("label_year", "style")
        self.style.configure(style_data.pop("name", None), **style_data)

        style_data = json_data.getElement("labels_days", "style")
        self.style.configure(style_data.pop("name", None), **style_data)

        style_data = json_data.getElement("button_day", "style")
        self.style.configure(style_data.pop("name", None), **style_data)
