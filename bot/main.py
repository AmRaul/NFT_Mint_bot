import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import asyncio
from dotenv import load_dotenv
import os

# Настройка логирования
logging.basicConfig(
    filename="bot_errors.log",  # файл для хранения логов
    level=logging.ERROR,  # минимальный уровень логирования (для ошибок)
    format="%(asctime)s - %(levelname)s - %(message)s",  # формат логов
)
tg_id = "****"
load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

# Функция для получения текущего счётчика
def get_mint_count():
    try:
        with open("mint_counter.json", "r") as f:
            data = json.load(f)
            return data["minted"]
    except FileNotFoundError:
        return 0

# Функция для обновления счётчика
def update_mint_count(new_count):
    with open("mint_counter.json", "w") as f:
        json.dump({"minted": new_count}, f)


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 Купить NFT - Fronted")],
            [KeyboardButton(text="📩 Получить NFT - Backend")]
        ],
        resize_keyboard=True
    )
    await message.answer("Выбери способ получения NFT:", reply_markup=kb)

@dp.message(lambda msg: msg.text == "🛒 Купить NFT - Fronted")
async def send_deep_link(message: types.Message):
    # # Генерация deep-link для MetaMask
    # buy_link = create_buy_link()
    #
    # # Кодируем buy_link для использования в URL
    # encoded_buy_link = quote(buy_link)
    #
    # # Ссылка на мини-апп, куда передается deep link как параметр
    # mini_app_url = f"https://amraul.github.io/metamask-redirect/?link={encoded_buy_link}"
    #
    # # Создаем клавиатуру с одной кнопкой
    # button = types.InlineKeyboardButton(text="Перейти в MetaMask", url=mini_app_url)
    # keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[button]])  # Явно передаем список кнопок

    # Отправка сообщения с клавиатурой
    # await message.answer("Нажмите на кнопку, чтобы открыть MetaMask:", reply_markup=keyboard)
    await message.answer("Раздел находится в разработке.")

@dp.message(lambda msg: msg.text == "📩 Получить NFT - Backend")
async def manual_mint_prompt(message: types.Message):
    await message.answer("Пришли свой кошелек (в формате 0x...)")

@dp.message()
async def manual_mint_handler(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "No username"
    wallet = message.text.strip()

    # Уведомление тебе
    await bot.send_message(
        tg_id,
        f"💡 Пользователь:\n🆔 ID: {user_id}\n👤 Username: @{username}\n📥 Попытка минта на: {wallet}"
    )
    if wallet.startswith("0x") and len(wallet) == 42:
        from web3_utils import mint_nft
        minted_count = get_mint_count()
        if minted_count < 25:
            to_address = message.text.strip()
            try:
                tx_hash = mint_nft(to_address)
                await message.answer("🎉 Транзакция отправлена! Появится в Arbiscan примерно через минуту.")
                minted_count += 1
                update_mint_count(minted_count)
                await asyncio.sleep(60)
                await message.answer(f"✅ NFT отправлен!\n\n🔗 Tx: https://arbiscan.io/tx/{tx_hash}")
            except Exception as e:
                # Логирование ошибки
                logging.error(f"Ошибка при обработке запроса от пользователя {message.from_user.id}: {e}")
                await message.answer(f"❌ Ошибка при отправке: {str(e)}")
        else:
            await message.answer("Первые 25 NFT подошли к концу.")
    else:
        await message.answer("⛔️ Пожалуйста, пришли корректный адрес кошелька (начинается с 0x и 42 символа).")




async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
