import re
from typing import Dict, Optional, Any

def assess_mood(mood_input: str) -> Optional[Dict[str, Any]]:
    """
    Assess mood from user input (1-5 or keywords)
    Args:
        mood_input: User's mood input (number 1-5 or keyword)    
    Returns:
        Dictionary with mood level and description, or None if invalid
    """
    if not mood_input:
        return None
    
    # Clean the input
    mood_input = mood_input.strip().lower()
    
    # Mood mappings, change the verbiage and order to resemble an easier flow for the user
    # Found this emoji feature and thought it added a more personal touch
    mood_map = {
        # Level 1: Very low mood
        '1': {'level': 1, 'description': 'Very Low', 'emoji': '😔'},
        'one': {'level': 1, 'description': 'Very Low', 'emoji': '😔'},
        'very low': {'level': 1, 'description': 'Very Low', 'emoji': '😔'},
        'terrible': {'level': 1, 'description': 'Very Low', 'emoji': '😔'},
        'awful': {'level': 1, 'description': 'Very Low', 'emoji': '😔'},
        'horrible': {'level': 1, 'description': 'Very Low', 'emoji': '😔'},
        'depressed': {'level': 1, 'description': 'Very Low', 'emoji': '😔'},
        'hopeless': {'level': 1, 'description': 'Very Low', 'emoji': '😔'},
        
        # Level 2: Low mood
        '2': {'level': 2, 'description': 'Low', 'emoji': '😟'},
        'two': {'level': 2, 'description': 'Low', 'emoji': '😟'},
        'low': {'level': 2, 'description': 'Low', 'emoji': '😟'},
        'down': {'level': 2, 'description': 'Low', 'emoji': '😟'},
        'sad': {'level': 2, 'description': 'Low', 'emoji': '😟'},
        'unhappy': {'level': 2, 'description': 'Low', 'emoji': '😟'},
        'blue': {'level': 2, 'description': 'Low', 'emoji': '😟'},
        'gloomy': {'level': 2, 'description': 'Low', 'emoji': '😟'},
        
        # Level 3: Neutral mood
        '3': {'level': 3, 'description': 'Neutral', 'emoji': '😐'},
        'three': {'level': 3, 'description': 'Neutral', 'emoji': '😐'},
        'neutral': {'level': 3, 'description': 'Neutral', 'emoji': '😐'},
        'okay': {'level': 3, 'description': 'Neutral', 'emoji': '😐'},
        'fine': {'level': 3, 'description': 'Neutral', 'emoji': '😐'},
        'meh': {'level': 3, 'description': 'Neutral', 'emoji': '😐'},
        'alright': {'level': 3, 'description': 'Neutral', 'emoji': '😐'},
        'so-so': {'level': 3, 'description': 'Neutral', 'emoji': '😐'},
        
        # Level 4: Good mood
        '4': {'level': 4, 'description': 'Good', 'emoji': '🙂'},
        'four': {'level': 4, 'description': 'Good', 'emoji': '🙂'},
        'good': {'level': 4, 'description': 'Good', 'emoji': '🙂'},
        'happy': {'level': 4, 'description': 'Good', 'emoji': '🙂'},
        'content': {'level': 4, 'description': 'Good', 'emoji': '🙂'},
        'pleased': {'level': 4, 'description': 'Good', 'emoji': '🙂'},
        'satisfied': {'level': 4, 'description': 'Good', 'emoji': '🙂'},
        'cheerful': {'level': 4, 'description': 'Good', 'emoji': '🙂'},
        
        # Level 5: Very good mood
        '5': {'level': 5, 'description': 'Very Good', 'emoji': '😊'},
        'five': {'level': 5, 'description': 'Very Good', 'emoji': '😊'},
        'very good': {'level': 5, 'description': 'Very Good', 'emoji': '😊'},
        'excellent': {'level': 5, 'description': 'Very Good', 'emoji': '😊'},
        'great': {'level': 5, 'description': 'Very Good', 'emoji': '😊'},
        'fantastic': {'level': 5, 'description': 'Very Good', 'emoji': '😊'},
        'wonderful': {'level': 5, 'description': 'Very Good', 'emoji': '😊'},
        'amazing': {'level': 5, 'description': 'Very Good', 'emoji': '😊'},
        'ecstatic': {'level': 5, 'description': 'Very Good', 'emoji': '😊'},
    }
    
    # Check if input is in mood map
    if mood_input in mood_map:
        return mood_map[mood_input]
    
    # Check for numeric input that might have spaces or special characters
    if mood_input.isdigit():
        mood_num = int(mood_input)
        if 1 <= mood_num <= 5:
            return mood_map[str(mood_num)]
    
    # Check for "very" patterns
    if mood_input.startswith('very '):
        base_mood = mood_input[5:]
        if base_mood in mood_map:
            result = mood_map[base_mood].copy()
            result['level'] = min(5, result['level'] + 1)
            result['description'] = 'Very ' + result['description']
            return result
    
    # Check for "a bit" or "slightly" patterns
    bit_patterns = ['a bit ', 'slightly ', 'kind of ', 'sort of ']
    for pattern in bit_patterns:
        if mood_input.startswith(pattern):
            base_mood = mood_input[len(pattern):]
            if base_mood in mood_map:
                result = mood_map[base_mood].copy()
                result['level'] = max(1, result['level'] - 1)
                result['description'] = 'Slightly ' + result['description']
                return result
    
    # If no match found
    return None

def display_mood_scale() -> str:
    """
    Display the mood scale for user reference
    Returns:
        Formatted mood scale string
    """
    scale = """
╔══════════════════════════════════════════════════════════╗
║                     MOOD SCALE (1-5)                     ║
╠═══════╦══════════════════════════════════════════════════╣
║ Level ║ Description                                      ║
╠═══════╬══════════════════════════════════════════════════╣
║   1   ║ Very Low  😔  (Terrible, Awful, Hopeless)        ║
║   2   ║ Low       😟  (Sad, Down, Unhappy)               ║
║   3   ║ Neutral   😐  (Okay, Fine, Meh)                  ║
║   4   ║ Good      🙂  (Happy, Content, Cheerful)         ║
║   5   ║ Very Good 😊  (Great, Fantastic, Wonderful)      ║
╚═══════╩══════════════════════════════════════════════════╝

You can use the number (1-5) or any of the keywords shown above.
Examples: "3", "happy", "a bit sad", "very good"
"""
    return scale

def get_mood_color(mood_level: int) -> str:
    """
    Get color code for mood level (for display purposes)
    Args:
        mood_level: Mood level (1-5)    
    Returns:
        Color name for the mood level
    """
    mood_colors = {
        1: 'red',      # Very Low
        2: 'yellow',   # Low  
        3: 'white',    # Neutral
        4: 'cyan',     # Good
        5: 'green'     # Very Good
    }
    return mood_colors.get(mood_level, 'white')

def suggest_mood_activities(mood_level: int) -> list:
    """
    Suggest activities based on mood level
    Args:
        mood_level: Mood level (1-5)    
    Returns:
        List of suggested activities
    """
    activities = {
        1: [
            "Take 3 deep breaths",
            "Drink a glass of water",
            "Name one thing you can see, hear, and feel",
            "Reach out to someone you trust"
        ],
        2: [
            "Go for a short walk",
            "Write down what's bothering you",
            "Listen to calming music",
            "Do one small, kind thing for yourself"
        ],
        3: [
            "Check in with what you need right now",
            "Try a brief mindfulness exercise",
            "Do something creative for 10 minutes",
            "Connect with a friend"
        ],
        4: [
            "Savor this positive moment",
            "Share your good mood with someone",
            "Do something you enjoy",
            "Practice gratitude"
        ],
        5: [
            "Celebrate this great feeling!",
            "Share your positivity",
            "Do something energizing",
            "Capture this moment in your journal"
        ]
    }
    
    return activities.get(mood_level, ["Take a moment to check in with yourself"])

# Example usage and testing
if __name__ == "__main__":
    print("Testing Mood Assessment:")
    print(f"\n{'-'*64}")
    
    # Test mood assessment
    test_inputs = [
        "1", "one", "very low",
        "2", "two", "sad",
        "3", "three", "meh",
        "4", "four", "happy",
        "5", "five", "fantastic",
        "a bit sad", "very happy",
        "invalid", ""
    ]
    
    for test in test_inputs:
        result = assess_mood(test)
        if result:
            print(f"✓ '{test}' -> Level {result['level']}: {result['description']} {result['emoji']}")
        else:
            print(f"✗ '{test}' -> Invalid mood input")
    
    print(f"\n{'-'*64}")
    print("Mood Scale Display:")
    print(display_mood_scale())
    
    print(f"\n{'-'*64}")
    print("Activity Suggestions:")
    for level in range(1, 6):
        activities = suggest_mood_activities(level)
        print(f"\nLevel {level} activities:")
        for i, activity in enumerate(activities, 1):
            print(f"  {i}. {activity}")