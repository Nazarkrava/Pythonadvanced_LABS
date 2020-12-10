from ViolationAct.trips import Trip
from Directions.directions import Direction
from Clients.clients import Client


class Application:
    def __init__(self):
        self.urls = {
            'trips': lambda: Trip().mainloop(),
            'directions': lambda: Direction().mainloop(),
            'clients': lambda: Client().mainloop(),
            'exit': lambda: exit(),
        }

    def mainloop(self):
        while True:
            for key, value in self.urls.items():
                print(':', key)

            choice = input('Enter your choice:\n > ')

            if choice in self.urls.keys():
                self.urls[choice]()
            else:
                print('Incorrect choice')


if __name__ == '__main__':
    app = Application()
    app.mainloop()
