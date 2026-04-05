import logging
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from app import App  # noqa: E402

logging.basicConfig(level='INFO', format='%(asctime)s [%(levelname)s] %(name)s -- %(message)s',
                    handlers=[logging.StreamHandler()])

if __name__ == "__main__":
    try:
        App().run()
    except Exception as e:
        logging.error(f"Error occurred whilst running app. {e}")
