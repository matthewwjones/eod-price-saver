import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from eodpriceloaderapp import EodPriceLoaderApp  # noqa: E402

logging.basicConfig(level='INFO', format='%(asctime)s [%(levelname)s] %(name)s -- %(message)s')

logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    try:
        EodPriceLoaderApp().run()
    except Exception as e:
        logger.error(f"Error occurred in lambda handler: {e}")
        raise
