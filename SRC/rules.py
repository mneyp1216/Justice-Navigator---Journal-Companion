# rules.py

def validate_choice(choice: str) -> str:
    """
    Decision rule to validate user menu choice.
    Safe default returns "4" and Exits if input is invalid
    """

    # "1 = Daily Reflection", "2 = Weekly Check-in", "3 = View Previous Entry", "4 = Exit"
    valid_choices = ["1", "2", "3", "4"]
    if choice in valid_choices:
        return choice
    else:
        return "4"      # safe default