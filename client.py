# GNU GPLv3-or-later
# Lorenzo Mari - 2022

import requests, crypto, json

# for tor connection

def refresh_proxy(tor_port="9050"):
	global proxies
	proxies = {
	    'http': 'socks5h://127.0.0.1:'+tor_port,
	    'https': 'socks5h://127.0.0.1:'+tor_port
	}


# get key
def get_key(peer):
	return crypto.load(requests.get(peer+'/get_key', proxies=proxies).text)


def send_message(user, message, peer, public_key):

	msg = crypto.encrypt(json.dumps({
		"author": user,
		"content": message
	}), public_key)

	return requests.get(peer+'/send?msg='+msg.hex(), proxies=proxies).text


if __name__ == '__main__':
	refresh_proxy()

	PEER = "http://" + input("peer reciever address (abc.onion): ")

	user = input("username:")

	key = get_key(PEER)

	while 1:
		send_message(user, input("message: "), PEER, key)
