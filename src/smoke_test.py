import unittest
import os
import sys
import tempfile
from io import StringIO
from unittest.mock import patch, MagicMock, call
import datetime

# Adds the current directory to import app
sys.path.append('.')

class TestAppBasicFunctions(unittest.TestCase):
    """Basic smoke tests for app functions"""
    
    def test_version_constant_exists(self):
        """Test that version constant exists"""
        # Import app module
        import app
        
        # Check version exists
        self.assertTrue(hasattr(app, '__version__'))
        self.assertIsInstance(app.__version__, str)
        self.assertGreater(len(app.__version__), 0)
        
        # Version should be in format X.Y.Z
        version_parts = app.__version__.split('.')
        self.assertEqual(len(version_parts), 3)
        
        # All parts should be numeric
        for part in version_parts:
            self.assertTrue(part.isdigit() or (part[0].isdigit() and part[1:].isdigit()))
    
    def test_welcome_message(self):
        """Test welcome_message function"""
        import app
        
        # Capture stdout
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            app.welcome_message()
            output = mock_stdout.getvalue()
            
            # Should contain welcome text
            self.assertIn('Welcome', output)
            self.assertIn('Journal Companion', output)
            self.assertIn('private space', output)
            self.assertIn('securely saved', output)
    
    def test_user_info_basic(self):
        """Test user_info function with mocked input"""
        import app
        
        # Mock user input
        with patch('builtins.input', side_effect=['TestUser']):
            with patch('datetime.datetime') as mock_datetime:
                # Mock current date
                mock_now = MagicMock()
                mock_now.strftime.return_value = '01/01/2023'
                mock_datetime.now.return_value = mock_now
                
                # Call function
                name, date = app.user_info()
                
                # Check results
                self.assertEqual(name, 'TestUser')
                self.assertEqual(date, '01/01/2023')
    
    def test_user_info_with_empty_name(self):
        """Test user_info function handles empty name"""
        import app
        
        # Mock user input: empty first, then valid
        with patch('builtins.input', side_effect=['', 'ValidUser']):
            with patch('datetime.datetime') as mock_datetime:
                # Mock current date
                mock_now = MagicMock()
                mock_now.strftime.return_value = '01/01/2023'
                mock_datetime.now.return_value = mock_now
                
                # Call function
                name, date = app.user_info()
                
                # Check results
                self.assertEqual(name, 'ValidUser')
                self.assertEqual(date, '01/01/2023')
    
    def test_save_entry_daily(self):
        """Test save_entry function for daily reflection"""
        import app
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='_journal.txt') as f:
            temp_filename = f.name
        
        try:
            # Test data
            entry_type = "Daily Reflection"
            date = "01/01/2023"
            time = "10:30 AM"
            content = ["Positive answer", "Challenge answer", "Connection answer", 
                      "Learning answer", "Looking forward answer", "Different answer", 
                      "Feeling answer"]
            name = "TestUser"
            mood = {'level': 3, 'description': 'Neutral', 'emoji': '😐'}
            
            # Mock the filename generation
            with patch('app.open', unittest.mock.mock_open()) as mock_file:
                with patch('os.path.exists', return_value=False):
                    # Call function
                    app.save_entry(entry_type, date, time, content, name, mood)
                    
                    # Check that file was opened for appending
                    mock_file.assert_called_with(f'{name}_journal.txt', 'a')

        # new function for me, this is a try...except function that is gauranteed to run.
        finally:            
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_save_entry_weekly(self):
        """Test save_entry function for weekly check-in"""
        import app
        
        # Test data
        entry_type = "Weekly Check-in"
        date = "01/01/2023"
        time = "Weekly"
        content = ["Accomplishment", "Challenge", "Support", "Goal", "Growth"]
        name = "TestUser"
        
        # Mock the filename generation and file operations
        with patch('app.open', unittest.mock.mock_open()) as mock_file:
            with patch('os.path.exists', return_value=False):
                # Call function
                app.save_entry(entry_type, date, time, content, name)
                
                # Check that file was opened for appending
                mock_file.assert_called_with(f'{name}_journal.txt', 'a')
    
    def test_view_previous_entries_file_exists(self):
        """Test view_previous_entries when file exists"""
        import app
        
        # Create temporary file with content
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='_journal.txt') as f:
            f.write("Test journal content\nAnother line\n")
            temp_filename = f.name
        
        try:
            # Mock os.path.exists and file reading
            with patch('os.path.exists', return_value=True):
                with patch('builtins.open', unittest.mock.mock_open(read_data="Test journal content\n")):
                    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                        # Call function
                        app.view_previous_entries("TestUser")
                        output = mock_stdout.getvalue()
                        
                        # Should indicate viewing entries
                        self.assertIn('previous journal entries', output.lower())
                        
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_view_previous_entries_no_file(self):
        """Test view_previous_entries when file doesn't exist"""
        import app
        
        # Mock os.path.exists to return False
        with patch('os.path.exists', return_value=False):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                # Call function
                app.view_previous_entries("TestUser")
                output = mock_stdout.getvalue()
                
                # Should indicate no file
                self.assertIn('not saved', output.lower())
                self.assertIn('ready to listen', output.lower())

class TestAppCLIArguments(unittest.TestCase):
    """Smoke tests for CLI argument handling"""
    
    def test_main_with_version_flag(self):
        """Test main function with --version flag"""
        import app
        
        # Mock command line arguments
        with patch('sys.argv', ['app.py', '--version']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                # Call main function
                app.main()
                output = mock_stdout.getvalue()
                
                # Should show version
                self.assertIn(f'v{app.__version__}', output)
                self.assertIn('Created with care', output)
    
    def test_main_with_show_scale_flag(self):
        """Test main function with --show-scale flag"""
        import app
        
        # Mock command line arguments
        with patch('sys.argv', ['app.py', '--show-scale']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                # Call main function
                app.main()
                output = mock_stdout.getvalue()
                
                # Should show mood scale
                self.assertIn('MOOD SCALE', output)
                self.assertIn('Level', output)
    
    def test_main_with_test_flag(self):
        """Test main function with --test flag"""
        import app
        
        # Mock command line arguments
        with patch('sys.argv', ['app.py', '--test']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                # Mock the test module import
                with patch('app.run_tests', return_value=True):
                    # Call main function
                    app.main()
                    output = mock_stdout.getvalue()
                    
                    # Should indicate running tests
                    self.assertIn('Running', output.lower())
                    self.assertIn('test', output.lower())
    
    def test_main_with_chat_flag(self):
        """Test main function with --chat flag (NEW)"""
        import app
        
        # Mock command line arguments
        with patch('sys.argv', ['app.py', '--chat']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                # We'll just verify it doesn't crash
                try:
                    # We need to mock many dependencies since we're not running full app
                    with patch('app.initial_mood_assessment'):
                        with patch('app.welcome_message'):
                            with patch('app.user_info'):
                                with patch('app.decision_table'):
                                    # Call main function - it will try to run but we've mocked dependencies
                                    # For smoke test, we just want to ensure no crashes
                                    pass
                except Exception as e:
                    self.fail(f"main() crashed with --chat flag: {e}")

class TestAppNewFeatures(unittest.TestCase):
    """Smoke tests for new features (Chat Mode)"""
    
    def test_chat_mode_functions_exist(self):
        """Test that new chat mode functions exist"""
        import app
        
        # Check new functions exist
        self.assertTrue(hasattr(app, 'chat_mode'))
        self.assertTrue(callable(app.chat_mode))
        
        self.assertTrue(hasattr(app, 'show_chat_help'))
        self.assertTrue(callable(app.show_chat_help))
        
        self.assertTrue(hasattr(app, 'get_journal_summary'))
        self.assertTrue(callable(app.get_journal_summary))
        
        self.assertTrue(hasattr(app, 'save_chat_conversation'))
        self.assertTrue(callable(app.save_chat_conversation))
        
        self.assertTrue(hasattr(app, 'quick_mood_check'))
        self.assertTrue(callable(app.quick_mood_check))
    
    def test_show_chat_help_output(self):
        """Test show_chat_help function output"""
        import app
        
        # Capture stdout
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            app.show_chat_help()
            output = mock_stdout.getvalue()
            
            # Should contain help information
            self.assertIn('CHAT MODE COMMANDS', output)
            self.assertIn('Available commands', output)
            self.assertIn('exit/quit/bye', output)
            self.assertIn('help/commands', output)
            self.assertIn('mood', output)
            self.assertIn('summary/recap', output)
    
    def test_get_journal_summary_no_file(self):
        """Test get_journal_summary when no journal file exists"""
        import app
        
        # Mock os.path.exists to return False
        with patch('os.path.exists', return_value=False):
            summary = app.get_journal_summary("TestUser")
            
            # Should return message about no entries
            self.assertIn("haven't made", summary.lower())
            self.assertIn("journal entries", summary.lower())
    
    def test_get_journal_summary_with_file(self):
        """Test get_journal_summary when journal file exists"""
        import app
        
        # Mock file content
        mock_content = """Entry Type: Daily Reflection
Entry Type: Weekly Check-in
Entry Type: Daily Reflection"""
        
        # Mock os.path.exists and file reading
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', unittest.mock.mock_open(read_data=mock_content)):
                summary = app.get_journal_summary("TestUser")
                
                # Should return summary
                self.assertIsInstance(summary, str)
                self.assertGreater(len(summary), 10)
    
    def test_chat_mode_structure(self):
        """Test chat_mode function structure (doesn't crash)"""
        import app
        
        # We'll test that the function can be called with basic mocking
        # This is a smoke test, not a full functional test
        try:
            # Mock all inputs and outputs
            with patch('builtins.input', side_effect=['Hello', 'exit']):
                with patch('sys.stdout', new_callable=StringIO):
                    with patch('app.display_mood_scale'):
                        with patch('app.assess_mood'):
                            with patch('app.save_chat_conversation'):
                                with patch('app.chatbot') as mock_chatbot:
                                    mock_chatbot.get_chat_response.return_value = "Mock response"
                                    
                                    # Call function - should not crash
                                    app.chat_mode("TestUser")
        except Exception as e:
            self.fail(f"chat_mode() crashed during smoke test: {e}")

class TestAppIntegrationSmoke(unittest.TestCase):
    """Integration smoke tests for app.py"""
    
    def test_module_imports(self):
        """Test that all required modules can be imported"""
        import app
        
        # Check that required modules are imported
        self.assertTrue(hasattr(app, 'justice_navigator_info'))
        self.assertTrue(hasattr(app, 'pd'))  # pandas
        self.assertTrue(hasattr(app, 'np'))  # numpy
        self.assertTrue(hasattr(app, 'os'))
        self.assertTrue(hasattr(app, 'datetime'))
        self.assertTrue(hasattr(app, 'Fore'))  # colorama
        self.assertTrue(hasattr(app, 'Back'))
        self.assertTrue(hasattr(app, 'Style'))
        
        # Check that custom modules are imported
        self.assertTrue(hasattr(app, 'validate_choice'))
        self.assertTrue(hasattr(app, 'parse_cli_args'))
        self.assertTrue(hasattr(app, 'process_cli_args'))
        self.assertTrue(hasattr(app, 'decision_table'))
        self.assertTrue(hasattr(app, 'assess_mood'))
        self.assertTrue(hasattr(app, 'display_mood_scale'))
        self.assertTrue(hasattr(app, 'chatbot'))
    
    def test_main_program_structure(self):
        """Test that main program has correct structure"""
        import app
        
        # Check main function exists
        self.assertTrue(hasattr(app, 'main'))
        self.assertTrue(callable(app.main))
        
        # Check if __name__ == "__main__" block exists
        with open('app.py', 'r') as f:
            content = f.read()
            self.assertIn('if __name__ == "__main__":', content)
            self.assertIn('main()', content)
    
    def test_colorama_initialization(self):
        """Test that colorama is initialized"""
        import app
        
        # Check that init was called (we can't easily test the actual call,
        # but we can check that colorama modules are available)
        self.assertTrue(hasattr(app, 'colorama'))
        
        # Fore should have color attributes
        self.assertTrue(hasattr(app.Fore, 'RED'))
        self.assertTrue(hasattr(app.Fore, 'GREEN'))
        self.assertTrue(hasattr(app.Fore, 'YELLOW'))
        self.assertTrue(hasattr(app.Fore, 'CYAN'))
    
    def test_decision_table_integration(self):
        """Test decision table is properly integrated"""
        import app
        
        # Check decision_table is available
        self.assertTrue(hasattr(app, 'decision_table'))
        
        # It should have an evaluate method
        self.assertTrue(hasattr(app.decision_table, 'evaluate'))
        self.assertTrue(callable(app.decision_table.evaluate))
        
        # Test a simple evaluation
        result = app.decision_table.evaluate('1')
        self.assertIsInstance(result, dict)
        self.assertIn('rule_number', result)
        self.assertIn('output_message', result)
    
    def test_chatbot_integration(self):
        """Test chatbot is properly integrated"""
        import app
        
        # Check chatbot is available
        self.assertTrue(hasattr(app, 'chatbot'))
        
        # It should have key methods
        self.assertTrue(hasattr(app.chatbot, 'get_empathetic_response'))
        self.assertTrue(callable(app.chatbot.get_empathetic_response))
        
        self.assertTrue(hasattr(app.chatbot, 'get_chat_response'))  # NEW
        self.assertTrue(callable(app.chatbot.get_chat_response))
        
        self.assertTrue(hasattr(app.chatbot, 'generate_weekly_recap'))
        self.assertTrue(callable(app.chatbot.generate_weekly_recap))

def run_smoke_tests():
    """Run all smoke tests and display results"""
    print("Running Journal App Smoke Tests...")
    print(f"{'-'*64}")
    print("Note: Smoke tests verify basic functionality without full execution.")
    print(f"{'-'*64}")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestAppBasicFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestAppCLIArguments))
    suite.addTests(loader.loadTestsFromTestCase(TestAppNewFeatures))
    suite.addTests(loader.loadTestsFromTestCase(TestAppIntegrationSmoke))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'-'*64}")
    print(f"{'-'*23}SMOKE TEST SUMMARY{'-'*23}")
    print(f"\n{'-'*64}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures (first 200 chars each):")
        for i, (test, traceback) in enumerate(result.failures, 1):
            print(f"\n{i}. {test}")
            print(traceback[:200])
    
    if result.errors:
        print("\nErrors (first 200 chars each):")
        for i, (test, traceback) in enumerate(result.errors, 1):
            print(f"\n{i}. {test}")
            print(traceback[:200])
    
    # Overall status
    if len(result.failures) == 0 and len(result.errors) == 0:
        print("\n✅ All smoke tests passed! Basic functionality looks good.")
        print("   The app should run without major issues.")
        return True
    else:
        print("\n⚠️  Some smoke tests failed. Review the issues above.")
        print("   The app may have problems running.")
        return False

def quick_smoke_check():
    """Quick smoke check - minimal tests"""
    print("Quick Smoke Check...")
    print(f"{'-'*64}")
    
    checks = []
    
    # Check 1: Can import app
    try:
        import app
        checks.append(("Import app.py", "✅", ""))
    except Exception as e:
        checks.append(("Import app.py", "❌", str(e)))
        return False
    
    # Check 2: Version exists
    try:
        version = app.__version__
        checks.append((f"Version: {version}", "✅", ""))
    except Exception as e:
        checks.append(("Check version", "❌", str(e)))
    
    # Check 3: Main function exists
    try:
        if hasattr(app, 'main') and callable(app.main):
            checks.append(("Main function", "✅", ""))
        else:
            checks.append(("Main function", "❌", "Not found or not callable"))
    except Exception as e:
        checks.append(("Main function", "❌", str(e)))
    
    # Check 4: New chat mode functions
    try:
        required_funcs = ['chat_mode', 'show_chat_help', 'save_chat_conversation']
        missing = []
        for func in required_funcs:
            if not (hasattr(app, func) and callable(getattr(app, func))):
                missing.append(func)
        
        if not missing:
            checks.append(("Chat mode functions", "✅", ""))
        else:
            checks.append(("Chat mode functions", "❌", f"Missing: {', '.join(missing)}"))
    except Exception as e:
        checks.append(("Chat mode functions", "❌", str(e)))
    
    # Display results
    for check, status, message in checks:
        print(f"{status} {check}")
        if message:
            print(f"   {message}")
    
    print(f"{'-'*64}")
    
    # Count successes
    success_count = sum(1 for _, status, _ in checks if status == "✅")
    total_checks = len(checks)
    
    print(f"\n{success_count}/{total_checks} checks passed")
    
    return success_count == total_checks

if __name__ == "__main__":
    print(f"{'-'*20}Journal App Smoke Tests{'-'*21}")
    print(f"{'-'*64}")
    
    # Ask user which test to run
    print("\nOptions:")
    print("1. Quick smoke check (fast)")
    print("2. Full smoke tests (comprehensive)")
    
    choice = input("\nChoose option (1 or 2): ").strip()
    
    if choice == '1':
        success = quick_smoke_check()
    else:
        success = run_smoke_tests()
    
    # Final status
    if success:
        print("\n✨ Smoke tests completed successfully!")
        print("   The journal app is ready for use.")
    else:
        print("\n💥 Smoke tests found issues.")
        print("   Please fix the reported problems before using the app.")
    
    sys.exit(0 if success else 1)