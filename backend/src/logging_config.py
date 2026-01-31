import logging
from .config.settings import settings


def setup_logging():
    # Set up basic logging configuration
    log_level = logging.DEBUG if settings.environment == "development" else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # Log to stdout
        ]
    )


# Call setup_logging to initialize logging when this module is imported
setup_logging()