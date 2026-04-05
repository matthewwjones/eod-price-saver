import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.load.eodloader import EodLoader


class TestEodLoader(TestCase):
    json = [{
        "date": "2023-10-31", "open": 169.35, "high": 170.9, "low": 167.9, "close": 170.77, "adjusted_close": 170.77,
        "volume": 44846000}
    ]

    def test_extract_from_response_returns_date_and_close(self):
        date, close = EodLoader.extract_from_response(self.json)
        self.assertEqual(date, "2023-10-31")
        self.assertEqual(close, 170.77)

    @patch('src.load.eodloader.requests.get')
    def test_load_prices_returns_date_and_close_per_instrument(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.json
        mock_get.return_value = mock_response

        prices = EodLoader('test-token', ['AAPL.US'], load_date=datetime.date(2024, 1, 15)).load_prices()

        self.assertEqual(prices, {'AAPL.US': ('2023-10-31', 170.77)})

    @patch('src.load.eodloader.requests.get')
    def test_load_prices_uses_one_week_lookback_in_url(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.json
        mock_get.return_value = mock_response

        EodLoader('my-token', ['ISF.LSE'], load_date=datetime.date(2024, 3, 22)).load_prices()

        called_url = mock_get.call_args[0][0]
        self.assertIn('from=2024-03-15', called_url)