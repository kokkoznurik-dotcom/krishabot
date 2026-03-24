import asyncio
import re
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def extract_id(text):
    match = re.search(r'(\d{6,})', text)
    return match.group(1) if match else None


@dp.message()
async def handle_message(message: types.Message):
    if not message.text:
        return

    ad_id = extract_id(message.text)

    if ad_id:
        if not hasattr(handle_message, "seen"):
            handle_message.seen = set()

        if ad_id in handle_message.seen:
            try:
                await message.delete()
            except:
                pass
        else:
            handle_message.seen.add(ad_id)


@dp.message(Command("cleanup"))
async def cleanup(message: types.Message):
    await message.answer("🧹 Чищу последние сообщения...")

    seen = set()
    deleted = 0

    async for msg in bot.iter_chat_history(message.chat.id, limit=200):
        if msg.text:
            ad_id = extract_id(msg.text)

            if ad_id:
                if ad_id in seen:
                    try:
                        await bot.delete_message(message.chat.id, msg.message_id)
                        deleted += 1
                    except:
                        pass
                else:
                    seen.add(ad_id)

    await message.answer(f"✅ Удалено дублей: {deleted}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
