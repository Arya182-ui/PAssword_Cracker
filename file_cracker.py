import rarfile
import pikepdf
import zipfile
import time
from tqdm import tqdm

# Brute-force attack on ZIP files
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

# Brute-force attack on RAR files
def brute_force_rar(rar_file, wordlist, update_gui):
    with rarfile.RarFile(rar_file) as rf:
        for word in tqdm(wordlist, desc="Trying passwords", unit="attempts"):
            password = word.strip()
            update_gui(f"Trying: {word}")

            try:
                rf.extractall(pwd=password)
                return f"✔ Password cracked: {word}"
            except:
                continue

    return "✘ Password not found in wordlist."

# Brute-force attack on PDF files
def brute_force_pdf(pdf_file, wordlist, update_gui):
    for word in tqdm(wordlist, desc="Trying passwords", unit="attempts"):
        password = word.strip()
        update_gui(f"Trying: {word}")

        try:
            pdf = pikepdf.open(pdf_file, password=password)
            return f"✔ Password cracked: {word}"
        except:
            continue

    return "✘ Password not found in wordlist."
