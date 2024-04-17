EMPLOYEES = [
    {
        "id": 1,
        "name": "Jenna Solis"
    }
]

def get_all_employees():
    return EMPLOYEES

# Function with a single parameter
def get_single_employee(id):
  # Variable to hold the found animal, if it exists
    requested_employee = None

  # Iterate the ANIMALS list above. Very similar to the
  # for..of loops you used in JavaScript.
    for employee in EMPLOYEES:
    # Dictionaries in Python use [] notation to find a key
    # instead of the dot notation that JavaScript used.
        if employee["id"] == id:
            requested_employee = employee
    return requested_employee

def create_employee(employee):
    max_id = EMPLOYEES[-1]["id"]

    new_id = max_id + 1

    employee["id"] = new_id

    EMPLOYEES.append(employee)

    return employee

def delete_employee(id):
    employee_index = -1

    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            employee_index = index

    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)
