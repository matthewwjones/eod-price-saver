import datetime
import logging
import os

import boto3

from load.eodloader import EodLoader
from notify.sesnotifier import SesNotifier


class EodPriceLoaderApp:

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.api_token = os.environ['EOD_LOADER_API_TOKEN']
        self.instrument_codes = [c.strip() for c in os.environ['EOD_LOADER_INSTRUMENT_CODES'].split(',') if c.strip()]
        ses_client = boto3.client('ses', region_name=os.environ['EOD_LOADER_AWS_REGION'])
        self.notifier = SesNotifier(ses_client,
                                    os.environ['EOD_LOADER_EMAIL_TO'],
                                    os.environ['EOD_LOADER_EMAIL_FROM'])

    def run(self):
        self.log.info("Starting EOD price loader app...")
        today = datetime.date.today()
        prices = EodLoader(self.api_token, self.instrument_codes, load_date=today).load_prices()
        self.notifier.send_prices(prices, today)
