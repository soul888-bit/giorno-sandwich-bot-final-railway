from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
import os
from bot import send_alert, watched_tokens, user_settings

api = FastAPI()

@api.post("/webhook")
async def webhook_listener(request: Request):
    body = await request.json()
    print("📥 Webhook reçu :", json.dumps(body, indent=2))
    for event in body:
        if event.get("type") == "SWAP":
            token = event.get("token", {}).get("mint")
            amount = float(event.get("nativeInputAmount", 0)) / 1e9
            if token in watched_tokens and watched_tokens[token]["active"]:
                if amount >= user_settings["min_swap"]:
                    await send_alert(f"🔍 Swap détecté sur {token}\nMontant : {amount:.2f} SOL")
    return JSONResponse(content={"status": "ok"})

app = api