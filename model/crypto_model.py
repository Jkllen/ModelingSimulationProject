import hashlib
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).digest()


def encrypt_report(report_text: str, password: str, filename: str = "report.enc") -> str:
    if not report_text:
        raise ValueError("Report text cannot be empty.")

    if not password:
        raise ValueError("Password cannot be empty.")

    key = derive_key(password)
    aesgcm = AESGCM(key)
    
    # the system generates a random nonce
    nonce = os.urandom(12)
    
    # the report is then encrypted using AES-GCM
    ciphertext = aesgcm.encrypt(nonce, report_text.encode("utf-8"), None)

    # the encrypted data is saved into a file together with the nonce.
    with open(filename, "wb") as file:
        file.write(nonce + ciphertext)

    return filename


def decrypt_report(password: str, filename: str = "report.enc") -> str | None:
    if not password:
        return None

    try:
        with open(filename, "rb") as file:
            data = file.read()

        if len(data) < 13:
            return None

        key = derive_key(password)
        aesgcm = AESGCM(key)

        # the system reads the file and separates the nonce and ciphertext.
        nonce = data[:12]
        ciphertext = data[12:]
        
        # if the correct password is used, the original report is recovered.
        decrypted = aesgcm.decrypt(nonce, ciphertext, None)

        return decrypted.decode("utf-8")

    except Exception:
        return None