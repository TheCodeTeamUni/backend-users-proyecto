import hashlib
import re


def encrypt(salt, user_pass):
    hash = hashlib.sha256()
    hash.update(('%s%s' % (salt, user_pass)).encode('utf-8'))
    password_encrypt = hash.hexdigest()

    return password_encrypt


def validate_password(password):
    if 8 <= len(password) <= 24:
        if re.search('[a-z]', password) and re.search('[A-Z]', password):
            if re.search('[0-9]', password):
                return True
    return False
