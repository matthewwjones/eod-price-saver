import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.load.eodloader import EodLoader


class TestEodLoader(TestCase):
    json = [{
        "date": "2023-10-31", "open": 169.35, "high": 170.9, "low": 167.9, "close": 170.77, "adjusted_close": 170.77,
        "volume": 44846000}
    ]

    def test_extract_close_from_response_returns_expected_value(self):
        loader = EodLoader(None, [])
        close_price = loader.extract_close_from_response(self.json)
        self.assertEqual(close_price, 170.77)

    @patch('src.load.eodloader.requests.get')
    def test_load_prices_returns_price_dict(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.json
        mock_get.return_value = mock_response

        loader = EodLoader('test-token', ['AAPL.US'], load_date=datetime.date(2024, 1, 15))
        result = loader.load_prices()

        self.assertEqual(result, {'AAPL.US': 170.77})

    @patch('src.load.eodloader.requests.get')
    def test_load_prices_uses_date_in_url(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.json
        mock_get.return_value = mock_response

        loader = EodLoader('my-token', ['ISF.LSE'], load_date=datetime.date(2024, 3, 22))
        loader.load_prices()

        called_url = mock_get.call_args[0][0]
        self.assertIn('from=2024-03-22', called_url)
        self.assertIn('to=2024-03-22', called_url)
