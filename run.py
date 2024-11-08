import os
import sys
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from colorama import init, Fore, Style
from tabulate import tabulate
import pyfiglet
import time

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

def menu():

    print(Fore.CYAN + "**** Main Menu ****\n")
    print(" 1. Add new medication")
    print(" 2. Create a new log")
    print(" 3. View medication logs")
    print(" 4. Evaluate efficacy")
    print(" 5. Exit\n")
    print("*" * 50)

def add_medication(SHEET):
    """
    Create a new worksheet with a new medication name and headings to log progress
    """
    while True:
        try:
            medication_name = input(Fore.YELLOW + "Enter the new medication name: \n" + Fore.RESET).capitalize()
            new_medication = SHEET.add_worksheet(title=medication_name, rows='100', cols='9')
            new_medication.append_row(
                ["Date", "Dose(mg)", "Intak(day)", "Dose 1", "Dose 2", "Dose 3", "Efficacy(0-10)", "Side effects", "Observations"]
            )
            print(Fore.GREEN + f"New medication '{medication_name}' successfully created\n")
            return new_medication
        except Exception as e:
            print(Fore.RED + f"Could not create a worksheet: {e}\n")

def validate_date(worksheet):
    """
    Logic that handles current date autofill 
    and skips it if the current date log was already filled
    """
    date_log = datetime.today().date().strftime("%d/%m/%Y")
    if worksheet.findall(date_log):
        print(Fore.RED + "Today's log already exists, skipping...\n")
        return False
    else:
        return date_log

def validate_dose():
    """
    Function that handles the dose input 
    """
    while True:
        try:
            dose_log = int(input(Fore.YELLOW + "Enter medication dose in (mg): \n" + Fore.RESET))
            if dose_log == 0:
                print(Fore.RED + f"Medication dose cannot be {dose_log}, please enter a correct dose in (mg)\n")
            else:
                return dose_log
        except Exception as e:
            print(Fore.RED + f"Medication dose cannot be a word or a letter, please enter a number in mg:\n")

def validate_intake():
    """
    Function to handle the medication intake input;
    user prompted to input medicationmfrequency and based on that
    the intake is adjusted
    """
    while True:
        frequency_log = int(input(Fore.YELLOW + "What is the frequency of the medication intake per day (1-3): \n" + Fore.RESET))
        if frequency_log > 3:
            print(Fore.RED + "The frequency is invalid, try again\n")
        else:
            break
    intake_log = ['None', 'None', 'None']
    for i in range(frequency_log):
        while True:
            dose_choice = input(Fore.YELLOW + f"Have you taken dose {i+1} today (yes/no): \n" + Fore.RESET).lower()
            if "yes" in dose_choice:
                intake_log[i] = ("Yes")
                break
            elif "no" in dose_choice:
                intake_log[i] = ("No")
                break
            else:
                print(Fore.RED + f"{dose_choice} is an invalid answer, please enter (yes/no)\n")
    return [frequency_log, intake_log]

def validate_efficacy():
    """
    Function that handles efficacy of medication input; 
    the user can rate the effectivnes from 0-10,
    if str or a int higher than 10 is input, it shows error
    """
    while True:

        try:
            efficacy_log = int(input(Fore.YELLOW + "How effective did you find the medication (0-10)?: \n" + Fore.RESET))
            if efficacy_log <= int(10):
                return efficacy_log
            elif efficacy_log > int(10):
                print(Fore.RED + f"{efficacy_log} is above the rating range, please enter (0-10)\n")
        except Exception as e:
                print(Fore.RED + f"Your input is invalid, please enter a number rating (0-10)\n")

def validate_side_effects():
    """
    Function that handles medication side effect input; 
    making sure it returns only a yes or a no string and triggers error if int is input
    """
    while True:
        side_effects_log = input(Fore.YELLOW + "Have you experienced any side effects today (yes/no)?: \n" + Fore.RESET).lower()
        if "yes" in side_effects_log:
            return "Yes"
        elif "no" in side_effects_log:
            return "No"
        else:
            print(Fore.RED + f"{side_effects_log} is an invalid answer, please enter (yes or no) answer\n") 

def validate_user_observation():
    """
    Function to handle users personal str input describing effects and observations;
    to prevent user from writing more than 35 words max. if limit is reached, shows error in logging
    """
    while True:
        observation_log = input(Fore.YELLOW + "Describe in short, personal observations regarding your experience taking the medication (max 20 words): \n" + Fore.RESET)
        isolate_words = observation_log.split()
        contains_words = any(word.isalpha() for word in isolate_words)
        if len(isolate_words) > 20:
            print(Fore.RED + "You have entered more than 30 words, please enter no more than 20 words\n")
        elif not contains_words:
            print(Fore.RED + f"You have entered '{observation_log}', please use words, not only numbers\n")
        else:
            return observation_log


def new_log(SHEET):
    """
    Function autofills current date, and appends user input(dose, 
    frequency of intake, doses taken/missed, presense of side effects, 
    and user observation) to an existing medication worksheer. 
    The function checks for existance of worksheet selected by the user,
    and offers the user to create new medication worksheet if it does not exist
    """
    choose_medication = input(Fore.YELLOW + "Enter medication name you want to log: \n" + Fore.RESET).capitalize()
    try:
        # Add current date autofill
        medication_worksheet = SHEET.worksheet(choose_medication)
        if not validate_date(medication_worksheet):
            return
        else:
            date = validate_date(medication_worksheet)
            dose = validate_dose()
            frequency_log, intake_log = validate_intake()
            efficacy = validate_efficacy()
            side_effects = validate_side_effects()
            user_observation = validate_user_observation()

            medication_worksheet.append_row([
                date, dose, frequency_log, intake_log[0], intake_log[1], intake_log[2], efficacy, side_effects, user_observation
                ])

        print(Fore.GREEN + "Creating a log for today.....\n")

    except gspread.exceptions.WorksheetNotFound:
        print(Fore.RED + f"Medication with a name'{choose_medication}'does not exist\n")
        add_medication(SHEET) # If medication does not exist you can opt to create new one


def view_medication_logs():
    """
    Function that retrieves and shows the user their chosen medication logs
    """

    try:
        find_medication = input(Fore.YELLOW + "Enter the name of medication which logs you want to view: \n" + Fore.RESET).capitalize()
        medication_info = SHEET.worksheet(find_medication)
        print(Fore.CYAN + f"You chose to view log history for '{find_medication}': \n")
        logs = medication_info.get_all_values()
        print(tabulate(logs, tablefmt="fancy_grid", maxcolwidths=[10,4,6,4,4,4,8,7,14], stralign="center"))

    except gspread.exceptions.WorksheetNotFound:
        print(Fore.RED + f"Medication with a name '{find_medication}' does not exist\n")

def exit_or_menu():
    """
    Function that handles return to Menu or Exit program
    """
    
    while True:

        print(" Press 1. to return to Menu:")
        print(" Press 2. to Exit.\n")
        select = input(Fore.CYAN + "Enter your choice (1 or 2): \n" + Fore.RESET)
        if select == "1":
            print(Fore.GREEN + "Returning to Main Menu")
            time.sleep(1)
            return
        elif select == "2":
            print(Fore.MAGENTA + "Exiting the ADHD Medication Tracker....See you soon!....\n")
            time.sleep(1)
            sys.exit()
        else:
            print(Fore.RED + "Invalid choice. Please enter 1 to return to Menu or 2 to Exit.")
            continue
        
def main():
    """
    Display the primary menu where the user is introduced to the tracker and
    can input one of the options
    """
    header_ascii = pyfiglet.figlet_format("Welcome to ADHD Medication Tracker", font="smslant")
    print(Fore.YELLOW + header_ascii)
    
    while True:
        menu()
        choice = input(Fore.CYAN + "Make your choice (1 - 5) and press 'Enter': \n" + Fore.RESET)
        if choice == "1":
            add_medication(SHEET)
            exit_or_menu()
        elif choice == "2":
            new_log(SHEET)
            exit_or_menu()
        elif choice == "3":
            view_medication_logs()
            exit_or_menu()

main()    