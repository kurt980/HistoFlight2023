import hashlib
def sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()