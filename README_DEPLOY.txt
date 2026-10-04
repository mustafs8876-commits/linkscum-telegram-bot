LINKSCUM TELEGRAM BOT — VERCEL WEBHOOK
=====================================

Этот проект работает через Telegram webhook.
После настройки компьютер можно выключить: Telegram будет отправлять обновления
на HTTPS-адрес Vercel, а Vercel запустит Python-функцию по запросу.

ВАЖНО
-----
1. Не храните BOT_TOKEN в GitHub или прямо в app.py.
2. Если токен когда-либо публиковался, перевыпустите его через @BotFather.
3. MINI_APP_URL должен вести только на легитимный HTTPS-сервис.
   Не используйте Mini App для обманного сбора паролей, токенов или аккаунтных данных.

СТРУКТУРА
---------
app.py
requirements.txt
pyproject.toml
setup_webhook.py
public/
  banner.png

ШАГ 1 — ЗАГРУЗИТЬ В GITHUB
---------------------------
Создайте новый репозиторий и загрузите в него ВСЕ файлы из этой папки.
Файл .env в GitHub не загружайте.

ШАГ 2 — СОЗДАТЬ ПРОЕКТ В VERCEL
--------------------------------
1. Откройте Vercel.
2. Add New -> Project.
3. Import Git Repository.
4. Выберите репозиторий с этим ботом.
5. Framework можно оставить Auto/Other — Vercel определит FastAPI.
6. Пока не нажимайте Deploy, если хотите сначала добавить переменные.

ШАГ 3 — ENVIRONMENT VARIABLES
------------------------------
В Vercel -> Project -> Settings -> Environment Variables добавьте:

BOT_TOKEN
    Новый токен Telegram-бота.

WEBHOOK_SECRET
    Случайный секрет. Можно создать в Windows CMD:
    python -c "import secrets; print(secrets.token_urlsafe(32))"

MINI_APP_URL
    HTTPS-адрес вашего легитимного Mini App.
    Если пока не готов — можно временно:
    https://example.com

После изменения Environment Variables обязательно сделайте Redeploy.

ШАГ 4 — ПРОВЕРИТЬ VERCEL
-------------------------
После Deploy Vercel даст адрес вроде:

https://my-telegram-bot.vercel.app

Откройте его в браузере.

Если видите:
{"status":"ok","service":"telegram-webhook"}

значит Python-приложение работает.

Также картинка должна открываться:
https://my-telegram-bot.vercel.app/banner.png

ШАГ 5 — ПРИВЯЗАТЬ TELEGRAM WEBHOOK
-----------------------------------
На своем ПК откройте CMD в этой папке и выполните:

python setup_webhook.py

Скрипт спросит:
- BOT_TOKEN (ввод скрыт)
- WEBHOOK_SECRET (тот же, что в Vercel; ввод скрыт)
- Vercel production URL

В конце Telegram должен ответить примерно:

{
  "ok": true,
  "result": true,
  "description": "Webhook was set"
}

ШАГ 6 — ПРОВЕРИТЬ
-----------------
Откройте бота в Telegram и отправьте:

/start

Должны прийти:
- баннер
- приветственный текст
- кнопки

ВАЖНО ПРО ЛОКАЛЬНЫЙ bot.py
---------------------------
После установки webhook НЕ запускайте старую версию с:

dp.start_polling(...)

одновременно с webhook-версией.

Telegram не использует getUpdates/polling, пока установлен webhook.

ЕСЛИ НУЖНО ВЕРНУТЬ POLLING
---------------------------
Удалите webhook через Telegram Bot API методом deleteWebhook,
а затем снова запускайте локальную polling-версию.

ОШИБКИ
------
Если /start молчит:

1. Vercel -> Project -> Logs.
2. Убедитесь, что BOT_TOKEN задан в Production.
3. Убедитесь, что после изменения ENV был Redeploy.
4. Проверьте, что WEBHOOK_SECRET в Vercel и setup_webhook.py совпадает.
5. Убедитесь, что Production URL начинается с https://.
