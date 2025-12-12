# test_rules.py - Comprehensive unit tests for rules module
import unittest
import sys
import argparse
from io import StringIO
from unittest.mock import patch, MagicMock

# Import the rules module
from src.rules import (
    validate_choice,
    parse_cli_args,
    process_cli_args,
    get_valid_menu_options,
    is_valid_menu_choice,
    get_menu_option_number
)

class TestValidationFunctions(unittest.TestCase):
    """Test cases for validation functions"""
    
    def test_validate_choice_valid(self):
        """Test validate_choice with valid inputs"""
        valid_options = ['1', 'one', 'daily', '2', 'two', 'weekly']
        
        # Test exact matches
        self.assertTrue(validate_choice('1', valid_options))
        self.assertTrue(validate_choice('daily', valid_options))
        self.assertTrue(validate_choice('two', valid_options))
        
        # Test case insensitive
        self.assertTrue(validate_choice('ONE', valid_options))
        self.assertTrue(validate_choice('Daily', valid_options))
        self.assertTrue(validate_choice('TWO', valid_options))
        
        # Test with whitespace
        self.assertTrue(validate_choice(' 1 ', valid_options))
        self.assertTrue(validate_choice(' daily ', valid_options))
    
    def test_validate_choice_invalid(self):
        """Test validate_choice with invalid inputs"""
        valid_options = ['1', 'one', 'daily']
        
        # Test invalid choices
        self.assertFalse(validate_choice('7', valid_options))
        self.assertFalse(validate_choice('invalid', valid_options))
        self.assertFalse(validate_choice('', valid_options))
        self.assertFalse(validate_choice('   ', valid_options))
        
        # Test partial matches (should not match)
        self.assertFalse(validate_choice('dai', valid_options))  # Partial
        self.assertFalse(validate_choice('on', valid_options))   # Partial
    
    def test_validate_choice_empty_list(self):
        """Test validate_choice with empty valid options list"""
        self.assertFalse(validate_choice('1', []))
        self.assertFalse(validate_choice('anything', []))
    
    def test_is_valid_menu_choice(self):
        """Test is_valid_menu_choice function"""
        # Valid choices (including new chat mode)
        valid_choices = [
            '1', 'one', 'daily', 'd', 'day',
            '2', 'two', 'weekly', 'w', 'week',
            '3', 'three', 'view', 'v', 'entries', 'journal',
            '4', 'four', 'recap', 'r', 'summary',
            '5', 'five', 'chat', 'c', 'talk', 'conversation',  # NEW: Chat mode
            '6', 'six', 'exit', 'e', 'quit', 'q', 'bye'
        ]
        
        for choice in valid_choices:
            with self.subTest(choice=choice):
                self.assertTrue(is_valid_menu_choice(choice))
        
        # Invalid choices
        invalid_choices = ['0', '7', '8', '9', 'help', 'menu', 'options', 'invalid']
        
        for choice in invalid_choices:
            with self.subTest(choice=choice):
                self.assertFalse(is_valid_menu_choice(choice))
    
    def test_get_menu_option_number(self):
        """Test get_menu_option_number function"""
        test_cases = [
            # Input, Expected output
            ('1', '1'),
            ('one', '1'),
            ('daily', '1'),
            ('2', '2'),
            ('two', '2'),
            ('weekly', '2'),
            ('3', '3'),
            ('three', '3'),
            ('view', '3'),
            ('4', '4'),
            ('four', '4'),
            ('recap', '4'),
            ('5', '5'),           # NEW: Chat mode
            ('five', '5'),
            ('chat', '5'),
            ('6', '6'),
            ('six', '6'),
            ('exit', '6'),
            # Case variations
            ('ONE', '1'),
            ('Daily', '1'),
            ('CHAT', '5'),      # NEW: Chat mode
            ('Exit', '6'),
            # Invalid inputs
            ('invalid', None),
            ('7', None),
            ('', None),
            ('   ', None),
        ]
        
        for input_str, expected in test_cases:
            with self.subTest(input=input_str):
                result = get_menu_option_number(input_str)
                self.assertEqual(result, expected)
    
    def test_get_valid_menu_options(self):
        """Test get_valid_menu_options function"""
        options = get_valid_menu_options()
        
        # Should return a dictionary
        self.assertIsInstance(options, dict)
        
        # Should have 6 options (1-6)
        self.assertEqual(len(options), 6)
        
        # Check each option exists
        for i in range(1, 7):
            self.assertIn(str(i), options)
            
            # Each should have a list of valid inputs
            self.assertIsInstance(options[str(i)], list)
            self.assertGreater(len(options[str(i)]), 0)
        
        # Check specific options
        self.assertIn('daily', options['1'])
        self.assertIn('weekly', options['2'])
        self.assertIn('view', options['3'])
        self.assertIn('recap', options['4'])
        self.assertIn('chat', options['5'])  # NEW: Chat mode
        self.assertIn('exit', options['6'])

class TestCLIFunctions(unittest.TestCase):
    """Test cases for CLI argument parsing functions"""
    
    def test_parse_cli_args_no_args(self):
        """Test parse_cli_args with no arguments"""
        # Mock sys.argv to simulate no arguments
        with patch('sys.argv', ['app.py']):
            args = parse_cli_args()
            
            # Default values should be False/None
            self.assertFalse(args.version)
            self.assertFalse(args.show_scale)
            self.assertFalse(args.test)
            self.assertFalse(args.chat)  # NEW: Chat mode flag
            self.assertIsNone(args.mood)
            self.assertIsNone(args.name)
    
    def test_parse_cli_args_version(self):
        """Test parse_cli_args with version flag"""
        with patch('sys.argv', ['app.py', '--version']):
            args = parse_cli_args()
            self.assertTrue(args.version)
    
    def test_parse_cli_args_short_version(self):
        """Test parse_cli_args with short version flag"""
        with patch('sys.argv', ['app.py', '-v']):
            args = parse_cli_args()
            self.assertTrue(args.version)
    
    def test_parse_cli_args_mood(self):
        """Test parse_cli_args with mood argument"""
        test_cases = [
            ('--mood', '3'),
            ('-m', 'happy'),
            ('--mood', '5'),
        ]
        
        for flag, mood_value in test_cases:
            with patch('sys.argv', ['app.py', flag, mood_value]):
                args = parse_cli_args()
                self.assertEqual(args.mood, mood_value)
    
    def test_parse_cli_args_show_scale(self):
        """Test parse_cli_args with show-scale flag"""
        with patch('sys.argv', ['app.py', '--show-scale']):
            args = parse_cli_args()
            self.assertTrue(args.show_scale)
    
    def test_parse_cli_args_test(self):
        """Test parse_cli_args with test flag"""
        with patch('sys.argv', ['app.py', '--test']):
            args = parse_cli_args()
            self.assertTrue(args.test)
    
    def test_parse_cli_args_chat(self):
        """Test parse_cli_args with chat flag (NEW)"""
        with patch('sys.argv', ['app.py', '--chat']):
            args = parse_cli_args()
            self.assertTrue(args.chat)
    
    def test_parse_cli_args_short_chat(self):
        """Test parse_cli_args with short chat flag (NEW)"""
        with patch('sys.argv', ['app.py', '-c']):
            args = parse_cli_args()
            self.assertTrue(args.chat)
    
    def test_parse_cli_args_name(self):
        """Test parse_cli_args with name argument"""
        with patch('sys.argv', ['app.py', '--name', 'TestUser']):
            args = parse_cli_args()
            self.assertEqual(args.name, 'TestUser')
    
    def test_parse_cli_args_multiple_flags(self):
        """Test parse_cli_args with multiple flags"""
        with patch('sys.argv', ['app.py', '--version', '--test', '--chat']):
            args = parse_cli_args()
            self.assertTrue(args.version)
            self.assertTrue(args.test)
            self.assertTrue(args.chat)
    
    def test_process_cli_args_version(self):
        """Test process_cli_args with version flag"""
        mock_args = MagicMock()
        mock_args.version = True
        mock_args.show_scale = False
        mock_args.test = False
        mock_args.chat = False
        mock_args.mood = None
        mock_args.name = None
        
        result = process_cli_args(mock_args)
        
        self.assertEqual(result['action'], 'version')
        self.assertFalse(result['chat_mode'])
        self.assertIsNone(result['mood'])
        self.assertIsNone(result['user_name'])
    
    def test_process_cli_args_show_scale(self):
        """Test process_cli_args with show-scale flag"""
        mock_args = MagicMock()
        mock_args.version = False
        mock_args.show_scale = True
        mock_args.test = False
        mock_args.chat = False
        mock_args.mood = None
        mock_args.name = None
        
        result = process_cli_args(mock_args)
        
        self.assertEqual(result['action'], 'show_scale')
    
    def test_process_cli_args_test(self):
        """Test process_cli_args with test flag"""
        mock_args = MagicMock()
        mock_args.version = False
        mock_args.show_scale = False
        mock_args.test = True
        mock_args.chat = False
        mock_args.mood = None
        mock_args.name = None
        
        result = process_cli_args(mock_args)
        
        self.assertEqual(result['action'], 'test')
    
    def test_process_cli_args_chat(self):
        """Test process_cli_args with chat flag (NEW)"""
        mock_args = MagicMock()
        mock_args.version = False
        mock_args.show_scale = False
        mock_args.test = False
        mock_args.chat = True
        mock_args.mood = None
        mock_args.name = None
        
        result = process_cli_args(mock_args)
        
        self.assertEqual(result['action'], 'run')
        self.assertTrue(result['chat_mode'])
    
    def test_process_cli_args_with_mood(self):
        """Test process_cli_args with mood argument"""
        mock_args = MagicMock()
        mock_args.version = False
        mock_args.show_scale = False
        mock_args.test = False
        mock_args.chat = False
        mock_args.mood = '3'
        mock_args.name = None
        
        # Mock assess_mood to return a test result
        with patch('rules.assess_mood') as mock_assess:
            mock_assess.return_value = {'level': 3, 'description': 'Neutral', 'emoji': '😐'}
            
            result = process_cli_args(mock_args)
            
            self.assertEqual(result['action'], 'run')
            self.assertEqual(result['mood']['level'], 3)
            mock_assess.assert_called_once_with('3')
    
    def test_process_cli_args_with_invalid_mood(self):
        """Test process_cli_args with invalid mood argument"""
        mock_args = MagicMock()
        mock_args.version = False
        mock_args.show_scale = False
        mock_args.test = False
        mock_args.chat = False
        mock_args.mood = 'invalid'
        mock_args.name = None
        
        # Mock assess_mood to return None
        with patch('rules.assess_mood') as mock_assess:
            mock_assess.return_value = None
            
            result = process_cli_args(mock_args)
            
            self.assertEqual(result['action'], 'run')
            self.assertIsNone(result['mood'])
    
    def test_process_cli_args_with_name(self):
        """Test process_cli_args with name argument"""
        mock_args = MagicMock()
        mock_args.version = False
        mock_args.show_scale = False
        mock_args.test = False
        mock_args.chat = False
        mock_args.mood = None
        mock_args.name = 'TestUser'
        
        result = process_cli_args(mock_args)
        
        self.assertEqual(result['action'], 'run')
        self.assertEqual(result['user_name'], 'TestUser')
    
    def test_process_cli_args_default(self):
        """Test process_cli_args with no flags (default)"""
        mock_args = MagicMock()
        mock_args.version = False
        mock_args.show_scale = False
        mock_args.test = False
        mock_args.chat = False
        mock_args.mood = None
        mock_args.name = None
        
        result = process_cli_args(mock_args)
        
        self.assertEqual(result['action'], 'run')
        self.assertFalse(result['chat_mode'])
        self.assertIsNone(result['mood'])
        self.assertIsNone(result['user_name'])

class TestRulesIntegration(unittest.TestCase):
    """Integration tests for rules module"""
    
    def test_full_cli_workflow(self):
        """Test complete CLI workflow from parsing to processing"""
        # Test with version flag
        with patch('sys.argv', ['app.py', '--version']):
            args = parse_cli_args()
            result = process_cli_args(args)
            self.assertEqual(result['action'], 'version')
        
        # Test with chat flag (NEW)
        with patch('sys.argv', ['app.py', '--chat']):
            args = parse_cli_args()
            result = process_cli_args(args)
            self.assertEqual(result['action'], 'run')
            self.assertTrue(result['chat_mode'])
        
        # Test with mood and name
        with patch('sys.argv', ['app.py', '--mood', '4', '--name', 'Alice']):
            with patch('rules.assess_mood') as mock_assess:
                mock_assess.return_value = {'level': 4, 'description': 'Good', 'emoji': '🙂'}
                
                args = parse_cli_args()
                result = process_cli_args(args)
                
                self.assertEqual(result['action'], 'run')
                self.assertEqual(result['mood']['level'], 4)
                self.assertEqual(result['user_name'], 'Alice')
    
    def test_menu_validation_integration(self):
        """Test integration between validation functions"""
        # Get all valid options
        all_options = get_valid_menu_options()
        
        # Flatten the list of all valid choices
        all_valid_choices = []
        for option_list in all_options.values():
            all_valid_choices.extend(option_list)
        
        # Test each valid choice
        for choice in all_valid_choices:
            with self.subTest(choice=choice):
                # Should be valid
                self.assertTrue(is_valid_menu_choice(choice))
                
                # Should map to an option number
                option_num = get_menu_option_number(choice)
                self.assertIsNotNone(option_num)
                self.assertIn(option_num, ['1', '2', '3', '4', '5', '6'])
                
                # Should be in the valid options list
                self.assertIn(choice.lower(), [c.lower() for c in all_options[option_num]])

def run_rules_tests():
    """Run all rules module tests and display results"""
    print("Running Rules Module Unit Tests...")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestValidationFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestCLIFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestRulesIntegration))
    
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
            print(traceback[:200])  # Print first 200 chars of traceback
    
    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == "__main__":
    success = run_rules_tests()
    if success:
        print("\n✓ All rules module tests passed!")
    else:
        print("\n✗ Some rules module tests failed.")