import logging
from aiogram import types
import io
import html
from services.transcription_service import transcribe_audio

async def handle_voice_message(message: types.Message):
    """
    Обрабатывает голосовые сообщения и видеосообщения (кружочки),
    скачивает их и отправляет на транскрибирование.
    Транскрипция отображается как цитата.
    """
    logging.info(f"Received voice/video_note message from {message.from_user.full_name} ({message.from_user.id}).")

    file_to_process = None
    if message.voice:
        file_to_process = message.voice
        logging.info("Detected message type: VOICE.")
    elif message.video_note:
        file_to_process = message.video_note
        logging.info("Detected message type: VIDEO_NOTE.")
    else:
        logging.warning("Message is neither a voice nor a video_note despite handler type. Skipping.")
        await message.reply("Не удалось обработать аудио/видеосообщение.")
        return

    processing_message = await message.reply("Начинаю транскрибирование аудио, пожалуйста, подождите...")

    try:
        file_id = file_to_process.file_id
        suggested_filename_extension = "ogg" if message.voice else "mp4"


        file_info = await message.bot.get_file(file_id)
        file_path_on_telegram = file_info.file_path

        downloaded_file: io.BytesIO = await message.bot.download_file(file_path_on_telegram)
        
        audio_bytes = downloaded_file.read()

        transcript = await transcribe_audio(audio_bytes, filename=f"{file_id}.{suggested_filename_extension}")
        
        escaped_transcript = html.escape(transcript)

        await message.reply(
            f"Транскрипция:\n<blockquote expandable=\"false\">{escaped_transcript}</blockquote>",
            parse_mode=types.ParseMode.HTML
        )

    except Exception as e:
        logging.error(f"Error processing voice/video_note message for {message.from_user.full_name}: {e}", exc_info=True)
        await message.reply("Произошла ошибка при обработке вашего аудио/видеосообщения.")
    finally:
        try:
            await message.bot.delete_message(chat_id=processing_message.chat.id, message_id=processing_message.message_id)
        except Exception as e:
            logging.warning(f"Could not delete processing message: {e}")
