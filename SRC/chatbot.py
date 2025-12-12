import random
from typing import Dict, List, Optional, Any
import json
import datetime

class UnifiedChatbot:
    """A chatbot for journal companion with empathetic responses and chat mode support"""
    
    def __init__(self, ai_enabled: bool = False):
        self.ai_enabled = ai_enabled
        self.conversation_history = []
        self.user_context = {}
        
        # Empathetic responses based on mood levels (1-5)
        self.mood_responses = {
            1: {  # Very low mood
                'empathetic': [
                    "I hear you're having a really tough time. That sounds incredibly hard.",
                    "I'm so sorry you're feeling this way. Thank you for sharing with me.",
                    "It takes courage to acknowledge when things are this difficult. I'm here with you.",
                    "This sounds really heavy to carry. Would you like to talk more about what's coming up?"
                ],
                'supportive': [
                    "Would it help to take a few deep breaths together?",
                    "Sometimes just naming the feeling can help a little. Would you like to try?",
                    "I want you to know that your feelings are valid, no matter how dark they seem.",
                    "You don't have to go through this alone. Would you like some grounding techniques?"
                ]
            },
            2: {  # Low mood
                'empathetic': [
                    "I can sense you're going through a challenging time. That sounds really difficult.",
                    "Thank you for being honest about how you're feeling. That's not easy to do.",
                    "It sounds like things feel heavy right now. Would you like to unpack that a bit?",
                    "I'm here to listen, without judgment, whenever you're ready to share more."
                ],
                'supportive': [
                    "Would it help to focus on one small, kind thing you can do for yourself right now?",
                    "Sometimes writing down what's bothering us can make it feel more manageable.",
                    "Remember that feelings come in waves - this one will pass too.",
                    "Would you like me to suggest some gentle self-care ideas?"
                ]
            },
            3: {  # Neutral mood
                'empathetic': [
                    "Thanks for checking in with yourself. Being aware is the first step.",
                    "It's okay to feel neutral sometimes - not every day has to be high or low.",
                    "How interesting that you're noticing this middle ground. What's that like for you?",
                    "Sometimes neutrality can be a sign of balance. What do you think?"
                ],
                'supportive': [
                    "This might be a good time to check in with what you need right now.",
                    "Would you like to explore what might bring a little more lightness to your day?",
                    "Sometimes neutral moments are opportunities for gentle reflection.",
                    "Is there something small that might bring you a bit of comfort or joy?"
                ]
            },
            4: {  # Good mood
                'empathetic': [
                    "It's wonderful to hear you're feeling good! That's something to acknowledge.",
                    "I'm genuinely happy to hear you're in a positive space today!",
                    "This sounds lovely! Would you like to savor this feeling a bit more?",
                    "It's great that you're recognizing and enjoying this positive moment!"
                ],
                'supportive': [
                    "Would you like to explore what's contributing to this good feeling?",
                    "This might be a perfect time for some positive journaling or gratitude practice.",
                    "How can you nurture this good feeling?",
                    "Would you like to set a small intention to carry this feeling forward?"
                ]
            },
            5: {  # Very good mood
                'empathetic': [
                    "WOW! That's amazing to hear! I'm smiling just knowing you're feeling so good!",
                    "This is wonderful! Thank you for sharing this positive energy!",
                    "I'm genuinely thrilled to hear you're feeling fantastic!",
                    "What fantastic news! Would you like to celebrate this feeling with me?"
                ],
                'supportive': [
                    "This is a perfect moment to practice gratitude for this feeling.",
                    "Would you like to capture this moment in your journal to remember later?",
                    "How can you share this positive energy with yourself or others?",
                    "This great feeling is something to acknowledge and honor. Well done!"
                ]
            }
        }
        
        # Follow-up questions for each mood level
        self.followup_questions = {
            1: [
                "What does this heavy feeling feel like in your body?",
                "Is there one small thing that might feel slightly less heavy today?",
                "What would feel supportive right now, even if it's very small?",
                "Can you remember a time when you felt slightly better, even briefly?"
            ],
            2: [
                "What's one thing that might help shift this feeling, even a tiny bit?",
                "Is there a person or memory that usually brings you comfort?",
                "What does your body need right now - rest, movement, nourishment?",
                "What would you tell a friend who was feeling this way?"
            ],
            3: [
                "What might help you move toward feeling a bit more positive?",
                "Is there something you've been curious about trying?",
                "What small pleasure could you add to your day?",
                "How do you feel about this neutral space?"
            ],
            4: [
                "What's contributing to this good feeling?",
                "How can you savor or extend this positive moment?",
                "What would you like to do with this good energy?",
                "Is there someone you'd like to share this feeling with?"
            ],
            5: [
                "What's making today so wonderful?",
                "How can you capture this feeling to remember on harder days?",
                "Is there a way to pay this positive feeling forward?",
                "What does this fantastic feeling make you want to do?"
            ]
        }
        
        # Chat mode responses for different conversation types
        self.chat_responses = {
            'greeting': [
                "Hi there! I'm here to listen. How's your day going?",
                "Hello! I'm glad you're here. What's on your mind today?",
                "Hi! I'm ready to chat whenever you are. How are things?",
                "Hello! I'm here to talk about anything you'd like. What's up?"
            ],
            'feeling': [
                "I hear you. Tell me more about what that feels like for you.",
                "That sounds significant. Would you like to explore that feeling further?",
                "Thank you for sharing that. How long have you been feeling this way?",
                "I understand. What's been coming up for you with this feeling?"
            ],
            'journal': [
                "Your journal is a safe space for all your thoughts and feelings.",
                "It's great that you're reflecting on your journal. What stands out to you?",
                "Journaling can be such a powerful tool. What brings you to it today?",
                "Your reflections matter. Would you like to explore any particular entry?"
            ],
            'support': [
                "I'm here to support you. What do you need right now?",
                "You're not alone in this. I'm listening.",
                "Whatever you're going through, your feelings are valid.",
                "Take your time. I'm right here with you."
            ],
            'reflection': [
                "That's an interesting perspective. What makes you think that?",
                "I appreciate you sharing that reflection. How did you come to that insight?",
                "That's a powerful observation. How does that feel to acknowledge?",
                "Thank you for that reflection. What's next for you with this realization?"
            ]
        }
        
        # Weekly recap templates
        self.recap_templates = [
            "Looking back at your journal entries, I notice {observation}. This week, you showed {quality}. Remember: {encouragement}",
            "Your reflections this week revealed {theme}. You demonstrated {strength} in how you approached things. A reminder: {insight}",
            "Based on your entries, you've been exploring {topic}. Your journey shows {growth}. Keep in mind: {advice}",
            "This week's journaling highlights {focus}. I see {progress} in your reflections. Consider this: {suggestion}"
        ]
        
        # Observations, qualities, and encouragement phrases
        self.recap_elements = {
            'observations': [
                "a mix of different emotions and experiences",
                "some meaningful reflections",
                "progress in your self-awareness",
                "moments of insight and growth"
            ],
            'qualities': [
                "courage in being honest with yourself",
                "resilience in facing challenges",
                "thoughtfulness in your reflections",
                "self-compassion in your journey"
            ],
            'encouragements': [
                "every entry is a step forward, no matter how small",
                "your willingness to reflect is itself a form of growth",
                "there's no right or wrong way to feel - only your authentic experience",
                "each day brings new opportunities for understanding"
            ],
            'themes': [
                "self-discovery and personal growth",
                "emotional awareness and processing",
                "daily experiences and their meanings",
                "personal challenges and triumphs"
            ],
            'strengths': [
                "honesty and vulnerability",
                "persistence and dedication",
                "insight and self-awareness",
                "courage and openness"
            ],
            'insights': [
                "growth often happens in small, daily moments",
                "your feelings are valuable messengers",
                "reflection is a powerful tool for understanding",
                "every emotion has something to teach us"
            ]
        }
        
        print(f"Chatbot initialized: {'AI Mode Enabled' if ai_enabled else 'Rule-based Mode'}")

    def get_empathetic_response(self, mood_level: int, mood_description: str = "") -> str:
        """
        Get an empathetic response based on mood level
        Args:
            mood_level: Integer from 1-5 representing mood
            mood_description: Optional description of mood    
        Returns:
            Empathetic response string
        """
        # Validate mood level
        mood_level = max(1, min(5, mood_level))
        
        # Get appropriate responses
        empathetic_list = self.mood_responses[mood_level]['empathetic']
        supportive_list = self.mood_responses[mood_level]['supportive']
        
        # Combine or choose randomly
        if random.random() > 0.3:  # 70% chance of empathetic, 30% of supportive
            response = random.choice(empathetic_list)
        else:
            response = random.choice(supportive_list)
        
        # Add to conversation history
        self.conversation_history.append({
            'type': 'mood_response',
            'mood_level': mood_level,
            'response': response,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        return response
    
    def offer_support(self, mood_level: int) -> str:
        """
        Offer additional support based on mood level
        Args:
            mood_level: Integer from 1-5    
        Returns:
            Support offer string
        """
        offers = {
            1: "Would you like some gentle guidance through this difficult moment?",
            2: "Would you like to explore some coping strategies together?",
            3: "Would you like to reflect a bit more on what you need right now?",
            4: "Would you like to build on this positive feeling?",
            5: "Would you like to celebrate and explore this fantastic feeling?"
        }
        
        return offers.get(mood_level, "Would you like to explore this further?")
    
    def get_followup_questions(self, mood_level: int, count: int = 3) -> List[str]:
        """
        Get follow-up questions for a given mood level
        Args:
            mood_level: Integer from 1-5
            count: Number of questions to return    
        Returns:
            List of follow-up questions
        """
        mood_level = max(1, min(5, mood_level))
        questions = self.followup_questions[mood_level]
        
        # Return random selection of questions
        if len(questions) <= count:
            return questions
        else:
            return random.sample(questions, count)
    
    def get_chat_response(self, user_message: str, conversation_history: List[str] = None, 
                         mood_context: Dict = None) -> str:
        """
        NEW: Get a conversational response for chat mode
        Args:
            user_message: The user's message
            conversation_history: List of previous messages
            mood_context: Current mood context    
        Returns:
            Chat response string
        """
        # Update conversation history
        if conversation_history:
            self.conversation_history = conversation_history[-10:]  # Keep last 10 messages
        
        # Add mood context if available
        if mood_context:
            self.user_context['current_mood'] = mood_context
        
        # Convert message to lowercase for analysis
        msg_lower = user_message.lower()
        
        # Categorize the message type
        message_type = self._categorize_message(msg_lower)
        
        # Get appropriate response
        if message_type == 'greeting':
            response = random.choice(self.chat_responses['greeting'])
        elif message_type == 'feeling':
            response = random.choice(self.chat_responses['feeling'])
        elif message_type == 'journal':
            response = random.choice(self.chat_responses['journal'])
        elif message_type == 'support':
            response = random.choice(self.chat_responses['support'])
        elif message_type == 'reflection':
            response = random.choice(self.chat_responses['reflection'])
        else:
            # Generic empathetic response
            response = self._get_generic_chat_response(msg_lower)
        
        # Add context if we have mood information
        if mood_context and 'feeling' in msg_lower:
            mood_desc = mood_context.get('description', '')
            if mood_desc:
                response = f"I remember you mentioned feeling {mood_desc.lower()}. {response}"
        
        # Track in history
        self.conversation_history.append(f"User: {user_message}")
        self.conversation_history.append(f"Companion: {response}")
        
        return response
    
    def _categorize_message(self, message: str) -> str:
        """Categorize the type of message for appropriate response"""
        message = message.lower()
        
        # Check for greetings
        greetings = ['hi', 'hello', 'hey', 'greetings']
        if any(greet in message for greet in greetings):
            return 'greeting'
        
        # Check for feelings
        feeling_words = ['feel', 'feeling', 'emotion', 'mood', 'sad', 'happy', 'angry', 
                        'anxious', 'stressed', 'overwhelmed', 'excited', 'nervous']
        if any(word in message for word in feeling_words):
            return 'feeling'
        
        # Check for journal references
        journal_words = ['journal', 'entry', 'entries', 'wrote', 'writ', 'reflect']
        if any(word in message for word in journal_words):
            return 'journal'
        
        # Check for support requests
        support_words = ['help', 'support', 'need', 'struggle', 'hard', 'difficult', 'tough']
        if any(word in message for word in support_words):
            return 'support'
        
        # Check for reflections
        reflection_words = ['think', 'thought', 'realize', 'understand', 'learn', 'know']
        if any(word in message for word in reflection_words):
            return 'reflection'
        
        return 'general'
    
    def _get_generic_chat_response(self, message: str) -> str:
        """Get a generic response for uncategorized messages"""
        generic_responses = [
            "I hear you. Tell me more about that.",
            "Thank you for sharing that. What comes up for you as you say that?",
            "I'm listening. Would you like to explore that further?",
            "That's interesting. What makes you bring that up?",
            "I appreciate you sharing that. How does that feel to talk about?"
        ]
        
        # Check if it's a question
        if '?' in message:
            return "That's a thoughtful question. What are your thoughts on it?"
        
        return random.choice(generic_responses)
    
    def generate_weekly_recap(self, entries: List[Dict]) -> str:
        """
        Generate a weekly recap based on journal entries
        Args:
            entries: List of journal entry dictionaries    
        Returns:
            Weekly recap string
        """
        if not entries:
            return "It looks like this was a quiet week for journaling. That's okay! Every season has its rhythm. Sometimes, the space between entries is just as meaningful as the writing itself."
        
        # Get a random template
        template = random.choice(self.recap_templates)
        
        # Fill in the template with random elements
        recap = template.format(
            observation=random.choice(self.recap_elements['observations']),
            quality=random.choice(self.recap_elements['qualities']),
            encouragement=random.choice(self.recap_elements['encouragements']),
            theme=random.choice(self.recap_elements['themes']),
            strength=random.choice(self.recap_elements['strengths']),
            insight=random.choice(self.recap_elements['insights']),
            topic=random.choice(self.recap_elements['themes']),
            growth=random.choice(self.recap_elements['qualities']),
            advice=random.choice(self.recap_elements['encouragements']),
            focus=random.choice(self.recap_elements['observations']),
            progress=random.choice(self.recap_elements['strengths']),
            suggestion=random.choice(self.recap_elements['insights'])
        )
        
        # Add entry count information if available
        if entries and 'entry_count' in entries[0]:
            entry_count = entries[0]['entry_count']
            if entry_count > 0:
                recap += f"\n\nYou completed {entry_count} journal entries this week. That's a meaningful commitment to your self-reflection practice!"
        
        return recap
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("Conversation history cleared.")

# Create a global instance for easy import
chatbot = UnifiedChatbot(ai_enabled=False)

# Example usage
if __name__ == "__main__":
    # Test the chatbot
    print("Testing Unified Chatbot:")
    print(f"\n{'-'*64}")
    
    # Test mood responses
    for mood in range(1, 6):
        response = chatbot.get_empathetic_response(mood)
        print(f"Mood {mood}: {response}")
    
    print(f"\n{'-'*64}")
    
    # Test chat mode
    test_messages = [
        "Hi there!",
        "I'm feeling a bit anxious today",
        "I wrote in my journal about my day",
        "I need some support",
        "I realized something important about myself"
    ]
    
    for msg in test_messages:
        response = chatbot.get_chat_response(msg)
        print(f"\nUser: {msg}")
        print(f"Chatbot: {response}")
    
    print(f"\n{'-'*64}")
    
    # Test weekly recap
    test_entries = [{'entry_count': 3, 'daily_count': 2, 'weekly_count': 1}]
    recap = chatbot.generate_weekly_recap(test_entries)
    print(f"Weekly Recap:\n{recap}")