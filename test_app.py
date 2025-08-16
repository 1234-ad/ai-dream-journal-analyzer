"""
Unit tests for AI Dream Journal Analyzer
"""
import unittest
import sys
import os
from datetime import datetime, date
import json

# Add the current directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import (
    DataValidator, DataProcessor, ErrorHandler, 
    AdvancedAnalyzer, export_dreams_advanced, calculate_dream_statistics
)

class TestDataValidator(unittest.TestCase):
    """Test the DataValidator class"""
    
    def setUp(self):
        self.validator = DataValidator()
    
    def test_validate_dream_text_valid(self):
        """Test valid dream text"""
        valid_text = "I had a wonderful dream about flying over mountains."
        is_valid, message = self.validator.validate_dream_text(valid_text)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Valid")
    
    def test_validate_dream_text_empty(self):
        """Test empty dream text"""
        is_valid, message = self.validator.validate_dream_text("")
        self.assertFalse(is_valid)
        self.assertIn("cannot be empty", message)
    
    def test_validate_dream_text_too_short(self):
        """Test too short dream text"""
        short_text = "Short"
        is_valid, message = self.validator.validate_dream_text(short_text)
        self.assertFalse(is_valid)
        self.assertIn("too short", message)
    
    def test_validate_dream_text_too_long(self):
        """Test too long dream text"""
        long_text = "A" * 5001
        is_valid, message = self.validator.validate_dream_text(long_text)
        self.assertFalse(is_valid)
        self.assertIn("too long", message)
    
    def test_validate_sleep_quality_valid(self):
        """Test valid sleep quality"""
        is_valid, message = self.validator.validate_sleep_quality(7)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Valid")
    
    def test_validate_sleep_quality_invalid_range(self):
        """Test invalid sleep quality range"""
        is_valid, message = self.validator.validate_sleep_quality(11)
        self.assertFalse(is_valid)
        self.assertIn("between 1 and 10", message)
    
    def test_validate_date_valid(self):
        """Test valid date"""
        today = date.today()
        is_valid, message = self.validator.validate_date(today)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Valid")
    
    def test_validate_date_future(self):
        """Test future date"""
        from datetime import timedelta
        future_date = date.today() + timedelta(days=1)
        is_valid, message = self.validator.validate_date(future_date)
        self.assertFalse(is_valid)
        self.assertIn("cannot be in the future", message)

class TestDataProcessor(unittest.TestCase):
    """Test the DataProcessor class"""
    
    def setUp(self):
        self.processor = DataProcessor()
    
    def test_clean_text(self):
        """Test text cleaning"""
        dirty_text = "  This   has    extra   spaces!  "
        clean_text = self.processor.clean_text(dirty_text)
        self.assertEqual(clean_text, "This has extra spaces!")
    
    def test_extract_keywords(self):
        """Test keyword extraction"""
        text = "I was flying over the beautiful mountains and rivers"
        keywords = self.processor.extract_keywords(text)
        
        # Should include meaningful words
        self.assertIn("flying", keywords)
        self.assertIn("beautiful", keywords)
        self.assertIn("mountains", keywords)
        
        # Should exclude stop words
        self.assertNotIn("was", keywords)
        self.assertNotIn("the", keywords)
        self.assertNotIn("and", keywords)

class TestAdvancedAnalyzer(unittest.TestCase):
    """Test the AdvancedAnalyzer class"""
    
    def setUp(self):
        self.analyzer = AdvancedAnalyzer()
    
    def test_analyze_dream_complexity(self):
        """Test dream complexity analysis"""
        dream_text = "I was flying over a beautiful landscape with mountains and rivers. The feeling was incredible."
        
        result = self.analyzer.analyze_dream_complexity(dream_text)
        
        # Check that all expected keys are present
        expected_keys = [
            'word_count', 'sentence_count', 'avg_sentence_length',
            'uniqueness_ratio', 'symbol_density', 'complexity_score'
        ]
        
        for key in expected_keys:
            self.assertIn(key, result)
        
        # Check reasonable values
        self.assertGreater(result['word_count'], 0)
        self.assertGreater(result['complexity_score'], 0)
        self.assertLessEqual(result['complexity_score'], 100)
    
    def test_detect_lucidity_indicators(self):
        """Test lucidity detection"""
        lucid_text = "I realized I was dreaming and took control of the dream"
        non_lucid_text = "I was walking in a park and saw a dog"
        
        lucid_result = self.analyzer.detect_lucidity_indicators(lucid_text)
        non_lucid_result = self.analyzer.detect_lucidity_indicators(non_lucid_text)
        
        # Lucid dream should have higher probability
        self.assertGreater(lucid_result['probability'], non_lucid_result['probability'])
        self.assertTrue(lucid_result['likely_lucid'])
        self.assertFalse(non_lucid_result['likely_lucid'])

class TestExportFunctions(unittest.TestCase):
    """Test export and statistics functions"""
    
    def setUp(self):
        self.sample_dreams = [
            {
                'date': '2025-01-15',
                'text': 'Flying dream',
                'polarity': 0.8,
                'emotion': 'joy',
                'themes': ['flying'],
                'lucid': True,
                'sleep_quality': 9
            },
            {
                'date': '2025-01-14',
                'text': 'Scary nightmare',
                'polarity': -0.7,
                'emotion': 'fear',
                'themes': ['chase'],
                'lucid': False,
                'sleep_quality': 4
            }
        ]
    
    def test_export_dreams_json(self):
        """Test JSON export"""
        result = export_dreams_advanced(self.sample_dreams, 'json')
        
        # Should be valid JSON
        parsed = json.loads(result)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]['emotion'], 'joy')
    
    def test_export_dreams_csv(self):
        """Test CSV export"""
        result = export_dreams_advanced(self.sample_dreams, 'csv')
        
        # Should contain CSV headers
        self.assertIn('date', result)
        self.assertIn('text', result)
        self.assertIn('emotion', result)
    
    def test_export_dreams_markdown(self):
        """Test Markdown export"""
        result = export_dreams_advanced(self.sample_dreams, 'markdown')
        
        # Should contain markdown formatting
        self.assertIn('# Dream Journal Export', result)
        self.assertIn('## Dream 1', result)
        self.assertIn('**Text:**', result)
    
    def test_calculate_dream_statistics(self):
        """Test statistics calculation"""
        stats = calculate_dream_statistics(self.sample_dreams)
        
        # Check basic stats
        self.assertEqual(stats['total_dreams'], 2)
        self.assertEqual(stats['lucid_dream_stats']['total_lucid'], 1)
        self.assertEqual(stats['lucid_dream_stats']['lucid_percentage'], 50.0)
        
        # Check sentiment stats
        self.assertAlmostEqual(stats['sentiment_stats']['mean_polarity'], 0.05, places=2)

class TestErrorHandling(unittest.TestCase):
    """Test error handling functionality"""
    
    def test_handle_analysis_error(self):
        """Test analysis error handling"""
        test_error = ValueError("Test error")
        result = ErrorHandler.handle_analysis_error(test_error, "test_context")
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
        self.assertIn('fallback_data', result)
    
    def test_handle_data_error(self):
        """Test data error handling"""
        test_error = KeyError("Test key error")
        result = ErrorHandler.handle_data_error(test_error, "test_operation")
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
        self.assertIn('suggestion', result)

def run_tests():
    """Run all tests and return results"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestDataValidator,
        TestDataProcessor,
        TestAdvancedAnalyzer,
        TestExportFunctions,
        TestErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result

if __name__ == '__main__':
    print("🧪 Running AI Dream Journal Analyzer Tests...")
    print("=" * 50)
    
    result = run_tests()
    
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"- {test}: {traceback}")
        
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"- {test}: {traceback}")