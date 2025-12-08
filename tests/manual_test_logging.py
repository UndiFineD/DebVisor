import logging
import structlog
import sys
import os

# Add workspace root to path
sys.path.append(os.getcwd())

from opt.core.logging import configure_logging  # noqa: E402


def test_logging():
    print("Testing Structured Logging...")

    configure_logging(service_name="test-service", json_format=True)

    # Test standard logging
    logging.info("This is a standard logging message", extra={"user_id": "123"})

    # Test structlog
    logger = structlog.get_logger()
    logger.info("This is a structlog message", request_id="req-abc")

    try:
        1 / 0
    except ZeroDivisionError:
        logging.exception("Caught an exception via logging")
        logger.exception("Caught an exception via structlog")


if __name__ == "__main__":
    test_logging()
