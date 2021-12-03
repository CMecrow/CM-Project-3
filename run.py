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

def command_required():
    """
    Get a task number input from the user.
    Runs a while loop to ensure input entered is valid ie a number between 1-3
    """
    while True:
        print("Welcome to Tone Deaf Newcastle\n")
        print("[1]Sell Existing Event\n[2]Create Event\n[3]Generate Sales Report\n")
        command_input = input("Enter your task number from the list above: ")

        if validate_data(command_input):
            print("Correct")
            break

    return command_input
    validate_data(command_input)


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
        print(f"Invalid data: {e}")
        return False

    return True

command_required()
