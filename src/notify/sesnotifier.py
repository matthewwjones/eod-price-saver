import logging

from .priceemailbody import PriceEmailBody


class SesNotifier:

    def __init__(self, ses_client, recipient, sender):
        self.log = logging.getLogger(__name__)
        self.ses_client = ses_client
        self.recipient = recipient
        self.sender = sender

    def send_prices(self, prices):
        email_body = PriceEmailBody(prices)
        response = self.ses_client.send_email(
            Destination={'ToAddresses': [self.recipient]},
            Message={
                'Body': {
                    'Html': {'Charset': 'UTF-8', 'Data': email_body.build_html()},
                    'Text': {'Charset': 'UTF-8', 'Data': email_body.build()},
                },
                'Subject': {'Charset': 'UTF-8', 'Data': f'EOD Prices - {email_body.most_recent_date()}'},
            },
            Source=self.sender,
        )
        self.log.info(f"Email sent. MessageId: {response['MessageId']}")