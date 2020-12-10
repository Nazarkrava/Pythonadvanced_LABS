from Database.database_class import DB
from Utils.default_settings import *
from Clients.Clients import ClientController
from Directions.Directions import DirectionController

class TripController(DB):
    def insert_trip(self, day_quantity, full_price, purpose_of_trip, way_to_trip, client_full_name):
        sql = '''INSERT INTO trips
                (day_quantity, full_price, purpose_of_trip, way_to_trip, client_full_name)
                VALUES(?, ?, ?, ?, ?)'''
        value = (day_quantity, full_price, purpose_of_trip, way_to_trip, client_full_name)
        self._execute_query(sql, value)

    def delete_trip(self, trip_id):
        sql = 'DELETE FROM trips WHERE id=?'
        value = (trip_id,)
        self._execute_query(sql, value)

    def update_trip(self, day_quantity, full_price, purpose_of_trip, way_to_trip, client_full_name, trip_id):
        sql = '''UPDATE trips
                 SET day_quantity = ?,
                     full_price = ?,
                     purpose_of_trip = ?,
                     way_to_trip = ?,
                     client_full_name = ?
                 WHERE id = ?'''
        value = (day_quantity, full_price, purpose_of_trip, way_to_trip, client_full_name, trip_id)
        self._execute_query(sql, value)

    def select_trips(self):
        sql = '''SELECT * FROM trips'''
        return self._execute_select_query(sql)

    def select_trip(self, trip_id):
        sql = '''SELECT * FROM trips WHERE id=?'''
        value = (trip_id, )
        return self._execute_select_query(sql, value)


class TripWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.window = None
        self.client_controller = ClientController()
        self.direction_controller = DirectionController()
        self.trip_controller = TripController()
        self.trips = list()

        self.grid = QGridLayout()
        self._init_buttons()
        self.init_table()
        self.setLayout(self.grid)

    def _init_buttons(self):
        label = QLabel("trip Window")
        self.grid.addWidget(label, *(0, 0))

        button = QPushButton('Add trip')
        button.clicked.connect(self.add_trip)
        self.grid.addWidget(button, *(2, 0))

        button = QPushButton('Update trip')
        button.clicked.connect(self.update_trip)
        self.grid.addWidget(button, *(2, 1))

        button = QPushButton('Delete trip')
        button.clicked.connect(self.del_trip)
        self.grid.addWidget(button, *(2, 2))

        button = QPushButton('Return')
        button.clicked.connect(self.close)
        self.grid.addWidget(button, *(2, 3))

    def init_table(self):
        self.table = QTableWidget(self)
        self.headers = ['Client', 'Direction', 'Full Price', 'Day Quantity', 'Purpose Of Trip']
        self.trips = self.trip_controller.select_trips()

        self.table.setColumnCount(len(self.headers))
        self.table.setRowCount(len(self.trips))
        self.table.setHorizontalHeaderLabels(self.headers)

        def set_trips(i):
            trip = self.trips[i]

            client = self.client_controller.select_client(trip[5])[0]
            direction = self.direction_controller.select_direction(trip[4])[0]

            string = [str(e) for e in client[1:]]
            client_str = ' '.join(string)

            self.table.setItem(i, 0, QTableWidgetItem(client_str))
            self.table.setItem(i, 1, QTableWidgetItem(direction[1]))
            self.table.setItem(i, 2, QTableWidgetItem(str(trip[2])))
            self.table.setItem(i, 3, QTableWidgetItem(str(trip[1])))
            self.table.setItem(i, 4, QTableWidgetItem(str(trip[3])))

        for i in range(len(self.trips)):
            set_trips(i)

        self.table.resizeColumnsToContents()
        self.grid.addWidget(self.table, *(1, 0, 1, 5))

    def add_trip(self):
        if self.window is None:
            self.window = TripAddForm(base_widget=self)
            self.window.show()
        else:
            self.window.close()
            self.window = None

    def update_trip(self):
        trip = self._get_one_row()
        if trip:
            if self.window is None:
                self.window = TripUpdateForm(base_widget=self, trip=trip)
                self.window.show()
            else:
                self.window.close()
                self.window = None

    def del_trip(self):
        trip = self._get_one_row()
        if trip:
            if self.window is None:
                self.window = TripDeleteForm(base_widget=self, trip=trip)
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
            row = self.trips[rows[0]]
        else:
            print('select 1 row!')
        return row


class BaseForm(QWidget):
    def __init__(self, base_widget):
        super().__init__()
        self.base_widget = base_widget

        self.controller = TripController()
        self.direction_controller = DirectionController()
        self.client_controller = ClientController()

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

        label = QLabel('Client: ', self)
        self.grid.addWidget(label, *(column, row))
        column += 1

        label = QLabel('Direction: ', self)
        self.grid.addWidget(label, *(column, row))
        column += 1

        label = QLabel('Full Price:', self)
        self.grid.addWidget(label, *(column, row))
        column += 1

        label = QLabel('Day Quantity', self)
        self.grid.addWidget(label, *(column, row))
        column += 1

        label = QLabel('Purpose Of Trip', self)
        self.grid.addWidget(label, *(column, row))
        column += 1

    def _init_entries(self):
        row = 1
        column = 0

        self.entry_client = QComboBox(self)
        values = list()
        for n, client in enumerate(self.client_controller.select_clients(), start=1):
            string = [str(e) for e in client[1:]]
            client_str = ' '.join(string)
            current = '%d: %s' % (n, client_str)
            values.append(current)
        self.entry_client.addItems(values)
        self.grid.addWidget(self.entry_client, *(column, row))
        column += 1

        self.entry_direction = QComboBox(self)
        values = list()
        for n, direction in enumerate(self.direction_controller.select_directions(), start=1):
            current = '%d: %s' % (n, direction[1])
            values.append(current)
        self.entry_direction.addItems(values)
        self.grid.addWidget(self.entry_direction, *(column, row))
        column += 1

        self.entry_date = QLineEdit(self)
        self.grid.addWidget(self.entry_date, *(column, row))
        column += 1

        self.entry_day_quantity = QLineEdit(self)
        self.grid.addWidget(self.entry_day_quantity, *(column, row))
        column += 1

        self.entry_purpose_of_trip = QLineEdit(self)
        self.grid.addWidget(self.entry_purpose_of_trip, *(column, row))
        column += 1

        self.last_row = row
        self.last_column = column

    def get_trip_data(self):
        try:
            directions = self.direction_controller.select_directions()
            clients = self.client_controller.select_clients()

            direction_index = self.entry_direction.currentIndex()
            client_index = self.entry_client.currentIndex()

            full_price = self.entry_date.text()

            day_quantity = int(self.entry_day_quantity.text())
            if day_quantity <= 0:
                raise ValueError

            purpose_of_trip = self.entry_purpose_of_trip.text()
            if purpose_of_trip is None or len(purpose_of_trip) == 0:
                raise ValueError
        except ValueError:
            error_str = '\tday quantity - integer\n' + \
                        '\tpurpose of trip - text\n' + \
                        '\tfull price - integer\n' + \
                        '\tway_to_trip - selected direction\n' + \
                        '\tclient_full_name - selected client\n'
            QMessageBox.warning(self, 'Error', error_str)
            self.close()
        else:
            client_id = clients[client_index][0]
            direction_id = directions[direction_index][0]
            return day_quantity, full_price, purpose_of_trip, direction_id, client_id
        self.close()


class FilledBaseForm(BaseForm):
    def __init__(self, base_widget, trip):
        super().__init__(base_widget)
        self.trip = trip

        client = self.client_controller.select_client(self.trip[5])[0]
        clients = self.client_controller.select_clients()
        client_index = clients.index(client)
        self.entry_client.setCurrentIndex(client_index)

        direction = self.direction_controller.select_direction(self.trip[4])[0]
        directions = self.direction_controller.select_directions()
        direction_index = directions.index(direction)
        self.entry_direction.setCurrentIndex(direction_index)

        self.entry_day_quantity.setText(str(self.trip[1]))
        self.entry_purpose_of_trip.setText(str(self.trip[3]))

        date = self.trip[2].split('-')
        date = '-'.join(date[::-1])
        self.entry_date.setText(date)


class ReadonlyBaseForm(FilledBaseForm):
    def __init__(self, base_widget, trip):
        super().__init__(base_widget, trip)

        self.entry_client.setEnabled(False)
        self.entry_direction.setEnabled(False)
        self.entry_day_quantity.setEnabled(False)
        self.entry_purpose_of_trip.setEnabled(False)
        self.entry_date.setEnabled(False)


class TripAddForm(BaseForm):
    def __init__(self, base_widget):
        super().__init__(base_widget)

        button = QPushButton('Save')
        button.clicked.connect(self.save)
        self.grid.addWidget(button, *(self.last_column, self.last_row))

    def save(self):
        trip = self.get_trip_data()
        if trip:
            self.controller.insert_trip(*trip)
            self.base_widget.init_table()
        self.close()


class TripUpdateForm(FilledBaseForm):
    def __init__(self, base_widget, trip):
        super().__init__(base_widget, trip)
        button = QPushButton('Update')
        button.clicked.connect(self.update)
        self.grid.addWidget(button, *(self.last_column, self.last_row))

    def update(self):
        trip = self.get_trip_data()
        if trip:
            self.controller.update_trip(*trip, self.trip[0])
            self.base_widget.init_table()
        self.close()


class TripDeleteForm(ReadonlyBaseForm):
    def __init__(self, base_widget, trip):
        super().__init__(base_widget, trip)

        button = QPushButton('Delete')
        button.clicked.connect(self.delete)
        self.grid.addWidget(button, *(self.last_column, self.last_row))

    def delete(self):
        self.controller.delete_trip(self.trip[0])
        self.base_widget.init_table()
        self.close()
