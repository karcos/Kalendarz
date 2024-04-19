from tkinter import ttk
import tkinter as tk
from json_handler import JsonHandler


class Styles:
    def __init__(self, master: tk.Tk):
        json_data: JsonHandler = JsonHandler("const/calendar.json")
        self.style: ttk.Style = ttk.Style(master)

        style_data: dict = json_data.getElement("header", "button_today", "style")
        self.style.configure(style_data.pop("name", None), **style_data)

        style_data = json_data.getElement("header", "arrow_month_left", "style")
        self.style.configure(style_data.pop("name", None), **style_data)

        style_data = json_data.getElement("header", "arrow_month_right", "style")
        self.style.configure(style_data.pop("name", None), **style_data)
