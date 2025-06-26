import logging
from aiogram import types

from constants.mention_config import (
    ALL_MENTION_PATTERNS,
    GLOBAL_MENTION_THRESHOLD,
    generate_thanks_message
)

mention_counts = {}

async def process_mentions(message: types.Message):
    """
    Обрабатывает текстовые сообщения, ищет упоминания настроенных имен (Паша, Захар, Дед и т.д.).
    Все найденные упоминания увеличивают *единый* счетчик для чата.
    При достижении порога отправляет сообщение #Спасибо<Имя>,
    где <Имя> - это базовое имя последнего распознанного слова из текущего сообщения.
    """
    if message.chat.type not in [types.ChatType.GROUP, types.ChatType.SUPERGROUP]:
        return

    user_text = message.text
    if not user_text:
        return

    chat_id = message.chat.id
    
    current_total_count = mention_counts.get(chat_id, 0)

    total_mentions_in_message = 0
    last_matched_base_name = None

    for base_name, pattern in ALL_MENTION_PATTERNS:
        matches = pattern.findall(user_text)
        if matches:
            total_mentions_in_message += len(matches)
            last_matched_base_name = base_name

    if total_mentions_in_message > 0:
        mention_counts[chat_id] = current_total_count + total_mentions_in_message
        
        new_total_count = mention_counts[chat_id]
        logging.info(f"Chat {chat_id}: Total mention(s) detected. Added {total_mentions_in_message}. Current total count: {new_total_count}/{GLOBAL_MENTION_THRESHOLD}")

        if new_total_count >= GLOBAL_MENTION_THRESHOLD:
            logging.info(f"Chat {chat_id}: Global mention threshold reached ({new_total_count}/{GLOBAL_MENTION_THRESHOLD}).")
            
            name_to_thank = last_matched_base_name if last_matched_base_name else "Generic" 
            
            thanks_message = generate_thanks_message(name_to_thank)
            await message.reply(thanks_message)
            
            mention_counts[chat_id] = 0
            logging.info(f"Chat {chat_id}: Global counter reset to 0.")
