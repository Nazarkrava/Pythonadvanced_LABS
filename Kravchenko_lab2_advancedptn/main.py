import tkinter as tk
from tkinter import font

from Trips.Trips import TripApplication
from Directions.directions import DirectionApplication
from Clients.Clients import ClientApplication
from Fileworker.fileworker import Fileworker

OPTION = {'family': 'sans-serif', 'size': 12, 'weight': 'bold', 'width': 60}


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.root = tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = font.Font(family=OPTION['family'], size=OPTION['size'] * 2, weight=OPTION['weight'])

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=OPTION['size'])

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, TripApplication, DirectionApplication, ClientApplication):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        try:
            frame.update_table()
            frame.tkraise()
        except AttributeError:
            frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="WELCOME TO TOURIST AGENCY APPLICATION ", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="TRIPS",
                            command=lambda: controller.show_frame("TripApplication"),
                            width=OPTION['width'])
        button2 = tk.Button(self, text="DIRECTIONS",
                            command=lambda: controller.show_frame("DirectionApplication"),
                            width=OPTION['width'])
        button3 = tk.Button(self, text="CLIENTS",
                            command=lambda: controller.show_frame("ClientApplication"),
                            width=OPTION['width'])
        button4 = tk.Button(self, text="SAVE DB RECORDS TO DOC/XLSX FILE",
                            command=Fileworker().save_to_files,
                            width=OPTION['width'])
        button1.pack()
        button2.pack()
        button3.pack()
        button4.pack()

        quit_button = tk.Button(self, text='EXIT', command=quit, width=OPTION['width'])
        quit_button.pack()


if __name__ == '__main__':
    app = Application()
    app.mainloop()
