from datetime import datetime
import logging
import os
import time
import config
from telebot import types

from app.utils.utils import main_duty_new
from config import ROOT_DIR

logger = logging.getLogger(__name__)
picDir = os.path.join(ROOT_DIR, "pic/")


def clock(interval, bot):  # Ежедневный постинг
    try:
        while True:
            d = datetime.today()
            day_of_week = d.weekday()  # Monday is 0 and Sunday is 6

            if day_of_week < 5:  # Working days (0 to 4, Monday to Friday)
                time_start = "17:00"
            else:  # Weekend or holiday (5 to 6, Saturday and Sunday)
                time_start = "08:00"

            time_x = d.strftime("%H:%M")
            if time_x == time_start:
                q = 0
                now = datetime.today().day
                month = datetime.today().month
                all_data = main_duty_new(now, q)
                q = all_data[0]
                table_month = all_data[1]
                print(table_month)
                print(month)
                if table_month == month:
                    if q != 0:
                        bot.send_message(
                            config.chat_id,
                            "Доброе утро, коллеги! \nСегодня дежурит " + q,
                        )
                        for file in os.listdir(picDir):
                            if file.split(".")[-1] == "png":
                                f = open(picDir + file, "rb")
                                bot.send_photo(
                                    config.chat_id,
                                    f,
                                    None,
                                    reply_markup=types.ReplyKeyboardRemove(),
                                )
                            time.sleep(1)
                else:
                    bot.send_message(
                        config.chat_id,
                        "Отсутствует актуальное расписание на данный месяц!",
                    )
            time.sleep(interval)
    except Exception as e:
        logger.error(f"{e}")
        print(f"Error: {e}")
        bot.send_message(config.admin_id, e,parse_mode="HTML",)
