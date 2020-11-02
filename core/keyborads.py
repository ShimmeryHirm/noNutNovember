from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class Keyboards:
    """Base class for inline keyboards objects."""

    def __init__(self, **_):
        self.main_menu_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👹 Перейти на темную сторону", callback_data='confirm')]
            , [InlineKeyboardButton("🔄 Обновить статистику", callback_data='reload')]]
        )
        self.confirm = InlineKeyboardMarkup(
            [[InlineKeyboardButton("✅ Уверен.", callback_data='activate')],
             [InlineKeyboardButton("❌ Это был миссклик", callback_data='cancel')]])
        self.back = InlineKeyboardMarkup(
            [[InlineKeyboardButton("◀️Вернуться в главное меню", callback_data='back')]])
        self.sith = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔄 Обновить статистику", callback_data='reload')]])
