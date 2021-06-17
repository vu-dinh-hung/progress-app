"""Utils for hashing and comparing passwords"""
import bcrypt


def hash_password(password):
    """Return a secure hash for the given password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(14))


def check_password(password, password_hash):
    """Compare the given password with the user's password_hash"""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
