import logging
from aiogram import types
import re

from constants.pasha_mentions import (
    PASHA_MENTION_PATTERNS,
    PASHA_MENTION_THRESHOLD,
    PASHA_THANKS_MESSAGE
)

pasha_mention_counts = {}

async def process_pasha_mention(message: types.Message):
    """
    Обрабатывает текстовые сообщения, ищет упоминания "Паша" (учитывая множественные вхождения)
    и отправляет сообщение #СпасибоПаша при достижении порога.
    """
    if message.chat.type not in [types.ChatType.GROUP, types.ChatType.SUPERGROUP]:
        return

    user_text = message.text
    if not user_text:
        return

    total_mentions_in_message = 0
    for pattern in PASHA_MENTION_PATTERNS:
        matches = pattern.findall(user_text)
        total_mentions_in_message += len(matches)

    if total_mentions_in_message > 0:
        chat_id = message.chat.id
        
        pasha_mention_counts[chat_id] = pasha_mention_counts.get(chat_id, 0) + total_mentions_in_message
        
        current_count = pasha_mention_counts[chat_id]
        logging.info(f"Pasha mention(s) detected in chat {chat_id}. Added {total_mentions_in_message}. Current count: {current_count}/{PASHA_MENTION_THRESHOLD}")

        if current_count >= PASHA_MENTION_THRESHOLD:
            logging.info(f"Pasha mention threshold reached in chat {chat_id}. Sending '{PASHA_THANKS_MESSAGE}'.")
            await message.reply(PASHA_THANKS_MESSAGE)
            
            pasha_mention_counts[chat_id] = 0
