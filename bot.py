import os
from flask import Flask, request
from pywa import WhatsApp, types, filters
from dotenv import load_dotenv

load_dotenv()

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
APP_ID = os.getenv("WHATSAPP_APP_ID")
APP_SECRET = os.getenv("WHATSAPP_APP_SECRET")
CALLBACK_URL = os.getenv("WHATSAPP_CALLBACK_URL")
PORT = os.getenv("PORT")
DEBUG = os.getenv("DEBUG") == "TRUE"

app = Flask(__name__)

wa = WhatsApp(
    phone_id=PHONE_ID,      
    token=TOKEN,     
    server=app,                                    
    verify_token=VERIFY_TOKEN, 
    callback_url=CALLBACK_URL,
    app_secret=APP_SECRET,
    app_id=APP_ID
)

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Forbidden", 403

@wa.on_message() 
def echo_message(client: WhatsApp, msg: types.Message):
    msg.reply(
        text="Hello! How old are you?",
        buttons=[types.Button("😅", callback_data="cancel")]
    )
    age = client.listen(
        to=msg.sender,
        filters=filters.message & filters.text,
        timeout=20, # 20s
        cancelers=filters.callback_button & filters.matches("cancel")
    )
    age.react('👍')
    msg.reply(f"Your age is {age.text}.")
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)  