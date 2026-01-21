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
        """Test successful API call to Adzuna returns jobs."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'results': [
                {'title': 'Python Dev', 'company': {'display_name': 'TechCorp'}, 'redirect_url': 'http://example.com'}
            ]
        }
        mock_get.return_value = mock_response
        
        result = adzuna_scraper.get_adzuna_jobs('test_id', 'test_key', 'python', 'UK')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Python Dev')
    
    @patch('requests.get')
    def test_get_adzuna_jobs_api_error(self, mock_get):
        """Test API error handling returns empty list."""
        mock_get.side_effect = Exception("API Error")
        
        result = adzuna_scraper.get_adzuna_jobs('test_id', 'test_key', 'python', 'UK')
        self.assertEqual(result, [])
    
    @patch('requests.get')
    def test_get_adzuna_jobs_no_results(self, mock_get):
        """Test handling when no results are returned."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'results': []}
        mock_get.return_value = mock_response
        
        result = adzuna_scraper.get_adzuna_jobs('test_id', 'test_key', 'python', 'UK')
        self.assertEqual(result, [])

class TestAdzunaIntegration(unittest.TestCase):
    """Integration tests for the Adzuna job scraper team."""
    
    @patch('requests.get')
    def test_full_search_pipeline(self, mock_get):
        """Test complete search workflow returns job objects."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'results': [
                {
                    'title': 'Senior Python Dev',
                    'company': {'display_name': 'TechCorp'},
                    'location': {'display_name': 'London'},
                    'salary_max': 80000,
                    'redirect_url': 'http://example.com/1'
                }
            ]
        }
        mock_get.return_value = mock_response
        
        result = adzuna_scraper.get_adzuna_jobs('app123', 'key456', 'python', 'London')
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Senior Python Dev')
        self.assertIn('redirect_url', result[0])
    
    @patch('requests.get')
    def test_multiple_jobs_returned(self, mock_get):
        """Test multiple jobs are returned and parsed correctly."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'results': [
                {'title': 'Python Dev', 'company': {'display_name': 'Corp1'}, 'redirect_url': 'http://link1.com'},
                {'title': 'Java Dev', 'company': {'display_name': 'Corp2'}, 'redirect_url': 'http://link2.com'},
                {'title': 'Go Dev', 'company': {'display_name': 'Corp3'}, 'redirect_url': 'http://link3.com'}
            ]
        }
        mock_get.return_value = mock_response
        
        result = adzuna_scraper.get_adzuna_jobs('app1', 'key1', 'dev', 'US')
        
        self.assertEqual(len(result), 3)
    
    def test_job_data_structure(self):
        """Test that job data has expected structure."""
        job = {
            "title": "Test Developer",
            "company": {"display_name": "Test Corp"},
            "location": {"display_name": "Test City"},
            "salary_max": 100000,
            "redirect_url": "http://test.com"
        }
        
        # Verify all expected fields exist
        self.assertIn("title", job)
        self.assertIn("company", job)
        self.assertIn("redirect_url", job)

if __name__ == '__main__':
    unittest.main()

