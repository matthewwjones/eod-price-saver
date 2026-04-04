import logging


class SesNotifier:

    def __init__(self, ses_client, recipient, sender):
        self.log = logging.getLogger(__name__)
        self.ses_client = ses_client
        self.recipient = recipient
        self.sender = sender

    def send_prices(self, prices, date):
        date_str = date.strftime('%Y-%m-%d')
        response = self.ses_client.send_email(
            Destination={'ToAddresses': [self.recipient]},
            Message={
                'Body': {'Text': {'Charset': 'UTF-8', 'Data': self._format_body(prices, date_str)}},
                'Subject': {'Charset': 'UTF-8', 'Data': f'EOD Prices - {date_str}'},
            },
            Source=self.sender,
        )
        self.log.info(f"Email sent. MessageId: {response['MessageId']}")

    def _format_body(self, prices, date_str):
        lines = [f'EOD Closing Prices - {date_str}', '']
        for instrument, price in prices.items():
            lines.append(f'{instrument}: {price if price is not None else "N/A"}')
        return '\n'.join(lines)
