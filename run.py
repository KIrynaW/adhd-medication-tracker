import gspread
import datetime
from google.oauth2.service_account import Credentials
from colorama import init, Fore, Style
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

def primary_menu():
    """
    Display the primary menu where the user is introduced to the tracker and
    can input one of the options:
    1. Track current medication
    2. Create new medication tracking
    3. Exit
    """
    header_ascii = pyfiglet.figlet_format("Welcome to ADHD Medication Tracker", font="smslant")
    print(Fore.YELLOW + header_ascii)
    print(Fore.CYAN + "Please choose an option:\n")
    print("1. Track current medication")
    print("2. Create new medication tracking")
    print("3. Exit\n")

    choice = input(Fore.CYAN + "Make your choice (1/2/3): ")
    print(Fore.GREEN + f"Your choice is {choice}")

primary_menu()    
