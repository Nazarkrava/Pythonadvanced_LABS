from Database.database_class import DB
from Utils.default_settings import *

class DirectionController(DB):
    def insert_direction(self, place_of_arrival, country_of_arrival, price_per_day, visa_price, transport_price):
        sql = '''INSERT INTO directions
                (place_of_arrival, country_of_arrival, price_per_day, visa_price, transport_price)
                VALUES(?, ?, ?, ?, ?)'''
        value = (place_of_arrival, country_of_arrival, price_per_day, visa_price, transport_price)
        self._execute_query(sql, value)

    def delete_direction(self, direction_id):
        sql = 'DELETE FROM directions WHERE id=?'
        value = (direction_id,)
        self._execute_query(sql, value)

    def update_direction(self, direction_id, place_of_arrival, country_of_arrival, price_per_day, visa_price, transport_price):
        sql = '''UPDATE directions
                    SET direction_id = ?,
                    place_of_arrival = ?, 
                    country_of_arrival = ?,
                    price_per_day = ?, 
                    visa_price = ?, 
                    transport_price = ?
                    WHERE id = ?'''
        value = (direction_id, place_of_arrival, country_of_arrival, price_per_day, visa_price, transport_price)
        self._execute_query(sql, value)

    def select_directions(self):
        sql = '''SELECT * FROM directions'''
        return self._execute_select_query(sql)

    def select_direction(self, direction_id):
        sql = 'SELECT * FROM directions WHERE id=?'
        value = (direction_id,)
        return self._execute_select_query(sql, value)


class DirectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.window = None
        self.direction_controller = DirectionController()
        self.directions = list()

        self.grid = QGridLayout()
        self._init_buttons()
        self.init_table()
        self.setLayout(self.grid)

    def _init_buttons(self):
        label = QLabel("DIRECTION WINDOW")
        self.grid.addWidget(label, *(0, 0))

        button = QPushButton('Add direction')
        button.clicked.connect(self.add_direction)
        self.grid.addWidget(button, *(2, 0))

        button = QPushButton('Update direction')
        button.clicked.connect(self.update_direction)
        self.grid.addWidget(button, *(2, 1))

        button = QPushButton('Delete direction')
        button.clicked.connect(self.del_direction)
        self.grid.addWidget(button, *(2, 2))

        button = QPushButton('Return')
        button.clicked.connect(self.close)
        self.grid.addWidget(button, *(2, 3))

    def init_table(self):
        self.table = QTableWidget(self)

        self.headers = ['Place of Arrival', 'Country Of Arrival', 'Price Per Day', 'Visa Price','Transport Price']
        self.directions = self.direction_controller.select_directions()

        self.table.setColumnCount(len(self.headers))
        self.table.setRowCount(len(self.directions))

        self.table.setHorizontalHeaderLabels(self.headers)

        def set_direction(i):
            direction = self.directions[i]
            self.table.setItem(i, 0, QTableWidgetItem(str(direction[1])))
            self.table.setItem(i, 1, QTableWidgetItem(str(direction[2])))
            self.table.setItem(i, 2, QTableWidgetItem(str(direction[3])))
            self.table.setItem(i, 3, QTableWidgetItem(str(direction[4])))
            self.table.setItem(i, 4, QTableWidgetItem(str(direction[5])))

        for i in range(len(self.directions)):
            set_direction(i)

        self.table.resizeColumnsToContents()
        self.grid.addWidget(self.table, *(1, 0, 1, 5))

    def add_direction(self):
        if self.window is None:
            self.window = DirectionAddForm(base_widget=self)
            self.window.show()
        else:
            self.window.close()
            self.window = None

    def update_direction(self):
        direction = self._get_one_row()
        if direction:
            if self.window is None:
                self.window = DirectionUpdateForm(base_widget=self, direction=direction)
                self.window.show()
            else:
                self.window.close()
                self.window = None

    def del_direction(self):
        direction = self._get_one_row()
        if direction:
            if self.window is None:
                self.window = DirectionDeleteForm(base_widget=self, direction=direction)
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
            row = self.directions[rows[0]]
        else:
            print('select 1 row!')
        return row


class BaseForm(QWidget):
    def __init__(self, base_widget):
        super().__init__()
        self.base_widget = base_widget
        self.controller = DirectionController()
        self.grid = QGridLayout()

        self._init_label()
        self._init_entries()

        quit_button = QPushButton('Quit')
        quit_button.clicked.connect(self.close)
        self.grid.addWidget(quit_button, *(self.last_column, 0))
        self.setLayout(self.grid)

    def _init_label(self):
        row = 0
        column = 0

        label = QLabel('Place Of Arrival', self)
        self.grid.addWidget(label, *(column, row))
        column += 1

        label = QLabel('Country of Arrival', self)
        self.grid.addWidget(label, *(column, row))
        column += 1

        label = QLabel('Price Per Day', self)
        self.grid.addWidget(label, *(column, row))
        column += 1

        label = QLabel('Visa Price', self)
        self.grid.addWidget(label, *(column, row))
        column += 1

        label = QLabel('Transport Price', self)
        self.grid.addWidget(label, *(column, row))
        column += 1

    def _init_entries(self):
        row = 1
        column = 0

        self.entry_place_of_arrival = QLineEdit(self)
        self.grid.addWidget(self.entry_place_of_arrival, *(column, row))
        column += 1

        self.entry_country_of_arrival = QLineEdit(self)
        self.grid.addWidget(self.entry_country_of_arrival, *(column, row))
        column += 1

        self.entry_price_per_day = QLineEdit(self)
        self.grid.addWidget(self.entry_price_per_day, *(column, row))
        column += 1

        self.entry_visa_price = QLineEdit(self)
        self.grid.addWidget(self.entry_visa_price, *(column, row))
        column += 1

        self.entry_transport_price = QLineEdit(self)
        self.grid.addWidget(self.entry_transport_price, *(column, row))
        column += 1

        self.last_row = row
        self.last_column = column

    def get_direction_data(self):
        try:
            place_of_arrival = self.entry_place_of_arrival.text()

            country_of_arrival = self.entry_country_of_arrival.text()

            visa_price = self.entry_visa_price.text()

            price_per_day = int(self.entry_price_per_day.text())

            transport_price = self.entry_transport_price.text()

        except ValueError:
            error_str = '\tplace of arrival - text\n' + \
                        '\tprice per day - integer\n' + \
                        '\tvisa price - integer\n' + \
                        '\ttransport price - integer'
            QMessageBox.warning(self, 'Error', error_str)
            self.close()
        else:
            return place_of_arrival, country_of_arrival, price_per_day, visa_price, transport_price

        self.close()


class FilledBaseForm(BaseForm):
    def __init__(self, base_widget, direction):
        super().__init__(base_widget)
        self.direction = direction

        self.entry_place_of_arrival.setText(str(self.direction[1]))
        self.entry_country_of_arrival.setText(str(self.direction[2]))
        self.entry_price_per_day.setText(str(self.direction[3]))
        self.entry_visa_price.setText(str(self.direction[4]))
        self.entry_transport_price.setText(str(self.direction[5]))


class ReadonlyBaseForm(FilledBaseForm):
    def __init__(self, base_widget, direction):
        super().__init__(base_widget, direction)

        self.entry_place_of_arrival.setReadOnly(True)
        self.entry_visa_price.setReadOnly(True)
        self.entry_country_of_arrival.setReadOnly(True)
        self.entry_price_per_day.setReadOnly(True)
        self.entry_transport_price.setReadOnly(True)


class DirectionAddForm(BaseForm):
    def __init__(self, base_widget):
        super().__init__(base_widget)

        button = QPushButton('Save')
        button.clicked.connect(self.save)
        self.grid.addWidget(button, *(self.last_column, self.last_row))

    def save(self):
        direction = self.get_direction_data()
        if direction:
            self.controller.insert_direction(*direction)
            self.base_widget.init_table()
        self.close()


class DirectionUpdateForm(FilledBaseForm):
    def __init__(self, base_widget, direction):
        super().__init__(base_widget, direction)

        button = QPushButton('Update')
        button.clicked.connect(self.update)
        self.grid.addWidget(button, *(self.last_column, self.last_row))

    def update(self):
        direction = self.get_direction_data()
        if direction:
            self.controller.update_direction(*direction, self.direction[0])
            self.base_widget.init_table()
        self.close()


class DirectionDeleteForm(ReadonlyBaseForm):
    def __init__(self, base_widget, direction):
        super().__init__(base_widget, direction)

        button = QPushButton('Delete')
        button.clicked.connect(self.delete)
        self.grid.addWidget(button, *(self.last_column, self.last_row))

    def delete(self):
        self.controller.delete_direction(self.direction[0])
        self.base_widget.init_table()
        self.close()
