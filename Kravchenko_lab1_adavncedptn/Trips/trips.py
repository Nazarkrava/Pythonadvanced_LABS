from Directions.directions import DirectionController, Direction
from Clients.clients import ClientController, Client
from Database.database_class import DB

class TripsController(DB):
    def insert_trip(self, day_quantity, purpose_of_trip, way_to_tip, client_full_name, full_price):
        sql = '''INSERT INTO trips
                (day_quantity, purpose_of_trip, way_to_tip, client_full_name, full_price)
                VALUES(?, ?, ?, ?, ?)'''
        value = (day_quantity, purpose_of_trip, way_to_tip, client_full_name, full_price)
        self._execute_query(sql, value)

    def delete_trip(self, trip_id):
        sql = 'DELETE FROM trips WHERE id=?'
        value = (trip_id,)
        self._execute_query(sql, value)

    def update_trip(self, day_quantity, purpose_of_trip, way_to_tip, client_full_name, full_price, trip_id):
        sql = '''UPDATE trips
                 SET day_quantity = ?, 
                 purpose_of_trip = ?, 
                 way_to_tip = ?, 
                 client_full_name = ?, 
                 full_price = ?
                 WHERE id = ?'''
        value = (day_quantity, purpose_of_trip, way_to_tip, client_full_name, full_price, trip_id)
        self._execute_query(sql, value)

    def select_trips(self):
        sql = '''SELECT * FROM trips'''
        return self._execute_select_query(sql)


class Trip:
    def __init__(self):
        print('<<< Welcome to Trips panel >>>')
        self.controller = TripsController()
        self.direction_controller = DirectionController()
        self.client_controller = ClientController()
        self.acts = list()
        self.urls = {
            'print': lambda: self._print(),
            'add': lambda: self._add(),
            'delete': lambda: self._delete(),
            'update': lambda: self._update(),
            'exit': None
        }

    def mainloop(self):
        while True:
            for key, value in self.urls.items():
                print(':', key)

            choice = input('Enter your choice:\n > ')

            if 'exit' == choice:
                print('<<< Quit from Act worker >>')
                break
            elif choice in self.urls.keys():
                self.urls[choice]()
            else:
                print('Incorrect choice')

    def _get_trips(self):
        qs = self.controller.select_trips()
        self.trips = qs

    def _print(self):
        self._get_trips()
        print('Trips:')
        for n, trip in enumerate(self.trips, start=1):
            trip_id, day_quantity, purpose_of_trip, way_to_tip, client_full_name, full_price  = trip
            print(
                '\t%d: \n\tNumber of days: %s\n\tPurpose of trip: %s\n\tWay to tip: %s\n\tClient full name: %s\n\tFull price: %s' %
                (n, day_quantity, purpose_of_trip, way_to_tip, client_full_name, full_price))

    def _add(self):
        trip = self._create_trip()
        if trip is not None:
            day_quantity, purpose_of_trip, way_to_tip, client_full_name, full_price = trip
            self.controller.insert_trip(day_quantity = day_quantity,
                                        purpose_of_trip = purpose_of_trip,
                                        way_to_tip = way_to_tip,
                                        client_full_name = client_full_name,
                                        full_price  = full_price)
            print('<<< Trip was created >>>')

    def _delete(self):
        self._print()
        number = self._get_number(self.trips)
        trip = self.trips[number - 1]
        self.controller.delete_trip(trip_id = trip[0])
        print('<<< Act was deleted >>>')

    def _update(self):
        self._print()
        number = self._get_number(self.acts)
        selected_trip = self.acts[number - 1]
        trip = self._create_trip()
        if trip is not None:
            day_quantity, purpose_of_trip, way_to_tip, client_full_name, full_price = trip
            self.controller.update_trip(day_quantity = day_quantity,
                                        purpose_of_trip = purpose_of_trip,
                                        way_to_tip = way_to_tip,
                                        client_full_name = client_full_name,
                                        full_price  = full_price,
                                        trip_id = selected_trip[0])
            print(' <<< Trip was updated >>> ')

    def _create_trip(self):
        try:
            day_quantity = int(input('Enter the number of days: '))
            if day_quantity <= 0:
                raise ValueError

            purpose_of_trip = input('Enter the purpose of a trip: ')
            if purpose_of_trip is None or len(purpose_of_trip) == 0:
                raise ValueError

            Direction()._print()
            directions = self.direction_controller.select_directions()
            number = self._get_number(directions)
            way_to_tip = directions[number - 1]
            way_to_tip = way_to_tip[0]

            Client()._print()
            clients = self.client_controller.select_clients()
            number = self._get_number(clients)
            client_full_name = clients[number - 1]
            client_full_name = client_full_name[0]

            full_price = (print('Currently not available'))

        except ValueError:
            print('Enter correct data')
            print('\tfine amount - text\n'
                  '\tdriver full name - text\n'
                  '\tdate of violation - date\n'
                  '\ttype of violation - selected type of violation\n'
                  '\tcar of violation - selected car of violation\n')
        else:
            return day_quantity, purpose_of_trip, way_to_tip, client_full_name, full_price

    def _get_number(self, sequence):
        while True:
            try:
                number = int(input('Select number: '))
                if not 0 < number < len(sequence) + 1:
                    raise ValueError
                return number
            except ValueError:
                print('Incorrect number')
