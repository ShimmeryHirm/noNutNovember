from telegram import ParseMode
from telegram.ext import *

import config
from core import db_map
from core.callback_worker import callback_worker
from core.db_map import UsersTable, session_scope, Base, engine
from core.error import error
from core.keyborads import Keyboards
from core.utils import create_new_account


def start(update, context):
    user = update.effective_user
    chat = update.effective_chat

    with session_scope() as session:
        slave = session.query(UsersTable).filter_by(id=user.id).first()  # Find slave in DB

        if slave is None:  # Slave not in DB

            create_new_account(context, user)  # Create new account for slave
            slave = session.query(UsersTable).filter_by(id=user.id).first()
        if slave.side == 1:
            context.bot.send_message(chat_id=chat.id,
                                     reply_markup=Keyboards().sith,

                                     parse_mode=ParseMode.HTML,
                                     text=f'<i>👋Приветствую {user.name}</i>\n'
                                          f'<b>Ты на темной стороне 👹 </b>\n')
        else:
            context.bot.send_message(chat_id=chat.id,
                                     reply_markup=Keyboards().main_menu_keyboard,
                                     parse_mode=ParseMode.HTML,
                                     text=f'<i>👋Приветствую {user.name}</i>\n'
                                          f'<b>Ты на светлой стороне✊</b>\n'
                                          '\n'
                                          '<code>Чтобы чтобы примкнуть к ситхам нажми кнопку ниже🔽:</code>')


def donate(update, context):
    context.bot.send_message(
        text='__Если понравился бот и есть желание отблагодарить разработчика, подкинуть на жижку или на оплату сервера__ - `4890 4947 2224 6220`',
        chat_id=update.message.chat_id, parse_mode='Markdown')




def main():
    #db_map.Base.metadata.drop_all(db_map.engine)  # Drop all tables
    Base.metadata.create_all(engine)  # Create all tables if not exist
    updater = Updater(config.TOKEN, use_context=True)  # http://t.me/SyneXbot
    dp = updater.dispatcher

    admins = (382182253, 934540473)  # add your ID here
    filters = ~Filters.update.edited_message & \
              ~Filters.update.channel_post & ~Filters.update.edited_channel_post & ~Filters.poll
    admin_filters = ~Filters.update.edited_message & Filters.user(user_id=admins)

    dp.add_handler(CommandHandler("start", start, filters=filters))

    dp.add_handler(CommandHandler("donate", donate, filters=filters))

    dp.add_handler(CallbackQueryHandler(callback_worker))

    dp.add_error_handler(error)

    print("[+]: SERVER STARTED!")

    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    main()
