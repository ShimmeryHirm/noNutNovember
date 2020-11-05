from datetime import datetime
from time import strftime

import pytz
from telegram import ParseMode

from core import utils
from core.db_map import UsersTable, session_scope
from core.keyborads import Keyboards


def callback_worker(update, context):
    query = update.callback_query

    if query.data == 'confirm':
        query.message.edit_text(
            f'<i>Уверен ли ты, что хочешь перейти на сторону зла?</i>\n'
            f'<code>Учти, обратного пути не будет..</code>',
            parse_mode=ParseMode.HTML,
            reply_markup=Keyboards().confirm)

    if query.data == 'activate':
        with session_scope() as session:
            session.query(UsersTable).filter_by(id=query.message.chat.id).update({UsersTable.side: 1})
            context.bot.answer_callback_query(callback_query_id=query.id,
                                              text='Ты сделал правильный выбор.',
                                              show_alert=True)

            query.message.edit_text(
                parse_mode=ParseMode.HTML,
                reply_markup=Keyboards().sith,

                text=f'<i>👋Приветствую</i>\n\n'
                     f'<b>Ты на темной стороне🤝</b>\n'
                     f'<i>Джедаям страдать еще <b>{utils.calc_days()}</b> дней</i>\n\n'

            )

    if query.data == 'cancel':
        context.bot.answer_callback_query(callback_query_id=query.id, text='Будь аккуратнее пожалуйста!')

        query.message.edit_text(
            parse_mode=ParseMode.HTML,
            reply_markup=Keyboards().main_menu_keyboard,

            text=f'<i>👋Приветствую</i>\n\n'
                 f'<b>Ты на светлой стороне✊</b>\n'
                 f'<i>До конца недрочабря <b>{utils.calc_days()}</b> дней</i>\n\n'
        )
    if query.data == 'reload':
        d = datetime.now(pytz.timezone("Europe/Moscow"))
        t = d.strftime("%d.%m.%Y %H:%M")
        x = query.message.text.split()
        l = []
        for i in x:
            if i.isdigit():
                l.append(int(i))
        l.pop(0)
        with session_scope() as session:
            slave = session.query(UsersTable).filter_by(id=query.message.chat.id).first()  # Find slave in DB

            users = session.query(UsersTable).all()
            dark = session.query(UsersTable).filter(UsersTable.side == 1).all()
            white = session.query(UsersTable).filter(UsersTable.side == 0).all()
            if len(l) == 0:
                l = [len(users), len(white), len(dark)]
            new_users = len(users) - l[0]
            new_white = len(white) - l[1]
            new_dark = len(dark) - l[2]

            try:
                if slave.side == 1:
                    query.message.edit_text(
                        parse_mode=ParseMode.HTML,
                        reply_markup=Keyboards().sith,

                        text=f'<i>👋Приветствую</i>\n\n'
                             f'<b>Ты на темной стороне 🤝</b>\n'
                             f'<i>Джедаям страдать еще <b>{utils.calc_days()}</b> дней</i>\n\n'
                             f'<b>[📈СТАТИСТИКА от {t}]\n</b>'
                             f'<i>👷Людей в боте:</i> <b>{len(users)} (+{new_users})\n</b>'
                             f'<i>✊Джедаев:</i> <b>{len(white)} (+{new_white})\n</b>'
                             f'<i>👹Ситхов:</i> <b>{len(dark)} (+{new_dark})</b>')
                else:
                    query.message.edit_text(
                        reply_markup=Keyboards().main_menu_keyboard,
                        parse_mode=ParseMode.HTML,
                        text=f'<i>👋Приветствую </i>\n'
                             f'<b>Ты на светлой стороне✊</b>\n'
                             f'<i>До конца недрочабря <b>{utils.calc_days()}</b> дней</i>\n\n'
                             f'<b>[📈СТАТИСТИКА от {t}]\n</b>'
                             f'<i>👷Людей в боте:</i> <b>{len(users)} (+{new_users})\n</b>'
                             f'<i>✊Джедаев:</i> <b>{len(white)} (+{new_white})\n</b>'
                             f'<i>👹Ситхов:</i> <b>{len(dark)} (+{new_dark})</b>\n\n'

                             '<code>Чтобы чтобы примкнуть к ситхам нажми кнопку ниже🔽:</code>')
            except Exception as e:
                context.bot.answer_callback_query(callback_query_id=query.id, text='Новой информации не появилось')
