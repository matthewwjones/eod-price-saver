from unittest import TestCase
from unittest.mock import MagicMock

from src.notify.sesnotifier import SesNotifier


class TestSesNotifier(TestCase):

    def test_send_prices_uses_most_recent_date_in_subject(self):
        mock_ses = MagicMock()
        mock_ses.send_email.return_value = {'MessageId': 'test-id'}
        notifier = SesNotifier(mock_ses, 'to@example.com', 'from@example.com')

        notifier.send_prices({'VTI.US': [('2024-01-15', 255.92)], 'BTC-USD.CC': [('2024-01-14', 42000.0)]})

        subject = mock_ses.send_email.call_args[1]['Message']['Subject']['Data']
        self.assertIn('2024-01-15', subject)