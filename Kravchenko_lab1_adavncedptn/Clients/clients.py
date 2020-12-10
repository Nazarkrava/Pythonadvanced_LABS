from Database.database_class import DB

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


class Client:
    def __init__(self):
        print('<<< Welcome to Clients panel >>>')
        self.controller = ClientController()
        self.cars = list()
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
                print('<<< Quit from Clients panel >>>')
                break
            elif choice in self.urls.keys():
                self.urls[choice]()
            else:
                print('Incorrect choice')

    def _get_clients(self):
        qs = self.controller.select_clients()
        self.clients = qs

    def _print(self):
        self._get_clients()
        print('Clients:')
        for n, client in enumerate(self.clients, start=1):
            client_id, client_full_name, foreign_passport_ID, local_passport_ID, phone_number, personal_discount_percent = client
            print(
                '\t%d: \n\tclient_full_name: %s\n\tforeign_passport_ID: %s\n\tlocal_passport_ID: %s\n\tphone_number: %s\n\tpersonal_discount_percent: %s' %
                (n, client_full_name, foreign_passport_ID, local_passport_ID, phone_number, personal_discount_percent))

    def _add(self):
        client = self._create_client()
        if client is not None:
            client_full_name, foreign_passport_ID, local_passport_ID, phone_number, personal_discount_percent = client
            self.controller.insert_client(client_full_name=client_full_name,
                                          foreign_passport_ID=foreign_passport_ID,
                                          local_passport_ID=local_passport_ID,
                                          phone_number=phone_number,
                                          personal_discount_percent=personal_discount_percent
                                          )
            print(' <<< Client was created >>>')

    def _delete(self):
        self._print()
        number = self._get_number()
        client = self.clients[number - 1]
        self.controller.delete_client(client_id = client[0])
        print(' <<< Client was deleted >>> ')

    def _update(self):
        self._print()
        number = self._get_number()
        selected_client = self.clients[number - 1]
        client = self._create_client()
        if client is not None:
            client_full_name, foreign_passport_ID, local_passport_ID, phone_number, personal_discount_percent = client
            self.controller.update_client(client_full_name=client_full_name,
                                          foreign_passport_ID=foreign_passport_ID,
                                          local_passport_ID=local_passport_ID,
                                          phone_number=phone_number,
                                          personal_discount_percent=personal_discount_percent,
                                          client_id=selected_client[0])
            print(' <<< Client was updated >>>')

    def _create_client(self):
        try:
            client_full_name = input('Enter client full name: ')
            if client_full_name is None or len(client_full_name) == 0:
                raise ValueError

            foreign_passport_ID = input('Enter client foreign passport ID: ')
            if foreign_passport_ID is None or len(foreign_passport_ID) == 0:
                raise ValueError

            local_passport_ID = int(input('Enter client local passport ID: '))

            phone_number = int(input('Enter phone number: '))

            personal_discount_percent = input('Enter personal discount percent: ')

        except ValueError:
            print('Enter correct data')
            print('\tclient full name - text\n'
                  '\tforeign passport ID - non negative int\n'
                  '\tlocal passport ID - non negative int\n'
                  '\tphone number - non negative int\n'
                  '\tpersonal discount percent - non negative int')
        else:
            return client_full_name, foreign_passport_ID, local_passport_ID, phone_number, personal_discount_percent

    def _get_number(self):
        while True:
            try:
                number = int(input('Select client number: '))
                if not 0 < number < len(self.clients) + 1:
                    raise ValueError
                return number
            except ValueError:
                print('Incorrect number')