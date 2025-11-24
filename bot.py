import os
import logging
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Настройки
BOT_TOKEN = os.getenv('BOT_TOKEN')
YOUR_USER_ID = "@hateillusion"  # Твой юзернейм

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def forward_message(update: Update, context: CallbackContext):
    try:
        user = update.message.from_user
        chat_id = update.message.chat_id
        
        # Информация о отправителе
        user_info = f"📨 Новое сообщение от:\n"
        user_info += f"👤 Имя: {user.first_name}\n"
        user_info += f"🆔 ID: {user.id}\n"
        user_info += f"💬 Юзернейм: @{user.username}\n" if user.username else "💬 Юзернейм: нет\n"
        
        # Пересылаем сообщение
        if update.message.text:
            # Текстовое сообщение
            context.bot.send_message(
                chat_id=YOUR_USER_ID,
                text=f"{user_info}\n📝 Текст: {update.message.text}"
            )
        elif update.message.photo:
            # Фото
            photo_file = update.message.photo[-1].file_id
            context.bot.send_photo(
                chat_id=YOUR_USER_ID,
                photo=photo_file,
                caption=f"{user_info}\n🖼 Фото"
            )
        elif update.message.video:
            # Видео
            video_file = update.message.video.file_id
            context.bot.send_video(
                chat_id=YOUR_USER_ID,
                video=video_file,
                caption=f"{user_info}\n🎥 Видео"
            )
        elif update.message.document:
            # Документ
            doc_file = update.message.document.file_id
            context.bot.send_document(
                chat_id=YOUR_USER_ID,
                document=doc_file,
                caption=f"{user_info}\n📎 Документ"
            )
        else:
            # Любой другой тип сообщения
            context.bot.send_message(
                chat_id=YOUR_USER_ID,
                text=f"{user_info}\n📦 Другой тип сообщения"
            )
        
        # Отправляем подтверждение отправителю
        update.message.reply_text("✅ Сообщение переслано!")
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")

def main():
    # Получаем токен из переменных окружения
    token = os.getenv('BOT_TOKEN')
    if not token:
        print("❌ Ошибка: BOT_TOKEN не установлен!")
        return
    
    # Создаем updater
    updater = Updater(token)
    dispatcher = updater.dispatcher
    
    # Добавляем обработчик всех сообщений
    dispatcher.add_handler(MessageHandler(Filters.all, forward_message))
    
    # Запускаем бота
    print("🤖 Бот запущен!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
