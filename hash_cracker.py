import hashlib
from tqdm import tqdm

# Function to brute-force hash passwords
def crack_hash(hash_value, hash_type, wordlist, update_gui):
    for word in tqdm(wordlist, desc="Trying passwords", unit="attempts"):
        word = word.strip()
        update_gui(f"Trying: {word}")

        if hash_type == "MD5":
            hashed_attempt = hashlib.md5(word.encode()).hexdigest()
        elif hash_type == "SHA256":
            hashed_attempt = hashlib.sha256(word.encode()).hexdigest()
        else:
            return "✘ Unsupported hash type."

        if hashed_attempt == hash_value:
            return f"✔ Hash cracked: {word}"

    return "✘ Hash not found in wordlist."
