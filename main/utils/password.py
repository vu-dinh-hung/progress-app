"""Utils for hashing and comparing passwords"""
import bcrypt

# This is the cost factor needed to calculate a hash. It is set to the minimum factor I benchmarked
# to be needed for bcrypt to take around 1s to hash a password on a 2015 MacBook Pro
SALT_ROUNDS = 14


def hash_password(password):
    """Return a secure hash for the given password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(SALT_ROUNDS))


def check_password(password, password_hash):
    """Compare the given password with the user's password_hash"""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
