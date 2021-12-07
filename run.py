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
    then inputs how many tickets they'd like to sell
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
                print(f"\nSelected Event: {event_input}\n")
                num_tickets = int(input("How many tickets would you like to purchase? "))
                if validate_tickets(num_tickets):
                    sales.update_cell(2, event_column, num_tickets + previous_sales)
                    capacity_num = int(capacity.cell(2, event_column).value)
                    availability.update_cell(2, event_column, capacity_num - (previous_sales + num_tickets))
                    amended_avail = int(availability.cell(2, event_column).value)
                    print(f"\n{num_tickets} successfuly sold for {event_input}. {amended_avail} left on sale.\n")
                    break    
                    
            if event_input not in events:
                raise ValueError(
                    f"Please enter a valid event name from the list above, you entered {event_input}"
                )
        except ValueError as e:
            print(f"\nInvalid selection: {e}\n")            
      
    
def command_required():
    """
    Get a task number input from the user.
    Runs a while loop to ensure input entered is valid ie a number between 1-3
    """
    while True:
        print("Welcome to Tone Deaf Newcastle\n")
        print("[1]Sell Existing Event\n[2]Create Event\n[3]Generate Sales Report\n")
        command_input = input("Enter your task number from the list above: ")

        if command_input == '1':
            sell_event()
            break
        elif command_input == '2':
            print("Create")
            break
        elif command_input == '3':
            print("Report")
            break
        else:
            validate_task(command_input)            

    return command_input
    

def validate_task(value):
    """
    Validates the input from the user
    """
    try:
        raise ValueError(
            f"Please enter a task number between 1-3. You entered {value}"
        )
    except ValueError as e:
        print(f"\nInvalid selection: {e}\n")
        return False

    return True

def validate_tickets(values):
    """
    """
    try:
        if int(values) >= 9:
            raise ValueError(
                f"This event has a ticket limit of 8"
            )
    except ValueError as e:
        print(f"\nInvalid entry: {e}, please try again")   
        return False

    return True    

command_required()
