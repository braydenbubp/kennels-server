import sqlite3
import json
from models import Animal, Location, Customer


def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address location_address,
            c.name customer_name,
            c.address customer_address,
            c.email customer_email
        FROM Animal a
        JOIN Location l
            ON l.id = a.location_id
        JOIN Customer c
            ON c.id = a.customer_id
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])

            # Create a Location instance from the current row
            location = Location(
                row['location_id'], row['location_name'], row['location_address'])
            del location.employee
            del location.animal

            customer = Customer(row['customer_id'], row['customer_name'],
                                row['customer_address'], row['customer_email'])
            del customer.password #removed the password from the query but didnt delete it

            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__
            animal.customer = customer.__dict__

            # see the notes below for an explanation on this line of code.
            animals.append(animal.__dict__)

    return animals

# Function with a single parameter


def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # use a ? parameter to inject a variable value
        # into the SQL statement
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.id = ?
        """, (id, ))

        # load single result into memory
        data = db_cursor.fetchone()

        # create animal instance from current row
        animal = Animal(data['id'], data['name'], data['breed'],
                        data['status'], data['location_id'],
                        data['customer_id'])

        return animal.__dict__


def create_animal(new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['location_id'],
              new_animal['customer_id'], ))

        #the 'lastrowid' prop on the cursor will return PK of last thing that got added to db
        id = db_cursor.lastrowid

        #add 'id' prop to animal dict that was sent by client so client sees PK in response
        new_animal['id'] = id

    # return dictionary with id property added
    return new_animal


def delete_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))


def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['location_id'],
              new_animal['customer_id'], id, ))

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


def get_animals_by_location(location_id):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.location_id = ?
        """, (location_id, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])
            animals.append(animal.__dict__)

    return animals


def get_animals_by_status(status):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.status = ?
        """, (status, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])
            animals.append(animal.__dict__)

    return animals

def search_animals(search_string):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
        *
        FROM animal a
        WHERE a.name LIKE ?
        """, ('%' + search_string + '%', ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])
            animals.append(animal.__dict__)

        db_cursor.execute("""
        SELECT
        *
        FROM animal a
        WHERE a.breed LIKE ?
        """, ('%' + search_string + '%', ))

        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])
            animals.append(animal.__dict__)

    return animals
