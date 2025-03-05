import logging


def setup_logger():
    """Configures the application-wide logger."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger("booking_system")


# Initialize the logger
logger = setup_logger()
