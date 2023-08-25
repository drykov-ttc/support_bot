import logging
import os
import signal
import sys
from app.bot import App
import config

from config import ROOT_DIR


logFile = os.path.join(ROOT_DIR, config.LOG_DIR, config.LOG_STABLE)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename=logFile,
)

logger = logging.getLogger(__name__)


def main():
    bot = App()
    logger.info("Bot started.")

    def handle_exit(signum, frame):
        logger.info("Received signal to exit. Stopping the bot...")
        bot.stop()
        print("Bot stopped.")
        exit(0)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    try:
        bot.run()
    except Exception as e:
        logger.error("An error occurred during bot execution: %s", e)


if __name__ == "__main__":
    main()
