import sqlite3
import json
from models import Location, Animal

def get_all_locations():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address,
            a.name animal_name,
            a.status animal_status
        FROM Location l
        JOIN Animal a
            ON a.location_id = l.id
        """)

        # Initialize an empty list to hold all representations
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # class above.
            location = Location(row['id'], row['name'], row['address'])

            # employee = Employee(row['employee_id'], row['name'], row['address'], row['location_id'])

            animal = Animal(row['animal_id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])

            # location.employee = employee.__dict__
            location.animal = animal.__dict__

            # see the notes below for an explanation on this line of code.
            locations.append(location.__dict__)

    return locations

# Function with a single parameter
def get_single_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        #use a ? parameter to inject a variable value
        #into the SQL statement
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        WHERE l.id = ?
        """, (id, ))

        #load single result into memory
        data = db_cursor.fetchone()

        #create instance from current row
        location = Location(data['id'], data['name'], data['address'])

        return location.__dict__

def create_location(location):
    max_id = LOCATIONS[-1]["id"]

    new_id = max_id + 1

    location["id"] = new_id

    LOCATIONS.append(location)

    return location

def delete_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM location
        WHERE id = ?
        """, (id, ))

def update_location(id, new_location):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Location
            SET
                id = ?,
                name = ?,
                address = ?
        WHERE id = ?
        """, (new_location['id'], new_location['name'], new_location['address'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    # return value of this function
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
