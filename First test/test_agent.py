import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from reporter import generate_report
from analyzer import analyze_batch

class TestAgent(unittest.TestCase):
    
    def test_reporter(self):
        print("\nTesting Reporter...")
        dummy_papers = [
            {
                "title": "Test Tier 1",
                "url": "http://test.com/1",
                "venue": "Nature",
                "date": "2024-01-01",
                "tier": 1,
                "analysis": {"innovation": "New thing", "process": "Flow", "insight": "Good"}
            }
        ]
        dummy_events = []
        filename = generate_report(dummy_papers, dummy_events)
        self.assertTrue(os.path.exists(filename))
        print(f"Report generated successfully: {filename}")
        # Cleanup
        os.remove(filename)

    @patch('analyzer.model')
    def test_analyzer(self, mock_model):
        print("\nTesting Analyzer (Mocked)...")
        # Mock Gemini response
        mock_response = MagicMock()
        mock_response.text = '```json\n{"excluded": false, "tier": 1, "analysis": {"innovation": "Mocked"}}\n```'
        mock_model.generate_content.return_value = mock_response
        
        papers = [{"title": "Test", "abstract": "Test Abstract"}]
        results = analyze_batch(papers)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['tier'], 1)
        print("Analyzer logic verified.")

if __name__ == '__main__':
    unittest.main()
