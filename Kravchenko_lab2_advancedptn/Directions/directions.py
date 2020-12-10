from Database.database_class import DB
import tkinter as tk
from Utils.table import TableClass
from tkinter import messagebox


OPTION = {'family': 'open-sans', 'size': 12, 'weight': 'bold', 'width': 28}


class DirectionController(DB):
    def insert_direction(self, place_of_arrival, price_per_day, visa_price, transport_price ):
        sql = '''INSERT INTO directions
                (place_of_arrival, price_per_day, visa_price, transport_price)
                VALUES(?, ?, ?, ?)'''
        value = (place_of_arrival, price_per_day, visa_price, transport_price)
        self._execute_query(sql, value)

    def delete_direction(self, direction_id):
        sql = 'DELETE FROM directions WHERE id=?'
        value = (direction_id,)
        self._execute_query(sql, value)

    def update_direction(self, direction_id, place_of_arrival, price_per_day, visa_price, transport_price):
        sql = '''UPDATE directions
                    SET direction_id = ?,
                    place_of_arrival = ?, 
                    price_per_day = ?, 
                    visa_price = ?, 
                    transport_price = ?
                    WHERE id = ?'''
        value = (direction_id, place_of_arrival, price_per_day, visa_price, transport_price)
        self._execute_query(sql, value)

    def select_directions(self):
        sql = '''SELECT * FROM directions'''
        return self._execute_select_query(sql)

    def select_direction(self, direction_id):
        sql = 'SELECT * FROM directions WHERE id=?'
        value = (direction_id,)
        return self._execute_select_query(sql, value)


class DirectionApplication(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.direction_controller = DirectionController()
        self.directions = list()

        self.app = None

        label = tk.Label(self, text="DIRECTION PANEL", font=controller.title_font)
        label.grid(row=0, column=0, columnspan=4)

        self.table = TableClass(parent=self,
                                hidden_columns=('ID',),
                                headings=('Place of arrival', 'Price per day','Visa price', 'Transport price'),
                                grid={'row': 1, 'column': 0, 'columnspan': 4})
        self.update_table()

        add_button = tk.Button(self, text="Add Direction",
                               command=self.add_frame, width=OPTION['width'])
        add_button.grid(row=2, column=0)

        update_button = tk.Button(self, text="Update Direction",
                                  command=self.update_frame, width=OPTION['width'])
        update_button.grid(row=2, column=1)

        delete_button = tk.Button(self, text="Delete Direction",
                                  command=self.delete_frame, width=OPTION['width'])
        delete_button.grid(row=2, column=2)

        exit_button = tk.Button(self, text="Return",
                                command=lambda: controller.show_frame("StartPage"), width=OPTION['width'])
        exit_button.grid(row=2, column=3)

    def add_frame(self):
        if self.app:
            self.app.close_windows()
        add_window = tk.Toplevel(self.master)
        self.app = AddFrame(add_window, base_frame=self)

    def update_frame(self):
        if self.app:
            self.app.close_windows()
        try:
            row = self.table.get_selected_item()
            direction = self.find_direction(row)
            update_window = tk.Toplevel(self.master)
            self.app = UpdateFrame(update_window, direction = direction, base_frame=self)
        except IndexError:
            messagebox.showerror('Select someone', 'Select someone')

    def delete_frame(self):
        if self.app:
            self.app.close_windows()
        try:
            row = self.table.get_selected_item()
            direction = self.find_direction(row)
            delete_window = tk.Toplevel(self.master)
            self.app = DeleteFrame(delete_window, direction = direction, base_frame=self)
        except IndexError:
            messagebox.showerror('Select someone', 'Select someone')

    def find_direction(self, row):
        filter_direction = filter(lambda x: x[0] == row[0], self.directions)
        direction = next(filter_direction)
        return direction

    def update_table(self):
        self.directions = self.direction_controller.select_directions()
        rows = [direction for direction in self.directions]
        self.table.update_table(rows)


class FieldsFrame:
    def __init__(self, master, base_frame):
        self.master = master
        self.base_frame = base_frame
        self.controller = DirectionController()

        self._init_labels()
        self._init_entries()

        quit_button = tk.Button(self.master, text='Quit', width=25, command=self.close_windows)
        quit_button.grid(row=self.last_row, column=0)

    def _init_labels(self):
        row, column = 0, 0
        label_place_of_arrival = tk.Label(master=self.master, text='Place of arrival: ')
        label_place_of_arrival.grid(row=row, column=column)
        row += 1

        label_price_per_day = tk.Label(master=self.master, text='Price per day: ')
        label_price_per_day.grid(row=row, column=column)
        row += 1

        label_visa_price = tk.Label(master=self.master, text='Visa price: ')
        label_visa_price.grid(row=row, column=column)
        row += 1

        label_transport_price = tk.Label(master=self.master, text='Transport price: ')
        label_transport_price.grid(row=row, column=column)
        row += 1

    def _init_entries(self):
        row, column = 0, 1
        self.entry_place_of_arrival = tk.Entry(master=self.master)
        self.entry_place_of_arrival.grid(row=row, column=column)
        row += 1

        self.entry_price_per_day = tk.Entry(master=self.master)
        self.entry_price_per_day.grid(row=row, column=column)
        row += 1

        self.entry_visa_price = tk.Entry(master=self.master)
        self.entry_visa_price.grid(row=row, column=column)
        row += 1

        self.entry_transport_price = tk.Entry(master=self.master)
        self.entry_transport_price.grid(row=row, column=column)
        row += 1

        self.last_row = row

    def get_direction_data(self):
        while True:
            try:
                place_of_arrival = self.entry_place_of_arrival.get()

                price_per_day = self.entry_price_per_day.get()

                visa_price = int(self.entry_visa_price.get())

                transport_price = int(self.entry_transport_price.get())


            except ValueError:
                error_str = '\tplace of arrival - text\n' + \
                            '\tprice per day - integer\n' + \
                            '\tvisa price - integer\n' + \
                            '\ttransport price - integer'
                messagebox.showerror('Enter correct data', error_str)
                return

            return place_of_arrival, price_per_day, visa_price, transport_price

    def close_windows(self):
        self.master.destroy()


class AddFrame(FieldsFrame):
    def __init__(self, master, base_frame):
        super().__init__(master, base_frame)
        self.master = master
        self.frame = tk.Frame(self.master)

        self.frame.grid(row=0, column=0)

        save_button = tk.Button(self.master, text='Save', width=25, command=self.save)
        save_button.grid(row=self.last_row, column=1)

    def save(self):
        self.controller.insert_direction(*self.get_direction_data())
        self.base_frame.update_table()
        self.close_windows()


class UpdateFrame(FieldsFrame):
    def __init__(self, master, base_frame, direction):
        super().__init__(master, base_frame)
        self.master = master
        self.direction = direction
        self.frame = tk.Frame(self.master)

        self._init_initial_direction()

        self.frame.grid(row=0, column=0)
        update_button = tk.Button(self.master, text='Update', width=25, command=self.update)
        update_button.grid(row=self.last_row, column=1)

    def _init_initial_direction(self):
        self.entry_place_of_arrival.insert(0, self.direction[1])
        self.entry_price_per_day.insert(0, self.direction[4])
        self.entry_visa_price.insert(0, self.direction[2])
        self.entry_transport_price.insert(0, self.direction[3])

    def update(self):
        direction = self.get_direction_data()
        self.controller.update_direction(*direction, self.direction[0])
        self.base_frame.update_table()
        self.close_windows()


class DeleteFrame(FieldsFrame):
    def __init__(self, master, base_frame, direction):
        super().__init__(master, base_frame)
        self.master = master
        self.direction = direction
        self.frame = tk.Frame(self.master)

        self._init_initial_direction()

        self.frame.grid(row=0, column=0)
        delete_button = tk.Button(self.master, text='Delete', width=25, command=self.delete)
        delete_button.grid(row=self.last_row, column=1)

    def _init_initial_direction(self):
        self.entry_place_of_arrival.insert(0, self.direction[1])
        self.entry_price_per_day.insert(0, self.direction[4])
        self.entry_visa_price.insert(0, self.direction[2])
        self.entry_transport_price.insert(0, self.direction[3])

        self.entry_place_of_arrival.config(state=tk.DISABLED)
        self.entry_price_per_day.config(state=tk.DISABLED)
        self.entry_visa_price.config(state=tk.DISABLED)
        self.entry_transport_price.config(state=tk.DISABLED)

    def delete(self):
        self.controller.delete_direction(self.direction[0])
        self.base_frame.update_table()
        self.close_windows()