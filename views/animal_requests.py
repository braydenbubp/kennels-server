ANIMALS = [
    {
        "id": 1,
        "name": "Snickers",
        "species": "Dog",
        "locationId": 1,
        "customerId": 4,
        "status": "Admitted"
    },
    {
        "id": 2,
        "name": "Roman",
        "species": "Dog",
        "locationId": 1,
        "customerId": 2,
        "status": "Admitted"
    },
    {
        "id": 3,
        "name": "Blue",
        "species": "Cat",
        "locationId": 2,
        "customerId": 1,
        "status": "Admitted"
    }
]
class Animals():
    
    #class initializer - has 5 parameters with self param that every method on a class needs as first param
    def __init__(self, id, name, breed, status, location_id, customer_id):
        self.id = id
        self.name = name
        self.breed = breed
        self.status = status
        self.location_id = location_id
        self.customer_id = customer_id

def get_all_animals():
    return ANIMALS

# Function with a single parameter
def get_single_animal(id):
  # Variable to hold the found animal, if it exists
    requested_animal = None

  # Iterate the ANIMALS list above. Very similar to the
  # for..of loops you used in JavaScript.
    for animal in ANIMALS:
    # Dictionaries in Python use [] notation to find a key
    # instead of the dot notation that JavaScript used.
        if animal["id"] == id:
            requested_animal = animal
    return requested_animal

def create_animal(animal):
    # get id value of last animal in the list
    max_id = ANIMALS[-1]["id"]

    #add 1 to that number
    new_id = max_id + 1

    #add an id property to the animal dictionary
    animal["id"] = new_id

    #add the animal dictionary to the list
    ANIMALS.append(animal)

    #return dictionary with id property added
    return animal

def delete_animal(id):
    #initial -1 value for animal index, in case one isnt found
    animal_index = -1

    #iterate the ANIMALS list, but use enumerate() so you can access the index value of each item
    for index, animal in enumerate(ANIMALS):
        if animal["id"] == id:
            #found the animal - store the current index
            animal_index = index

    #if the animal was found use pop(int) to remove it from list
    if animal_index >= 0:
        ANIMALS.pop(animal_index)

def update_animal(id, new_animal):
    #iterate animals list but use enumerate() so you can access the index value of each item
    for index, animal in enumerate(ANIMALS):
        if animal["id"] == id:
            #found the animal, update the value
            ANIMALS[index] = new_animal
            break
