import zipfile
import time
import threading
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Function to brute-force a simulated password
def brute_force_simulated(target_password, wordlist, update_gui):
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        for word in tqdm(wordlist, desc="Trying passwords", unit="attempts"):
            word = word.strip()
            update_gui(f"Trying: {word}")

            future = executor.submit(check_password, target_password, word)
            if future.result():
                end_time = time.time()
                return f"✔ Password cracked: {word} (Time: {end_time - start_time:.2f}s)"
    
    return "✘ Password not found in wordlist."

# Function to check password (used in multithreading)
def check_password(target, attempt):
    return target == attempt

# Function to brute-force a ZIP file
def brute_force_zip(zip_file, wordlist, update_gui):
    with zipfile.ZipFile(zip_file, 'r') as zf:
        for word in tqdm(wordlist, desc="Trying passwords", unit="attempts"):
            password = word.strip().encode('utf-8')
            update_gui(f"Trying: {word}")
            
            try:
                zf.extractall(pwd=password)
                return f"✔ Password cracked: {word}"
            except:
                continue

    return "✘ Password not found in wordlist."
