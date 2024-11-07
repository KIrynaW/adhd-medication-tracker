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
        medication_name = input(Fore.YELLOW + "Enter the new medication name: \n" + Fore.RESET).capitalize()
        new_medication = SHEET.add_worksheet(title=medication_name, rows='100', cols='9')
        new_medication.append_row(
            ["Date", "Dose(mg)", "Intake per day", "First dose intake", "Second dose intake", "Third dose intake", "Efficacy(1-10)", "Side effects", "Personal observations"]
        )
        print(f"New medication '{medication_name}' successfully created")
        return new_medication
    except Exception as e:
        print(Fore.RED + f"Could not create a worksheet: {e}")

def validate_date(worksheet):
    """
    Logic that handles current date autofill 
    and skips it if the current date log was already filled
    """
    date_log = datetime.today().date().strftime("%d/%m/%Y")
    if worksheet.findall(date_log):
        print(Fore.RED + "Today's log already exists, skipping...")
        return False
    else:
        return date_log

#def past_date():
#    """
#    Logic to validate past date input and return error if the wrong format or future date is applied
#    """
#    while True:
#        date_choice = input("Create a log for a missed log date?: Y/N \n")
#        if 'n' in date_choice.lower():
#            print("Creating a log for today")
#            validate_date(worksheet)
#        else:
#            date_entry = input(Fore.LIGHTBLACK_EX +"Enter missed date in this format DD/MM/YYY: \n" + Fore.RESET)
#            today_date = datetime.today().date()
#            try:
#                date_entry = datetime.strptime(date_entry, "%d/%m/%Y") 
#                if date_entry.date() <= today_date:
#                    print(f"{date_entry} was successfully logged")
#                else:
#                    print(Fore.RED +"You have entered a future date. To enter a previous/missed log, past date must be entered")
#                break
#            except ValueError as error_creation_time:
#                print(Fore.RED + f" {date_entry} is an invalid date")
#    return date_entry.strftime("%d/%m/%Y")

def validate_dose():
    """
    Function that handles the dose input 
    """
    while True:
        try:
            dose_log = int(input(Fore.YELLOW + "Enter medication dose in (mg): \n" + Fore.RESET))
            if dose_log == int(0):
                print(Fore.RED + f"Medication dose cannot be {dose_log}, please enter a correct dose in (mg)")
            else:
                return dose_log
        except ValueError:
            print(Fore.RED + f"Medication dose cannot be {dose_log}, please enter a correct dose in (mg)")

def validate_intake():
    """
    Function to handle the medication intake input;
    user prompted to input medicationmfrequency and based on that
    the intake is adjusted
    """
    while True:
        frequency_log = int(input(Fore.YELLOW + "What is the frequency of the medication intake per day: \n" + Fore.RESET))
        if frequency_log > 3:
            print(Fore.RED + "The frequency is invalid, try again")
        else:
            break
    doses_log = ['None', 'None', 'None']
    for i in range(frequency_log):
        if "yes" in input(Fore.YELLOW + f"Have you taken dose {i+1} today (yes/no): \n" + Fore.RESET).lower():
            doses_log[i] = ("Yes")
        else:
            doses_log[i] = ("No")
    return [frequency_log, doses_log]

def validate_efficacy():
    while True:
        efficacy_log = int(input(Fore.YELLOW + "How effective did you find the medication (0-10)?: \n" + Fore.RESET))
        if efficacy_log <= int(10):
            return efficacy_log
        elif efficacy_log > int(10):
            print(Fore.RED + f"{efficacy_log} is above the grading range, please input (0-10)")
        else:
            print(Fore.RED + f"{efficacy_log} is not a number, please input (0-10)")


def new_log(SHEET):
    """
    Add current date to the selected worksheet
    """
    choose_medication = input(Fore.YELLOW + "Enter medication name you want to log: \n" + Fore.RESET).capitalize()
    try:
        medication_worksheet = SHEET.worksheet(choose_medication)
        if not validate_date(medication_worksheet):
            return
        else:
            date = validate_date(medication_worksheet)
            dose = validate_dose()
            frequency_log, doses_log = validate_intake()
            efficacy = validate_efficacy()
            medication_worksheet.append_row([
                date, dose, frequency_log, doses_log[0], doses_log[1], doses_log[2], efficacy, 
                ])
        # Add current date autofill
        print("Creating a log for today...")
        # get input arguments from user ...
        side_effects = input("Have you experienced any side effects today?: Y/N")
        personal_observation = input("Describe in short, personal observations regarding your experience: max 30 words")
    except gspread.exceptions.WorksheetNotFound:
        print(Fore.RED + f"Medication with a name'{choose_medication}'does not exist")
        add_medication(SHEET) # If medication does not exist you can opt to create new one
        

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
    choice = input(Fore.CYAN + "Make your choice (1 - 5) and press 'Enter': \n" + Fore.RESET)

    while True:
        if choice == "1":
            add_medication(SHEET)
        elif choice == "2":
            new_log(SHEET)

main()    