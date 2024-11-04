import os
import sys
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from colorama import init, Fore, Style
from tabulate import tabulate
import pyfiglet

# Initialize colorama library
init(autoreset=True)

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("adhd_medication_tracker")


def add_medication(SHEET):
    """
    Create a new worksheet with a new medication name and headings to log progress
    """

    try:
        medication_name = input("Enter the new medication name: \n")
        new_medication = SHEET.add_worksheet(title=medication_name, rows='100', cols='9')
        new_medication.append_row(
            ["Date", "Dose(mg)", "Intake per day", "First dose intake", "Second dose intake", "Third dose intake", "Efficacy(1-10)", "Side effects", "Personal observations"]
        )
        print(f"New medication '{medication_name}' successfully created")
        return new_medication
    except Exception as e:
        print(f"Could not create a worksheet: {e}")
        


def main():
    """
    Display the primary menu where the user is introduced to the tracker and
    can input one of the options
    """
    header_ascii = pyfiglet.figlet_format("Welcome to ADHD Medication Tracker", font="smslant")
    print(Fore.YELLOW + header_ascii)
    print(Fore.CYAN + "Please choose an option:\n")
    print("1. Add new medication")
    print("2. Create a new log")
    print("3. View medication logs")
    print("4. Evaluate efficacy")
    print("5. Exit\n")

    while True:
        choice = input(Fore.CYAN + "Make your choice (1 - 5) and press 'Enter': \n")
        if choice == "1":
            add_medication(SHEET)

main()    