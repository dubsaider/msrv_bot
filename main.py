import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType

import config
from handlers.text_handlers import handle_text_message
from handlers.audio_handlers import handle_voice_message

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

def register_handlers(dp: Dispatcher):
    """
    Регистрирует все обработчики сообщений в диспетчере.
    """
    dp.message_handler(content_types=ContentType.TEXT)(handle_text_message)

    dp.message_handler(content_types=[ContentType.VOICE, ContentType.VIDEO_NOTE])(handle_voice_message)

    @dp.message_handler(content_types=ContentType.ANY)
    async def handle_other_message_types(message: types.Message):
        logging.info(f"Received unsupported message type ({message.content_type}) from {message.from_user.full_name}.")
        

if __name__ == '__main__':
    logging.info("Starting bot...")
    register_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
