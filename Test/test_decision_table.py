# test_decision_table.py - Comprehensive unit tests for decision table
import unittest
from src.decision_table import DecisionTable, decision_table

class TestDecisionTableClass(unittest.TestCase):
    """Test cases for DecisionTable class"""
    
    def setUp(self):
        """Set up test fixture - fresh DecisionTable for each test"""
        self.dt = DecisionTable()
    
    def test_initialization(self):
        """Test DecisionTable initialization"""
        self.assertIsInstance(self.dt.rules, list)
        self.assertGreater(len(self.dt.rules), 0)
        
        # Should have 7 rules (R1-R6 + Default)
        self.assertEqual(len(self.dt.rules), 7)
    
    def test_rule_structure(self):
        """Test that each rule has correct structure"""
        for rule in self.dt.rules:
            # Each rule should be a tuple with 3 elements
            self.assertIsInstance(rule, tuple)
            self.assertEqual(len(rule), 3)
            
            # Unpack the rule
            condition, rule_number, output_message = rule
            
            # Check types
            self.assertTrue(callable(condition))
            self.assertIsInstance(rule_number, str)
            self.assertIsInstance(output_message, str)
            
            # Output message should not be empty
            self.assertGreater(len(output_message), 0)
    
    def test_evaluate_daily_reflection(self):
        """Test evaluation for Daily Reflection choices"""
        test_cases = ['1', 'one', 'daily', 'd', 'day']
        
        for choice in test_cases:
            with self.subTest(choice=choice):
                result = self.dt.evaluate(choice)
                self.assertEqual(result['rule_number'], 'R1')
                self.assertEqual(result['output_message'], 'Starting Daily Reflection...')
                self.assertEqual(result['input_received'], choice)
    
    def test_evaluate_weekly_checkin(self):
        """Test evaluation for Weekly Check-in choices"""
        test_cases = ['2', 'two', 'weekly', 'w', 'week']
        
        for choice in test_cases:
            with self.subTest(choice=choice):
                result = self.dt.evaluate(choice)
                self.assertEqual(result['rule_number'], 'R2')
                self.assertEqual(result['output_message'], 'Starting Weekly Check-in...')
                self.assertEqual(result['input_received'], choice)
    
    def test_evaluate_view_entries(self):
        """Test evaluation for View Entries choices"""
        test_cases = ['3', 'three', 'view', 'v', 'entries', 'journal']
        
        for choice in test_cases:
            with self.subTest(choice=choice):
                result = self.dt.evaluate(choice)
                self.assertEqual(result['rule_number'], 'R3')
                self.assertEqual(result['output_message'], 'Viewing Previous Entries...')
                self.assertEqual(result['input_received'], choice)
    
    def test_evaluate_weekly_recap(self):
        """Test evaluation for Weekly Recap choices"""
        test_cases = ['4', 'four', 'recap', 'r', 'summary']
        
        for choice in test_cases:
            with self.subTest(choice=choice):
                result = self.dt.evaluate(choice)
                self.assertEqual(result['rule_number'], 'R4')
                self.assertEqual(result['output_message'], 'Generating Weekly Recap...')
                self.assertEqual(result['input_received'], choice)
    
    def test_evaluate_chat_mode(self):
        """Test evaluation for Chat Mode choices (NEW)"""
        test_cases = ['5', 'five', 'chat', 'c', 'talk', 'conversation']
        
        for choice in test_cases:
            with self.subTest(choice=choice):
                result = self.dt.evaluate(choice)
                self.assertEqual(result['rule_number'], 'R5')
                self.assertEqual(result['output_message'], 'Starting Chat Mode...')
                self.assertEqual(result['input_received'], choice)
    
    def test_evaluate_exit_program(self):
        """Test evaluation for Exit Program choices"""
        test_cases = ['6', 'six', 'exit', 'e', 'quit', 'q', 'bye']
        
        for choice in test_cases:
            with self.subTest(choice=choice):
                result = self.dt.evaluate(choice)
                self.assertEqual(result['rule_number'], 'R6')
                self.assertEqual(result['output_message'], 'Exiting Program...')
                self.assertEqual(result['input_received'], choice)
    
    def test_evaluate_case_insensitive(self):
        """Test evaluation is case insensitive"""
        test_cases = [
            ('ONE', 'R1'),
            ('DAILY', 'R1'),
            ('CHAT', 'R5'),      # NEW: Chat mode
            ('EXIT', 'R6'),
            ('Quit', 'R6'),
        ]
        
        for choice, expected_rule in test_cases:
            with self.subTest(choice=choice):
                result = self.dt.evaluate(choice)
                self.assertEqual(result['rule_number'], expected_rule)
    
    def test_evaluate_whitespace(self):
        """Test evaluation handles whitespace"""
        test_cases = [
            (' 1 ', 'R1'),
            (' daily ', 'R1'),
            (' chat ', 'R5'),    # NEW: Chat mode
            (' exit ', 'R6'),
            ('\t3\t', 'R3'),
            ('\n5\n', 'R5'),     # NEW: Chat mode
        ]
        
        for choice, expected_rule in test_cases:
            with self.subTest(choice=choice):
                result = self.dt.evaluate(choice)
                self.assertEqual(result['rule_number'], expected_rule)
                # Input should be preserved with whitespace
                self.assertEqual(result['input_received'], choice)
    
    def test_evaluate_invalid_choices(self):
        """Test evaluation with invalid choices"""
        invalid_choices = [
            '0', '7', '8', '9',
            'invalid', 'help', 'menu',
            'dai', 'weekl', 'cha',  # Partial matches
            '', '   ',               # Empty/whitespace
        ]
        
        for choice in invalid_choices:
            with self.subTest(choice=choice):
                result = self.dt.evaluate(choice)
                self.assertEqual(result['rule_number'], 'Default')
                self.assertEqual(result['output_message'], 'Invalid choice')
                self.assertEqual(result['input_received'], choice)
    
    def test_get_valid_choices(self):
        """Test get_valid_choices method"""
        valid_choices = self.dt.get_valid_choices()
        
        # Should return a list
        self.assertIsInstance(valid_choices, list)
        
        # Should have at least the basic options
        expected_options = ['1', 'one', 'daily', '2', 'two', 'weekly', 
                           '3', 'three', 'view', '4', 'four', 'recap',
                           '5', 'five', 'chat', '6', 'six', 'exit']  # Updated for chat mode
        
        for option in expected_options:
            self.assertIn(option, valid_choices)
        
        # Should not include invalid options
        self.assertNotIn('0', valid_choices)
        self.assertNotIn('7', valid_choices)
        self.assertNotIn('invalid', valid_choices)
    
    def test_get_options_for_rule(self):
        """Test _get_options_for_rule helper method"""
        test_cases = [
            ('R1', ['1', 'one', 'daily']),
            ('R2', ['2', 'two', 'weekly']),
            ('R3', ['3', 'three', 'view']),
            ('R4', ['4', 'four', 'recap']),
            ('R5', ['5', 'five', 'chat']),  # NEW: Chat mode
            ('R6', ['6', 'six', 'exit']),
            ('Invalid', []),  # Non-existent rule
            ('Default', []),  # Default rule
        ]
        
        for rule_number, expected_options in test_cases:
            with self.subTest(rule=rule_number):
                options = self.dt._get_options_for_rule(rule_number)
                self.assertEqual(options, expected_options)
    
    def test_rule_order(self):
        """Test that rules are evaluated in correct order"""
        # Create a test case that could match multiple rules
        # 'daily' should match R1, not any other rule
        
        result = self.dt.evaluate('daily')
        self.assertEqual(result['rule_number'], 'R1')
        
        # 'exit' should match R6
        result = self.dt.evaluate('exit')
        self.assertEqual(result['rule_number'], 'R6')
    
    def test_default_rule_position(self):
        """Test that default rule is last"""
        # Default rule should be the last one
        last_rule = self.dt.rules[-1]
        _, rule_number, _ = last_rule
        self.assertEqual(rule_number, 'Default')
        
        # Default rule condition should always return True
        condition, _, _ = last_rule
        self.assertTrue(condition('anything'))
        self.assertTrue(condition(''))
        self.assertTrue(condition('123'))

class TestGlobalDecisionTable(unittest.TestCase):
    """Test cases for the global decision_table instance"""
    
    def test_global_instance_exists(self):
        """Test that global decision_table instance exists"""
        self.assertIsInstance(decision_table, DecisionTable)
    
    def test_global_instance_functionality(self):
        """Test functionality of global decision_table instance"""
        # Test some evaluations
        test_cases = [
            ('1', 'R1'),
            ('chat', 'R5'),  # NEW: Chat mode
            ('exit', 'R6'),
            ('invalid', 'Default'),
        ]
        
        for choice, expected_rule in test_cases:
            with self.subTest(choice=choice):
                result = decision_table.evaluate(choice)
                self.assertEqual(result['rule_number'], expected_rule)
    
    def test_global_valid_choices(self):
        """Test get_valid_choices on global instance"""
        valid_choices = decision_table.get_valid_choices()
        
        self.assertIsInstance(valid_choices, list)
        self.assertGreater(len(valid_choices), 0)
        
        # Should include chat mode options
        self.assertIn('chat', valid_choices)
        self.assertIn('5', valid_choices)

class TestDecisionTableIntegration(unittest.TestCase):
    """Integration tests for decision table"""
    
    def test_decision_table_with_rules_module(self):
        """Test decision table works with rules module validation"""
        from src.rules import is_valid_menu_choice, get_menu_option_number
        
        # Get all valid choices from decision table
        valid_choices = decision_table.get_valid_choices()
        
        # All should be valid according to rules module
        for choice in valid_choices:
            with self.subTest(choice=choice):
                self.assertTrue(is_valid_menu_choice(choice))
                
                # Should map to an option number
                option_num = get_menu_option_number(choice)
                self.assertIsNotNone(option_num)
                
                # Decision table should give appropriate rule
                result = decision_table.evaluate(choice)
                self.assertNotEqual(result['rule_number'], 'Default')
        
        # Test some invalid choices
        invalid_choices = ['0', '7', 'invalid', 'help']
        for choice in invalid_choices:
            with self.subTest(choice=choice):
                self.assertFalse(is_valid_menu_choice(choice))
                
                # Should map to None
                option_num = get_menu_option_number(choice)
                self.assertIsNone(option_num)
                
                # Decision table should give Default rule
                result = decision_table.evaluate(choice)
                self.assertEqual(result['rule_number'], 'Default')
    
    def test_rule_consistency(self):
        """Test that decision table rules are consistent"""
        # Test that each rule gives consistent output for its inputs
        rule_mappings = {
            'R1': ['1', 'one', 'daily'],
            'R2': ['2', 'two', 'weekly'],
            'R3': ['3', 'three', 'view'],
            'R4': ['4', 'four', 'recap'],
            'R5': ['5', 'five', 'chat'],  # NEW: Chat mode
            'R6': ['6', 'six', 'exit'],
        }
        
        for rule_number, inputs in rule_mappings.items():
            for choice in inputs:
                with self.subTest(rule=rule_number, choice=choice):
                    result = decision_table.evaluate(choice)
                    self.assertEqual(result['rule_number'], rule_number)
                    
                    # Check output message is appropriate
                    if rule_number == 'R1':
                        self.assertIn('Daily Reflection', result['output_message'])
                    elif rule_number == 'R5':  # NEW: Chat mode
                        self.assertIn('Chat Mode', result['output_message'])
                    elif rule_number == 'R6':
                        self.assertIn('Exiting', result['output_message'])

def run_decision_table_tests():
    """Run all decision table tests and display results"""
    print("Running Decision Table Unit Tests...")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestDecisionTableClass))
    suite.addTests(loader.loadTestsFromTestCase(TestGlobalDecisionTable))
    suite.addTests(loader.loadTestsFromTestCase(TestDecisionTableIntegration))
    
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
    success = run_decision_table_tests()
    if success:
        print("\n✓ All decision table tests passed!")
    else:
        print("\n✗ Some decision table tests failed.")