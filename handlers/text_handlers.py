import logging
from aiogram import types

from constants.answers import ANSWERS
from handlers.pasha_counter_handler import process_pasha_mention 

async def handle_text_message(message: types.Message):
    """
    Обрабатывает текстовые сообщения.
    Включает логику для словаря ANSWERS и вызывает логику счетчика Паши.
    """
    logging.info(f"Received text message from {message.from_user.full_name}: {message.text}")

    await process_pasha_mention(message)

    user_text_lower = message.text.lower()
    
    reply_text = ANSWERS.get(user_text_lower)

    if reply_text:
        logging.info(f"Matching text '{message.text}' from {message.from_user.full_name} in ANSWERS. Replying with: '{reply_text}'")
        await message.reply(reply_text)
