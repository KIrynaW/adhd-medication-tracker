import gspread
import datetime
from google.oauth2.service_account import Credentials
from colorama import init, Fore, Style
from pyfiglet import Figlet

# Initialize colorama library
init()

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("adhd_medication_tracker")

ritalin = SHEET.worksheet("Ritalin")

data = ritalin.get_all_values()
print(data)