# GNU GPLv3-or-later
# Lorenzo Mari - 2022

from flask import Flask, request
from flask_tor import run_with_tor

from threading import Thread
import crypto, json, logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

STOP_SIGNAL = "!!STOPCONNECTION!!"
DEBUG = 1

messages = []

public_key, private_key = crypto.generate_keys()
#print(public_key.save_pkcs1('PEM'))#dir(public_key))
#exit()

app = Flask(__name__)
port = run_with_tor()

@app.route("/")
def home():

    return "usage:\n address/send?msg=encrypted_json - send message of the form {\"author\": \"me\", \"content\": \"Hello, world!\"}\n address/get_key - get public key"


@app.route("/send")
def send():
    try:
        raw = crypto.decrypt(bytes.fromhex(request.args["msg"]), private_key)
    except:
        if DEBUG: print("unable to decrypt message")

    msg = json.loads(raw)

    if "content" in msg:
        messages.append(msg)

    return "message recieved"




@app.route("/get_key")
def get_key():

    return public_key.save_pkcs1('PEM')



def shutdown():
    print("Connection closed, listening node terminated.")
    print("Since I'm a bad programmer, spam CTRL+C to close client, ignore errors")
    exit()




def print_messages():
    old = []
    while 1:

        if STOP_SIGNAL in [i["content"] for i in messages]:
            shutdown()


        if messages != old:
            print('\n'.join([f"{i.get('author', 'anon')}: {i['content']}" for i in messages if i not in old]))
            old = messages[:]


def run():
    print("running on port", port)

    Thread(target=print_messages).start()
    app.run(port=port)



if __name__ == '__main__':
    run()
