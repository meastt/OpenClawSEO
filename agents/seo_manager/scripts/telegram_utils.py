#!/usr/bin/env python3
"""
Shared Telegram alerting utility.
All SEO scripts import send_telegram_alert from here — single source of truth.
"""
import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def send_telegram_alert(message):
    """Send failure alert to Michael via Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️  TELEGRAM NOT CONFIGURED — cannot send alert!")
        print(f"ALERT: {message}")
        return
    try:
        requests.post(
            f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
            json={
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message,
                'parse_mode': 'Markdown'
            },
            timeout=10
        )
    except Exception as e:
        print(f"⚠️  Failed to send Telegram alert: {e}")
