import logging


class InstrumentCodeLoader:

    def __init__(self, instrument_codes_file):
        self.log = logging.getLogger(__name__)
        self.instrument_codes_file = instrument_codes_file

    def load_instrument_codes(self):
        self.log.info(f"Loading instrument codes from {self.instrument_codes_file}")
        try:
            with open(self.instrument_codes_file) as file:
                instruments = [line.rstrip() for line in file]
            self.log.info(f"Loaded {len(instruments)} instruments from {self.instrument_codes_file}.")
            return instruments
        except FileNotFoundError as e:
            raise Exception(f"File {self.instrument_codes_file} does not exist.", e)
