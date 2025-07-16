from flask import Flask, request
import discord
import asyncio
import secrets

app = Flask(__name__)
loop = asyncio.get_event_loop()
discord_client = None  # We will set this externally

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    from_number = request.form.get("From")
    body = request.form.get("Body")
    print(f"📥 Incoming WhatsApp: {body} from {from_number}")

    if body.startswith("@"):
        parts = body[1:].split(" ", 1)
        if len(parts) == 2:
            channel_name, content = parts
            channel = discord.utils.get(discord_client.get_all_channels(), name=channel_name)
            if channel:
                loop.create_task(channel.send(f"[From WhatsApp] {content}"))
                return "✅ Message delivered", 200
            else:
                print(f"❌ Channel {channel_name} not found")
    return "⚠️ Invalid command", 200
