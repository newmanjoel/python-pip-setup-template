import logging
import colorlog


def setup_common_logger(logger: logging.Logger) -> logging.Logger:
    """
    Sets up a logger to the console with colored outputs.

    Parameters
    ----------
    logger : logging.Logger
        the logger that you want to modify

    Returns
    -------
    logging.Logger
        the logger that was modified

    Raises
    ------
    None
        No known issues


    """
    if type(logger) == str:
        logger = logging.getLogger(logger)

    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    return logger
