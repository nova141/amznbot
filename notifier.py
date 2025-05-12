import requests

def notify_discord(message, webhook_url):
    try:
        requests.post(webhook_url, json={"content": message})
    except Exception as e:
        print(f"Notification failed: {e}")