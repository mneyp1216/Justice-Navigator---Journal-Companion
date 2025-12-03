import justice_navigator_info
import pandas as pd
import numpy as np
import os
import datetime
from colorama import init, Fore, Back, Style      # type: ignore   
import colorama                                   # type: ignore

# auto reset to bring codes back to original coloring
autoreset=True                                    

def welcome_message():
    """introduction to journal"""
    print(f"\n{"="*14} Welcome to your Journal Companion {"="*15}\n")
    print(f"This is a private space to reflect on your journey.")
    print(f"All entries will be securely saved on your device.")
    print(f"Take your time, there's no rush.\n")

def user_info():
    """capture basic information from user"""
    print(f"As we begin this journey, let's get to know some more ...")

    # capture user name with validation
    while True:
        name = input("What is your first name, or what would like to be addressed as? ").strip()
        if name:
            break
        else:
            print(f"Please enter you name to continue.")

    # date capture for time stamps
    while True:
        start_date = input("When did you begin your journey? (MM/DD/YYYY) ")
        try:
            datetime.datetime.strptime(start_date, "%m/%d/%Y")
            break
        except ValueError:
            print(f"Please enter a valid date in MM/DD/YYYY format.")

    return name, start_date

def daily_reflection(name):
    """guide user through daily reflection"""
    print(f"\n Hello {name}, let's reflect on today...")

    # record date and time
    current_date = datetime.datetime.now().strftime("%m/%d/%Y")
    current_time = datetime.datetime.now().strftime("%I:%M %p")

    print(f"\nToday's Date: {current_date}")
    print(f"Current Time: {current_time}")

    # need to evaluate the daily questions with team, these are possible examples
    daily_questions = [
        "What's a positive thing that happened today?",
        "What made the day challenging, and how did you handle it?",
        "Did you connect with anyone today, how was that experience?",
        "What did you learn about yourself today?",
        "Is there is something that you are looking forward to tomorrow?",
        "What would you do differently tomorrow? ",
        "How are you feeling at this moment? (use 1-5 words)"
    ]

    # blank space for response
    answers = []

    for e, question in enumerate(daily_questions, 1):
        print(f"\n{e}. {question}")
        answer = input("Let me hear your thoughts: ")
        answers.append(answer)

        # user control to skip questions
        if e < len(daily_questions):
            skip = input("\nPress ENTER to continue or type 'SKIP' to finish: ")
            if skip.lower() == 'skip':
                # if SKIP, fill in the rest of the questions with "Skipped"
                for s in range(e, len(daily_questions)):
                    answers.append("Skipped")
                break

    return current_date, current_time, answers

def weekly_check_in(name):
    """Weekly checkin with deeper questions"""
    print(f"\n{name}, let's check-in...")

    weekly_questions = [
        "What do you feel was your biggest accomplishment this week? ",
        "What do you feel was the most challenging this week? ",
        "What support do you need right now? ",
        "What is one goal you would like to set for next week? ",
        "How have you grown of changed this week? "
    ]

    answers = []
    current_date = datetime.datetime.now().strftime("%m/%d/%Y")

    for e, question in enumerate(weekly_questions, 1):
        print(f"\n{e}. {question}")
        answer = input("Your response: ")
        answers.append(answer)

        # user control to skip questions
        if e < len(weekly_questions):
            skip = input("\nPress ENTER to continue or type 'SKIP' to finish: ")
            if skip.lower() == 'skip':
                # if SKIP, fill in the rest of the questions with "Skipped"
                for s in range(e, len(weekly_questions)):
                    answers.append("Skipped")
                break

    return current_date, answers

def save_entry(entry_type, date, time, content, name):
    """Create file for Journal Entries"""
    filename = f"{name}_journal.txt"

    with open(filename, "a") as file:
        file.write(f"\n{'='*64}\n")
        file.write(f"Entry Type: {entry_type}")
        file.write(f"Date: {date} | Time: {time}")
        file.write(f"\n{'='*64}\n")

        if entry_type == "Daily Reflection":
            questions = [
                "Positive moment: ",
                "Challenge handled: ",
                "Connections: ",
                "Self-discovery: ",
                "Looking forward: ",
                "Do differently: ",
                "Current feelings: "
            ]

            for e, (question, answer) in enumerate(zip(questions, content)):
                file.write(f"{e}. {question}{answer}\n")

        elif entry_type == "Weekly Check-in":
            questions = [
                "Biggest accomplishment: ",
                "Most challenging: ",
                "Support needed: ",
                "Goal for next week: ",
                "Personal goal: "
            ]

            for e, (question, answer) in enumerate(zip(questions, content)):
                file.write(f"{e}. {question}{answer}\n")

    print(f"\n{Fore.GREEN} √ Your entry has been saved to {filename}{Style.RESET_ALL}")

def view_previous_entries(name):
    """Review previous journal entries"""
    filename = f"{name}_journal.txt"

    if os.path.exists(filename):
        print(f"\n Here are your previous journal entires, {name}:\n")
        with open(filename, "r") as file:
            print(file.read())
    else:
        print(f"\nUnfortunately you have not saved a file yet. Your Journal is ready to listen when you are ready to say.")

def main():

    # counter for invalid numbers when on the dashboard.
    invalid_count = 0

    """Main program function"""
    welcome_message()

    # Gather user information 
    name, start_date = user_info()

    # Personalization of welcome
    print(f"\nWelcome, {name}! I am glad you are here.")
    print(f"Keep in mind, this is your journey - we'll take it one day at a time.")

    while True:
        print(f"{Fore.CYAN}\n{'='*64}")
        print(f"Hello {name}! What would you like to do? ")
        print(f"1) Daily Reflection")
        print(f"2) Weekly Check-in")
        print(f"3) View Previous Entries")
        print(f"4) Exit{Style.RESET_ALL}")

        choice = input("\n Please select (1-4): ")

        if invalid_count >= 3:
            break

        if choice == "1":
            date, time, answers = daily_reflection(name)
            save_entry("Daily Reflection", date, time, answers, name)

        elif choice == "2":
            date, answers = weekly_check_in(name)
            save_entry("Weekly Check-in", date, "Weekly", answers, name)

        elif choice == "3":
            view_previous_entries(name)

        elif choice == "4":
            print(f"\nThank you for doing an entry today, {name}.")
            print(f"Remember: Progress, not perfection. You've got this!")
            print(F"Hope to see you tomorrow.\n")
            break

        elif choice not in ["1", "2", "3", "4"]:
            print(f"\n{colorama.Fore.RED}{'='*10} That's the Wrong Number {'='*11}\n")
            print(f"Please choose one of the options shown (1-4){colorama.Style.RESET_ALL}")
            invalid_count += 1
            if invalid_count >= 3:
                print(f"\n{colorama.Fore.RED}You should have followed the rules, now you need to start over.{colorama.Style.RESET_ALL}\n")
                break

# Run the program
if __name__ == "__main__":
    main()