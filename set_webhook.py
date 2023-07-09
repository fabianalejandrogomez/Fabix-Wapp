

import requests

TOKEN = "6346479954:AAFboa-ZDY6Hkg6kSmrlyd_R9xNKwLrtXXA"
WEBHOOK_URL = "https://3.16.31.246/webhook"

response = requests.post(f"https://api.telegram.org/bot{TOKEN}/setWebhook", data={"url": WEBHOOK_URL})

print(response.json())
