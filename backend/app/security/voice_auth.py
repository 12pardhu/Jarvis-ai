import hashlib

# ⚠️ First time: run once and copy hash
def generate_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

# Replace this with your generated hash
AUTHORIZED_HASH = "REPLACE_WITH_YOUR_HASH"

def verify_voice(command):
    return generate_hash(command) == AUTHORIZED_HASH