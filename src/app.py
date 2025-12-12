import justice_navigator_info
import pandas as pd
import numpy as np
import os
import datetime
import time
from colorama import init, Fore, Back, Style      # type: ignore   
import colorama                                   # type: ignore
from rules import validate_choice, parse_cli_args, process_cli_args
from decision_table import decision_table
from mood_assessment import assess_mood, display_mood_scale
from chatbot import chatbot   
                   

init(autoreset=True)

# New version, added AI and Chat Mode feature
__version__ = "1.3.0"  

def welcome_message():
    """introduction to journal"""
    print(f"\n{'='*14}Welcome to your Journal Companion{'='*15}\n")
    print(f"This is a private space to reflect on your journey.")
    print(f"All entries will be securely saved on your device.")
    print(f"Take your time, there's no rush.\n")

def initial_mood_assessment():
    """
    Assess user's mood immediately upon opening the application
    """
    print(f"\n{Fore.BLUE}{'='*64}")
    print(f"{Fore.BLUE}{'='*21}INITIAL MOOD CHECK-IN{'='*22}")
    print(f"{Fore.BLUE}{'='*64}{Style.RESET_ALL}")
    
    print(f"\nBefore we begin, let's check in with how you're feeling right now.\n")
    
    # Display mood scale
    print(display_mood_scale())
    
    while True:
        mood_input = input(f"\n{Fore.GREEN}How are you feeling? (1-5 or keyword): ").strip()
        mood_result = assess_mood(mood_input)
        
        if mood_result:
            mood_level = mood_result['level']
            mood_description = mood_result['description']
            
            print(f"\n{Fore.YELLOW}✓ Mood recorded: {mood_description}{Style.RESET_ALL}")
            
            # Chatbot response
            print(f"\n{Fore.CYAN}Journal Companion:{Style.RESET_ALL}")
            response = chatbot.get_empathetic_response(mood_level, mood_description)
            print(f"{Fore.GREEN}{response}{Style.RESET_ALL}")
            
            return mood_result
        else:
            print(f"{Fore.RED}Invalid input. Please use 1-5 or a keyword.{Style.RESET_ALL}")

def user_info():
    """capture basic information from user"""
    print(f"As we begin this journey, let's get to know some more ...")

    # capture user name with validation
    while True:
        name = input("What is your first name, or what would like to be addressed as? ").strip()
        if name:
            break
        else:
            print(f"Please enter your name to continue.")

    # date capture for time stamps/ updated to an auto timestamp
    start_date = datetime.datetime.now().strftime("%m/%d/%Y")

    return name, start_date

def daily_reflection(name, initial_mood=None):
    """guide user through daily reflection with mood assessment"""
    print(f"\n Hello {name}, let's reflect on today...")

    # record date and time
    current_date = datetime.datetime.now().strftime("%m/%d/%Y")
    current_time = datetime.datetime.now().strftime("%I:%M %p")

    print(f"\nToday's Date: {current_date}")
    print(f"Current Time: {current_time}")
    
    # Mood Assessment integration
    if initial_mood:
        print(f"\n{Fore.CYAN}Initial Mood (from start of session):")
        print(f"{Fore.YELLOW}{initial_mood['description']}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Let's check in with your mood...")
    print(display_mood_scale())
    
    while True:
        mood_input = input(f"\n{Fore.GREEN}How are you feeling right now? (1-5 or keyword): ").strip()
        current_mood = assess_mood(mood_input)
        
        if current_mood:
            current_level = current_mood['level']
            current_description = current_mood['description']
            
            # Compare with initial mood if available
            if initial_mood:
                mood_change = current_level - initial_mood['level']
                
                print(f"\n{Fore.YELLOW}✓ Current mood: {current_description}{Style.RESET_ALL}")
                
                # Provide response based on mood change
                if mood_change < 0:
                    print(f"\n{Fore.CYAN}I notice you're feeling a bit lower than when we started.")
                    print(f"That's okay - let's explore what's coming up for you.{Style.RESET_ALL}")
                elif mood_change > 0:
                    print(f"\n{Fore.CYAN}Great to see an improvement in how you're feeling!")
                    print(f"Let's build on this positive shift.{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.CYAN}Your mood has remained steady since we started.{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.YELLOW}✓ Mood recorded: {current_description}{Style.RESET_ALL}")
            
            # Chatbot response
            print(f"\n{Fore.CYAN}Journal Companion:{Style.RESET_ALL}")
            response = chatbot.get_empathetic_response(current_level, current_description)
            print(f"{Fore.GREEN}{response}{Style.RESET_ALL}")
            
            # Optional: Offer additional support
            support_offer = chatbot.offer_support(current_level)
            print(f"\n{Fore.CYAN}{support_offer} (yes/no){Style.RESET_ALL}")
            user_choice = input().strip().lower()
            if user_choice in ['yes', 'y', 'yeah']:
                print(f"\n{Fore.GREEN}Let's explore that together...{Style.RESET_ALL}")
                # Offer follow-up questions
                questions = chatbot.get_followup_questions(current_level)
                print(f"\n{Fore.YELLOW}Here are some questions for reflection:{Style.RESET_ALL}")
                for i, question in enumerate(questions[:3], 1):  # Show first 3 questions
                    print(f"\n{i}. {question}")
                    response = input(f"Your thoughts (or press Enter to skip): ").strip()
                    if response:
                        # Optional: You could save these responses
                        pass
                print(f"\n{Fore.GREEN}✓ Reflection completed{Style.RESET_ALL}")
            
            break
        else:
            print(f"{Fore.RED}Invalid mood input. Please use 1-5 or a keyword.{Style.RESET_ALL}")

    # daily questions
    daily_questions = [
        "What's a positive thing that happened today?",
        "What made the day challenging, and how did you handle it?",
        "Did you connect with anyone today, how was that experience?",
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

    return current_date, current_time, answers, current_mood

def weekly_check_in(name):
    """Weekly checkin with deeper questions"""
    print(f"\n{name}, let's check-in...")

    weekly_questions = [
        "What do you feel was your biggest accomplishment this week? ",
        "What do you feel was the most challenging this week? ",
        "What support do you need right now? ",
        "What is one goal you would like to set for next week? ",
        "How have you grown or changed this week? "
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

def chat_mode(name, initial_mood=None):
    """
    New Chat Mode - Allows users to have a conversation with the companion
    """
    print(f"\n{Fore.CYAN}{'='*64}")
    print(f"CHAT MODE - Talk with your Journal Companion")
    print(f"{'='*64}{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}Hello {name}! I'm here to listen and chat.")
    print(f"You can talk about anything - your day, feelings, thoughts, or just chat.")
    print(f"Type 'exit' to return to the main menu, or 'help' for commands.{Style.RESET_ALL}")
    
    # Initialize conversation history
    conversation_history = []
    
    # Add greeting to history
    greeting = f"User: Hello {name}! Ready to chat?"
    conversation_history.append(greeting)
    
    # Get initial mood for context
    if initial_mood:
        mood_context = f"User's current mood: {initial_mood['description']}"
        conversation_history.append(mood_context)
    
    print(f"\n{Fore.YELLOW}Journal Companion:{Style.RESET_ALL} Hi {name}! How are you feeling today?")
    
    message_count = 0
    max_messages = 25  # Prevent infinite loops
    
    while message_count < max_messages:
        try:
            # Get user input
            user_input = input(f"\n{Fore.GREEN}You: {Style.RESET_ALL}").strip()
            
            # Check for exit command
            if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print(f"\n{Fore.CYAN}Journal Companion:{Style.RESET_ALL} Thanks for chatting, {name}! I'm here whenever you need to talk.")
                save_chat_conversation(name, conversation_history)
                break
            
            # Check for help command
            elif user_input.lower() in ['help', 'commands', '?']:
                show_chat_help()
                continue
            
            # Check for mood check
            elif user_input.lower() in ['mood', 'how am i feeling', 'check mood']:
                mood_result = quick_mood_check(name)
                if mood_result:
                    user_input = f"I'm feeling {mood_result['description'].lower()}"
            
            # Check for journal summary
            elif user_input.lower() in ['summary', 'recap', 'my journal']:
                summary = get_journal_summary(name)
                user_input = f"Tell me about my journal: {summary}"
            
            # Add user input to conversation history
            conversation_history.append(f"You: {user_input}")
            
            # Get chatbot response
            print(f"\n{Fore.YELLOW}Journal Companion:{Style.RESET_ALL} ", end="")
            
            # Simulate thinking/ love this feature
            time.sleep(0.5)
            
            # Get response based on conversation history
            response = chatbot.get_chat_response(user_input, conversation_history, initial_mood)
            print(f"{Fore.GREEN}{response}{Style.RESET_ALL}")
            
            # Add response to conversation history
            conversation_history.append(f"Companion: {response}")
            
            message_count += 1
            
            # Check if we should offer to save
            if message_count % 10 == 0:
                save_option = input(f"\n{Fore.CYAN}Would you like to save this conversation to your journal? (yes/no): {Style.RESET_ALL}").strip().lower()
                if save_option in ['yes', 'y']:
                    save_chat_conversation(name, conversation_history)
                    conversation_history = []  # Reset history after saving
            
            # instead of a skip key, this will allow the user to exit from chat conversation
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Returning to main menu...{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"\n{Fore.RED}Error in chat: {e}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Journal Companion:{Style.RESET_ALL} I'm having trouble. Let's start fresh.")
    
    if message_count >= max_messages:
        print(f"\n{Fore.YELLOW}We've had a long chat! Let's take a break.{Style.RESET_ALL}")
        save_chat_conversation(name, conversation_history)

def quick_mood_check(name):
    """Quick mood check for chat mode"""
    print(f"\n{Fore.CYAN}Quick Mood Check:{Style.RESET_ALL}")
    print(display_mood_scale())
    
    mood_input = input(f"\n{Fore.GREEN}How are you feeling? (1-5 or keyword): {Style.RESET_ALL}").strip()
    mood_result = assess_mood(mood_input)
    
    if mood_result:
        print(f"\n{Fore.YELLOW}✓ Mood noted: {mood_result['description']}{Style.RESET_ALL}")
        return mood_result
    else:
        print(f"{Fore.RED}Couldn't assess mood. Let's continue chatting.{Style.RESET_ALL}")
        return None

def get_journal_summary(name):
    """Get a quick summary of journal entries for chat context"""
    filename = f"{name}_journal.txt"
    
    if not os.path.exists(filename):
        return "You haven't made any journal entries yet."
    
    try:
        with open(filename, 'r') as file:
            content = file.read()
            
        daily_count = content.count("Entry Type: Daily Reflection")
        weekly_count = content.count("Entry Type: Weekly Check-in")
        
        return f"You have {daily_count} daily entries and {weekly_count} weekly check-ins."
    except:
        return "I can see you have some journal entries."

def show_chat_help():
    """Show chat mode help commands"""
    print(f"\n{Fore.CYAN}{'='*64}")
    print(f"{'='*22}CHAT MODE COMMANDS{'='*21}")
    print(f"{'='*64}{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}Available commands:{Style.RESET_ALL}")
    print(f"  • {Fore.GREEN}exit/quit/bye{Style.RESET_ALL} - Return to main menu")
    print(f"  • {Fore.GREEN}help/commands{Style.RESET_ALL} - Show this help")
    print(f"  • {Fore.GREEN}mood{Style.RESET_ALL} - Quick mood check")
    print(f"  • {Fore.GREEN}summary/recap{Style.RESET_ALL} - Get journal summary")
    print(f"\n{Fore.CYAN}You can talk about:{Style.RESET_ALL}")
    print(f"  • Your day, feelings, or thoughts")
    print(f"  • Journal entries or reflections")
    print(f"  • Goals, challenges, or achievements")
    print(f"  • Anything on your mind!")

def save_chat_conversation(name, conversation_history):
    """Save chat conversation to journal"""
    if not conversation_history:
        print(f"\n{Fore.YELLOW}No conversation to save.{Style.RESET_ALL}")
        return
    
    filename = f"{name}_journal.txt"
    current_time = datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")
    
    try:
        with open(filename, "a") as file:
            file.write(f"\n{'='*64}\n")
            file.write(f"Entry Type: Chat Conversation\n")
            file.write(f"Date: {current_time}\n")
            file.write(f"{'='*64}\n")
            
            for line in conversation_history[-10:]:                 # Save last 10 messages
                file.write(f"{line}\n")
            
            file.write(f"{'='*64}\n")
        
        print(f"\n{Fore.GREEN}✓ Chat conversation saved to your journal!{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"\n{Fore.RED}Error saving conversation: {e}{Style.RESET_ALL}")
        return False

def save_entry(entry_type, date, time, content, name, mood=None):
    """Create file for Journal Entries"""
    filename = f"{name}_journal.txt"

    with open(filename, "a") as file:
        file.write(f"\n{'='*64}\n")
        file.write(f"Entry Type: {entry_type}\n")
        file.write(f"Date: {date} | Time: {time}\n")
        if mood:
            file.write(f"Mood: {mood['description']}\n")
        file.write(f"{'='*64}\n")

        if entry_type == "Daily Reflection":                    # Reduced from 7 questions to 5
            daily_questions = [
                "Positive moment: ",
                "Challenge handled: ",
                "Connections: ",
                "Do differently: ",
                "Current feelings: "
            ]

            for e, (question, answer) in enumerate(zip(daily_questions, content)):
                file.write(f"{question}{answer}\n")

        elif entry_type == "Weekly Check-in":
            weekly_questions = [
                "Biggest accomplishment: ",
                "Most challenging: ",
                "Support needed: ",
                "Goal for next week: ",
                "Personal growth: "
            ]

            for e, (question, answer) in enumerate(zip(weekly_questions, content)):
                file.write(f"{question}{answer}\n")
        
        elif entry_type == "Chat Conversation":
            for line in content:
                file.write(f"{line}\n")
    
    print(f"\n{Fore.GREEN}✓ Your entry has been saved to {filename}")

def view_previous_entries(name):
    """Review previous journal entries"""
    filename = f"{name}_journal.txt"

    if os.path.exists(filename):
        print(f"\nHere are your previous journal entries, {name}:\n")
        with open(filename, "r") as file:
            print(file.read())
    else:
        print(f"\nUnfortunately you have not saved a file yet. Your Journal is ready to listen when you are ready to say.")

def generate_weekly_recap(name):
    """Generate weekly recap from journal entries"""
    print(f"\n{Fore.CYAN}Generating your weekly recap, {name}...{Style.RESET_ALL}")
    
    filename = f"{name}_journal.txt"
    
    if not os.path.exists(filename):
        print(f"{Fore.YELLOW}No journal entries found yet. Start journaling to get a weekly recap!{Style.RESET_ALL}")
        return
    
    # Read and parse journal entries
    entries = []
    try:
        with open(filename, 'r') as file:
            content = file.read()
            
        # Count entries
        daily_count = content.count("Entry Type: Daily Reflection")
        weekly_count = content.count("Entry Type: Weekly Check-in")
        chat_count = content.count("Entry Type: Chat Conversation")
        total_entries = daily_count + weekly_count + chat_count
        
        print(f"\n{Fore.GREEN}Found {total_entries} journal entries ({daily_count} daily, {weekly_count} weekly, {chat_count} chat).{Style.RESET_ALL}")
        
        # Create entry structure for chatbot
        entries.append({
            'date': datetime.datetime.now().strftime("%m/%d/%Y"),
            'entry_count': total_entries,
            'daily_count': daily_count,
            'weekly_count': weekly_count,
            'chat_count': chat_count,
            'note': f"User has {total_entries} journal entries."
        })
        
    except Exception as e:
        print(f"{Fore.RED}Error reading journal file: {e}{Style.RESET_ALL}")
        entries = []
    
    # Generate recap using chatbot/ a great way for user to 
    recap = chatbot.generate_weekly_recap(entries)
    
    print(f"\n{Fore.CYAN}{'='*64}")
    print(f"{'='*22}WEEKLY RECAP{'='*22}")
    print(f"{'='*64}{Style.RESET_ALL}")
    print(f"\n{recap}")
    print(f"\n{Fore.CYAN}{'='*64}{Style.RESET_ALL}")
    
    # Ask if user wants to save the recap
    save = input(f"\n{Fore.YELLOW}Save this recap to your journal? (yes/no): {Style.RESET_ALL}").strip().lower()
    if save in ['yes', 'y']:
        with open(filename, 'a') as file:
            file.write(f"\n\n{'-'*64}\n")
            file.write(f"Weekly Recap - {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}\n")
            file.write(f"{'-'*64}\n")
            file.write(f"{recap}\n")
            file.write(f"{'-'*64}\n")
        print(f"{Fore.GREEN}✓ Recap saved to your journal!{Style.RESET_ALL}")

def main():
    """Main program function with CLI support"""
    
    # Parse command line arguments
    args = parse_cli_args()
    cli_results = process_cli_args(args)
    
    # Handle CLI actions
    if cli_results['action'] == 'version':
        print(f"Journal Companion v{__version__}")
        print("Created with care for reflective practice")
        print("Now with empathetic Chatbot and Chat Mode support! 💭")
        return
    
    if cli_results['action'] == 'show_scale':
        print(display_mood_scale())
        return
    
    if cli_results['action'] == 'test':
        print("Running unit tests...")
        # Try to import and run chatbot tests
        try:
            from test.test_chatbot import run_tests
            run_tests()
        except ImportError:
            print("Chatbot test module not found.")
            # Run basic functionality test
            test_mood = assess_mood("3")
            print(f"Basic test: Mood assessment working - {test_mood}")
        return
    
    if cli_results['action'] == 'exit':
        return
    
    # Store initial mood if provided via CLI
    initial_mood = cli_results.get('mood', None)
    
    # Show chatbot status
    print(f"\n{Fore.CYAN}Journal Companion Chatbot: ")
    if hasattr(chatbot, 'ai_enabled') and chatbot.ai_enabled:
        print(f"{Fore.GREEN}✓ AI Chatbot enabled - I'm here to support you!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}✓ Empathetic responses enabled - Ready to listen{Style.RESET_ALL}")
    
    # Highlight New Feautre
    print(f"\n{Fore.MAGENTA}✨ NEW: Chat Mode available! Select option 6 to have a conversation. ✨{Style.RESET_ALL}")
    
    # Initial mood assessment
    if not initial_mood:
        initial_mood = initial_mood_assessment()
    else:
        print(f"\n{Fore.CYAN}Initial mood from command line: {initial_mood['description']}{Style.RESET_ALL}")
        # Provide response to CLI mood
        print(f"\n{Fore.CYAN}Journal Companion:{Style.RESET_ALL}")
        response = chatbot.get_empathetic_response(initial_mood['level'], initial_mood['description'])
        print(f"{Fore.GREEN}{response}{Style.RESET_ALL}")
    
    welcome_message()

    # Gather user information 
    name, date = user_info()

    # Personalization of welcome
    print(f"\nWelcome, {name}! I am glad you are here.")
    print(f"Keep in mind, this is your journey - we'll take it one day at a time.")

    # counter for invalid numbers when on the dashboard.
    invalid_count = 0

    while True:
        print(f"\n{'='*64}\n")
        print(f"Hello {name}! What would you like to do? ")
        print(f"\n{'='*64}\n")

        # UPDATED decision table - display valid choices INCLUDING CHAT MODE
        print(f"  [1, 'one', 'daily']    - Start a Daily Reflection")
        print(f"  [2, 'two', 'weekly']   - Complete Weekly Check-in")
        print(f"  [3, 'three', 'view']   - View Previous Entries")
        print(f"  [4, 'four', 'recap']   - Get Weekly Recap")
        print(f"  [5, 'five', 'chat']    - Chat with Companion (NEW!)")
        print(f"  [6, 'six', 'exit']     - Exit the Program")
        print(f"\n{'-'*64}{Style.RESET_ALL}")

        choice = input("\n Please select (1-6): ").strip()

        # use decision table to evaluate choice
        rule = decision_table.evaluate(choice)

        # check if choice is invalid (Default rule)
        if rule["rule_number"] == "Default":
            print(f"\n{Fore.RED}{'-'*23}Invalid Selection{'-'*24}\n")
            print(f"'{choice}' is not a valid option.")
            print(f"Please choose one of the options shown above {Style.RESET_ALL}")
            invalid_count += 1

            # check if too many invalid attempts
            if invalid_count >= 3:
                print(f"\n{Fore.RED}{'-'*11}Too many invalid attempts ({invalid_count}/3).{'-'*12}")
                print(f"The program will now exit to prevent misuse.")
                print(f"Please restart when you're ready.{Style.RESET_ALL}\n")
                break
            continue

        # process valid choices based on decision table rule
        print(f"\n{Fore.GREEN} {rule['output_message']}{Style.RESET_ALL}")

        if rule["rule_number"] == "R1":         # Daily Reflection
            date, time, answers, mood = daily_reflection(name, initial_mood)
            save_entry("Daily Reflection", date, time, answers, name, mood)
            invalid_count = 0                   # Reset on successful action
            initial_mood = None                 # Clear initial mood after first use

        elif rule["rule_number"] == "R2":       # Weekly Check-in
            date, answers = weekly_check_in(name)
            save_entry("Weekly Check-in", date, "Weekly", answers, name)
            invalid_count = 0                   # Reset on successful action

        elif rule["rule_number"] == "R3":       # View Entries
            view_previous_entries(name)
            invalid_count = 0                   # Reset on successful action

        elif rule["rule_number"] == "R4":       # Weekly Recap
            generate_weekly_recap(name)
            invalid_count = 0                   # Reset on successful action

        elif rule["rule_number"] == "R5":       # Chat Mode (NEW!)
            chat_mode(name, initial_mood)
            invalid_count = 0                   # Reset on successful action
            initial_mood = None                 # Clear initial mood after use

        elif rule["rule_number"] == "R6":       # Exit Program
            print(f"\n{Fore.CYAN}{'='*64}")
            print(f"{'='*24}SESSION COMPLETE{'='*24}")
            print(f"{'='*64}{Style.RESET_ALL}")
            print(f"\nThank you for journaling today, {name}.")
            print(f"Remember: Progress, not perfection. You've got this!")
            print(f"Hope to see you again soon.\n")
            break

# Run the program
if __name__ == "__main__":
    main()