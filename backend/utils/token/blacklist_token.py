blacklisted_tokens = set()

def add_token_to_blacklist(jti: str):
    blacklisted_tokens.add(jti)

def is_blacklisted(jti: str) -> bool:
    return jti in blacklisted_tokens
