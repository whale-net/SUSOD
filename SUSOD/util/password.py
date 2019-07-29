"""Password functions."""
import uuid
import hashlib


def password_db_string_create(password):
    """Generate password string for new account."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    return generate_hash(algorithm, salt, password)


def password_db_string_verify(password, password_db_string):
    """Verify password matches with database."""
    split_pasword_db = password_db_string.split('$')
    algorithm = split_pasword_db[0]
    salt = split_pasword_db[1]
    return password_db_string == generate_hash(algorithm, salt, password)


def generate_hash(algorithm, salt, password):
    """Generate the hash from the algorithm, salt and password."""
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string
