# test_mood_assessment.py - Comprehensive unit tests for mood assessment
import unittest
from src.mood_assessment import (
    assess_mood, 
    display_mood_scale, 
    get_mood_color, 
    suggest_mood_activities
)

class TestMoodAssessment(unittest.TestCase):
    """Test cases for the mood assessment module"""
    
    def test_assess_mood_numeric_valid(self):
        """Test mood assessment with valid numeric inputs"""
        test_cases = [
            ("1", 1, "Very Low", "😔"),
            ("2", 2, "Low", "😟"),
            ("3", 3, "Neutral", "😐"),
            ("4", 4, "Good", "🙂"),
            ("5", 5, "Very Good", "😊"),
        ]
        
        for input_str, expected_level, expected_desc, expected_emoji in test_cases:
            with self.subTest(input=input_str):
                result = assess_mood(input_str)
                self.assertIsNotNone(result, f"Failed for input: {input_str}")
                self.assertEqual(result['level'], expected_level)
                self.assertEqual(result['description'], expected_desc)
                self.assertEqual(result['emoji'], expected_emoji)
    
    def test_assess_mood_word_valid(self):
        """Test mood assessment with valid word inputs"""
        test_cases = [
            ("terrible", 1, "Very Low", "😔"),
            ("sad", 2, "Low", "😟"),
            ("meh", 3, "Neutral", "😐"),
            ("happy", 4, "Good", "🙂"),
            ("fantastic", 5, "Very Good", "😊"),
        ]
        
        for input_str, expected_level, expected_desc, expected_emoji in test_cases:
            with self.subTest(input=input_str):
                result = assess_mood(input_str)
                self.assertIsNotNone(result, f"Failed for input: {input_str}")
                self.assertEqual(result['level'], expected_level)
                self.assertEqual(result['description'], expected_desc)
                self.assertEqual(result['emoji'], expected_emoji)
    
    def test_assess_mood_case_insensitive(self):
        """Test mood assessment is case insensitive"""
        test_cases = ["SAD", "Sad", "sAd", "sad"]
        
        for input_str in test_cases:
            with self.subTest(input=input_str):
                result = assess_mood(input_str)
                self.assertIsNotNone(result, f"Failed for input: {input_str}")
                self.assertEqual(result['level'], 2)
    
    def test_assess_mood_with_modifiers(self):
        """Test mood assessment with modifiers like 'very' and 'a bit'"""
        test_cases = [
            ("very sad", 1),      # sad=2, very makes it 1
            ("a bit happy", 3),   # happy=4, a bit makes it 3
            ("slightly good", 3), # good=4, slightly makes it 3
            ("very good", 5),     # good=4, very makes it 5
        ]
        
        for input_str, expected_level in test_cases:
            with self.subTest(input=input_str):
                result = assess_mood(input_str)
                self.assertIsNotNone(result, f"Failed for input: {input_str}")
                self.assertEqual(result['level'], expected_level)
    
    def test_assess_mood_invalid(self):
        """Test mood assessment with invalid inputs"""
        invalid_inputs = [
            "",           # empty string
            "   ",        # whitespace only
            "0",          # below range
            "6",          # above range
            "invalid",    # not in dictionary
            "extremely",  # not a mood word
            "123",        # multi-digit number
        ]
        
        for input_str in invalid_inputs:
            with self.subTest(input=input_str):
                result = assess_mood(input_str)
                self.assertIsNone(result, f"Should have returned None for: {input_str}")
    
    def test_assess_mood_whitespace_handling(self):
        """Test mood assessment handles whitespace properly"""
        test_cases = [
            (" 3 ", 3),
            (" happy ", 4),
            ("\tsad\t", 2),
            ("\n5\n", 5),
        ]
        
        for input_str, expected_level in test_cases:
            with self.subTest(input=input_str):
                result = assess_mood(input_str)
                self.assertIsNotNone(result, f"Failed for input: {input_str}")
                self.assertEqual(result['level'], expected_level)
    
    def test_display_mood_scale(self):
        """Test that mood scale display returns a string with expected content"""
        scale = display_mood_scale()
        
        # Should return a string
        self.assertIsInstance(scale, str)
        
        # Should be reasonably long
        self.assertGreater(len(scale), 200)
        
        # Should contain expected headers
        self.assertIn("MOOD SCALE", scale)
        self.assertIn("Level", scale)
        self.assertIn("Description", scale)
        
        # Should contain all mood levels
        for level in range(1, 6):
            self.assertIn(str(level), scale)
        
        # Should contain emojis
        self.assertIn("😔", scale)
        self.assertIn("😟", scale)
        self.assertIn("😐", scale)
        self.assertIn("🙂", scale)
        self.assertIn("😊", scale)
        
        # Should contain usage instructions
        self.assertIn("Examples:", scale)
        self.assertIn("You can use", scale)
    
    def test_get_mood_color(self):
        """Test getting color codes for mood levels"""
        test_cases = [
            (1, 'red'),
            (2, 'yellow'),
            (3, 'white'),
            (4, 'cyan'),
            (5, 'green'),
        ]
        
        for level, expected_color in test_cases:
            with self.subTest(level=level):
                color = get_mood_color(level)
                self.assertEqual(color, expected_color)
        
        # Test invalid levels return default
        self.assertEqual(get_mood_color(0), 'white')
        self.assertEqual(get_mood_color(6), 'white')
        self.assertEqual(get_mood_color(-1), 'white')
    
    def test_suggest_mood_activities(self):
        """Test activity suggestions for all mood levels"""
        for level in range(1, 6):
            with self.subTest(level=level):
                activities = suggest_mood_activities(level)
                
                # Should return a list
                self.assertIsInstance(activities, list)
                
                # Should have at least one activity
                self.assertGreater(len(activities), 0)
                
                # All activities should be strings
                for activity in activities:
                    self.assertIsInstance(activity, str)
                    self.assertGreater(len(activity), 5)
        
        # Test edge cases
        self.assertEqual(len(suggest_mood_activities(0)), 1)  # Default
        self.assertEqual(len(suggest_mood_activities(6)), 1)  # Default
    
    def test_suggest_mood_activities_content(self):
        """Test specific activity suggestions for different levels"""
        # Level 1 should have grounding/support activities
        level1_activities = suggest_mood_activities(1)
        self.assertTrue(any('breath' in activity.lower() for activity in level1_activities))
        
        # Level 5 should have celebration activities
        level5_activities = suggest_mood_activities(5)
        self.assertTrue(any('celebrate' in activity.lower() for activity in level5_activities))
    
    def test_mood_consistency(self):
        """Test that mood assessment is consistent across multiple calls"""
        test_inputs = ["3", "happy", "sad", "5"]
        
        for input_str in test_inputs:
            with self.subTest(input=input_str):
                # Call multiple times
                results = []
                for _ in range(5):
                    result = assess_mood(input_str)
                    if result:  # Only append if not None
                        results.append(result)
                
                if results:  # If we got valid results
                    # All results should be the same
                    first_result = results[0]
                    for result in results[1:]:
                        self.assertEqual(result['level'], first_result['level'])
                        self.assertEqual(result['description'], first_result['description'])

class TestMoodAssessmentIntegration(unittest.TestCase):
    """Integration tests for mood assessment with other components"""
    
    def test_mood_range_boundaries(self):
        """Test mood levels stay within valid range"""
        # Test that modifiers don't push levels out of range
        test_cases = [
            ("very terrible", 1),    # Should stay at 1
            ("a bit terrible", 1),   # Should stay at 1
            ("very fantastic", 5),   # Should stay at 5
            ("a bit fantastic", 4),  # Should decrease from 5 to 4
        ]
        
        for input_str, expected_level in test_cases:
            with self.subTest(input=input_str):
                result = assess_mood(input_str)
                if result:  # Some combinations might be invalid
                    self.assertEqual(result['level'], expected_level)
                    self.assertGreaterEqual(result['level'], 1)
                    self.assertLessEqual(result['level'], 5)
    
    def test_mood_with_synonyms(self):
        """Test that synonyms give similar mood levels"""
        synonym_groups = [
            ["terrible", "awful", "horrible"],  # All level 1
            ["sad", "unhappy", "blue"],         # All level 2
            ["okay", "fine", "alright"],        # All level 3
            ["happy", "content", "cheerful"],   # All level 4
            ["great", "fantastic", "wonderful"], # All level 5
        ]
        
        for synonyms in synonym_groups:
            with self.subTest(synonyms=synonyms):
                levels = []
                for word in synonyms:
                    result = assess_mood(word)
                    if result:
                        levels.append(result['level'])
                
                # All synonyms in group should give same level
                if levels:
                    self.assertTrue(all(level == levels[0] for level in levels))

def run_mood_tests():
    """Run all mood assessment tests and display results"""
    print("Running Mood Assessment Unit Tests...")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestMoodAssessment))
    suite.addTests(loader.loadTestsFromTestCase(TestMoodAssessmentIntegration))
    
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
    success = run_mood_tests()
    if success:
        print("\n✓ All mood assessment tests passed!")
    else:
        print("\n✗ Some mood assessment tests failed.")