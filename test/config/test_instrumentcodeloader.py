import os
from unittest import TestCase

from src.config.instrumentcodeloader import InstrumentCodeLoader

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'test-data')


class TestInstrumentCodeLoader(TestCase):
    test_instrument_codes_file = os.path.join(TEST_DATA_DIR, 'test-instrument-codes.txt')
    empty_instrument_codes_file = os.path.join(TEST_DATA_DIR, 'empty-instrument-codes-file.txt')
    commented_instrument_codes_file = os.path.join(TEST_DATA_DIR, 'test-instrument-codes-with-comments.txt')

    def test_load_instrument_codes_returns_expected_list(self):
        loader = InstrumentCodeLoader(self.test_instrument_codes_file)
        self.assertEqual(loader.load_instrument_codes(), ['HSBA.LSE', 'OCDO.LSE', 'VOD.LSE'])

    def test_load_instrument_codes_empty_file(self):
        loader = InstrumentCodeLoader(self.empty_instrument_codes_file)
        self.assertEqual(loader.load_instrument_codes(), [])

    def test_commented_lines_are_ignored(self):
        loader = InstrumentCodeLoader(self.commented_instrument_codes_file)
        self.assertEqual(loader.load_instrument_codes(), ['HSBA.LSE', 'VOD.LSE'])

    def test_load_instrument_codes_raises_exception_for_invalid_path(self):
        with self.assertRaises(Exception) as context:
            InstrumentCodeLoader('invalid-path').load_instrument_codes()
        self.assertIn('File invalid-path does not exist.', str(context.exception))
