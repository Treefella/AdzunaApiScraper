import unittest
from unittest.mock import patch, MagicMock
import sys

# Mock tkinter for testing
sys.modules['tkinter'] = MagicMock()

# Import after mocking tkinter
import importlib
adzuna_scraper = importlib.import_module('AdzunaApiScraper')

class TestAdzunaJobScraper(unittest.TestCase):
    """Test cases for Adzuna API job scraper."""
    
    @patch('requests.get')
    def test_get_adzuna_jobs_success(self, mock_get):
        """Test successful API call to Adzuna."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'count': 150}
        mock_get.return_value = mock_response
        
        result = adzuna_scraper.get_adzuna_jobs('test_id', 'test_key', 'python', 'UK')
        self.assertEqual(result, 150)
    
    @patch('requests.get')
    def test_get_adzuna_jobs_api_error(self, mock_get):
        """Test API error handling."""
        mock_get.side_effect = Exception("API Error")
        
        result = adzuna_scraper.get_adzuna_jobs('test_id', 'test_key', 'python', 'UK')
        self.assertIsNone(result)
    
    @patch('requests.get')
    def test_get_adzuna_jobs_missing_count(self, mock_get):
        """Test handling when count is missing from response."""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        
        result = adzuna_scraper.get_adzuna_jobs('test_id', 'test_key', 'python', 'UK')
        self.assertEqual(result, 0)

class TestAdzunaIntegration(unittest.TestCase):
    """Integration tests for the Adzuna job scraper team."""
    
    @patch('requests.get')
    def test_full_search_pipeline(self, mock_get):
        """Test complete search workflow."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'count': 200}
        mock_get.return_value = mock_response
        
        result = adzuna_scraper.get_adzuna_jobs('app123', 'key456', 'javascript', 'London')
        
        self.assertEqual(result, 200)
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        self.assertIn('javascript', call_args)
        self.assertIn('London', call_args)
    
    @patch('requests.get')
    def test_multiple_search_queries(self, mock_get):
        """Test multiple search queries in sequence."""
        mock_response = MagicMock()
        
        # First call returns 100 jobs
        mock_response.json.return_value = {'count': 100}
        mock_get.return_value = mock_response
        result1 = adzuna_scraper.get_adzuna_jobs('app1', 'key1', 'python', 'UK')
        
        # Second call returns 150 jobs
        mock_response.json.return_value = {'count': 150}
        result2 = adzuna_scraper.get_adzuna_jobs('app1', 'key1', 'java', 'US')
        
        self.assertEqual(result1, 100)
        self.assertEqual(result2, 150)
    
    def test_results_list_format(self):
        """Test that results list format is correct."""
        results = [
            {"search_term": "python", "location": "UK", "count": 100},
            {"search_term": "java", "location": "US", "count": 150}
        ]
        
        for result in results:
            self.assertIn("search_term", result)
            self.assertIn("location", result)
            self.assertIn("count", result)
            self.assertIsInstance(result["count"], int)

if __name__ == '__main__':
    unittest.main()

