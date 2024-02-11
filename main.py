import ssl
import websocket
from websocket import WebSocketApp
import orjson
import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "redispw")

redis_client = redis.Redis(REDIS_HOST, REDIS_PORT, password=REDIS_PASSWORD)


def on_message(ws: WebSocketApp, message: str) -> None:
    json_message = orjson.loads(message)
    for event in json_message.get("events", []):
        redis_client.hset(f"GEMINI_BTCUSD_{event['side']}", event["price"], event["remaining"])


def on_error(ws: WebSocketApp, message: str) -> None:
    print(message)

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "wss://api.gemini.com/v1/marketdata/btcusd?bids=true&offers=true",
        on_message=on_message, on_error=on_error)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
