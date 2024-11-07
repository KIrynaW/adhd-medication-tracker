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
        medication_name = input(Fore.LIGHTBLACK_EX + "Enter the new medication name: \n" + Fore.RESET).capitalize()
        new_medication = SHEET.add_worksheet(title=medication_name, rows='100', cols='9')
        new_medication.append_row(
            ["Date", "Dose(mg)", "Intake per day", "First dose intake", "Second dose intake", "Third dose intake", "Efficacy(1-10)", "Side effects", "Personal observations"]
        )
        print(f"New medication '{medication_name}' successfully created")
        return new_medication
    except Exception as e:
        print(f"Could not create a worksheet: {e}")

def validate_date(worksheet):
    """
    Logic that handles current date autofill 
    and skips it if the current date log was already filled
    """
    date_log = datetime.today().date().strftime("%d/%m/%Y")
    if worksheet.findall(date_log):
        print("Today's log already exists, skipping...")
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
            dose = int(input("Enter medication dose in mg: \n"))
            return dose
        except ValueError:
            print("Please enter a number")

def validate_intake():
    """
    Function to handle the medication intake input;
    user prompted to input medicationmfrequency and based on that
    the intake is adjusted
    """
    while True:
        intake_per_day = int(input("What is the frequency of the medication intake per day: \n"))
        if intake_per_day == 1:
            return intake_per_day
            first_dose_validation()
        elif intake_per_day == 2:
            return intake_per_day
        elif intake_per_day == 3:
            return intake_per_day
            # second_dose = input("Have you taken your second dose today: yes/no \n").lower()
            # third_dose = input("Have you taken your third dose today: yes/no \n").lower()
        else:
            print("The frequency is invalid, try again")

def first_dose_validation():
    """
    Function that handles first dose intake validation
    """
    while True:
        first_dose = input("Have you taken your first dose today: yes/no \n").lower()
        if "yes" in first_dose:
            return "Yes"
        else:
            return "No"


def new_log(SHEET):
    """
    Add current date to the selected worksheet
    """
    choose_medication = input(Fore.LIGHTBLACK_EX + "Enter medication name you want to log: \n" + Fore.RESET).capitalize()
    
    try:
        medication_worksheet = SHEET.worksheet(choose_medication)
        if not validate_date(medication_worksheet):
            return
        else:
            medication_worksheet.append_row([
                validate_date(medication_worksheet), 
                validate_dose(),
                validate_intake(),
                ])
        # Add current date autofill
        print("Creating a log for today...")
        # get input arguments from user ...
        
        efficacy = input("How effective did you find the medication?: (1-10)")
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
    choice = input(Fore.LIGHTBLACK_EX + "Make your choice (1 - 5) and press 'Enter': \n" + Fore.RESET)

    while True:
        if choice == "1":
            add_medication(SHEET)
        elif choice == "2":
            new_log(SHEET)

main()    