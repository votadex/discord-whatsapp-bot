import discord
import asyncio
import secrets
from twilio.rest import Client
from threading import Thread
import webhook_server  # import the Flask app
import os

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM")
TWILIO_TO = os.getenv("TWILIO_TO")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Twilio client setup
twilio_client = Client(secrets.TWILIO_ACCOUNT_SID, secrets.TWILIO_AUTH_TOKEN)

# Start Flask server in background
def run_webhook():
    webhook_server.discord_client = client
    webhook_server.app.run(port=5000)

Thread(target=run_webhook).start()

def send_to_whatsapp(msg):
    try:
        message = twilio_client.messages.create(
            body=msg,
            from_=secrets.TWILIO_FROM,
            to=secrets.TWILIO_TO
        )
        print(f"✅ Sent to WhatsApp (SID: {message.sid})")
    except Exception as e:
        print(f"❌ Error sending to WhatsApp: {e}")

@client.event
async def on_ready():
    print(f"🤖 Bot is online as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.TextChannel):
        formatted = f"[{message.channel.name}] {message.author.name}: {message.content}"
        print(f"📤 Forwarding to WhatsApp: {formatted}")
        send_to_whatsapp(formatted)

client.run(secrets.DISCORD_BOT_TOKEN)
