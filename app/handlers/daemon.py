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
)

from app.utils.utils import main_duty_new, get_month


def clock(interval, bot):  # Ежедневный постинг
    try:
        while True:
            d = datetime.today()
            day_of_week = d.weekday()  # Monday is 0 and Sunday is 6
            day_of_month = d.day
            if day_of_week < 5:  # Working days (0 to 4, Monday to Friday)
                time_start = "08:45"
                time_reply = "17:00"
            else:  # Weekend or holiday (5 to 6, Saturday and Sunday)
                time_start = "08:45"
            time_x = d.strftime("%H:%M")
            if time_x == time_start or time_x == time_reply:
                if time_x == time_start:
                    msg = f"Доброе утро, коллеги! \n"
                elif time_x == time_reply:
                    msg = f"Добрый вечер, коллеги! \n"
                q = 0
                now = d.day
                month = get_month()
                all_data = main_duty_new(now, q)
                q = all_data[0]
                table_month = all_data[1]
                if table_month.lower() == month:
                    if day_of_month == 1:
                        for file in os.listdir(picDir):
                            if file.split(".")[-1] == "png":
                                f = open(picDir + file, "rb")
                                bot.send_photo(
                                    config.chat_id,
                                    f,
                                    f"{msg}График дежурств на  {month}",
                                    reply_markup=types.ReplyKeyboardRemove(),
                                )
                                time.sleep(1)
                    if q != 0:
                        bot.send_message(
                            config.chat_id,
                            f"{msg}Сегодня дежурит " + q,
                        )

                else:
                    bot.send_message(
                        config.chat_id,
                        "Отсутствует актуальное расписание на данный месяц!",
                    )
            time.sleep(interval)
    except Exception as e:
        logger.error(f"{e}")
        print(f"Error: {e}")
        bot.send_message(
            config.admin_id,
            e,
            parse_mode="HTML",
        )
