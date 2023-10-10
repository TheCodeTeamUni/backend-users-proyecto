import hashlib


def encrypt(salt, user_pass):
    hash = hashlib.sha256()
    hash.update(('%s%s' % (salt, user_pass)).encode('utf-8'))
    password_encrypt = hash.hexdigest()

    return password_encrypt