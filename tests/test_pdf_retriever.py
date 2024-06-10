import unittest
from unittest.mock import patch, MagicMock
from src.pdf_retriever import get_season_urls, retrieve_fia_pdfs, BASE_URL

class TestPdfRetriever(unittest.TestCase):

    @patch('src.pdf_retriever.requests.get')
    def test_get_season_urls(self, mock_get):
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = '''
        <select id="facetapi_select_facet_form_3">
            <option value="0">Season</option>
            <option value="/documents/championships/fia-formula-one-world-championship-14/season/season-2024-2043">SEASON 2024</option>
            <option value="/documents/championships/fia-formula-one-world-championship-14/season/season-2023-2042">SEASON 2023</option>
        </select>
        '''
        mock_get.return_value = mock_response

        base_url = BASE_URL + '/documents/championships/fia-formula-one-world-championship-14/'
        expected_urls = {
            'SEASON 2024': 'https://www.fia.com/documents/championships/fia-formula-one-world-championship-14/season/season-2024-2043',
            'SEASON 2023': 'https://www.fia.com/documents/championships/fia-formula-one-world-championship-14/season/season-2023-2042'
        }

        season_urls = get_season_urls(base_url)
        self.assertEqual(season_urls, expected_urls)

    @patch('src.pdf_retriever.requests.get')
    def test_retrieve_fia_pdfs(self, mock_get):
        # Mock the response from requests.get for the season page
        mock_season_response = MagicMock()
        mock_season_response.status_code = 200
        mock_season_response.content = '''
        <a href="/documents/championships/fia-formula-one-world-championship-14/season/season-2024-2043/australian-grand-prix-1.pdf">Australian GP PDF</a>
        <a href="/documents/championships/fia-formula-one-world-championship-14/season/season-2024-2043/bahrain-grand-prix-2.pdf">Bahrain GP PDF</a>
        '''
        mock_get.return_value = mock_season_response

        # Mock the response from requests.get for the PDF download
        mock_pdf_response = MagicMock()
        mock_pdf_response.status_code = 200
        mock_pdf_response.content = b'%PDF-1.4 mock pdf content'
        
        # The mock_get.side_effect will change the return value based on call order
        mock_get.side_effect = [mock_season_response, mock_pdf_response, mock_pdf_response]

        download_dir = 'tests/raw_pdfs'
        pdf_links = retrieve_fia_pdfs('https://www.fia.com/documents/championships/fia-formula-one-world-championship-14/season/season-2024-2043', download_dir, force=True)
        
        expected_links = [
            'https://www.fia.com/documents/championships/fia-formula-one-world-championship-14/season/season-2024-2043/australian-grand-prix-1.pdf',
            'https://www.fia.com/documents/championships/fia-formula-one-world-championship-14/season/season-2024-2043/bahrain-grand-prix-2.pdf'
        ]

        self.assertEqual(pdf_links, expected_links)

if __name__ == '__main__':
    unittest.main()
