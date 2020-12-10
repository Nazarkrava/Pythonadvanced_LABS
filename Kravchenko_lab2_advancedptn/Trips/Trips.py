from Database.database_class import DB
import tkinter as tk
from Utils.table import TableClass
from tkinter import messagebox

from Clients.Clients import ClientController
from Directions.directions import DirectionController

OPTION = {'family': 'verdana', 'size': 12, 'weight': 'bold', 'width': 28}


class TripController(DB):
    def insert_trip(self, day_quantity, full_price, purpose_of_time, way_to_trip, client_full_name):
        sql = '''INSERT INTO trips
                (day_quantity, full_price, purpose_of_time, way_to_trip, client_full_name)
                VALUES(?, ?, ?, ?, ?)'''
        value = (day_quantity, full_price, purpose_of_time, way_to_trip, client_full_name)
        self._execute_query(sql, value)

    def delete_trip(self, trip_id):
        sql = 'DELETE FROM trips WHERE id=?'
        value = (trip_id,)
        self._execute_query(sql, value)

    def update_trip(self, day_quantity, full_price, purpose_of_time, way_to_trip, client_full_name, trip_id):
        sql = '''UPDATE trips
                 SET day_quantity = ?,
                     full_price = ?,
                     purpose_of_time = ?,
                     way_to_trip = ?,
                     client_full_name = ?
                 WHERE id = ?'''
        value = (day_quantity, full_price, purpose_of_time, way_to_trip, client_full_name, trip_id)
        self._execute_query(sql, value)

    def select_trips(self):
        sql = '''SELECT * FROM trips'''
        return self._execute_select_query(sql)

    def select_trip(self, trip_id):
        sql = '''SELECT * FROM trips WHERE id=?'''
        value = (trip_id, )
        return self._execute_select_query(sql, value)


class TripApplication(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.client_controller = ClientController()
        self.direction_controller = DirectionController()
        self.trip_controller = TripController()
        self.trips = list()
        self.app = None

        label = tk.Label(self, text="TRIP PANEL", font=controller.title_font)
        label.grid(row=0, column=0, columnspan=5)

        self.table = TableClass(parent=self,
                                hidden_columns=('ID', 'ClientID', 'DirectionID'),
                                headings=('Client Full Name', 'Way To Trip', 'Full Price', 'Day Quantity', 'Purpose of Trip'),
                                grid={'row': 1, 'column': 0, 'columnspan': 4})
        self.update_table()

        add_button = tk.Button(self, text="Add Trip",
                               command=self.add_frame, width=OPTION['width'])
        add_button.grid(row=2, column=0)

        update_button = tk.Button(self, text="Update Trip",
                                  command=self.update_frame, width=OPTION['width'])
        update_button.grid(row=2, column=1)

        delete_button = tk.Button(self, text="Delete Trip",
                                  command=self.delete_frame, width=OPTION['width'])
        delete_button.grid(row=2, column=2)

        exit_button = tk.Button(self, text="Return",
                                command=lambda: controller.show_frame("StartPage"), width=OPTION['width'])
        exit_button.grid(row=2, column=3)

    def add_frame(self):
        if self.app:
            self.app.master.destroy()
        if len(self.client_controller.select_clients()) == 0 or len(self.direction_controller.select_directions()) == 0:
            messagebox.showerror('Empty set', 'Set of clients or directions types is empty')
        else:
            add_window = tk.Toplevel(self.master)
            self.app = AddFrame(add_window, base_frame=self)

    def update_frame(self):
        if self.app:
            self.app.master.destroy()
        try:
            row = self.table.get_selected_item()
            trip = self.find_trip(row)
            update_window = tk.Toplevel(self.master)
            self.app = UpdateFrame(update_window, trip=trip, base_frame=self)
        except IndexError as e:
            print(e)
            messagebox.showerror('Select someone', 'Select someone')
        except StopIteration:
            messagebox.showerror('Nothing to select', 'Nothing to select')

    def delete_frame(self):
        if self.app:
            self.app.master.destroy()
        try:
            row = self.table.get_selected_item()
            trip = self.find_trip(row)
            delete_window = tk.Toplevel(self.master)
            self.app = DeleteFrame(delete_window, trip=trip, base_frame=self)
        except IndexError as e:
            print(e)
            messagebox.showerror('Select someone', 'Select someone')
        except StopIteration:
            messagebox.showerror('Nothing to select', 'Nothing to select')

    def find_trip(self, row):
        trip = self.trip_controller.select_trip(row[0])[0]
        return trip

    def update_table(self):
        self.trips = self.trip_controller.select_trips()
        rows = self.trips
        for i, row in enumerate(rows):
            client = self.client_controller.select_client(row[-1])[0]
            string = [str(e) for e in client[1:]]
            client_str = ' '.join(string)
            direction = self.direction_controller.select_direction(row[-2])
            rows[i] = (row[0], row[-2], row[-1], client_str, direction[0][1], row[2], row[1], row[3])
        self.table.update_table(rows)


class FieldsFrame:
    def __init__(self, master, base_frame):
        self.master = master
        self.base_frame = base_frame
        self.controller = TripController()
        self.client_controller = ClientController()
        self.direction_controller = DirectionController()

        self._init_labels()
        self._init_entries()

        quit_button = tk.Button(self.master, text='Quit', width=25, command=self.close_windows)
        quit_button.grid(row=self.last_row, column=0)

    def _init_labels(self):
        row, column = 0, 0
        day_quantity = tk.Label(master=self.master, text='Day Quantity: ')
        day_quantity.grid(row=row, column=column)
        row += 1

        purpose_of_time = tk.Label(master=self.master, text='Purpose Of Trip: ')
        purpose_of_time.grid(row=row, column=column)
        row += 1

        full_price = tk.Label(master=self.master, text='Full Price: ')
        full_price.grid(row=row, column=column)
        row += 1

        client_full_name = tk.Label(master=self.master, text='Client Full Name: ')
        client_full_name.grid(row=row, column=column)
        row += 1

        way_to_trip = tk.Label(master=self.master, text='Way To Trip: ')
        way_to_trip.grid(row=row, column=column)
        row += 1

    def _init_entries(self):
        row, column = 0, 1
        self.entry_day_quantity = tk.Entry(master=self.master)
        self.entry_day_quantity.grid(row=row, column=column)
        row += 1

        self.entry_purpose_of_time = tk.Entry(master=self.master)
        self.entry_purpose_of_time.grid(row=row, column=column)
        row += 1

        self.entry_full_price = tk.Entry(master=self.master)
        self.entry_full_price.grid(row=row, column=column)
        row += 1

        self._init_client_drop_menu(row, column)
        row += 1

        self._init_direction_drop_menu(row, column)
        row += 1

        self.last_row = row

    def _init_direction_drop_menu(self, row, column):
        self.direction_var = tk.StringVar(self.master)
        self.direction_var.set('Select from the list')

        directions = self.direction_controller.select_directions()
        self.direction_choices = list()
        for n, v in enumerate(directions, start=1):
            self.direction_choices.append((n, v[1]))

        self.entry_way_to_trip = tk.OptionMenu(self.master, self.direction_var, *self.direction_choices)
        self.entry_way_to_trip.grid(row=row, column=column)
        self.entry_way_to_trip_value = None
        self.direction_var.trace('w', self.change_dropdown_direction)

    def change_dropdown_direction(self, *args):
        self.entry_way_to_trip_value = self.direction_var.get()
        print('direction', self.entry_way_to_trip_value)

    def _init_client_drop_menu(self, row, column):
        self.client_var = tk.StringVar(self.master)
        self.client_var.set('Select from the list')

        clients = self.client_controller.select_clients()
        self.client_choices = list()
        for n, c in enumerate(clients, start=1):
            string = [str(e) for e in c[1:]]
            client_str = ' '.join(string)
            self.client_choices.append((n, str(client_str)))

        self.entry_client_full_name = tk.OptionMenu(self.master, self.client_var, *self.client_choices)
        self.entry_client_full_name.grid(row=row, column=column)
        self.entry_client_full_name_value = None
        self.client_var.trace('w', self.change_dropdown_client)

    def change_dropdown_client(self, *args):
        self.entry_client_full_name_value = self.client_var.get()
        print('client', self.entry_client_full_name_value)

    def get_trip_data(self):
        while True:
            try:
                day_quantity = int(self.entry_day_quantity.get())
                if day_quantity <= 0:
                    raise ValueError

                purpose_of_time = self.entry_purpose_of_time.get()
                if purpose_of_time is None or len(purpose_of_time) == 0:
                    raise ValueError

                full_price = self.entry_full_price.get()

                number_way_to_trip = int(self.entry_way_to_trip_value[1:-1].split(',')[0])
                number_client_full_name = int(self.entry_client_full_name_value[1:-1].split(',')[0])

                way_to_trip = self.direction_controller.select_directions()[number_way_to_trip - 1][0]
                client_full_name = self.client_controller.select_clients()[number_client_full_name - 1][0]
            except (ValueError, TypeError):
                error_str = '\tday quantity - integer\n' + \
                            '\tpurpose of trip - text\n' + \
                            '\tfull price - integer\n' + \
                            '\tway_to_trip - selected direction\n' + \
                            '\tclient_full_name - selected client\n'
                messagebox.showerror('Enter correct data', error_str)
                return

            return day_quantity, full_price, purpose_of_time, way_to_trip, client_full_name

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
        self.controller.insert_trip(*self.get_trip_data())
        self.base_frame.update_table()
        self.close_windows()


class UpdateFrame(FieldsFrame):
    def __init__(self, master, base_frame, trip):
        super().__init__(master, base_frame)
        self.master = master
        self.trip = trip
        self.frame = tk.Frame(self.master)

        self._init_initial_trip()

        self.frame.grid(row=0, column=0)
        update_button = tk.Button(self.master, text='Update', width=25, command=self.update)
        update_button.grid(row=self.last_row, column=1)

    def _init_initial_trip(self):
        self.entry_day_quantity.insert(0, self.trip[1])
        self.entry_purpose_of_time.insert(0, self.trip[3])
        date = self.trip[2].split('-')
        date = '-'.join(date[::-1])
        self.entry_full_price.insert(0, date)

        self.client_var.set(self.client_choices[self.trip[-1] - 1])
        self.entry_client_full_name_value = self.client_var.get()

        self.direction_var.set(self.direction_choices[self.trip[-2] - 1])
        self.entry_way_to_trip_value = self.direction_var.get()

    def update(self):
        trip = self.get_trip_data()
        self.controller.update_trip(*trip, self.trip[0])
        self.base_frame.update_table()
        self.close_windows()


class DeleteFrame(FieldsFrame):
    def __init__(self, master, base_frame, trip):
        super().__init__(master, base_frame)
        self.master = master
        self.trip = trip
        self.frame = tk.Frame(self.master)

        self._init_initial_trip()

        self.frame.grid(row=0, column=0)
        delete_button = tk.Button(self.master, text='Delete', width=25, command=self.delete)
        delete_button.grid(row=self.last_row, column=1)

    def _init_initial_trip(self):
        self.entry_day_quantity.insert(0, self.trip[1])
        self.entry_purpose_of_time.insert(0, self.trip[3])
        date = self.trip[2].split('-')
        date = '-'.join(date[::-1])
        self.entry_full_price.insert(0, date)

        self.client_var.set(self.client_choices[self.trip[-1] - 1])
        self.entry_client_full_name_value = self.client_var.get()

        self.direction_var.set(self.direction_choices[self.trip[-2] - 1])
        self.entry_way_to_trip_value = self.direction_var.get()

        self.entry_day_quantity.config(state=tk.DISABLED)
        self.entry_purpose_of_time.config(state=tk.DISABLED)
        self.entry_full_price.config(state=tk.DISABLED)
        self.entry_client_full_name.config(state=tk.DISABLED)
        self.entry_way_to_trip.config(state=tk.DISABLED)

    def delete(self):
        self.controller.delete_trip(self.trip[0])
        self.base_frame.update_table()
        self.close_windows()
