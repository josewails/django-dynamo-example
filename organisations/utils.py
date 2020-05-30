import secrets


def generate_model_id():
    return str(secrets.token_hex(16))
