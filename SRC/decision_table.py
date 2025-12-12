from typing import Dict, Any

class DecisionTable:
    """A decision table for evaluating user choices in the journal app"""
    
    def __init__(self):
        # Define the rules for the decision table
        # Format: (condition, rule_number, output_message)

        self.rules = [
            # R1: Daily Reflection
            (lambda choice: choice in ['1', 'one', 'daily', 'd', 'day'], 
             "R1", "Starting Daily Reflection..."),
            
            # R2: Weekly Check-in
            (lambda choice: choice in ['2', 'two', 'weekly', 'w', 'week'], 
             "R2", "Starting Weekly Check-in..."),
            
            # R3: View Entries
            (lambda choice: choice in ['3', 'three', 'view', 'v', 'entries', 'journal'], 
             "R3", "Viewing Previous Entries..."),
            
            # R4: Weekly Recap
            (lambda choice: choice in ['4', 'four', 'recap', 'r', 'summary'], 
             "R4", "Generating Weekly Recap..."),
            
            # R5: Chat Mode (NEW!)
            (lambda choice: choice in ['5', 'five', 'chat', 'c', 'talk', 'conversation'], 
             "R5", "Starting Chat Mode..."),
            
            # R6: Exit Program
            (lambda choice: choice in ['6', 'six', 'exit', 'e', 'quit', 'q', 'bye'], 
             "R6", "Exiting Program..."),
            
            # Default rule (must be last)
            (lambda choice: True, 
             "Default", "Invalid choice")
        ]
    
    def evaluate(self, user_input: str) -> Dict[str, Any]:
        """
        Evaluate user input against the decision table rules
        Args:
            user_input: The user's choice as a string    
        Returns:
            Dictionary with rule_number and output_message
        """
        # Convert input to lowercase for case-insensitive matching
        input_lower = user_input.strip().lower()
        
        # Check each rule in order
        for condition, rule_number, output_message in self.rules:
            if condition(input_lower):
                return {
                    "rule_number": rule_number,
                    "output_message": output_message,
                    "input_received": user_input
                }
        
        # This should never be reached due to default rule
        return {
            "rule_number": "Default",
            "output_message": "Invalid choice",
            "input_received": user_input
        }
    
    def get_valid_choices(self) -> list:
        """Get a list of all valid choices for user guidance"""
        valid_choices = []
        
        # Extract all valid inputs from rules (excluding default)
        for condition, rule_number, _ in self.rules:
            if rule_number != "Default":
                # For simplicity, we'll return the main options
                # In a real app, you might want to extract from lambda
                valid_choices.extend(self._get_options_for_rule(rule_number))
        
        return list(set(valid_choices))  # Remove duplicates
    
    def _get_options_for_rule(self, rule_number: str) -> list:
        """Helper to get options for each rule"""
        options_map = {
            "R1": ['1', 'one', 'daily'],
            "R2": ['2', 'two', 'weekly'],
            "R3": ['3', 'three', 'view'],
            "R4": ['4', 'four', 'recap'],
            "R5": ['5', 'five', 'chat'],                # NEW: Chat mode options
            "R6": ['6', 'six', 'exit']
        }
        return options_map.get(rule_number, [])

# Create a global instance for easy import
decision_table = DecisionTable()

# Example usage and testing
if __name__ == "__main__":
    # Test the decision table
    test_cases = [
        "1", "daily", "one",
        "2", "weekly", "two", 
        "3", "view", "three",
        "4", "recap", "four",
        "5", "chat", "five",                            # NEW: Test chat mode
        "6", "exit", "six",
        "invalid", "7", "help"
    ]
    
    print("Testing Decision Table:")
    print(f"\n{'-'*64}")
    
    for test in test_cases:
        result = decision_table.evaluate(test)
        print(f"Input: '{test}' -> Rule: {result['rule_number']}, Message: {result['output_message']}")
    
    print("\nValid choices:")
    print(decision_table.get_valid_choices())