# GNU GPLv3-or-later
# Lorenzo Mari - 2022

from os import system
from time import sleep
from sys import argv

import client

from multiprocessing import Process
import node


STOP_SIGNAL = "!!STOPCONNECTION!!"


print("starting listening node")
server = Process(target=node.run)
server.start()

client.refresh_proxy()

if "--port" in argv:
	if argv.index("--port")+1 < len(argv):
		port = argv[argv.index("--port")+1]
		client.refresh_proxy(tor_port=port)


print("\n\npaste peer address (###.onion):\n\n")
PEER = "http://"+input()#sg.popup_get_text("peer address (###.onion):")
username = input("user: ")#sg.popup_get_text("username:")

public_key = client.get_key(PEER)


print("\nConversation initialized. Press CTRL+C to quit\n\n", '='*24)
try:
	while 1:
		client.send_message(username, input(":"), PEER, public_key)
		
except KeyboardInterrupt:
	print('\n'+'='*24+"\nquitting")
	client.send_message(username, STOP_SIGNAL, PEER, public_key)
	server.terminate()
	server.join()


print("goodbye")
