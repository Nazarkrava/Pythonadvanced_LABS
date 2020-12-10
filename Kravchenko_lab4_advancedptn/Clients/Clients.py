from Database.database_class import DB
from Utils.default_settings import *


class ClientController(DB):
    def insert_client(self, client_full_name, foreign_passport_ID, local_passport_ID, phone_number, personal_discount_percent):
        sql = '''INSERT INTO clients
                (client_full_name, foreign_passport_ID, local_passport_ID, phone_number, personal_discount_percent)
                VALUES(?, ?, ?, ?, ?)'''
        value = (client_full_name, foreign_passport_ID, local_passport_ID, phone_number, personal_discount_percent)
        self._execute_query(sql, value)

    def delete_client(self, client_id):
        sql = 'DELETE FROM clients WHERE id=?'
        value = (client_id,)
        self._execute_query(sql, value)

    def update_client(self, client_full_name, foreign_passport_ID, local_passport_ID, phone_number, personal_discount_percent, client_id):
        sql = '''UPDATE clients
                 SET client_full_name = ?,
                     foreign_passport_ID = ?,
                     local_passport_ID = ?,
                     phone_number = ?,
                     personal_discount_percent = ?
                 WHERE id = ?'''
        value = (client_full_name, foreign_passport_ID, local_passport_ID, phone_number, personal_discount_percent, client_id)
        self._execute_query(sql, value)

    def select_clients(self):
        sql = '''SELECT * FROM clients'''
        return self._execute_select_query(sql)

    def select_client(self, client_id):
        sql = 'SELECT * FROM clients WHERE id=?'
        value = (client_id,)
        return self._execute_select_query(sql, value)


class ClientWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.window = None
        self.client_controller = ClientController()
        self.clients = list()

        self.grid = QGridLayout()
        self._init_buttons()
        self.init_table()
        self.setLayout(self.grid)

    def _init_buttons(self):
        label = QLabel("CLIENT WINDOW")
        self.grid.addWidget(label, *(0, 0))

        button = QPushButton('Add client')
        button.clicked.connect(self.add_client)
        self.grid.addWidget(button, *(2, 0))

        button = QPushButton('Update client')
        button.clicked.connect(self.update_client)
        self.grid.addWidget(button, *(2, 1))

        button = QPushButton('Delete client')
        button.clicked.connect(self.del_client)
        self.grid.addWidget(button, *(2, 2))

        button = QPushButton('Return')
        button.clicked.connect(self.close)
        self.grid.addWidget(button, *(2, 3))

    def init_table(self):
        self.table = QTableWidget(self)

        self.headers = ['Client Full Name', 'Foreign Passport ID', 'Local Passport ID', 'Phone Number', 'Personal Discount']
        self.clients = self.client_controller.select_clients()

        self.table.setColumnCount(len(self.headers))
        self.table.setRowCount(len(self.clients))

        self.table.setHorizontalHeaderLabels(self.headers)

        def set_client(i):
            client = self.clients[i]
            self.table.setItem(i, 0, QTableWidgetItem(str(client[1])))
            self.table.setItem(i, 1, QTableWidgetItem(str(client[2])))
            self.table.setItem(i, 2, QTableWidgetItem(str(client[3])))
            self.table.setItem(i, 3, QTableWidgetItem(str(client[4])))
            self.table.setItem(i, 4, QTableWidgetItem(str(client[5])))

        for i in range(len(self.clients)):
            set_client(i)

        self.table.resizeColumnsToContents()
        self.grid.addWidget(self.table, *(1, 0, 1, 5))

    def add_client(self):
        if self.window is None:
            self.window = ClientAddForm(base_widget=self)
            self.window.show()
        else:
            self.window.close()
            self.window = None

    def update_client(self):
        client = self._get_one_row()
        if client:
            if self.window is None:
                self.window = ClientUpdateForm(base_widget=self, client=client)
                self.window.show()
            else:
                self.window.close()
                self.window = None

    def del_client(self):
        client = self._get_one_row()
        if client:
            if self.window is None:
                self.window = ClientDeleteForm(base_widget=self, client=client)
                self.window.show()
            else:
                self.window.close()
                self.window = None

    def _get_one_row(self):
        rows = []
        row = None
        for i in self.table.selectedIndexes():
            rows.append(i.row())
        if len(rows) == len(self.headers) and rows.count(rows[0]) == len(rows):
            row = self.clients[rows[0]]
        else:
            print('select 1 row!')
        return row


class BaseForm(QWidget):
    def __init__(self, base_widget):
        super().__init__()
        self.base_widget = base_widget
        self.controller = ClientController()
        self.grid = QGridLayout()

        self._init_label()
        self._init_entries()

        quit_buttin = QPushButton('Quit')
        quit_buttin.clicked.connect(self.close)
        self.grid.addWidget(quit_buttin, *(self.last_column, 0))
        self.setLayout(self.grid)

    def _init_label(self):
        row = 0
        column = 0

        label = QLabel('Client Full Name', self)
        self.grid.addWidget(label, *(column, row))
        column += 1

        label = QLabel('Foreign Passpost ID', self)
        self.grid.addWidget(label, *(column, row))
        column += 1

        label = QLabel('Local Passport ID', self)
        self.grid.addWidget(label, *(column, row))
        column += 1

        label = QLabel('Phone Number', self)
        self.grid.addWidget(label, *(column, row))
        column += 1

        label = QLabel('Personal Discount', self)
        self.grid.addWidget(label, *(column, row))
        column += 1

    def _init_entries(self):
        row = 1
        column = 0

        self.entry_client_full_name = QLineEdit(self)
        self.grid.addWidget(self.entry_client_full_name, *(column, row))
        column += 1

        self.entry_foreign_passport_ID = QLineEdit(self)
        self.grid.addWidget(self.entry_foreign_passport_ID, *(column, row))
        column += 1

        self.entry_local_passport_ID = QLineEdit(self)
        self.grid.addWidget(self.entry_local_passport_ID, *(column, row))
        column += 1

        self.entry_phone_number = QLineEdit(self)
        self.grid.addWidget(self.entry_phone_number, *(column, row))
        column += 1

        self.entry_personal_discount_percent = QLineEdit(self)
        self.grid.addWidget(self.entry_personal_discount_percent, *(column, row))
        column += 1

        self.last_row = row
        self.last_column = column

    def get_client_data(self):
        try:
            client_full_name = self.entry_client_full_name.text()
            if client_full_name is None or len(client_full_name) == 0:
                raise ValueError

            phone_number = self.entry_phone_number.text()
            if phone_number is None or len(phone_number) == 0:
                raise ValueError

            foreign_passport_ID = int(self.entry_foreign_passport_ID.text())

            local_passport_ID = int(self.entry_local_passport_ID.text())
            if local_passport_ID <= 0:
                raise ValueError

            personal_discount_percent = self.entry_personal_discount_percent.text()
            if not personal_discount_percent.isdigit():
                raise ValueError
        except ValueError:
            error_str = '\tclient full name - text\n' + \
                        '\tforeign passport id - integer\n' + \
                        '\tlocal passport id - integer\n' + \
                        '\tphone number - integer\n' + \
                        '\tpersonal discount - integer'
            QMessageBox.warning(self, 'Error', error_str)
            self.close()
        else:
            return client_full_name, foreign_passport_ID, local_passport_ID, phone_number, personal_discount_percent

        self.close()


class FilledBaseForm(BaseForm):
    def __init__(self, base_widget, client):
        super().__init__(base_widget)
        self.client = client

        self.entry_client_full_name.setText(str(self.client[1]))
        self.entry_foreign_passport_ID.setText(str(self.client[2]))
        self.entry_local_passport_ID.setText(str(self.client[3]))
        self.entry_phone_number.setText(str(self.client[4]))
        self.entry_personal_discount_percent.setText(str(self.client[5]))


class ReadonlyBaseForm(FilledBaseForm):
    def __init__(self, base_widget, client):
        super().__init__(base_widget, client)

        self.entry_client_full_name.setReadOnly(True)
        self.entry_phone_number.setReadOnly(True)
        self.entry_foreign_passport_ID.setReadOnly(True)
        self.entry_local_passport_ID.setReadOnly(True)
        self.entry_personal_discount_percent.setReadOnly(True)


class ClientAddForm(BaseForm):
    def __init__(self, base_widget):
        super().__init__(base_widget)

        button = QPushButton('Save')
        button.clicked.connect(self.save)
        self.grid.addWidget(button, *(self.last_column, self.last_row))

    def save(self):
        client = self.get_client_data()
        if client:
            self.controller.insert_client(*client)
            self.base_widget.init_table()
        self.close()


class ClientUpdateForm(FilledBaseForm):
    def __init__(self, base_widget, client):
        super().__init__(base_widget, client)

        button = QPushButton('Update')
        button.clicked.connect(self.update)
        self.grid.addWidget(button, *(self.last_column, self.last_row))

    def update(self):
        client = self.get_client_data()
        if client:
            self.controller.update_client(*client, self.client[0])
            self.base_widget.init_table()
        self.close()


class ClientDeleteForm(ReadonlyBaseForm):
    def __init__(self, base_widget, client):
        super().__init__(base_widget, client)

        button = QPushButton('Delete')
        button.clicked.connect(self.delete)
        self.grid.addWidget(button, *(self.last_column, self.last_row))

    def delete(self):
        self.controller.delete_client(self.client[0])
        self.base_widget.init_table()
        self.close()
