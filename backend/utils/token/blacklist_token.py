blacklisted_tokens = set()

def blacklist_token(jti: str):
    blacklisted_tokens.add(jti)

def is_blacklisted(jti: str) -> bool:
    return jti in blacklisted_tokens
