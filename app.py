#!/usr/bin/python3


from imports import (
    ROOT_DIR,
    logFile,
    picDir,
    raspDir,
    fileNAme,
    os,
    logging,
    datetime,
    signal,
    config,
    logger,
)

from app.bot import App


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
