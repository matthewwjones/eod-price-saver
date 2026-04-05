import datetime
import logging
import os

import boto3

from config.instrumentcodeloader import InstrumentCodeLoader
from load.eodloader import EodLoader
from notify.sesnotifier import SesNotifier

INSTRUMENT_CODES_FILE = '../instrument-codes.txt'


class EodPriceLoaderApp:

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.api_token = os.environ['EOD_LOADER_API_TOKEN']
        self.instrument_codes = InstrumentCodeLoader(INSTRUMENT_CODES_FILE).load_instrument_codes()
        ses_client = boto3.client('ses', region_name=os.environ['EOD_LOADER_AWS_REGION'])
        self.notifier = SesNotifier(ses_client,
                                    os.environ['EOD_LOADER_EMAIL_TO'],
                                    os.environ['EOD_LOADER_EMAIL_FROM'])

    def run(self):
        self.log.info("Starting EOD price loader app...")
        today = datetime.date.today()
        prices = EodLoader(self.api_token, self.instrument_codes, load_date=today).load_prices()
        self.notifier.send_prices(prices, today)
