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

    print(Fore.CYAN + "********* Main Menu **********")
    print("*" * 30)
    print(" \n 1. Add new medication file")
    print(" 2. Create new day log")
    print(" 3. View medication logs")
    print(" 4. View medication statistics")
    print(" 5. Exit\n")
    print("*" * 30)


def add_medication(SHEET):
    """
    Create a new worksheet with a new medication /
    name and headings to log progress
    """
    print("You chose:", Fore.MAGENTA + "*** '1.Add new medication file' ***\n")

    while True:
        try:

            medication_name = input(
                Fore.YELLOW + "Enter the new medication name: \n" + Fore.RESET
            ).capitalize()
            if medication_name.isdigit():
                print(
                    Fore.RED + "Your input cannot be a number,",
                    Fore.RED + "please enter the name of new medication:\n",
                )
            elif medication_name.strip() == "":
                print(
                    Fore.RED + "Your input cannot be empty,",
                    Fore.RED + "please enter the new medication name:\n",
                )
            else:
                new_medication = SHEET.add_worksheet(
                    title=medication_name, rows="100", cols="9"
                )
                new_medication.append_row(
                    [
                        "Date",
                        "Dose(mg)",
                        "Intak(day)",
                        "Dose 1",
                        "Dose 2",
                        "Dose 3",
                        "Efficacy(0-10)",
                        "Side effects",
                        "Observations",
                    ]
                )
                print(
                    Fore.GREEN + f"New medication '{medication_name}'",
                    Fore.GREEN + "successfully created \n",
                )
                new_log_prompt()
                break

        except Exception as e:
            print(
                Fore.RED + f"Could not create a new medication file:",
                Fore.RED + f"a file '{medication_name}' already exists\n",
            )
            all_medication_names = [
                worksheet.title
                for worksheet in SHEET.worksheets()
                if not worksheet.title == "Results"
            ]
            print(Fore.CYAN + "All current medications:")
            print(tabulate(None, all_medication_names, tablefmt="orgtbl"))


def validate_date(worksheet):
    """
    Logic that handles current date autofill
    and skips it if the current date log was already filled
    """
    date_log = datetime.today().date().strftime("%d/%m/%Y")
    if worksheet.findall(date_log):
        print(Fore.RED + "Today's log already exists, skipping...\n")
        exit_or_menu()
        return
    else:
        return date_log


def validate_dose():
    """
    Function that handles the dose input
    """
    while True:
        try:
            dose_log = int(
                input(
                    Fore.YELLOW
                    + "Enter medication dose in (mg):\n"
                    + Fore.RESET)
            )
            if dose_log == 0:
                print(
                    Fore.RED + f"Medication dose cannot be {dose_log},",
                    Fore.RED + "please enter a correct dose in (mg)\n",
                )
            else:
                return dose_log
        except ValueError:
            print(
                Fore.RED + f"Medication dose cannot be a word or a letter,",
                Fore.RED + "please enter a number in mg:\n",
            )


def validate_intake():
    """
    Function to handle the medication intake input;
    user prompted to input medicationmfrequency and based on that
    the intake is adjusted
    """
    while True:
        try:
            frequency_log = int(
                input(
                    Fore.YELLOW
                    + "Enter the frequency of intake per day (1-3):\n"
                    + Fore.RESET
                )
            )
            if frequency_log > 3:
                print(Fore.RED + "The frequency is invalid, try again\n")
            elif frequency_log == 0:
                print(Fore.RED + "The frequency is invalid, try again\n")
            else:
                break
        except ValueError:
            print(Fore.RED + f"The frequency is invalid, try again\n")
    intake_log = ["None", "None", "None"]
    for i in range(frequency_log):
        while True:
            dose_choice = input(
                Fore.YELLOW
                + f"Have you taken dose {i+1} today (yes/no):\n"
                + Fore.RESET
            ).lower()
            if "yes" in dose_choice:
                intake_log[i] = "Yes"
                break
            elif "no" in dose_choice:
                intake_log[i] = "No"
                break
            else:
                print(
                    Fore.RED + f"{dose_choice} is an invalid answer,",
                    Fore.RED + "please enter (yes/no)\n",
                )
    return [frequency_log, intake_log]


def validate_efficacy():
    """
    Function that handles efficacy of medication input;
    the user can rate the effectivnes from 0-10,
    if str or a int higher than 10 is input, it shows error
    """
    while True:

        try:
            efficacy_log = int(
                input(
                    Fore.YELLOW
                    + "How effective did you find the medication (0 to 10)\n"
                    + Fore.RESET,
                )
            )
            if efficacy_log <= int(10):
                return efficacy_log
            elif efficacy_log > int(10):
                print(
                    Fore.RED + f"{efficacy_log} is above the rating range,",
                    Fore.RED + "please enter (0-10)\n",
                )

        except ValueError:
            print(Fore.RED + f"Invalid input, please enter a rating (0-10)\n")


def validate_side_effects():
    """
    Function that handles medication side effect input;
    making sure it returns only a yes or a no string and/
    triggers error if int is input
    """
    while True:
        side_effects_log = input(
            Fore.YELLOW
            + "Have you experienced any side effects today (yes/no)?: \n"
            + Fore.RESET
        ).lower()
        if "yes" in side_effects_log:
            return "Yes"
        elif "no" in side_effects_log:
            return "No"
        else:
            print(
                Fore.RED + f"{side_effects_log} is an invalid answer,",
                Fore.RED + "please enter (yes or no)\n",
            )


def validate_user_observation():
    """
    Function to handle users personal str input describing /
    effects and observations;to prevent user from writing more/
    than 20 words max. if limit is reached, shows error in logging
    """
    while True:
        observation_log = input(
            Fore.YELLOW
            + "Write a note regarding your experience taking the medication"
            + "(max 20 words):\n"
            + Fore.RESET,
        )
        isolate_words = observation_log.split()
        contains_words = any(word.isalpha() for word in isolate_words)
        if len(isolate_words) > 20:
            print(
                Fore.RED + "You have entered more than 20 words,",
                Fore.RED + "please enter no more than 20 words\n",
            )
        elif not contains_words:
            print(
                Fore.RED + f"You have entered '{observation_log}',",
                Fore.RED + "please use words.\n",
            )
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
    print("You chose:", Fore.MAGENTA + "*** '2.Create a new day log' ***\n")

    all_medication_names = [
        worksheet.title
        for worksheet in SHEET.worksheets()
        if not worksheet.title == "Results"
    ]
    print(Fore.CYAN + "All current medications:")
    print(tabulate(None, all_medication_names, tablefmt="orgtbl"))

    while True:

        try:

            choose_medication = input(
                            Fore.YELLOW
                            + "Enter medication name you want to log:\n"
                            + Fore.RESET
            ).capitalize()
            if choose_medication.strip() == "":
                print(
                    Fore.RED + "Your input cannot be empty,",
                    Fore.RED + "please enter medication you want to log:\n",
                )
            else:
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

                    medication_worksheet.append_row(
                        [
                            date,
                            dose,
                            frequency_log,
                            intake_log[0],
                            intake_log[1],
                            intake_log[2],
                            efficacy,
                            side_effects,
                            user_observation,
                        ]
                    )
                    print("\n", Fore.GREEN + "Creating a log for today.....\n")
                    exit_or_menu()
                    break

        except gspread.exceptions.WorksheetNotFound as e:
            print(Fore.RED + f"'{choose_medication} file does not exist'\n")
            new_medication_prompt()
            return


def new_medication_prompt():
    """
    A function that prompts a user to add a new medication if the
    data for input medication is not found
    """

    while True:

        all_medication_names = [
            worksheet.title
            for worksheet in SHEET.worksheets()
            if not worksheet.title == "Results"
        ]
        print(Fore.CYAN + "All current medications:")
        print(tabulate(None, all_medication_names, tablefmt="orgtbl"))

        add_medication_prompt = input(
            Fore.YELLOW
            + "Would you like to add new medication? Type (yes or no): \n"
            + Fore.RESET
        ).lower()
        if "yes" in add_medication_prompt:
            add_medication(SHEET)
            break
        elif "no" in add_medication_prompt:
            exit_or_menu()
            break
        else:
            print(Fore.RED + "The input is invalid, please type (yes or no)\n")


def new_log_prompt():
    """
    A function that prompts a user to make a log for today
    when the user creates a new medication or views the list of logs
    """
    while True:

        create_log = input(
            Fore.YELLOW
            + "Would you like to create a log for today? Enter (yes/no): \n"
            + Fore.RESET
        ).lower()
        if "yes" in create_log:
            new_log(SHEET)
            break
        elif "no" in create_log:
            exit_or_menu()
            break
        else:
            print(Fore.RED + "Invalid input, please enter (yes or no)\n")


def view_medication_logs():
    """
    Function that retrieves and shows the user their chosen medication log date
    """
    print("You chose:", Fore.MAGENTA + "****3 - 'View medication logs' ****\n")

    try:

        find_medication = input(
            Fore.YELLOW
            + "Enter the name of medication which logs you want to view:\n"
            + Fore.RESET
        ).capitalize()
        log_data = SHEET.worksheet(find_medication)
        print(Fore.CYAN + f"Showing log history for '{find_medication}':\n")

        while True:

            try:
                date_input = input(
                    Fore.YELLOW
                    + "Enter the log date you want to view (DD/MM/YYYY): \n"
                    + Fore.RESET
                )
                entered_date = datetime.strptime(date_input, "%d/%m/%Y").date()
                log_values = log_data.get_all_values()

                sift_data = []

                for row in log_values[1:]:
                    date_row = datetime.strptime(row[0], "%d/%m/%Y").date()
                    if date_row == entered_date:
                        sift_data.append(row)
                        continue

                if not sift_data:
                    print(Fore.RED + f"No data found for {entered_date}\n")
                else:
                    headers = log_values[0]
                    data = sift_data[0]
                    for i in range(len(headers)):
                        print(f"{headers[i]}:", Fore.MAGENTA + f"{data[i]}")
                    exit_or_menu()
                    return
            except ValueError:
                print(
                    Fore.RED + f"Date format is invalid,",
                    Fore.RED + "please enter the date in (DD/MM/YYYY)\n",
                )

    except gspread.exceptions.WorksheetNotFound as e:
        print(Fore.RED + f"Medication '{find_medication}' does not exist \n")
        new_medication_prompt()


def calculate_medication_statistics():
    """
    Pull data from Google Sheets and calculate missed days,
    side effects, and average efficacy
    """
    print(
        "You chose:",
        Fore.MAGENTA + "*** '4.View medication statistics' ***\n",
    )

    try:
        all_medication_names = [
            worksheet.title
            for worksheet in SHEET.worksheets()
            if not worksheet.title == "Results"
        ]
        print(Fore.CYAN + "All current medications:")
        print(tabulate(None, all_medication_names, tablefmt="orgtbl"))

        search_medication = input(
            Fore.YELLOW
            + "Enter the name of medication you would like to evaluate: \n"
            + Fore.RESET
        ).capitalize()
        evaluation_data = SHEET.worksheet(search_medication)

        medication_data = evaluation_data.get_all_values()
        headers = medication_data[0]
        rows = medication_data[1:]

        # initialise counting
        days_total = 0
        missed_dose_one = 0
        missed_dose_two = 0
        missed_dose_three = 0
        missed_doses_days = 0
        side_effect_days = 0
        efficacy_total = 0
        efficacy_counted = 0

        for row in rows:
            date = row[headers.index("Date")]
            dose_one = row[headers.index("Dose 1")].lower()
            dose_two = row[headers.index("Dose 2")].lower()
            dose_three = row[headers.index("Dose 3")].lower()
            efficacy = row[headers.index("Efficacy(0-10)")]
            side_effects = row[headers.index("Side effects")].lower()

            if "2024" in date:
                days_total += 1

            if dose_one == "no":
                missed_dose_one += 1

            if dose_two == "no":
                missed_dose_two += 1

            if dose_three == "no":
                missed_dose_three += 1

            if dose_one == "no" or dose_two == "no" or dose_three == "no":
                missed_doses_days += 1

            if side_effects == "yes":
                side_effect_days += 1

            # total efficacy calculation
            try:
                efficacy_value = int(efficacy)
                if 0 <= efficacy_value <= 10:  # Efficacy range
                    efficacy_total += efficacy_value
                    efficacy_counted += 1
            except ValueError:
                continue  # if not valid number, ignore

        # Average efficacy equation
        efficacy_average = (
            efficacy_total / efficacy_counted if efficacy_counted > 0 else 0
        )
        # Convert to a whole number
        round_efficacy_average = round(efficacy_average)

        results_list = [
            search_medication,
            days_total,
            missed_dose_one,
            missed_dose_two,
            missed_dose_three,
            missed_doses_days,
            round_efficacy_average,
            side_effect_days,
        ]

        results_sheet = SHEET.worksheet("Results")
        results_sheet.append_row(results_list)

        print(Fore.CYAN + f"Showing statistics for '{search_medication}':\n")
        print("Days evaluated:", Fore.MAGENTA + f"{days_total}")
        print(f"Missed first doses:", Fore.MAGENTA + f"{missed_dose_one}")
        print(f"Missed second doses:", Fore.MAGENTA + f"{missed_dose_two}")
        print(f"Missed third doses:", Fore.MAGENTA + f"{missed_dose_three}")
        print(f"Incoplete intake days:", Fore.MAGENTA + f"{missed_doses_days}")
        print(f"Average efficacy:", Fore.MAGENTA + f"{round_efficacy_average}")
        print(f"Side effect days:", Fore.MAGENTA + f"{side_effect_days}\n")
        print(Fore.GREEN + f"Saving results....\n")

        exit_or_menu()
        return

    except gspread.exceptions.WorksheetNotFound as e:
        print(Fore.RED + f"Medication '{search_medication}' does not exist\n")
        new_medication_prompt()


def exit_or_menu():
    """
    Function that handles return to Menu or Exit program
    """

    while True:
        print(Fore.CYAN + "*" * 38)
        print("\n 1. Return to Main Menu:")
        print(" 2. Exit.\n")
        select = input(Fore.CYAN + "Enter a choice (1 or 2): \n" + Fore.RESET)
        if select == "1":
            print(Fore.GREEN + "Returning to Main Menu....\n")
            time.sleep(1)
            return
        elif select == "2":
            print(Fore.MAGENTA + "Exiting ADHD Medication Tracker...Bye!...\n")
            time.sleep(1)
            sys.exit()
        else:
            print(Fore.RED + "Invalid choice. Please enter (1 or 2)\n")


def main():
    """
    Display the primary menu where the user is introduced to the tracker and
    can input one of the options
    """
    header_ascii = pyfiglet.figlet_format(
        "Welcome to ADHD Medication Tracker", font="smslant"
    )
    print(Fore.YELLOW + header_ascii)

    results_sheet = None
    for worksheet in SHEET.worksheets():
        if worksheet.title == "Results":
            results_sheet = SHEET.worksheet("Results")
    if not results_sheet:
        results_sheet = SHEET.add_worksheet(
            title="Results", rows="100", cols="9"
            )
        results_sheet.append_row(
            [
                "Medication",
                "Evaluated days",
                "Missed doses 1",
                "Missed doses 2",
                "Missed doses 3",
                "Incomplete intake days",
                "Average efficiacy",
                "Side effects days",
            ]
        )

    while True:
        menu()
        choice = input(Fore.CYAN + "Enter your choice (1 - 5):\n" + Fore.RESET)
        if choice == "1":
            add_medication(SHEET)
        elif choice == "2":
            new_log(SHEET)
        elif choice == "3":
            view_medication_logs()
        elif choice == "4":
            calculate_medication_statistics()
        elif choice == "5":
            print(
                Fore.MAGENTA + "You chose to exit the program...",
                Fore.MAGENTA + "Shutting down...Goodbye...\n",
            )
            break
        else:
            print(Fore.RED + "Invalid choice, please enter (1-5): \n")


main()
