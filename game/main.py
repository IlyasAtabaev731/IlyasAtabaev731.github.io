import threading

import telebot
import sqlite3
import schedule
import time

bot = telebot.TeleBot('7124877891:AAFktRWMu54OcYBmSQBFwkJsvyzjUEEWb58')
lock_app = threading.Lock()

with lock_app:
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()

    c.execute(
        '''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, userid TEXT, 
        ref INTEGER, balance INTEGER, lang TEXT)''')
    conn.commit()


def get_user_language(userid):
    with lock_app:
        return c.execute("SELECT lang FROM users WHERE userid = ?", (userid,)).fetchone()[0] if c.execute(
            "SELECT lang FROM users WHERE userid = ?", (userid,)).fetchone() else None


def markup_menu_eng():
    markup = telebot.types.InlineKeyboardMarkup()

    markup.add(telebot.types.InlineKeyboardButton('Cashier 🛒', web_app=telebot.types.WebAppInfo(
        'https://ria-news.github.io/kassa_final/')))

    markup.add(telebot.types.InlineKeyboardButton('Balance 💰', callback_data='balance'))

    markup.add(telebot.types.InlineKeyboardButton('Hall of Fame 🎖', callback_data='ref'))

    markup.add(telebot.types.InlineKeyboardButton('Referral Link 🔗', callback_data='make'))

    markup.add(telebot.types.InlineKeyboardButton('Channel 👾', url='t.me/betblockton'))

    return markup


def markup_menu_rus():
    markup = telebot.types.InlineKeyboardMarkup()

    markup.add(telebot.types.InlineKeyboardButton('Касса 🛒', web_app=telebot.types.WebAppInfo(
        'https://ria-news.github.io/kassa_final/')))

    markup.add(telebot.types.InlineKeyboardButton('Баланс 💰', callback_data='balance'))

    markup.add(telebot.types.InlineKeyboardButton('Доска почета 🎖', callback_data='ref'))

    markup.add(telebot.types.InlineKeyboardButton('Получить реферальную ссылку 🔗', callback_data='make'))

    markup.add(telebot.types.InlineKeyboardButton('Канал 👾', url='t.me/betblockton'))

    return markup


def extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else None


@bot.message_handler(commands=['start'], content_types=['text'])
def main(message):
    unique_code = extract_unique_code(message.text)
    username = message.from_user.username
    userid = message.chat.id

    with lock_app:
        c.execute("SELECT username FROM users WHERE username=?", (username,))
        user = c.fetchone()

    if user is None:
        if unique_code:
            with lock_app:
                c.execute("UPDATE users SET ref = ref + 1 WHERE userid = ?", (unique_code,))
                c.execute("UPDATE users SET balance = balance + 50 WHERE userid = ?", (unique_code,))
        with lock_app:
            c.execute("INSERT INTO users (username, userid, ref, balance) VALUES (?, ?, ?, ?)",
                      (username, userid, 0, 50))
            conn.commit()

        markup = telebot.types.InlineKeyboardMarkup()

        markup.add(telebot.types.InlineKeyboardButton('English 🇬🇧', callback_data='menu_eng'))

        markup.add(telebot.types.InlineKeyboardButton('Русский 🇷🇺', callback_data='menu_ru'))

        bot.send_message(message.chat.id, 'Choose language/Выберите язык:', reply_markup=markup)
    else:
        lang = get_user_language(message.chat.id)
        if lang == 'ru':
            bot.send_message(message.chat.id, f'<b>Слил последний депозит на фьючерсах? Хватит играть в казино!</b>\n\n'
                                              f'Нам на кассу срочно требуется опытный крипто-аналитик.\n'
                                              f'Вставай за прилавок в разделе — '
                                              f'«<b>Касса 🛒</b>»\n\n'
                                              f'Зарплата ежедневная!\n'
                                              f'Проверяй сколько денег ты уже заработал в разделе — «<b>Баланс 💰</b>» \n\n'
                                              f'Не дай друзьям упустит свой шанс!\n'
                                              f'Свою реферальную ссылку сможешь найти в — «<b>Получить реферальную ссылку 🔗</b>»\n\n'
                                              f'Героев надо знать в лицо!\nЧем больше друзей ты пригласил - тем больше мы тебя ценим. '
                                              f'Посмотреть на каком ты месте можно в  — «<b>Доска почета 🎖</b>»',
                             reply_markup=markup_menu_rus(),
                             parse_mode='html')
        else:
            bot.send_message(message.chat.id,
                             f'<b>Liquidated your last deposit on futures?\nStop playing at the casino!</b>\n\n'
                             f'We urgently need an experienced cryptanalyst at the checkout.\n'
                             f'Get behind the counter in the section — '
                             f'"<b>Cashier 🛒</b>"\n\n'
                             f'Salary is daily! '
                             f'Check how much money you have already earned in the section — "<b>Balance 💰</b>" \n\n'
                             f'Do not let your friends miss your chance!'
                             f'You can find your referral link in — "<b>Referral Link 🔗</b>"\n\n'
                             f'You need to know heroes by sight! The more friends you invite, the more we appreciate you. '
                             f'To see what place you are in — "<b>Leaderboard 🎖</b>"',
                             reply_markup=markup_menu_eng(),
                             parse_mode='html')


@bot.callback_query_handler(func=lambda call: call.data.startswith('ref'))
def ref_call(call):
    with lock_app:
        c.execute('''SELECT * FROM users ORDER BY ref DESC LIMIT 5''')
        top_users = c.fetchall()

    lang = get_user_language(call.message.chat.id)
    if lang == 'ru':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Вернуться в меню ⬅', callback_data='menu_skip'))
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Main Menu ⬅', callback_data='menu_skip'))

    output = ''
    for i in range(len(top_users)):
        if i == 0:
            output += f'🥇 {i + 1}. @{top_users[i][0]} - {top_users[i][2]}\n'
        elif i == 1:
            output += f'🥈 {i + 1}. @{top_users[i][0]} - {top_users[i][2]}\n'
        elif i == 2:
            output += f'🥉 {i + 1}. @{top_users[i][0]} - {top_users[i][2]}\n'
        else:
            output += f'{i + 1}. @{top_users[i][0]} - {top_users[i][2]}\n'

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=output,
                          reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('menu'))
def menu_call(call):
    lang = call.data.split('_')[1]
    if lang != 'skip':
        with lock_app:
            c.execute("UPDATE users SET lang = ? WHERE userid = ?", (lang, call.message.chat.id,))

    lang = get_user_language(call.message.chat.id)
    if lang == 'ru':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'<b>Слил последний депозит на фьючерсах? Хватит играть в казино!</b>\n\n'
                                   f'Нам на кассу срочно требуется опытный крипто-аналитик.\n'
                                   f'Вставай за прилавок в разделе — '
                                   f'«<b>Касса 🛒</b>»\n\n'
                                   f'Зарплата ежедневная!\n'
                                   f'Проверяй сколько денег ты уже заработал в разделе — «<b>Баланс 💰</b>» \n\n'
                                   f'Не дай друзьям упустит свой шанс!\n'
                                   f'Свою реферальную ссылку сможешь найти в — «<b>Получить реферальную ссылку 🔗</b>»\n\n'
                                   f'Героев надо знать в лицо!\nЧем больше друзей ты пригласил - тем больше мы тебя ценим. '
                                   f'Посмотреть на каком ты месте можно в  — «<b>Доска почета 🎖</b>»',
                              reply_markup=markup_menu_rus(),
                              parse_mode='html')
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'<b>Liquidated your last deposit on futures?\nStop playing at the casino!</b>\n\n'
                                   f'We urgently need an experienced cryptanalyst at the checkout.\n'
                                   f'Get behind the counter in the section — '
                                   f'"<b>Cashier 🛒</b>"\n\n'
                                   f'Salary is daily! '
                                   f'Check how much money you have already earned in the section — "<b>Balance 💰</b>" \n\n'
                                   f'Do not let your friends miss your chance!'
                                   f'You can find your referral link in — "<b>Referral Link 🔗</b>"\n\n'
                                   f'You need to know heroes by sight! The more friends you invite, the more we appreciate you. '
                                   f'To see what place you are in — "<b>Leaderboard 🎖</b>"',
                              reply_markup=markup_menu_eng(),
                              parse_mode='html')


@bot.callback_query_handler(func=lambda call: call.data.startswith('make'))
def make_call(call):
    lang = get_user_language(call.message.chat.id)
    if lang == 'ru':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Вернуться в меню ⬅', callback_data='menu_skip'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Вот ваша реферальная ссылка - \
                                  <code>t.me/betblocktonbot?start={call.message.chat.id}</code>',
                              reply_markup=markup, parse_mode='html')
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Main Menu ⬅', callback_data='menu_skip'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Here is your link - '
                                   f'<code>t.me/betblocktonbot?start={call.message.chat.id}</code>',
                              reply_markup=markup, parse_mode='html')


def send_message_to_all(text):
    c.execute("SELECT userid FROM users")
    chat_ids = [row[0] for row in c.fetchall()]
    for chat_id in chat_ids:
        try:
            bot.send_message(chat_id=chat_id, text=text)
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")


@bot.callback_query_handler(func=lambda call: call.data.startswith('done'))
def done(call):
    with lock_app:
        c.execute("UPDATE users SET balance = balance + 50 WHERE userid = ?", (call.message.chat.id,))


@bot.callback_query_handler(func=lambda call: call.data.startswith('balance'))
def get_balance(call):
    lang = get_user_language(call.message.chat.id)
    if lang == 'ru':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Вернуться в меню ⬅', callback_data='menu_skip'))
        with lock_app:
            balance = c.execute('SELECT balance FROM users WHERE userid = ?',
                                (call.message.chat.id,)).fetchone()

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Вот ваш баланс - {balance[0]}$BBT 💰',
                              reply_markup=markup, parse_mode='html')
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Main Menu ⬅', callback_data='menu_skip'))

        with lock_app:
            balance = c.execute('SELECT balance FROM users WHERE userid = ?',
                                (call.message.chat.id,)).fetchone()

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Here is your balance - {balance[0]}$BBT 💰',
                              reply_markup=markup, parse_mode='html')


@bot.message_handler(commands=['sendall'])
def handle_sendall(message):
    if message.from_user.username == 'kirill_eth':
        text = message.text.split(' ', 1)[1]
        send_message_to_all(text)


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


def add_balance_to_all_users():
    with lock_app:
        c.execute("UPDATE users SET balance = balance + 50")
        conn.commit()


if __name__ == '__main__':
    schedule.every().day.at("00:00").do(add_balance_to_all_users)

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    bot.infinity_polling()
