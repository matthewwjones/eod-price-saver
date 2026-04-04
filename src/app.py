import logging
import os

from config.instrumentcodeloader import InstrumentCodeLoader
from load.eodloader import EodLoader


class App:

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.instrument_codes_file = '../instrument-codes.txt'

    def run(self):
        self.log.info("Starting EOD price loader app...")
        instrument_codes = InstrumentCodeLoader(self.instrument_codes_file).load_instrument_codes()
        api_token = os.environ['EOD_LOADER_API_TOKEN']
        EodLoader(api_token, instrument_codes).load_prices()
