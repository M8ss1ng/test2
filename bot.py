import telebot
import random
import string

TOKEN = "7534932740:AAH63ZYchUy9Py5hgq0I0W9S-0CLloXphvM"
bot = telebot.TeleBot(TOKEN)

password_history = {}
nickname_history = {}

def generate_password(length=12, strong=False):
    characters = string.ascii_uppercase + string.digits + string.punctuation if strong else string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def generate_nickname():
    adjectives = ["Dark", "Crazy", "Fast", "Epic", "Silent", "Mysterious", "Brave", "Wild"]
    nouns = ["Wolf", "Ninja", "Dragon", "Shadow", "Ghost", "Rider", "Hunter", "Warrior"]
    number = random.randint(100, 999)
    return random.choice(adjectives) + random.choice(nouns) + str(number)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для генерации паролей и никнеймов.\n"
                          "Команды:\n"
                          "/password <длина> — создать пароль\n"
                          "/password strong — сложный пароль\n"
                          "/history — последние 5 паролей\n"
                          "/nickname — случайный ник\n"
                          "/nickhistory — последние 5 никнеймов")

@bot.message_handler(commands=["password"])
def send_password(message):
    global password_history
    args = message.text.split()
    user_id = message.chat.id
    length = 16
    strong = False

    if len(args) > 1:
        if args[1].isdigit():
            length = int(args[1])
        elif args[1].lower() == "strong":
            strong = True

    if length < 4 or length > 100:
        bot.reply_to(message, "Длина пароля должна быть от 4 до 100 символов.")
        return

    password = generate_password(length, strong)

    if user_id not in password_history:
        password_history[user_id] = []
    password_history[user_id].append(password)
    if len(password_history[user_id]) > 5:
        password_history[user_id].pop(0)

    bot.reply_to(message, f"Твой пароль ({length} символов):\n`{password}`", parse_mode="Markdown")

@bot.message_handler(commands=["history"])
def show_history(message):
    user_id = message.chat.id
    if user_id in password_history and password_history[user_id]:
        history = "\n".join(f"`{p}`" for p in password_history[user_id])
        bot.reply_to(message, f"Твои последние пароли:\n{history}", parse_mode="Markdown")
    else:
        bot.reply_to(message, "История пуста.")

@bot.message_handler(commands=["nickname"])
def send_nickname(message):
    global nickname_history
    user_id = message.chat.id
    nickname = generate_nickname()

    if user_id not in nickname_history:
        nickname_history[user_id] = []
    nickname_history[user_id].append(nickname)
    if len(nickname_history[user_id]) > 5:
        nickname_history[user_id].pop(0)

    bot.reply_to(message, f"Твой никнейм: `{nickname}`", parse_mode="Markdown")

@bot.message_handler(commands=["nickhistory"])
def show_nick_history(message):
    user_id = message.chat.id
    if user_id in nickname_history and nickname_history[user_id]:
        history = "\n".join(f"`{p}`" for p in nickname_history[user_id])
        bot.reply_to(message, f"Твои последние никнеймы:\n{history}", parse_mode="Markdown")
    else:
        bot.reply_to(message, "История пуста.")

@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.reply_to(message, "Я не понимаю эту команду. Используй /password или /nickname.")

print("Бот запущен...")
bot.polling()