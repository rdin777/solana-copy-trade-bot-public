import asyncio
from aiogram import Bot
from solana.rpc.websocket_api import connect
from solders.pubkey import Pubkey

# --- SETTINGS ---
TELEGRAM_TOKEN =
CHAT_ID =
MIN_TRADE_SOL = 2.0
# -----------------

bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram_alert(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"[!] Error sending to Telegram: {e}")

async def monitor_wallet(wallet_address: str):
    pubkey = Pubkey.from_string(wallet_address)
    last_balance = 0
    print(f"[*] Monitor for {wallet_address[:6]} started.")

    while True:
        try:
            async with connect("wss://api.mainnet-beta.solana.com") as websocket:
                await websocket.account_subscribe(pubkey)
                while True:
                    data = await asyncio.wait_for(websocket.recv(), timeout=25.0)
                    new_balance = data[0].result.value.lamports

                    if last_balance != 0:
                        diff = abs(new_balance - last_balance) / 1_000_000_000
                        if diff >= MIN_TRADE_SOL:
                            msg = f"🚀 **Large Transaction!**\nWallet: {wallet_address[:8]}...\nAmount: {diff:.4f} SOL"
                            print(msg)
                            await send_telegram_alert(msg)

                    last_balance = new_balance
        except Exception:
            await asyncio.sleep(5)

async def main():
    wallets = ["5TyX6vmGcpTpuSH2pUmVc6YpGfZk2koSLU4Eb5c9thsS",
    "esx81H8KpkeJnjXG6od126Lowb4gqueDqjReHP3iEUW",
    "3YZF5wT1BHKuJDWp1znjPm1RyaUdkMsQ54UTxjUfsHzE",
    "CtcwbGhxAY5o7XmyWUC6TtMoY8gxiJGbSMaQ5ErhNLtY",
    "FK6WwRi2D5Wq6YVq8DkDSjd4MbLNmxiGkk9PGu6zrZFL",
    "8beVKgs4pdShYC5GAXY3r2oPiip9C2kxDkPt1vi1Z3Yk",
    "4UizhXhL7AgM13p5He1M8f7A9zJhCoRc5eFBkGWjfrjM",
    "BQXBTyWY3aLG9nKXKxRWYhGtRG6RQrk77YBzvjLKb7pa",
    "LNNRQiajaCV93kY6FFKNm3nQk9N13zMJcYshuEjhePr",
    "3sdf2D8HqYBknZXnozdAr3GVJCewh2oSdK91iZwXxgxU"] # Your list of addresses
    tasks = [monitor_wallet(w) for w in wallets]
    await asyncio.gather(*tasks)

# --- Add this function before the call. ---
async def send_test_message():
    print("[*] Sending a test message to Telegram...")
    await bot.send_message(chat_id=CHAT_ID, text="🚀 The bot has started!")
    print("[+] Message sent!")

if __name__ == "__main__":
    try:
        # To test, uncomment the line below and comment out `main()`:
#        asyncio.run(send_test_message())

        # Once you've checked it, change it back to this:
         asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")

