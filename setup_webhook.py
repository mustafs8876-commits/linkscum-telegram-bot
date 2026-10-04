import getpass
import json
import urllib.parse
import urllib.request


def ask_hidden(label: str) -> str:
    value = getpass.getpass(label).strip()
    if not value:
        raise SystemExit(f"{label.strip(': ')} is required")
    return value


print("Telegram webhook setup")
print("----------------------")
token = ask_hidden("BOT_TOKEN: ")
secret = ask_hidden("WEBHOOK_SECRET: ")
base_url = input("Vercel production URL (example: https://my-bot.vercel.app): ").strip().rstrip("/")

if not base_url.startswith("https://"):
    raise SystemExit("Vercel URL must start with https://")

webhook_url = f"{base_url}/webhook"

data = urllib.parse.urlencode(
    {
        "url": webhook_url,
        "secret_token": secret,
        "drop_pending_updates": "true",
        "allowed_updates": json.dumps(["message", "callback_query"]),
    }
).encode("utf-8")

request = urllib.request.Request(
    f"https://api.telegram.org/bot{token}/setWebhook",
    data=data,
    method="POST",
)

with urllib.request.urlopen(request, timeout=30) as response:
    result = json.loads(response.read().decode("utf-8"))

print(json.dumps(result, ensure_ascii=False, indent=2))
print(f"\nWebhook URL: {webhook_url}")
