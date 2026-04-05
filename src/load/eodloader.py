import datetime
import logging

import requests


class EodLoader:
    def __init__(self, api_token, instrument_codes, load_date=None):
        self.log = logging.getLogger(__name__)
        self.api_token = api_token
        self.instrument_codes = instrument_codes
        self.load_date = load_date if load_date is not None else datetime.date.today()
        self.log.info("Created EOD price loader.")

    def load_prices(self):
        self.log.info(f"Loading prices for {len(self.instrument_codes)} instrument codes.")
        eod_prices = {}
        for instrument in self.instrument_codes:
            eod_prices[instrument] = self.load_eod_for_instrument(instrument)
        self.log.info(f'Prices: {eod_prices}')
        return eod_prices

    def load_eod_for_instrument(self, instrument):
        date_str = (self.load_date - datetime.timedelta(weeks=1)).strftime('%Y-%m-%d')
        url = 'https://eodhd.com/api/eod/%s?api_token=%s&order=d&fmt=json&filter=last_close&from=%s' % (
            instrument, self.api_token, date_str)
        self.log.info(f'Loading EOD price for {instrument} from {url}')
        try:
            response = requests.get(url).json()
            self.log.info(f"Fetched {response}")
            return self.extract_close_from_response(response)
        except Exception as e:
            self.log.exception(f'Error loading price for instrument {instrument} - {e}')

    @staticmethod
    def extract_close_from_response(response):
        return response[0]['close']
