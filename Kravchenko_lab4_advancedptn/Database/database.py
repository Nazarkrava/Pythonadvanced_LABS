import sqlite3
import os

dirname = os.path.dirname(__file__)
DB_PATH = os.path.join(dirname, 'database.db')


CLIENTS_SCRIPT = '''
CREATE TABLE clients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_full_name TEXT,
    foreign_passport_ID INTEGER,
    local_passport_ID value INTEGER,
    phone_number INTEGER,
    personal_discount_percent INTEGER
)
'''

DIRECTIONS_SCRIP = '''
CREATE TABLE directions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_of_arrival TEXT,
    country_of_arrival TEXT,
    price_per_day INTEGER,
    visa_price INTEGER,
    transport_price INTEGER
)
'''

TRIPS_SCRIP = '''
CREATE TABLE trips(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day_quantity INTEGER,
    full_price INTEGER,
    purpose_of_trip TEXT,
    way_to_trip INTEGER,
    client_full_name INTEGER,
    FOREIGN KEY (way_to_trip) 
        REFERENCES directions (id) 
            ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (client_full_name) 
        REFERENCES clients (id)
            ON DELETE CASCADE ON UPDATE CASCADE
)
'''


def create_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')
    cursor = conn.cursor()

    cursor.execute(CLIENTS_SCRIPT)
    cursor.execute(DIRECTIONS_SCRIP)
    cursor.execute(TRIPS_SCRIP)

    conn.commit()
    conn.close()


def delete_db():
    import os
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


if __name__ == '__main__':
    delete_db()
    create_db()
