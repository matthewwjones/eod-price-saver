from unittest import TestCase
from unittest.mock import MagicMock

from src.notify.sesnotifier import SesNotifier


class TestSesNotifier(TestCase):

    def test_format_body_contains_instrument_and_price(self):
        notifier = SesNotifier(MagicMock(), 'to@example.com', 'from@example.com')
        prices = {'ITPS.LSE': 142.50, 'ISF.LSE': 824.50}
        body = notifier._format_body(prices, '2024-01-15')
        self.assertIn('EOD Closing Prices - 2024-01-15', body)
        self.assertIn('ITPS.LSE: 142.5', body)
        self.assertIn('ISF.LSE: 824.5', body)
