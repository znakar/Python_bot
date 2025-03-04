from telebot.util import quick_markup
markup = quick_markup({
    'GitHub':{'url': 'https://github.com/znakar'},
    'YouTube':{'url': 'https://www.youtube.com/'},
    'Images' : {'callback_data': 'images'},
    'Back' : {'callback_data': 'whatever'}
}, row_width=3)

