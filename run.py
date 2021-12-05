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
    User is displayed a list of on sale events, selects and event
    then inputs how many tickets they'd like to sell
    """
    events = SHEET.worksheet('sales').row_values(1)
    sales = SHEET.worksheet('sales')
    print(f"\nSell Existing Event:\n\n{events}\n")
    event_input = input("Enter event name from list above: ")

    if event_input in events:
        result = sales.find(event_input)
        print(result)
                       
    elif event_input not in events:
        raise ValueError(
            f"Please enter a valid event name from the list above, you entered {event_input}"
        )
    

        
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
            validate_data(command_input)            

    return command_input
    

def validate_data(value):
    """
    Validates the input from the user
    """
    try:
        if value not in ['1', '2', '3']:
            raise ValueError(
                f"Please enter a task number between 1-3. You entered {value}"
            )
    except ValueError as e:
        print(f"\nInvalid selection: {e}\n")
        return False

    return True

command_required()
