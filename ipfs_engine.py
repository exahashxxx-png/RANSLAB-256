import requests
import streamlit as st

# Mengambil JWT dari .streamlit/secrets.toml secara otomatis
PINATA_JWT = st.secrets["PINATA_JWT"]

def push_to_ipfs(file_bytes: bytes, filename: str) -> str:
    """
    Mengirimkan payload biner terenkripsi (.ranslab) ke jaringan P2P IPFS via Pinata.
    """
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    
    headers = {
        "Authorization": f"Bearer {PINATA_JWT}"
    }
    
    files = {
        'file': (filename, file_bytes)
    }
    
    response = requests.post(url, files=files, headers=headers)
    
    if response.status_code == 200:
        return response.json()["IpfsHash"]
    else:
        raise Exception(f"Gagal Push ke IPFS ({response.status_code}): {response.text}")

def fetch_from_ipfs(cid: str) -> bytes:
    """
    Narik data ciphertext (.ranslab) langsung dari IPFS Gateway.
    """
    gateway_url = f"https://gateway.pinata.cloud/ipfs/{cid}"
    response = requests.get(gateway_url)
    
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Gagal mengambil data dari IPFS Gateway ({response.status_code}).")