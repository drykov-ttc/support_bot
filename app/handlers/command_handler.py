from app.utils.utils import get_people, main_duty_new
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


keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(
    *[types.KeyboardButton(name) for name in ["Дежурный сегодня?", "Дежурный завтра?"]]
)


def start(m, bot):
    bot.send_message(m.chat.id, "Приветствую!", reply_markup=keyboard)


def help(m, bot):
    bot.send_message(
        m.chat.id,
        "Список команд: \n/today - Дежурный сегодня \n/tomorrow - Дежурный завтра "
        "\n/duty - График дежурств \n/change_duty - Смена дежурного на сегодня \n/all - "
        "Сделать оповещение",
        reply_markup=keyboard,
    )


def msg(m, bot):
    try:
        if m.from_user.username in config.a and m.from_user.id in config.ids:
            bot.send_message(
                config.chat_id,
                "Привет, коллеги!\n"
                "Небольшое обновление:\n\n"
                "✔ Переезд на новый сервер "
                "\n✔ Автозапуск бота и его прокси",
                reply_markup=keyboard,
            )
    except Exception as e:
        logger.error(f"{e}")
        print(f"Error: {e}")


def msg_all(m, bot):
    try:
        if m.from_user.username in config.a and m.from_user.id in config.ids:
            nicknames = [
                "@supervufel",
                "@white_yarkiy",
                "@Somtawl",
                "@Blackvvolf",
                "@mikhail_lavrenov",
                "@BorisBeloglazov",
                "@M4r4t1n4",
                "@Yok01337",
            ]
            message = "Важное оповещение!\n\n"
            formatted_nicknames = "\n".join(nicknames)

            bot.send_message(
                config.chat_id, message + formatted_nicknames, reply_markup=keyboard
            )
    except Exception as e:
        logger.error(f"{e}")
        print(f"Error: {e}")


def change_duty(m, bot):
    try:
        if m.from_user.username in config.a and m.from_user.id in config.ids:
            a = get_people()
            people = a[0]
            count_people = a[1]
            nicknames = a[2]
            keyboard = types.InlineKeyboardMarkup()
            for i in range(0, count_people):
                nicknames[i] = types.InlineKeyboardButton(
                    text=people[i], callback_data=nicknames[i]
                )
                keyboard.add(nicknames[i])
            bot.send_message(
                m.chat.id,
                "Назначьте дежурного на сегодня:",
                reply_markup=keyboard,
                parse_mode="HTML",
            )

    except Exception as e:
        logger.error(f"{e}")
        print(f"Error: {e}")


def send_duty(message, bot):
    try:
        for file in os.listdir(picDir):
            if file.split(".")[-1] == "png":
                picFile = os.path.join(picDir, file)
                f = open(picFile, "rb")
                bot.send_photo(message.chat.id, f, None, reply_markup=keyboard)
            time.sleep(1)
    except Exception as e:
        logger.error(f"{e}")
        print(f"Error: {e}")


def today(m, bot):
    try:
        q = 0
        now = datetime.today().day
        q = main_duty_new(now, q)
        q = q[0]
        if q != 0:
            bot.send_message(
                m.chat.id,
                "Сегодня дежурит\n<pre>" + q + "</pre>",
                reply_markup=keyboard,
                parse_mode="HTML",
            )
        else:  # исключение для того, чтобы был фидбэк пользователю
            bot.send_message(
                m.chat.id,
                "Сегодня выходной! \nОтдохните от работы, погуляйте на свежем воздухе :)",
                reply_markup=keyboard,
            )
    except Exception as e:
        logger.error(f"{e}")
        print(f"Error: {e}")
        bot.reply_to(m, "Ошибочка!", reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(
            config.admin_id,
            e,
            parse_mode="HTML",
        )


def tomorrow(m, bot):
    try:
        q = 0
        now = datetime.today().day + 1
        q = main_duty_new(now, q)
        q = q[0]
        if q != 0:
            bot.send_message(
                m.chat.id,
                "Завтра дежурит\n<pre>" + q + "</pre>",
                reply_markup=keyboard,
                parse_mode="HTML",
            )
        else:
            bot.send_message(
                m.chat.id,
                "Завтра выходной! \nПроведите это время с пользой для себя :)",
                reply_markup=keyboard,
            )
    except Exception as e:
        logger.error(f"{e}")
        print(f"Error: {e}")
        bot.reply_to(m, "Ошибочка!")
        bot.send_message(
            config.admin_id,
            e,
            parse_mode="HTML",
        )


# @bot.message_handler(func=lambda message: True, content_types=["text"])
def duty_main(m, bot):
    try:
        if m.text == "Дежурный сегодня?":
            today(m, bot)
        elif m.text == "Дежурный завтра?":
            tomorrow(m, bot)
        else:
            bot.send_message(
                m.chat.id,
                "К сожалению я не знаю данную команду. "
                "\nПопробуйте ввести /help, чтобы узнать доступные команды",
                reply_markup=keyboard,
            )
    except Exception as e:
        logger.error(f"{e}")
        print(f"Error: {e}")
        bot.send_message(
            config.admin_id,
            e,
            parse_mode="HTML",
        )


def register_handlers(bot):
    bot.register_message_handler(
        lambda message: start(message, bot), commands=["start"]
    )
    bot.register_message_handler(lambda message: help(message, bot), commands=["help"])
    bot.register_message_handler(
        lambda message: today(message, bot), commands=["today"]
    )
    bot.register_message_handler(
        lambda message: tomorrow(message, bot), commands=["tomorrow"]
    )

    bot.register_message_handler(
        lambda message: send_duty(message, bot), commands=["duty"]
    )
    bot.register_message_handler(
        lambda message: msg(message, bot), commands=["message"]
    )
    bot.register_message_handler(
        lambda message: msg_all(message, bot), commands=["msg_all"]
    )
    bot.register_message_handler(
        lambda message: change_duty(message, bot), commands=["change_duty"]
    )
    bot.register_message_handler(
        lambda message: duty_main(message, bot),
        content_types=["text"],  # Only trigger for text messages
        func=lambda message: True,
    )
