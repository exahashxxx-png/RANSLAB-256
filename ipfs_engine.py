import requests
import streamlit as st

# Mengambil JWT dari .streamlit/secrets.toml secara otomatis
PINATA_JWT = st.secrets["PINATA_JWT"]


def push_to_ipfs(file_bytes: bytes, filename: str) -> str:
  """Mengirimkan payload biner terenkripsi (.ranslab) ke jaringan P2P IPFS via Pinata."""
  url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

  headers = {"Authorization": f"Bearer {PINATA_JWT}"}

  files = {"file": (filename, file_bytes)}

  response = requests.post(url, files=files, headers=headers)

  if response.status_code == 200:
    return response.json()["IpfsHash"]
  else:
    raise Exception(
        f"Gagal Push ke IPFS ({response.status_code}): {response.text}"
    )


def fetch_from_ipfs(cid: str) -> bytes:
  """Narik data ciphertext (.ranslab) dengan MULTI-GATEWAY FALLBACK.

  Jika 1 gateway gagal/timeout, otomatis coba gateway publik lainnya.
  """
  gateways = [
      f"https://gateway.pinata.cloud/ipfs/{cid}",
      f"https://cloudflare-ipfs.com/ipfs/{cid}",
      f"https://ipfs.io/ipfs/{cid}",
      f"https://dweb.link/ipfs/{cid}",
  ]

  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      )
  }

  for gw_url in gateways:
    try:
      response = requests.get(gw_url, headers=headers, timeout=12)
      # Pastikan yang diterima beneran data biner file, bukan response HTML error
      if response.status_code == 200 and not response.headers.get(
          "Content-Type", ""
      ).startswith("text/html"):
        return response.content
    except Exception:
      continue

  raise Exception(
      "Gagal mengambil payload dari seluruh IPFS Gateways (Network Timeout /"
      " Invalid CID)."
  )