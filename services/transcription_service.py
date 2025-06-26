import logging
import aiohttp
import config

async def transcribe_audio(audio_bytes: bytes, filename: str = "voice.ogg") -> str:
    """
    Отправляет аудиофайл в TRANSCRIBE_API для транскрибирования.

    Args:
        audio_bytes (bytes): Содержимое аудиофайла в байтах.
        filename (str): Имя файла, которое будет использовано при отправке (важно для multipart/form-data).

    Returns:
        str: Транскрибированный текст или сообщение об ошибке.
    """
    url = config.TRANSCRIBE_API
    
    data = aiohttp.FormData()
    data.add_field('file', audio_bytes, filename=filename, content_type='audio/ogg')
    
    logging.info(f"Sending audio for transcription to: {url}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    transcript = result.get("text", "Не удалось извлечь текст из ответа API.")
                    logging.info(f"Transcription successful. Text: {transcript[:50]}...")
                    return transcript
                else:
                    error_text = await response.text()
                    logging.error(f"Transcription API returned non-200 status: {response.status}. Response: {error_text}")
                    return f"Ошибка транскрибирования: {response.status} - {error_text[:100]}..."
    except aiohttp.ClientError as e:
        logging.error(f"Network or client error during transcription: {e}")
        return "Ошибка сети или соединения с сервисом транскрибирования."
    except Exception as e:
        logging.error(f"Unexpected error during transcription: {e}")
        return "Произошла непредвиденная ошибка при транскрибировании."
