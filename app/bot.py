# -*- coding: utf-8 -*-
import logging
import sys
from app.handlers import command_handler, inline_handler
from app.handlers.daemon import clock
import telebot
import threading
import os
import config
from config import ROOT_DIR

logFile = os.path.join(ROOT_DIR, config.LOG_DIR, config.LOG_STABLE)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename=logFile,
)

logger = logging.getLogger(__name__)


class App:
    def __init__(self):
        self.bot = telebot.TeleBot(config.token)
        self.load_handlers()

    def load_handlers(self):
        command_handler.register_handlers(self.bot)
        inline_handler.register_handlers(self.bot)
        # Add 'pass' here

    def run(self):
        try:
            t = threading.Thread(target=clock, args=(60, self.bot))
            t.daemon = True
            t.start()
        except Exception as e:
            logger.error(f"{e}")
            print(f"Error: {e}")
            self.bot.send_message(
                config.admin_id,
                e,
                parse_mode="HTML",
            )
        self.bot.polling()
        self.bot.send_message(
            config.admin_id,
            "Bot startted:",
            parse_mode="HTML",
        )

    def stop(self):
        print("Stopping the bot...")
        self.bot.send_message(
            config.admin_id,
            "Stopping the bot..:",
            parse_mode="HTML",
        )

        self.bot.stop_polling()
        print("Bot stopped.")
