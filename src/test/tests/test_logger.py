from src.resources.utils.logger import LogGenerator

logger = LogGenerator.loggen()


def test_logger():

    logger.info("******** Logger Test Started ********")

    logger.debug("This is DEBUG message")

    logger.info("This is INFO message")

    logger.warning("This is WARNING message")

    logger.error("This is ERROR message")

    logger.critical("This is CRITICAL message")

    logger.info("******** Logger Test Completed ********")

    assert True

def test_logger_exception():

    try:
        x = 10 / 0

    except Exception as e:
        logger.error(f"Exception occurred: {e}")

    assert True
