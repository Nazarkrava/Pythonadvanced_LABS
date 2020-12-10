from Utils.default_settings import *
from Fileworker.fileworker import Fileworker
from Clients.Clients import ClientWindow
from Directions.Directions import DirectionWindow
from Trips.Trips import TripWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = None

        layout = QVBoxLayout()

        button = QPushButton('TRIPS')
        button.clicked.connect(self.show_act)
        layout.addWidget(button)

        button = QPushButton('DIRECTIONS')
        button.clicked.connect(self.show_violation)
        layout.addWidget(button)

        button = QPushButton('CLIENTS')
        button.clicked.connect(self.show_car)
        layout.addWidget(button)

        button = QPushButton('COPY DB TO DOC/XLSX FILE')
        button.clicked.connect(self.save_database)
        layout.addWidget(button)

        button = QPushButton('EXIT')
        button.clicked.connect(sys.exit)
        layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def save_database(self):
        Fileworker().save_to_files()

    def show_act(self, checked):
        self.call_window(TripWindow)

    def show_violation(self, checked):
        self.call_window(DirectionWindow)

    def show_car(self, checked):
        self.call_window(ClientWindow)

    def call_window(self, window_class):
        if self.window is None:
            self.window = window_class()
            self.window.show()
        else:
            self.window.close()
            self.window = None


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()
