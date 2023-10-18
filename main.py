import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
bot = telebot.TeleBot("6397664380:AAHXFtcz6njekdgbchsLp8_GcXdfzVk8pis",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Познакомимся)"
text_button_1 = "Смешные животные"
text_button_2 = "Интересный факт"
text_button_3 = "Пока-пока"

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Что я могу сделать для *Вас*?',
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Супер! Давайте скорее знакомиться! Как *Вас* зовут?')
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Красивое имя! Меня зовут Ника! Очень рада нашему знакомству! Сколько *Вам* лет?')
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id,
                     'Ух ты! А я еще совсем молодеький бот и умею выполнять совсем немного функций.Я мечтаю о том, что когда подрасту стать нейросетью, которая будет знать ответ на любой вопрос и выполнять любые функции!)',
                     reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "Я безумно люблю смотреть видосики с забавными животными!Скорее посмотрите этот видосик)(https://youtu.be/lDiCMgrxUDM?si=MtIjVP0m2gnIB3_J) ",
                     reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "Шоколад *Ritter Sport* стали выпускать в форме квадрата после того, как в 30-е годы прошлого века стали популярны куртки с квадратными карманами. Компания решила наладить производство квадратных шоколадных плиток, которые помещались бы в эти карманы, но при этом не ломались и имели вес обычной шоколадки.",
                     reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Так быстро уходите? Очень жаль( Буду с нетерпением *Вас* ждать вновь!",
                     reply_markup=menu_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()