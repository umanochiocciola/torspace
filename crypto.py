# GNU GPLv3-or-later
# Lorenzo Mari - 2022

import rsa

def generate_keys():
	
    return rsa.newkeys(1024) # public, private


def encrypt(msg, key):
    return rsa.encrypt(msg.encode('utf-8'), key)


def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('utf-8')
    except:
        return False


def load(stuff):
	return rsa.PublicKey.load_pkcs1(stuff)



if __name__ == '__main__':
	public, private = generate_keys()
	print(decrypt(encrypt("Hello, World!", public), private))