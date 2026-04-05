from unittest import TestCase

from src.notify.priceemailbody import PriceEmailBody


class TestPriceEmailBody(TestCase):

    def test_header_row_contains_instrument_codes_in_order(self):
        prices = {'VTI.US': ('2024-01-15', 255.92), 'AAPL.US': ('2024-01-15', 170.77), 'TSLA.US': ('2024-01-15', 280.50)}
        header = PriceEmailBody(prices).build().splitlines()[0]
        self.assertLess(header.index('VTI.US'), header.index('AAPL.US'))
        self.assertLess(header.index('AAPL.US'), header.index('TSLA.US'))

    def test_single_date_produces_one_data_row(self):
        prices = {'VTI.US': ('2024-01-15', 255.92), 'AAPL.US': ('2024-01-15', 170.77)}
        body = PriceEmailBody(prices).build()
        data_row = body.splitlines()[1]
        self.assertIn('2024-01-15', data_row)
        self.assertIn('255.92', data_row)
        self.assertIn('170.77', data_row)

    def test_different_dates_produce_separate_rows(self):
        prices = {'VTI.US': ('2024-01-15', 255.92), 'BTC-USD.CC': ('2024-01-14', 42000.0)}
        lines = PriceEmailBody(prices).build().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertIn('2024-01-15', lines[1])
        self.assertIn('255.92', lines[1])
        self.assertIn('N/A', lines[1])
        self.assertIn('2024-01-14', lines[2])
        self.assertIn('42000.0', lines[2])
        self.assertIn('N/A', lines[2])

    def test_na_shown_for_failed_fetch(self):
        prices = {'VTI.US': None}
        self.assertIn('N/A', PriceEmailBody(prices).build())

    def test_build_html_produces_table_with_instrument_headers_and_prices(self):
        prices = {'VTI.US': ('2024-01-15', 255.92), 'AAPL.US': ('2024-01-15', 170.77)}
        html = PriceEmailBody(prices).build_html()
        self.assertIn('<table', html)
        self.assertIn('<th', html)
        self.assertIn('VTI.US', html)
        self.assertIn('AAPL.US', html)
        self.assertIn('2024-01-15', html)
        self.assertIn('255.92', html)
        self.assertIn('170.77', html)

    def test_most_recent_date_returns_latest_date(self):
        prices = {'VTI.US': ('2024-01-15', 255.92), 'BTC-USD.CC': ('2024-01-14', 42000.0)}
        self.assertEqual(PriceEmailBody(prices).most_recent_date(), '2024-01-15')