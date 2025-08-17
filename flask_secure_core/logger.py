import logging
import sys
from logging.handlers import RotatingFileHandler

# ANSI-Farbcodes
RESET = "\033[0m"
GRAY = "\033[90m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
WHITE = "\033[97m"

class ColoredFormatter(logging.Formatter):
    """
    Formatter that adds color for console output.
    """
    LEVEL_COLORS = {
        logging.DEBUG: GRAY,
        logging.INFO: WHITE,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: RED + MAGENTA
    }

    def __init__(self):
        super().__init__()
        self.base_fmt = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        self.detailed_fmt = "%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d:%(funcName)s | %(message)s"
        self.datefmt = "%m-%d-%Y %H:%M:%S"

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, WHITE)
        if record.levelno >= logging.WARNING:
            fmt = self.detailed_fmt
        else:
            fmt = self.base_fmt

        formatter = logging.Formatter(fmt, self.datefmt)
        msg = formatter.format(record)

        parts = msg.split(" | ")
        if len(parts) >= 4:
            parts[0] = CYAN + parts[0] + RESET       # Zeit
            parts[1] = BLUE + parts[1] + RESET       # Logger Name
            parts[2] = color + parts[2] + RESET      # Level
            # Nachricht selbst farbig bei Warning/Error/Critical
            if record.levelno >= logging.WARNING:
                parts[4] = color + parts[4] + RESET
            if record.levelno == logging.DEBUG:
                parts[3] = GRAY + parts[3] + RESET
        msg = " | ".join(parts)
        return msg


def get_logger(name=None, log_level=logging.DEBUG, log_file='logs.log', max_bytes=1000*1024, backup_count=20):
    log_file = "logs/" + log_file
    logger_var = logging.getLogger(name)
    logger_var.setLevel(logging.DEBUG)

    if not logger_var.handlers:
        # Console Handler mit Farben
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(log_level)
        stdout_handler.setFormatter(ColoredFormatter())

        # File Handler (immer detailliert, keine Farben)
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d:%(funcName)s | %(message)s",
            "%m-%d-%Y %H:%M:%S"
        ))

        logger_var.addHandler(stdout_handler)
        logger_var.addHandler(file_handler)

    return logger_var


if __name__ == '__main__':
    logger = get_logger("colorTest")
    logger.debug("Debug message.")
    logger.info("Info message.")
    logger.warning("Warning message.")
    logger.error("Error message.")
    logger.critical("Critical message.")
