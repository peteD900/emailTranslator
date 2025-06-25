import logging


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Configures and returns a logger with a consistent format.

    Args:
        name (str): The logger name (typically __name__)

    Returns:
        logging.Logger: Configured logger instance
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(name)
