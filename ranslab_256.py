import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def derive_key(passphrase: str, salt: bytes) -> bytes:
    """
    EDUKASI: Mengubah Kata Sandi dari otak user menjadi Kunci Matematika AES 256-bit.
    Menggunakan PBKDF2 dengan 100.000 kali putaran (hashing) biar kebal dari brute-force.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,          # 32 Bytes = 256 Bits
        salt=salt,          # Garam biner acak pengamannya
        iterations=100_000, # Dimasak 100 ribu kali biar hacker pusing
    )
    return kdf.derive(passphrase.encode('utf-8'))

def encrypt_file_bytes(file_bytes: bytes, passphrase: str) -> bytes:
    """Mengunci file biner (foto/video/PDF) menggunakan Passphrase User."""
    salt = os.urandom(16)   # 16 byte Salt acak
    key = derive_key(passphrase, salt)
    
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 12 byte Nonce acak
    ciphertext = aesgcm.encrypt(nonce, file_bytes, None)
    
    # Bungkus jadi satu paket: SALT (16 Byte) + NONCE (12 Byte) + CIPHERTEXT
    return salt + nonce + ciphertext

def decrypt_file_bytes(encrypted_payload: bytes, passphrase: str) -> bytes:
    """Membuka kembali file biner menggunakan Passphrase User yang sama."""
    salt = encrypted_payload[:16]             # Potong 16 byte pertama
    nonce = encrypted_payload[16:28]          # Potong 12 byte berikutnya
    ciphertext = encrypted_payload[28:]       # Sisanya adalah isi file terenkripsi
    
    key = derive_key(passphrase, salt)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)

# TES MESIN FILE BINARY
if __name__ == "__main__":
    sandi_user = "BumiKeMars2026!"
    
    # Simulasi data foto/video dalam bentuk bytes biner
    simulasi_foto_biner = b"\xFF\xD8\xFF\xE0\x00\x10JFIF" + b"ISI_FOTO_RAHASIA_RANSLAB"
    
    print("--- TES ENKRIPSI FILE BINARY RANSLAB-256 ---")
    payload_terkunci = encrypt_file_bytes(simulasi_foto_biner, sandi_user)
    print(f"File Terkunci : {len(payload_terkunci)} Bytes (Format Biner Terproteksi)")
    
    # Dekripsi kembali
    foto_terbuka = decrypt_file_bytes(payload_terkunci, sandi_user)
    print(f"File Terbuka  : {foto_terbuka}")
    
    if foto_terbuka == simulasi_foto_biner:
        print("STATUS : SUCCESS 100%! Data File Asli Kembali Tanpa Cacat.")