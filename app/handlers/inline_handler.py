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
    requests,
    load_workbook
)


# @bot.callback_query_handler(func=lambda call: True)
def callback_inline(call, bot):
    try:
        wb = load_workbook(fileNAme)
        sheet = wb["Лист1"]
        now = datetime.today().day
        a = get_people()
        people = a[0]
        count_people = a[1]
        nicknames = a[2]
        today_id = a[3]
        for i in range(3, 10):  # удаляем за сегодня
            sheet.cell(row=i, column=(now + 5)).value = None
        d = nicknames.index(call.data)  # узнаем кто будет сегодня дежурить
        next_column = 45
        for i in range(now + 3, 40):
            if (
                sheet.cell(row=i, column=(now + 5)).value == "Х"
                or sheet.cell(row=i, column=(now + 5)).value == 1
            ):
                next_column = i
                break
        for i in range(3, 10):
            sheet.cell(row=i, column=next_column).value = None
        sheet.cell(row=today_id, column=next_column).value = "Х"
        sheet.cell(row=d + 3, column=(now + 5)).value = "Х"
        bot.send_message(
            call.message.chat.id,
            people[d] + " " + nicknames[d] + " назначен дежурным на сегодня",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        bot.answer_callback_query(
            callback_query_id=call.id,
            show_alert=True,
            text="Вы изменили дежурного на сегодня!",
        )
        bot.delete_message(
            call.message.chat.id,
            call.message.message_id,
        )
        wb.save(fileNAme)
    except Exception as e:
        logger.error(f"{e}")
        print(f"Error: {e}")
        bot.send_message(
            config.admin_id,
            e,
            parse_mode="HTML",
        )


# @bot.message_handler(content_types=["document"])
def handle_file(message, bot):
    try:
        if (
            message.from_user.username in config.a
            and message.from_user.id in config.ids
        ):
            file = requests.get(
                "https://api.telegram.org/bot{0}/getFile?file_id={1}".format(
                    config.token, message.document.file_id
                )
            )
            file_path = file.json()["result"]["file_path"]
            src = raspDir + message.document.file_name
            src2 = picDir + message.document.file_name
            url = "https://api.telegram.org/file/bot{0}/{1}".format(
                config.token, file_path
            )
            r = requests.get(url)
            if message.document.file_name == curr_month + ".xlsx":
                with open(src, "wb") as new_file:
                    new_file.write(r.content)
                bot.reply_to(message, "Новое расписание успешно загружено")
            elif message.document.file_name == curr_month + ".png":
                with open(src2, "wb") as new_file:
                    new_file.write(r.content)
                bot.reply_to(message, "Новая картинка расписания успешно загружено")
    except Exception as e:
        logger.error(f"{e}")
        print(f"Error: {e}")
        bot.reply_to(message, e)


def register_handlers(bot):
    bot.register_message_handler(
        lambda call: callback_inline(call, bot),
        content_types=["text"],  # Only trigger for text messages
        func=lambda call: True,
    )
    bot.register_message_handler(
        lambda message: handle_file(message, bot),
        content_types=["document"],  # Only trigger for text messages
        func=lambda message: True,
    )
