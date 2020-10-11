from os import path

from bcrypt import hashpw, checkpw, gensalt
from cryptography.fernet import Fernet


def codec(password, flag):
    if not path.exists('../key'):
        key = generateKey()
    else:
        with open('../key', 'rb') as file:
            key = file.read()

    cipher_suite = Fernet(key)

    if flag:
        encrypted_hash = cipher_suite.encrypt(hashPassword(password))
        return encrypted_hash
    else:
        decrypted_hash = cipher_suite.decrypt(password)
        return decrypted_hash


def generateKey():
    key = Fernet.generate_key()

    with open('../key', 'wb') as file:
        file.write(key)

    return key


def hashPassword(password):
    password_hash = hashpw(password.encode(), gensalt())
    return password_hash


def checkPassword(password, hashed):
    return checkpw(password, hashed)
