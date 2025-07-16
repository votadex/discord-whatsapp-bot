from flask import Flask, request
import discord
import asyncio
import secrets

app = Flask(__name__)
discord_client = None  # This will be set from bot.py

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    global discord_client

    body = request.form.get("Body", "").strip()
    sender = request.form.get("From")

    print(f"📥 Incoming WhatsApp from {sender}: {body}")

    if body.startswith("@"):
        try:
            channel_name, content = body[1:].split(" ", 1)
        except ValueError:
            print("❌ Invalid format. Use @channelname your message")
            return "Invalid format", 200

        # Try to find the Discord channel by name
        channel = discord.utils.get(discord_client.get_all_channels(), name=channel_name)
        if channel:
            # Post to Discord channel
            discord_client.loop.create_task(
                channel.send(f"[From WhatsApp] {content}")
            )
            print(f"✅ Sent to #{channel_name}: {content}")
            return "✅ Message delivered", 200
        else:
            print(f"❌ Channel '{channel_name}' not found.")
            return f"Channel '{channel_name}' not found", 200

    return "⚠️ Message must start with @channel", 200
