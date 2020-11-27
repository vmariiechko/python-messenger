from os import path

from bcrypt import hashpw, checkpw, gensalt
from cryptography.fernet import Fernet


def codec(password, flag):
    """
    Encrypts and decrypts hashed password.

    Generates key using :func:`generate_key` if doesn't exist.
    Hashes password using :func:'hash_password'.
    Depending on the flag, encrypts or decrypts hashed password.

    :param password: string for processing
    :param flag: switch, 1 - encrypts, 0 - decrypts
    :return: encrypted / decrypted byte string
    """

    if not path.exists('../../key.txt'):
        key = generate_key()
    else:
        with open('../../key.txt', 'rb') as file:
            key = file.read()

    cipher_suite = Fernet(key)

    if flag:
        encrypted_hash = cipher_suite.encrypt(hash_password(password))
        return encrypted_hash
    else:
        decrypted_hash = cipher_suite.decrypt(password)
        return decrypted_hash


def generate_key():
    """
    Generates and writes key to the file in the parent directory.

    :return: key byte string
    """

    key = Fernet.generate_key()

    with open('../../key.txt', 'wb') as file:
        file.write(key)

    return key


def hash_password(password):
    """
    Hashes specified string of password.

    :param password: string to hash
    :return: byte string of hashed password
    """

    password_hash = hashpw(password.encode(), gensalt())
    return password_hash


def check_password(password, hashed):
    """
    Verifies if password conforms to hash.

    :param password: string in bytes
    :param hashed: hashed byte string
    :return: bool, ``True`` if password and hash matches, ``False`` otherwise
    """

    return checkpw(password, hashed)
