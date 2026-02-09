import os
import telebot
from flask import Flask, request

# ====== НАСТРОЙКИ ======
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ID менеджера
MANAGER_CHAT_ID = os.environ.get('MANAGER_CHAT_ID', 952957376)

# Хранилище данных пользователей
user_data = {}

# Каталог товаров (используем прямые ссылки на фото)
catalog = {
    "product_1": {
        "name": "Грецкий орех очищенный",
        "description": "Это ценили дороже золота 👑\n\nВ Древнем Вавилоне простым людям запрещали есть грецкие орехи. Считалось, что они сильно развивают ум и предназначены только для знати.\n\nХорошо, что сегодня все могут быть умными 🤪\n\nГрецкий орех очищенный\nУпаковка 500 г\nЦена 400 ₽",
        "photo_url": "https://files.catbox.moe/dviaum.JPG"  # Пример фото
    },
    "product_2": {
        "name": "Орехи: Миндаль золотой", 
        "description": "Символ женской красоты\n\nСамый богатый витамином Е орех, и самый мощный антиоксидант с интересной историей.\n\nКстати, в разных культурах он символизировал богатство, удачу и женскую красоту 💎\n\nМиндаль золотой\nУпаковка 1000 г\nЦена 950 ₽",
        "photo_url": "https://files.catbox.moe/4vb5wf.JPG"
    }, 
    "product_3": {
        "name": "Орехи: Кешью", 
        "description": "Кешью\nУпаковка 1000 г\nЦена 1000 ₽",
        "photo_url": "https://files.catbox.moe/ncqm5q.JPG"
    },
    "product_4": {
        "name": "Клубника сушеная", 
        "description": "Самый легкий способ стать счастливее\n\nЭти ягоды стимулируют выработку гормонов радости, а их аромат мгновенно поднимает настроение.\n\nСчастья много не бывает 😉\n\nКлубника сушеная\nУпаковка 500 г\nЦена 350 ₽",
        "photo_url": "https://files.catbox.moe/hzg6v0.JPG"
    },
    "product_5": {
        "name": "Манго сушеное",
        "description": "Фрукт солнца и любви❤️\n\nЭто не только вкусно, но и очень полезно. Настоящая кладезь витаминов, которая оставляет в восторге взрослых и детей!\n\nИнтересный факт: для 1 кг сушеного фрукта используется около 10 кг свежих плодов😁\n\nСушенное манго без сахара\nУпаковка 500 г\nЦена 250 ₽",
        "photo_url": "https://files.catbox.moe/oqrkvn.JPG"
    }
}

# ====== КЛАВИАТУРЫ ======
def main_menu():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📖 Каталог товаров")
    keyboard.add("ℹ️ О нас")
    return keyboard

def catalog_menu():
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    for product_id, product_info in catalog.items():
        keyboard.add(
            telebot.types.InlineKeyboardButton(
                text=product_info["name"],
                callback_data=f"product_{product_id}"
            )
        )
    return keyboard

def city_selection():
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            "🏙️ Сделать предзаказ в Славгороде",
            callback_data="city_a"
        ),
        telebot.types.InlineKeyboardButton(
            "🏙️ Сделать предзаказ в Яровом", 
            callback_data="city_b"
        ),
        telebot.types.InlineKeyboardButton(
            "🔙 Назад в каталог",
            callback_data="back_to_catalog"
        )
    )
    return keyboard

def new_order_keyboard():
    """Клавиатура с кнопкой 'Сделать новый заказ'"""
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            "🔄 Сделать новый заказ",
            callback_data="new_order"
        )
    )
    return keyboard

# ====== ОБРАБОТЧИКИ ======
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Добро пожаловать, здесь Вы можете оформить предзаказ товаров!\n\n"
        "Забрать заказы в Славгороде можно будет 14 февраля.\n"
        "Забрать заказы в Яровом можно будет 15 февраля.\n"
        "Переходите в каталог👇.\n"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "📖 Каталог товаров")
def show_catalog(message):
    bot.send_message(
        message.chat.id,
        "📋 Выберите товар из каталога:",
        reply_markup=catalog_menu()
    )

@bot.message_handler(func=lambda message: message.text == "ℹ️ О нас")
def about_us(message):
    bot.send_message(
        message.chat.id,
        "🏢 О нашей компании:\n\n"
        "DP SBOR — отборные орехи и сухофрукты.\n"
        "Мы выбираем продукты по качеству, вкусу и внешнему виду, а не по минимальной цене.\n"
        "Сама компания находится в Новосибирске.\n"
        "Периодически делаем поставки в Славгород и Яровое.\n"
        "Мы обрабатываем предзаказы и связываемся с Вами в личных сообщениях\n"
        "Ссылка на наш канал t.me/dp_sbor"
    )

@bot.callback_query_handler(func=lambda call: call.data == 'new_order')
def handle_new_order(call):
    """Обработчик кнопки 'Сделать новый заказ'"""
    bot.answer_callback_query(call.id, "Начинаем новый заказ!")
    
    # Удаляем сообщение с кнопкой (если это inline-кнопка)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    
    # Отправляем пользователя в каталог
    bot.send_message(
        call.message.chat.id,
        "🔄 *Начинаем новый заказ!*\n\nВыберите товар из каталога:",
        parse_mode="Markdown",
        reply_markup=catalog_menu()
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('product_'))
def show_product_details(call):
    product_id = call.data
    
    # Убираем лишний префикс если есть
    if product_id.startswith("product_product_"):
        product_id = product_id.replace("product_", "", 1)
    
    product_info = catalog.get(product_id)
    
    if product_info:
        try:
            # Отправляем фото товара
            bot.send_photo(
                chat_id=call.message.chat.id,
                photo=product_info["photo_url"],
                caption=f"📦 *{product_info['name']}*\n\n{product_info['description']}",
                parse_mode="Markdown",
                reply_markup=city_selection()
            )
        except Exception as e:
            # Если фото не загрузилось, отправляем только текст
            print(f"Ошибка загрузки фото: {e}")
            bot.send_message(
                call.message.chat.id,
                f"📦 *{product_info['name']}*\n\n{product_info['description']}",
                parse_mode="Markdown",
                reply_markup=city_selection()
            )
        
        # Сохраняем выбранный товар
        user_data[call.message.chat.id] = {"product": product_info["name"]}
        bot.answer_callback_query(call.id)
    else:
        bot.answer_callback_query(call.id, "Товар не найден")

@bot.callback_query_handler(func=lambda call: call.data in ['city_a', 'city_b'])
def select_city(call):
    city_name = "Славгород" if call.data == "city_a" else "Яровое"
    
    # Сохраняем выбранный город
    if call.message.chat.id in user_data:
        user_data[call.message.chat.id]["city"] = city_name
    else:
        user_data[call.message.chat.id] = {"city": city_name}
    
    instruction_text = (
        "🟢 *Пошаговая инструкция:*\n\n"
        "1. Напишите, что хотите заказать (например: 'Грецкий орех, 2 упаковки')\n"
        "2. Менеджер свяжется с вами"
    )
    
    # Пытаемся обновить подпись, если это фото
    try:
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=instruction_text,
            parse_mode="Markdown"
        )
        
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None
        )
    except:
        # Если не фото, а текстовое сообщение
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=instruction_text,
            parse_mode="Markdown"
        )
    
    # Просим написать заказ
    bot.send_message(
        call.message.chat.id,
        f"📍 Вы выбрали: {city_name}\n\n"
        f"Теперь напишите, что именно Вы хотите заказать "
        f"(например: '{user_data[call.message.chat.id].get('product', 'товар')}', 2 упаковки)"
    )
    
    bot.answer_callback_query(call.id, f"Выбрано: {city_name}")

@bot.callback_query_handler(func=lambda call: call.data == "back_to_catalog")
def back_to_catalog(call):
    try:
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=catalog_menu()
        )
    except:
        # Если не получается обновить, отправляем новое сообщение
        bot.send_message(
            call.message.chat.id,
            "📋 Выберите товар из каталога:",
            reply_markup=catalog_menu()
        )
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_order(message):
    chat_id = message.chat.id
    
    # Проверяем, есть ли у пользователя выбранный город
    if chat_id in user_data and "city" in user_data[chat_id]:
        order_text = message.text
        city = user_data[chat_id]["city"]
        product = user_data[chat_id].get("product", "товар")
        
        # Формируем информацию о заказе
        user_info = {
            'name': message.from_user.first_name or "Покупатель",
            'username': message.from_user.username or "Нет username",
            'user_id': message.from_user.id,
            'order': order_text,
            'city': city,
            'product': product
        }
        
        # Сообщение покупателю с кнопкой нового заказа
        confirmation_text = (
            f"✅ *Ваш предзаказ принят!*\n\n"
            f"📍 Город получения: {city}\n"
            f"📝 Ваш заказ: {order_text}\n\n"
            f"Менеджер скоро свяжется с вами для уточнения деталей."
        )
        
        # Отправляем сообщение с кнопкой "Сделать новый заказ"
        bot.send_message(
            chat_id, 
            confirmation_text, 
            parse_mode="Markdown", 
            reply_markup=new_order_keyboard()
        )
        
        # Сообщение менеджеру
        manager_message = (
            f"📦 *НОВЫЙ ПРЕДЗАКАЗ!*\n\n"
            f"👤 Покупатель: {user_info['name']}\n"
            f"👤 Username: @{user_info['username']}\n"
            f"📍 Город: {city}\n"
            f"📝 Заказ: {order_text}\n"
            f"🛒 Товар: {product}\n"
            f"🆔 ID: {user_info['user_id']}\n\n"
            f"💬 Ссылка для связи: tg://user?id={user_info['user_id']}"
        )
        
        try:
            bot.send_message(MANAGER_CHAT_ID, manager_message, parse_mode="Markdown")
            print(f"✅ Заказ отправлен менеджеру: {user_info}")
        except Exception as e:
            print(f"❌ Ошибка отправки менеджеру: {e}")
            bot.send_message(
                chat_id,
                "⚠️ Заказ принят, но возникла проблема с уведомлением менеджера. "
                "Пожалуйста, свяжитесь с нами через контакты.",
                reply_markup=new_order_keyboard()
            )
        
        # Очищаем данные пользователя
        if chat_id in user_data:
            del user_data[chat_id]
    
    else:
        # Если пользователь просто пишет текст без выбора города
        if message.text not in ["📖 Каталог товаров", "ℹ️ О нас", "📞 Контакты"]:
            bot.send_message(
                chat_id,
                "Для оформления заказа сначала выберите товар из каталога 📖",
                reply_markup=main_menu()
            )

# ====== WEBHOOK ======
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'ok', 200
    return 'Bad Request', 400

@app.route('/')
def index():
    return '🤖 Бот предзаказов работает'

@app.route('/health')
def health():
    return 'OK', 200

# ====== ЗАПУСК ======
if __name__ == '__main__':
    # Настраиваем вебхук только если на Render
    if 'RENDER' in os.environ:
        service_name = os.environ.get('RENDER_SERVICE_NAME')
        webhook_url = f'https://{service_name}.onrender.com/webhook'
        bot.remove_webhook()
        bot.set_webhook(url=webhook_url)
        print(f"✅ Вебхук установлен: {webhook_url}")
    else:
        # Для локального тестирования
        bot.remove_webhook()
        print("🔧 Локальный режим (вебхук отключен)")
    
    # Запускаем сервер
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
