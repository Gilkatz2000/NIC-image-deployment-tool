import logging


def setup_logger(verbose=False):
    logger = logging.getLogger("nvme-imager")
    logger.handlers.clear()

    handler = logging.StreamHandler()

    if verbose:
        logger.setLevel(logging.INFO)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(levelname)s: %(message)s")
    else:
        logger.setLevel(logging.WARNING)
        handler.setLevel(logging.WARNING)
        formatter = logging.Formatter("%(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger