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

if __name__ == '__main__':
    unittest.main()
