from flask import Flask, request, Response
from nltk.chat.eliza import eliza_chatbot
import json
import requests
import settings


HUB_VERIFY_TOKEN = settings.HUB_VERIFY_TOKEN
PAGE_ACCESS_TOKEN = settings.PAGE_ACCESS_TOKEN

app = Flask(__name__)


@app.route("/394834jefhejfe09343843hjdhfjdffe93333h33g3h3g3")
def fb_token_verify():
    if request.args.get('hub.verify_token') == HUB_VERIFY_TOKEN:
        return Response(request.args.get('hub.challenge'))
    else:
        return Response("Error, invalid token.")


@app.route("/394834jefhejfe09343843hjdhfjdffe93333h33g3h3g3",methods=['POST'])
def fb_post():
    incoming_message = json.loads(request.data.decode('utf-8'))
    for entry in incoming_message["entry"]:
        for message in entry["messaging"]:
            # Check to make sure the received call is a message call
            # This might be delivery, optin, postback for other events
            if "message" in message:
                sender_id = message["sender"]["id"]

                message_text = message["message"]["text"]

                try:
                    eliza_chat_response = eliza_chatbot.respond(message_text)
                except Exception as e:
                    eliza_chat_response = "Sorry!!! Some error occured."
                    print(e)
                post_facebook_message(sender_id, eliza_chat_response)

    return Response()


def post_facebook_message(fbid, recevied_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)


if __name__ == "__main__":
    app.run(debug=True)
