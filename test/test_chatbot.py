# test_chatbot_unified.py - Unit tests for chatbot
import unittest
from src.chatbot import UnifiedChatbot
from src.mood_assessment import assess_mood

class TestUnifiedChatbot(unittest.TestCase):
    """Test cases for UnifiedChatbot class"""
    
    def setUp(self):
        """Set up test fixture"""
        self.chatbot = UnifiedChatbot(ai_enabled=False)
    
    def test_initialization(self):
        """Test chatbot initialization"""
        self.assertFalse(self.chatbot.ai_enabled)
        self.assertEqual(len(self.chatbot.conversation_history), 0)
        self.assertEqual(len(self.chatbot.user_context), 0)
    
    def test_get_empathetic_response_valid(self):
        """Test getting empathetic response with valid mood levels"""
        for mood_level in range(1, 6):
            response = self.chatbot.get_empathetic_response(mood_level)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 10)  # Response should have reasonable length
    
    def test_get_empathetic_response_invalid(self):
        """Test getting empathetic response with invalid mood levels"""
        # Test below range
        response = self.chatbot.get_empathetic_response(0)
        self.assertIsInstance(response, str)
        
        # Test above range
        response = self.chatbot.get_empathetic_response(6)
        self.assertIsInstance(response, str)
    
    def test_offer_support(self):
        """Test support offers for all mood levels"""
        for mood_level in range(1, 6):
            offer = self.chatbot.offer_support(mood_level)
            self.assertIsInstance(offer, str)
            self.assertIn("Would you like", offer)
    
    def test_get_followup_questions(self):
        """Test getting follow-up questions"""
        for mood_level in range(1, 6):
            questions = self.chatbot.get_followup_questions(mood_level, count=2)
            self.assertIsInstance(questions, list)
            self.assertEqual(len(questions), 2)
            
            for question in questions:
                self.assertIsInstance(question, str)
                self.assertGreater(len(question), 5)
    
    def test_get_chat_response(self):
        """Test chat mode responses"""
        test_messages = [
            "Hello!",
            "I'm feeling good today",
            "I need help",
            "What do you think?",
            ""
        ]
        
        for message in test_messages:
            response = self.chatbot.get_chat_response(message)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 5)
    
    def test_categorize_message(self):
        """Test message categorization"""
        test_cases = [
            ("hi there", "greeting"),
            ("i feel sad", "feeling"),
            ("my journal entry", "journal"),
            ("i need help", "support"),
            ("i think about", "reflection"),
            ("random message", "general")
        ]
        
        for message, expected_category in test_cases:
            category = self.chatbot._categorize_message(message)
            self.assertEqual(category, expected_category)
    
    def test_generate_weekly_recap(self):
        """Test weekly recap generation"""
        # Test with entries
        entries = [{'entry_count': 3, 'daily_count': 2, 'weekly_count': 1}]
        recap = self.chatbot.generate_weekly_recap(entries)
        self.assertIsInstance(recap, str)
        self.assertGreater(len(recap), 50)
        
        # Test without entries
        recap_empty = self.chatbot.generate_weekly_recap([])
        self.assertIsInstance(recap_empty, str)
        self.assertGreater(len(recap_empty), 20)
    
    def test_clear_history(self):
        """Test clearing conversation history"""
        # Add some history
        self.chatbot.get_empathetic_response(3)
        self.chatbot.get_chat_response("Hello")
        
        self.assertGreater(len(self.chatbot.conversation_history), 0)
        
        # Clear history
        self.chatbot.clear_history()
        self.assertEqual(len(self.chatbot.conversation_history), 0)

class TestChatbotIntegration(unittest.TestCase):
    """Integration tests for chatbot with mood assessment"""
    
    def test_mood_response_integration(self):
        """Test chatbot response to assessed mood"""
        # Test different mood inputs
        test_moods = ["1", "sad", "3", "happy", "fantastic"]
        
        for mood_input in test_moods:
            mood_result = assess_mood(mood_input)
            if mood_result:
                chatbot = UnifiedChatbot()
                response = chatbot.get_empathetic_response(
                    mood_result['level'], 
                    mood_result['description']
                )
                self.assertIsInstance(response, str)
                self.assertGreater(len(response), 10)
    
    def test_chat_mode_with_mood_context(self):
        """Test chat mode with mood context"""
        chatbot = UnifiedChatbot()
        mood_context = {'level': 3, 'description': 'Neutral', 'emoji': '😐'}
        
        response = chatbot.get_chat_response(
            "I'm feeling okay",
            mood_context=mood_context
        )
        
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 5)

def run_tests():
    """Run all tests and display results"""
    print("Running Chatbot Unit Tests...")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestUnifiedChatbot))
    suite.addTests(loader.loadTestsFromTestCase(TestChatbotIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"\n{test}:")
            print(traceback)
    
    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == "__main__":
    success = run_tests()
    if success:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed.")