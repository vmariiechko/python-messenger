from os import path

from bcrypt import hashpw, checkpw, gensalt
from cryptography.fernet import Fernet


def codec(password, flag):
    if not path.exists('../key'):
        key = generate_key()
    else:
        with open('../key', 'rb') as file:
            key = file.read()

    cipher_suite = Fernet(key)

    if flag:
        encrypted_hash = cipher_suite.encrypt(hash_password(password))
        return encrypted_hash
    else:
        decrypted_hash = cipher_suite.decrypt(password)
        return decrypted_hash


def generate_key():
    key = Fernet.generate_key()

    with open('../key', 'wb') as file:
        file.write(key)

    return key


def hash_password(password):
    password_hash = hashpw(password.encode(), gensalt())
    return password_hash


def check_password(password, hashed):
    return checkpw(password, hashed)
