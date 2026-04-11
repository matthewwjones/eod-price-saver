import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.load.eodloader import EodLoader


class TestEodLoader(TestCase):
    json = [
        {"date": "2023-10-31", "open": 169.35, "high": 170.9, "low": 167.9, "close": 170.77,
         "adjusted_close": 170.77, "volume": 44846000},
        {"date": "2023-10-30", "open": 168.00, "high": 169.50, "low": 167.00, "close": 168.50,
         "adjusted_close": 168.50, "volume": 40000000},
    ]

    def test_extract_from_response_returns_list_of_date_and_close_tuples(self):
        result = EodLoader.extract_from_response(self.json)
        self.assertEqual(result, [('2023-10-31', 170.77), ('2023-10-30', 168.50)])

    def test_extract_from_response_returns_at_most_ten_entries(self):
        many = [
            {"date": f"2023-10-{i:02d}", "close": float(i), "open": 0, "high": 0, "low": 0,
             "adjusted_close": 0, "volume": 0}
            for i in range(1, 16)
        ]
        result = EodLoader.extract_from_response(many)
        self.assertEqual(len(result), 10)

    @patch('src.load.eodloader.requests.get')
    def test_load_prices_returns_list_of_date_and_close_per_instrument(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.json
        mock_get.return_value = mock_response

        prices = EodLoader('test-token', ['AAPL.US'], load_date=datetime.date(2024, 1, 15)).load_prices()

        self.assertEqual(prices, {'AAPL.US': [('2023-10-31', 170.77), ('2023-10-30', 168.50)]})

    @patch('src.load.eodloader.requests.get')
    def test_load_prices_uses_three_week_lookback_in_url(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.json
        mock_get.return_value = mock_response

        EodLoader('my-token', ['ISF.LSE'], load_date=datetime.date(2024, 3, 22)).load_prices()

        called_url = mock_get.call_args[0][0]
        self.assertIn('from=2024-03-01', called_url)