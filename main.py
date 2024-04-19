import tkinter as tk
from tkinter import ttk
from calendar_handler import CalendarHandler
from json_handler import JsonHandler
import locale


if __name__ == '__main__':

    locale.setlocale(locale.LC_ALL, locale.getlocale())

    a = CalendarHandler()
    a.loop()