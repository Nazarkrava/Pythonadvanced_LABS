from Database.database_class import DB

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


class Direction:
    def __init__(self):
        print('<<< Welcome to Direction panel >>>')
        self.controller = DirectionController()
        self.directions = list()
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
                print('<<< Quit from Direction panel >>>')
                break
            elif choice in self.urls.keys():
                self.urls[choice]()
            else:
                print('Incorrect choice')

    def _get_directions(self):
        qs = self.controller.select_directions()
        self.directions = qs

    def _print(self):
        self._get_directions()
        print('Directions:')
        for n, direction in enumerate(self.directions, start=1):
            direction_id, place_of_arrival, price_per_day, visa_price, transport_price = direction
            print(
                '\t%d: \n\tPlace of arrival: %s\n\tPrice per day: %s\n\tVisa price: %s\n\tTransport price: %s' %
                (n, place_of_arrival, price_per_day, visa_price, transport_price))

    def _add(self):
        direction = self._create_direction()
        if direction is not None:
            place_of_arrival, price_per_day, visa_price, transport_price = direction
            self.controller.insert_direction(place_of_arrival = place_of_arrival,
                                             price_per_day = price_per_day,
                                             visa_price = visa_price,
                                             transport_price = transport_price)
            print(' <<< Direction was created >>>')

    def _delete(self):
        self._print()
        number = self._get_number()
        direction = self.directions[number - 1]
        self.controller.delete_direction(direction_id = direction[0])
        print(' <<< Direction was deleted >>> ')

    def _update(self):
        self._print()
        number = self._get_number()
        selected_direction = self.directions[number - 1]
        direction = self._create_direction()
        if direction is not None:
            place_of_arrival, price_per_day, visa_price, transport_price = direction
            self.controller.update_direction(place_of_arrival = place_of_arrival,
                                             price_per_day = price_per_day,
                                             visa_price = visa_price,
                                             transport_price = transport_price,
                                             direction_id = selected_direction[0])
            print(' <<< Direction was updated >>>')

    def _create_direction(self):
        try:
            place_of_arrival = input('Enter place of arrival: ')
            if place_of_arrival is None or len(place_of_arrival) == 0:
                raise ValueError

            price_per_day = input('Enter daily price: ')
            if price_per_day is None or len(price_per_day) == 0:
                raise ValueError

            visa_price = int(input('Enter visa price: '))

            transport_price = int(input('Enter transport price: '))

        except ValueError:
            print('Enter correct data')
            print('\tclient full name - text\n'
                  '\tforeign passport ID - non negative int\n'
                  '\tlocal passport ID - non negative int\n'
                  '\tphone number - non negative int\n'
                  '\tpersonal discount percent - non negative int')
        else:
            return place_of_arrival, price_per_day, visa_price, transport_price

    def _get_number(self):
        while True:
            try:
                number = int(input('Select client number: '))
                if not 0 < number < len(self.directions) + 1:
                    raise ValueError
                return number
            except ValueError:
                print('Incorrect number')