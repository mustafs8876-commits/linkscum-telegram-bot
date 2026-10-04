import os

from fastapi import FastAPI, HTTPException, Request
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    Update,
    WebAppInfo,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")
MINI_APP_URL = os.environ.get("MINI_APP_URL", "https://example.com")
BANNER_URL = os.environ.get("BANNER_URL", "")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not configured")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()


def get_banner_url() -> str:
    if BANNER_URL:
        return BANNER_URL

    host = (
        os.environ.get("VERCEL_PROJECT_PRODUCTION_URL")
        or os.environ.get("VERCEL_URL")
    )
    if host:
        return f"https://{host}/banner.png"

    # Used only for local testing if you set BANNER_URL yourself.
    return "https://placehold.co/1600x900/png?text=Telegram+Bot"


def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌐 ПРИОБРЕСТИ/ИНФОРМАЦИЯ",
                    web_app=WebAppInfo(url=MINI_APP_URL),
                )
            ],
            [
                InlineKeyboardButton(
                    text="👤 Поддержка",
                    url="https://t.me/rolexgolda_shop",
                ),
                InlineKeyboardButton(
                    text="🤝 Партнёры",
                    url="https://t.me/INFXTEAM_OFF",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⭐️ Отзывы",
                    url="https://t.me/otzuvudimargx",
                ),
                InlineKeyboardButton(
                    text="📢 Каналы",
                    url="https://t.me/LinkScumMod_Standoff2",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📁 Гайды",
                    url="https://t.me/INFXTEAM_GUIDE",
                ),
                InlineKeyboardButton(
                    text="🔐 Безопасность",
                    callback_data="security",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔥 Boost",
                    url="https://t.me/boost/INFXTEAM",
                ),
                InlineKeyboardButton(
                    text="💰 Поддержать проект",
                    callback_data="donate",
                ),
            ],
        ]
    )


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    text = (
        "🛡 <b>Здравствуйте! Добро пожаловать в LinkScum.</b>\n\n"
        "Здесь собрана основная информация о сервисе, "
        "официальные каналы, отзывы, инструкции и контакты поддержки.\n\n"
        "🎮 <b>Доступные игровые разделы:</b>\n"
        "• Standoff 2\n"
        "• Roblox\n"
        "• Brawl Stars / Clash Royale\n"
        "• PUBG Mobile\n\n"
        "⚠️ Используйте только официальные ссылки, указанные в этом боте.\n\n"
        "<b>Выберите нужный раздел ниже 👇</b>"
    )

    await message.answer_photo(
        photo=get_banner_url(),
        caption=text,
        reply_markup=main_keyboard(),
        parse_mode="HTML",
    )


@dp.callback_query(F.data == "security")
async def security_handler(callback: CallbackQuery) -> None:
    await callback.answer(
        text=(
            "🔐 БЕЗОПАСНОСТЬ\n\n"
            "‼️ Используйте только официальные ссылки сервиса.\n\n"
            "⚠️ Перед оплатой обязательно проверяйте username получателя.\n\n"
            "👤 Официальная поддержка:\n"
            "@rolexgolda_shop\n\n"
            "📢 Официальные ссылки:\n"
            "@rolexgolda_links\n\n"
            "⚠️ Не переводите деньги неизвестным аккаунтам."
        ),
        show_alert=True,
    )


@dp.callback_query(F.data == "donate")
async def donate_handler(callback: CallbackQuery) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Crypto Bot",
                    url="https://t.me/send?start=IVpFjeGEDimg",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Закрыть",
                    callback_data="close_donate",
                )
            ],
        ]
    )

    await callback.message.answer(
        "💰 <b>Поддержать проект</b>\n\nВыберите удобный способ 👇",
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await callback.answer()


@dp.callback_query(F.data == "close_donate")
async def close_donate_handler(callback: CallbackQuery) -> None:
    if callback.message:
        try:
            await callback.message.delete()
        except Exception:
            pass
    await callback.answer()


@app.get("/")
async def health() -> dict:
    return {"status": "ok", "service": "telegram-webhook"}


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


@app.post("/webhook")
async def telegram_webhook(request: Request) -> dict:
    if WEBHOOK_SECRET:
        incoming_secret = request.headers.get(
            "X-Telegram-Bot-Api-Secret-Token", ""
        )
        if incoming_secret != WEBHOOK_SECRET:
            raise HTTPException(status_code=403, detail="Invalid webhook secret")

    payload = await request.json()
    update = Update.model_validate(payload, context={"bot": bot})
    await dp.feed_update(bot, update)

    return {"ok": True}
