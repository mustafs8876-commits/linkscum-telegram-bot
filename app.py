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


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")
MINI_APP_URL = os.environ.get("MINI_APP_URL")
BANNER_URL = os.environ.get("BANNER_URL", "")


if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not configured")

if not WEBHOOK_SECRET:
    raise RuntimeError("WEBHOOK_SECRET is not configured")

if not MINI_APP_URL:
    raise RuntimeError("MINI_APP_URL is not configured")


# ============================================================
# BOT / FASTAPI
# ============================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()


# ============================================================
# BANNER
# ============================================================

def get_banner_url() -> str:
    """
    Если BANNER_URL указан вручную — используем его.

    Иначе Vercel автоматически отдаёт:
    /public/banner.png
    как:
    https://domain.vercel.app/banner.png
    """

    if BANNER_URL:
        return BANNER_URL

    host = (
        os.environ.get("VERCEL_PROJECT_PRODUCTION_URL")
        or os.environ.get("VERCEL_URL")
    )

    if host:
        return f"https://{host}/banner.png"

    return ""


# ============================================================
# MAIN KEYBOARD
# ============================================================

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


# ============================================================
# /START
# ============================================================

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

        "⚠️ Используйте только официальные ссылки, "
        "указанные в этом боте.\n\n"

        "<b>Выберите нужный раздел ниже 👇</b>"
    )

    banner = get_banner_url()

    # Если баннер доступен — отправляем фото + текст + кнопки
    if banner:
        try:
            await message.answer_photo(
                photo=banner,
                caption=text,
                reply_markup=main_keyboard(),
                parse_mode="HTML",
            )
            return
        except Exception as error:
            print(f"Banner send error: {error}")

    # Если баннер не загрузился — бот всё равно отвечает
    await message.answer(
        text=text,
        reply_markup=main_keyboard(),
        parse_mode="HTML",
    )


# ============================================================
# SECURITY POPUP
# ============================================================

@dp.callback_query(F.data == "security")
async def security_handler(callback: CallbackQuery) -> None:

    security_text = (
        "🔐 БЕЗОПАСНОСТЬ\n\n"

        "‼️ Используйте только официальные ссылки сервиса.\n\n"

        "⚠️ Перед оплатой обязательно проверяйте "
        "username получателя.\n\n"

        "👤 Официальная поддержка:\n"
        "@rolexgolda_shop\n\n"

        "📢 Официальные ссылки:\n"
        "@rolexgolda_links\n\n"

        "⚠️ Не переводите деньги неизвестным аккаунтам."
    )

    await callback.answer(
        text=security_text,
        show_alert=True,
    )


# ============================================================
# DONATE MENU
# ============================================================

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

    if callback.message:
        await callback.message.answer(
            "💰 <b>Поддержать проект</b>\n\n"
            "Выберите удобный способ 👇",
            reply_markup=keyboard,
            parse_mode="HTML",
        )

    await callback.answer()


# ============================================================
# CLOSE DONATE MENU
# ============================================================

@dp.callback_query(F.data == "close_donate")
async def close_donate_handler(callback: CallbackQuery) -> None:

    if callback.message:
        try:
            await callback.message.delete()
        except Exception as error:
            print(f"Delete message error: {error}")

    await callback.answer()


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
async def health() -> dict:
    return {
        "status": "ok",
        "service": "telegram-webhook",
    }


@app.get("/health")
async def health_check() -> dict:
    return {
        "status": "ok",
    }


# ============================================================
# TELEGRAM WEBHOOK
# ============================================================

@app.post("/webhook")
async def telegram_webhook(request: Request) -> dict:

    # Проверяем secret, который Telegram отправляет
    # в X-Telegram-Bot-Api-Secret-Token
    incoming_secret = request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token",
        "",
    )

    if incoming_secret != WEBHOOK_SECRET:
        print("Invalid webhook secret")

        raise HTTPException(
            status_code=403,
            detail="Invalid webhook secret",
        )

    try:
        payload = await request.json()

        update = Update.model_validate(
            payload,
            context={"bot": bot},
        )

        await dp.feed_update(
            bot,
            update,
        )

    except Exception as error:
        print(
            "Telegram webhook processing error:",
            repr(error),
        )

        raise

    return {
        "ok": True,
    }
