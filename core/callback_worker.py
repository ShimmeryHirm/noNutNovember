from telegram import  ParseMode

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
                                              text='Ты должен был бороться со злом, а не примкнуть к нему!',
                                              show_alert=True)

            query.message.edit_text(
                parse_mode=ParseMode.HTML,
                reply_markup=Keyboards().sith,

                text=f'<i>👋Приветствую</i>\n\n'
                     f'<b>Ты на темной стороне👹</b>\n'
            )

    if query.data == 'cancel':
        context.bot.answer_callback_query(callback_query_id=query.id, text='Будь аккуратнее пожалуйста!')

        query.message.edit_text(
            parse_mode=ParseMode.HTML,
            reply_markup=Keyboards().main_menu_keyboard,

            text=f'<i>👋Приветствую</i>\n\n'
                 f'<b>Ты на светлой стороне✊</b>\n')
    if query.data == 'reload':
        with session_scope() as session:
            slave = session.query(UsersTable).filter_by(id=query.message.chat.id).first()  # Find slave in DB

            users = session.query(UsersTable).all()
            dark = session.query(UsersTable).filter(UsersTable.side == 1).all()
            white = session.query(UsersTable).filter(UsersTable.side == 0).all()
            try:
                if slave.side == 1:
                    query.message.edit_text(
                        parse_mode=ParseMode.HTML,
                        reply_markup=Keyboards().sith,

                        text=f'<i>👋Приветствую</i>\n'
                             f'<b>Ты на темной стороне 👹</b>\n\n'
                             f'<b>[📈СТАТИСТИКА]\n</b>'
                             f'<i>👷Людей в боте:</i> <b>{len(users)}\n</b>'
                             f'<i>✊Джедаев:</i> <b>{len(white)}\n</b>'
                             f'<i>👹Ситхов:</i> <b>{len(dark)}</b>')
                else:
                    query.message.edit_text(
                        reply_markup=Keyboards().main_menu_keyboard,
                        parse_mode=ParseMode.HTML,
                        text=f'<i>👋Приветствую </i>\n'
                             f'<b>Ты на светлой стороне✊</b>\n\n'
                             f'<b>[📈СТАТИСТИКА]\n</b>'
                             f'<i>👷Людей в боте:</i> <b>{len(users)}\n</b>'
                             f'<i>✊Джедаев:</i> <b>{len(white)}\n</b>'
                             f'<i>👹Ситхов:</i> <b>{len(dark)}</b>\n\n'

                             '<code>Чтобы чтобы примкнуть к ситхам нажми кнопку ниже🔽:</code>')
            except:
                context.bot.answer_callback_query(callback_query_id=query.id, text='Новой информации не появилось')
