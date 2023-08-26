# -*- coding: utf-8 -*-
from app.handlers import command_handler, inline_handler
from app.handlers.daemon import clock


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
    curr_month,
    logger,
    types,
    time,
    config,
    requests,
    load_workbook,
    tabulate,
    telebot,
    threading,
)


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
