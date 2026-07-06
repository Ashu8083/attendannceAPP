import hashlib


def token_hashed( token : str) -> str:
    return hashlib.sha256( token.encode() ).hexdigest()
