# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('tone_deaf_newcastle')


def sell_event():
    """
    User is displayed a list of on sale events, selects an event
    then inputs how many tickets they'd like to sell.
    Validation on event selection occurs by pulling row data as a list
    Validation on availability occurs and either provides an error
    or provides confirmation of booking and displays remaining ticket count.
    """
    while True:
        events = SHEET.worksheet('sales').row_values(1)
        sales = SHEET.worksheet('sales')
        availability = SHEET.worksheet('availability')
        capacity = SHEET.worksheet('capacity')
        print(f"\nSell Existing Event:\n\n{events}\n")
        event_input = input("Enter event name from list above: ")

        try:
            if event_input in events:
                entered_event = sales.find(event_input)
                event_column = entered_event.col
                previous_sales = int(sales.cell(2, event_column).value)
                capacity_num = int(capacity.cell(2, event_column).value)
                print(f"\nSelected Event: {event_input}\n")
                num_tickets = int(input("How many tickets would you like to purchase? "))
                num_avail = int(availability.cell(2, event_column).value)
                try:
                    if validate_tickets(num_tickets):
                        if num_avail >= num_tickets:
                            sales.update_cell(2, event_column, num_tickets + previous_sales)
                            availability.update_cell(2, event_column, capacity_num - (previous_sales + num_tickets))
                            amended_avail = int(availability.cell(2, event_column).value)
                            print(f"\n{num_tickets} successfuly sold for {event_input}. {amended_avail} left on sale.\n")
                            break
                        else:
                            raise ValueError(
                                f"Not enough tickets available. Only {num_avail} remaining"
                            )
                except ValueError as e:
                    print(f"\nInvalid input: {e}\n")
                    break

            if event_input not in events:
                raise ValueError(
                    f"Please enter a valid event name from the list above, you entered {event_input}"
                )
        except ValueError as e:
            print(f"\nInvalid selection: {e}")
            break


def create_event():
    """
    The user can create an event to go on sale
    inputting event name and capacity with 
    availability being handled automatically.
    Also includes a confirmation print of the created event
    in a dictionary
    """
    sales = SHEET.worksheet('sales')
    availability = SHEET.worksheet('availability')
    capacity = SHEET.worksheet('capacity')
    row_len = len(sales.row_values(1))
    row_update = row_len + 1
    print("\nCreate Event:\n")
    new_event_name = input("Enter a name for your event: ")
    sales.update_cell(1, row_update, new_event_name)
    capacity.update_cell(1, row_update, new_event_name)
    availability.update_cell(1, row_update, new_event_name)
    ne_capacity_input = int(input(f"\nSet capacity for {new_event_name}: "))
    sales.update_cell(2, row_update, 0)
    capacity.update_cell(2, row_update, ne_capacity_input)
    availability.update_cell(2, row_update, ne_capacity_input)
    ne_details = {
        'Event': new_event_name,
        'Capacity': ne_capacity_input,
        'Sales': 0,
        'Availability': ne_capacity_input
    }
    print("\nEvent created:\n")
    for key, value in ne_details.items():
        print(key + ':', value)


def sales_report():
    """
    Creates a dictionary for each event then a nested dictionary
    within which displays Capacity, Sales and Availability
    Also includes print statements to improve readability of data
    """
    print("\nGenerating Sales Report...\n")
    events = SHEET.worksheet('sales').row_values(1)
    capacity_fig = SHEET.worksheet('capacity').row_values(2)
    sales_fig = SHEET.worksheet('sales').row_values(2)
    availability_fig = SHEET.worksheet('availability').row_values(2)
    report = {}

    for i, event in enumerate(events):
        report[event] = {
            'Capacity': capacity_fig[i],
            'Sales': sales_fig[i],
            'Availability': availability_fig[i]
        }

    for event_name, event in report.items():
        print(event_name + ':')
        for key, value in event.items():
            print('\t', key + ':', value)  # \t inserts a tab
        print("")


def command_required():
    """
    Get a task number input from the user.
    Runs a while loop to ensure input entered is valid ie a number between 1-3
    and also to continue programe runs even if input is incorrect
    """
    while True:
        print("Welcome to Tone Deaf Newcastle\n")
        print("[1] Sell Existing Event\n[2] Create Event\n[3] Generate Sales Report\n[4] Exit Program\n")
        command_input = input("Enter your task number from the list above: ")

        if command_input == '1':
            sell_event()
        elif command_input == '2':
            create_event()
        elif command_input == '3':
            sales_report()
        elif command_input == '4':
            print("\nGoodbye from Tone Deaf Newcastle!")
            break
        else:
            invalid_task(command_input)


def invalid_task(value):
    """
    Reports an invalid input from the user, guides them to a correct entry
    """
    try:
        raise ValueError(
            f"Please enter a task number between 1-4. You entered {value}"
        )
    except ValueError as e:
        print(f"\nInvalid selection: {e}\n")
        return False

    return True


def validate_tickets(values):
    """
    Enforces a ticket limit of 8 per purchase (industry standard)
    """
    try:
        if int(values) >= 9:
            raise ValueError(
                "This event has a ticket limit of 8"
            )
    except ValueError as e:
        print(f"\nInvalid entry: {e}, please try again")
        return False

    return True


command_required()
