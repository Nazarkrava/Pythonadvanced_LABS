from Database.database_class import DB
import tkinter as tk
from Utils.table import TableClass
from tkinter import messagebox

OPTION = {'family': 'open-sans', 'size': 12, 'weight': 'bold', 'width': 28}


class ClientController(DB):
    def insert_client(self, client_full_name, foreign_passport_ID, local_passport_ID, phone_number,
                      personal_discount_percent):
        sql = '''INSERT INTO clients
                (client_full_name, foreign_passport_ID, local_passport_ID, phone_number,
                      personal_discount_percent)
                VALUES(?, ?, ?, ?, ?)'''
        value = (client_full_name, foreign_passport_ID, local_passport_ID, phone_number,
                      personal_discount_percent)
        self._execute_query(sql, value)

    def delete_client(self, client_id):
        sql = 'DELETE FROM clients WHERE id=?'
        value = (client_id,)
        self._execute_query(sql, value)

    def update_client(self, client_id, client_full_name, foreign_passport_ID, local_passport_ID, phone_number,
                      personal_discount_percent):
        sql = '''UPDATE clients
                    SET client_full_name = ?,
                        foreign_passport_ID = ?, 
                        local_passport_ID = ?, 
                        phone_number = ?, 
                        personal_discount_percent = ?
                    WHERE id = ?'''
        value = (
        client_id, client_full_name, foreign_passport_ID, local_passport_ID, phone_number, personal_discount_percent)
        self._execute_query(sql, value)

    def select_clients(self):
        sql = '''SELECT * FROM clients'''
        return self._execute_select_query(sql)


    def select_client(self, client_id):
        sql = 'SELECT * FROM clients WHERE id=?'
        value = (client_id,)
        return self._execute_select_query(sql, value)


class ClientApplication(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.client_controller = ClientController()
        self.clients = list()

        self.app = None

        label = tk.Label(self, text="CLIENT PANEL", font=controller.title_font)
        label.grid(row=0, column=0, columnspan=4)

        self.table = TableClass(parent=self,
                                hidden_columns=('ID',),
                                headings=('Client full name', 'Foreign passport ID', 'Local passport ID', 'Phone number', 'Personal discount percent'),
                                grid={'row': 1, 'column': 0, 'columnspan': 4})
        self.update_table()

        add_button = tk.Button(self, text="Add Client",
                               command=self.add_frame, width=OPTION['width'])
        add_button.grid(row=2, column=0)

        update_button = tk.Button(self, text="Update Client",
                                  command=self.update_frame, width=OPTION['width'])
        update_button.grid(row=2, column=1)

        delete_button = tk.Button(self, text="Delete Client",
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
            client = self.find_client(row)
            update_window = tk.Toplevel(self.master)
            self.app = UpdateFrame(update_window, client = client, base_frame=self)
        except IndexError:
            messagebox.showerror('Select someone', 'Select someone')

    def delete_frame(self):
        if self.app:
            self.app.close_windows()
        try:
            row = self.table.get_selected_item()
            client = self.find_client(row)
            delete_window = tk.Toplevel(self.master)
            self.app = DeleteFrame(delete_window, client = client, base_frame=self)
        except IndexError:
            messagebox.showerror('Select someone', 'Select someone')

    def find_client(self, row):
        filter_client = filter(lambda x: x[0] == row[0], self.clients)
        client = next(filter_client)
        return client

    def update_table(self):
        self.clients = self.client_controller.select_clients()
        rows = [client for client in self.clients]
        self.table.update_table(rows)


class FieldsFrame:
    def __init__(self, master, base_frame):
        self.master = master
        self.base_frame = base_frame
        self.controller = ClientController()

        self._init_labels()
        self._init_entries()

        quit_button = tk.Button(self.master, text='Quit', width=25, command=self.close_windows)
        quit_button.grid(row=self.last_row, column=0)

    def _init_labels(self):
        row, column = 0, 0
        label_client_full_name = tk.Label(master=self.master, text='Client full name: ')
        label_client_full_name.grid(row=row, column=column)
        row += 1

        label_foreign_passport_ID = tk.Label(master=self.master, text='Foreign passport ID: ')
        label_foreign_passport_ID.grid(row=row, column=column)
        row += 1

        label_local_passport_ID = tk.Label(master=self.master, text='Local passport ID: ')
        label_local_passport_ID.grid(row=row, column=column)
        row += 1

        label_phone_number = tk.Label(master=self.master, text='Phone number: ')
        label_phone_number.grid(row=row, column=column)
        row += 1

        label_personal_discount_percent = tk.Label(master=self.master, text='Personal discount percent: ')
        label_personal_discount_percent.grid(row=row, column=column)
        row += 1

    def _init_entries(self):
        row, column = 0, 1
        self.entry_client_full_name = tk.Entry(master=self.master)
        self.entry_client_full_name.grid(row=row, column=column)
        row += 1

        self.entry_foreign_passport_ID = tk.Entry(master=self.master)
        self.entry_foreign_passport_ID.grid(row=row, column=column)
        row += 1

        self.entry_local_passport_ID = tk.Entry(master=self.master)
        self.entry_local_passport_ID.grid(row=row, column=column)
        row += 1

        self.entry_phone_number = tk.Entry(master=self.master)
        self.entry_phone_number.grid(row=row, column=column)
        row += 1

        self.entry_personal_discount_percent = tk.Entry(master=self.master)
        self.entry_personal_discount_percent.grid(row=row, column=column)
        row += 1

        self.last_row = row

    def get_client_data(self):
        while True:
            try:
                client_full_name = self.entry_client_full_name.get()
                if client_full_name is None or len(client_full_name) == 0:
                    raise ValueError

                foreign_passport_ID = self.entry_foreign_passport_ID.get()
                if foreign_passport_ID is None or len(foreign_passport_ID) == 0:
                    raise ValueError

                local_passport_ID = int(self.entry_local_passport_ID.get())

                phone_number = int(self.entry_phone_number.get())
                if local_passport_ID <= 0:
                    raise ValueError

                personal_discount_percent = self.entry_personal_discount_percent.get()

            except ValueError:
                error_str = '\tclient full name - text\n' + \
                            '\tforeign passport id - integer\n' + \
                            '\tlocal passport id - integer\n' + \
                            '\tphone number - integer\n' + \
                            '\tpersonal discount - integer'
                messagebox.showerror('Enter correct data', error_str)
                return

            return client_full_name, foreign_passport_ID, local_passport_ID, phone_number, personal_discount_percent

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
        self.controller.insert_client(*self.get_client_data())
        self.base_frame.update_table()
        self.close_windows()


class UpdateFrame(FieldsFrame):
    def __init__(self, master, base_frame, client):
        super().__init__(master, base_frame)
        self.master = master
        self.client = client
        self.frame = tk.Frame(self.master)

        self._init_initial_client()

        self.frame.grid(row=0, column=0)
        update_button = tk.Button(self.master, text='Update', width=25, command=self.update)
        update_button.grid(row=self.last_row, column=1)

    def _init_initial_client(self):
        self.entry_client_full_name.insert(0, self.client[1])
        self.entry_foreign_passport_ID.insert(0, self.client[4])
        self.entry_local_passport_ID.insert(0, self.client[2])
        self.entry_phone_number.insert(0, self.client[3])
        self.entry_personal_discount_percent.insert(0, self.client[5])

    def update(self):
        client = self.get_client_data()
        self.controller.update_client(*client, self.client[0])
        self.base_frame.update_table()
        self.close_windows()


class DeleteFrame(FieldsFrame):
    def __init__(self, master, base_frame, client):
        super().__init__(master, base_frame)
        self.master = master
        self.client = client
        self.frame = tk.Frame(self.master)

        self._init_initial_client()

        self.frame.grid(row=0, column=0)
        delete_button = tk.Button(self.master, text='Delete', width=25, command=self.delete)
        delete_button.grid(row=self.last_row, column=1)

    def _init_initial_client(self):
        self.entry_client_full_name.insert(0, self.client[1])
        self.entry_foreign_passport_ID.insert(0, self.client[4])
        self.entry_local_passport_ID.insert(0, self.client[2])
        self.entry_phone_number.insert(0, self.client[3])
        self.entry_personal_discount_percent.insert(0, self.client[5])

        self.entry_client_full_name.config(state=tk.DISABLED)
        self.entry_foreign_passport_ID.config(state=tk.DISABLED)
        self.entry_local_passport_ID.config(state=tk.DISABLED)
        self.entry_phone_number.config(state=tk.DISABLED)
        self.entry_personal_discount_percent.config(state=tk.DISABLED)

    def delete(self):
        self.controller.delete_client(self.client[0])
        self.base_frame.update_table()
        self.close_windows()
