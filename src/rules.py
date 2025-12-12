import argparse
import sys
from typing import Dict, Any, Optional

def validate_choice(choice: str, valid_options: list) -> bool:
    """
    Validate user choice against valid options
    Args:
        choice: User's input choice
        valid_options: List of valid choices   
    Returns:
        True if valid, False otherwise
    """
    if not choice:
        return False
    
    # Convert to lowercase for case-insensitive comparison
    choice_lower = choice.strip().lower()
    
    # Check against valid options
    return choice_lower in [opt.lower() for opt in valid_options]

def parse_cli_args():
    """Parse command line arguments for journal app"""
    parser = argparse.ArgumentParser(
        description="Journal Companion - A reflective journaling application with chatbot support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python app.py                     # Start normally
  python app.py --version           # Show version
  python app.py --mood 4            # Start with initial mood 4
  python app.py --show-scale        # Display mood scale
  python app.py --test              # Run unit tests
  python app.py --chat              # Start directly in chat mode (NEW!)
        """
    )
    
    parser.add_argument(
        '--version', '-v',
        action='store_true',
        help='Show version information'
    )
    
    parser.add_argument(
        '--mood', '-m',
        type=str,
        help='Set initial mood (1-5 or keyword)'
    )
    
    parser.add_argument(
        '--show-scale', '-s',
        action='store_true',
        help='Display the mood scale'
    )
    
    parser.add_argument(
        '--test', '-t',
        action='store_true',
        help='Run unit tests'
    )
    
    parser.add_argument(
        '--chat', '-c',                             # New Chat mode flag
        action='store_true',
        help='Start directly in chat mode'
    )
    
    parser.add_argument(
        '--name', '-n',
        type=str,
        help='Set user name (for testing)'
    )
    
    return parser.parse_args()

def process_cli_args(args) -> Dict[str, Any]:
    """
    Process command line arguments and return action dict
    Args:
        args: Parsed command line arguments    
    Returns:
        Dictionary with action and any parameters
    """
    from mood_assessment import assess_mood
    
    result = {
        'action': 'run',                            # Default action
        'mood': None,
        'chat_mode': False,                         # New Chat mode flag
        'user_name': None
    }
    
    # Check for version flag
    if args.version:
        result['action'] = 'version'
        return result
    
    # Check for show-scale flag
    if args.show_scale:
        result['action'] = 'show_scale'
        return result
    
    # Check for test flag
    if args.test:
        result['action'] = 'test'
        return result
    
    # NEW: Check for chat mode flag
    if args.chat:
        result['action'] = 'run'
        result['chat_mode'] = True
        print("Starting in Chat Mode...")
    
    # Process mood if provided
    if args.mood:
        mood_result = assess_mood(args.mood)
        if mood_result:
            result['mood'] = mood_result
            print(f"Initial mood set to: {mood_result['description']}")
        else:
            print(f"Warning: Invalid mood '{args.mood}'. Using default.")
    
    # Process name if provided
    if args.name:
        result['user_name'] = args.name
        print(f"User name set to: {args.name}")
    
    return result

def validate_mood_input(mood_input: str) -> Optional[Dict[str, Any]]:
    """
    Validate and normalize mood input
    Args:
        mood_input: User's mood input    
    Returns:
        Normalized mood dict or None if invalid
    """
    from mood_assessment import assess_mood
    return assess_mood(mood_input)

def get_valid_menu_options() -> Dict[str, list]:
    """
    Get valid menu options for the journal app
    Returns:
        Dictionary mapping option numbers to valid inputs
    """
    return {
        '1': ['1', 'one', 'daily', 'd', 'day'],
        '2': ['2', 'two', 'weekly', 'w', 'week'],
        '3': ['3', 'three', 'view', 'v', 'entries', 'journal'],
        '4': ['4', 'four', 'recap', 'r', 'summary'],
        '5': ['5', 'five', 'chat', 'c', 'talk', 'conversation'],  # New Chat mode
        '6': ['6', 'six', 'exit', 'e', 'quit', 'q', 'bye']
    }

def is_valid_menu_choice(choice: str) -> bool:
    """
    Check if a choice is valid for the main menu
    Args:
        choice: User's menu choice    
    Returns:
        True if valid, False otherwise
    """
    options = get_valid_menu_options()
    
    # Flatten all valid options
    all_valid_options = []
    for valid_list in options.values():
        all_valid_options.extend(valid_list)
    
    return validate_choice(choice, all_valid_options)

def get_menu_option_number(choice: str) -> Optional[str]:
    """
    Get the menu option number from a choice
    Args:
        choice: User's menu choice    
    Returns:
        Option number (1-6) or None if invalid
    """
    choice_lower = choice.strip().lower()
    options = get_valid_menu_options()
    
    for option_num, valid_options in options.items():
        if choice_lower in [opt.lower() for opt in valid_options]:
            return option_num
    
    return None

# Example usage and testing
if __name__ == "__main__":
    print("Testing Rules Module:")
    print(f"\n{'-'*64}")
    
    # Test validation
    test_choices = [
        ("1", True),
        ("daily", True),
        ("chat", True),                                     # New Test chat
        ("7", False),
        ("invalid", False)
    ]
    
    for choice, expected in test_choices:
        result = is_valid_menu_choice(choice)
        status = "✓" if result == expected else "✗"
        print(f"{status} Choice '{choice}': expected {expected}, got {result}")
    
    print(f"\n{'-'*64}")
    
    # Test option number mapping
    test_mapping = [
        ("1", "1"),
        ("chat", "5"),                                      # New Chat maps to 5
        ("exit", "6"),
        ("invalid", None)
    ]
    
    for choice, expected in test_mapping:
        result = get_menu_option_number(choice)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{choice}' -> expected '{expected}', got '{result}'")
    
    print(f"\n{'-'*64}")
    
    # Test CLI argument parsing
    print("CLI Argument Examples:")
    print("python app.py --version")
    print("python app.py --mood 4")
    print("python app.py --show-scale")
    print("python app.py --test")
    print("python app.py --chat  # NEW: Start in chat mode")