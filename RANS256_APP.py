import base64
import streamlit as st
from ipfs_engine import fetch_from_ipfs, push_to_ipfs
from ranslab_256 import decrypt_file_bytes, encrypt_file_bytes

# 1. STREAMLIT PAGE CONFIG (MODE CENTERED)
st.set_page_config(
    page_title="RANSLAB-256 Vault",
    page_icon="shield_logo.png",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# 2. HELPER BASE64 FOR IMAGES & BACKGROUND
def get_base64_file(file_path):
  try:
    with open(file_path, "rb") as f:
      return base64.b64encode(f.read()).decode()
  except Exception:
    return ""


# 3. CUSTOM CYBERPUNK CSS & WALLPAPER
bg_b64 = get_base64_file("bg_cyber.png")
bg_style = ""
if bg_b64:
  bg_style = f"""
    .stApp {{
        background-image: linear-gradient(rgba(3, 7, 18, 0.70), rgba(3, 7, 18, 0.70)), url("data:image/png;base64,{bg_b64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    """

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Share+Tech+Mono&display=swap');

{bg_style}

/* HAPUS JIDAT KOSONG (PAD PADDING ATAS & MUTE STREAMLIT HEADER) */
header[data-testid="stHeader"] {{
    background: transparent !important;
}}

.main .block-container {{
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    max-width: 800px !important;
}}

/* TEKS LABEL INPUT CYAN NEON MENYALA */
label, .stWidgetLabel, label p {{
    color: #00e5ff !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.95rem !important;
    font-weight: bold !important;
    letter-spacing: 1.5px !important;
    text-shadow: 0 0 8px rgba(0, 229, 255, 0.5) !important;
}}

h1, h2, h3, h4, .stCaption {{
    font-family: 'Orbitron', sans-serif !important;
}}

p, input, button, .stButton>button {{
    font-family: 'Share Tech Mono', monospace !important;
}}

/* HEADER TITLE & SUBTITLE */
.cyber-header {{
    text-align: center;
    padding: 0px 0 15px 0;
}}

.cyber-title {{
    font-family: 'Orbitron', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: 2px;
    color: #ffffff;
    text-shadow: 0 0 20px rgba(0, 229, 255, 0.8);
}}

.cyber-subtitle {{
    color: #00e5ff;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.9rem;
    letter-spacing: 3px;
    margin-top: 2px;
}}

/* TAB STYLE */
.stTabs [data-baseweb="tab-list"] {{
    gap: 12px;
    justify-content: center;
}}

.stTabs [data-baseweb="tab"] {{
    height: 48px;
    white-space: pre-wrap;
    background-color: rgba(15, 23, 42, 0.85);
    border-radius: 8px 8px 0px 0px;
    color: #94a3b8;
    font-family: 'Orbitron', sans-serif;
    font-size: 0.88rem;
    border: 1px solid rgba(0, 229, 255, 0.3);
}}

.stTabs [aria-selected="true"] {{
    background-color: rgba(0, 229, 255, 0.2) !important;
    color: #00e5ff !important;
    border-bottom: 2px solid #00e5ff !important;
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.4);
}}

/* COPY CODE BOX STYLING */
div[data-testid="stCodeBlock"] {{
    border: 1px solid #00e5ff !important;
    border-radius: 6px !important;
    box-shadow: 0 0 10px rgba(0, 229, 255, 0.3) !important;
}}
</style>
""",
    unsafe_allow_html=True,
)

# 4. HEADER WITH 3D METALLIC SHIELD LOGO
shield_b64 = get_base64_file("shield_logo.png")
if shield_b64:
  logo_html = f'<img src="data:image/png;base64,{shield_b64}" style="height: 52px; vertical-align: middle; margin: 0 8px; transform: translateY(-4px); filter: drop-shadow(0 0 10px #00e5ff);">'
else:
  logo_html = "🔰"

st.markdown(
    f"""
<div class="cyber-header">
    <div class="cyber-title">RANS{logo_html}LAB-256</div>
    <div class="cyber-subtitle">// QUANTUM-RESISTANT ZERO-KNOWLEDGE IPFS VAULT</div>
</div>
""",
    unsafe_allow_html=True,
)

# 5. MAIN VAULT TABS
tab_enc, tab_dec = st.tabs([
    "🔒 ENCRYPT & PUSH TO IPFS",
    "🔓 FETCH FROM IPFS & DECRYPT",
])

# --- TAB 1: ENCRYPT & PUSH ---
with tab_enc:
  st.write("")
  uploaded_file = st.file_uploader(
      "SELECT TARGET FILE (ANY BINARY FORMAT)", key="file_enc"
  )
  passphrase_enc = st.text_input(
      "PASSPHRASE MASTER KEY (MEMORIZED ONLY):",
      type="password",
      key="pass_enc",
  )

  st.write("")
  if st.button("EXECUTE ENCRYPTION & PUSH TO IPFS 🚀", key="btn_enc"):
    if uploaded_file and passphrase_enc:
      with st.spinner("Locking file & Pushing payload to IPFS..."):
        try:
          file_bytes = uploaded_file.read()
          encrypted_payload = encrypt_file_bytes(file_bytes, passphrase_enc)
          filename_ranslab = f"{uploaded_file.name}.ranslab"

          cid = push_to_ipfs(encrypted_payload, filename_ranslab)

          if cid:
            st.success("✅ VAULT LOCK SUCCESSFUL!")
            st.write("📋 **YOUR IPFS CID (CLICK ICON TO COPY):**")
            st.code(cid, language="text")

            st.info(
                "Keep this CID and your Master Passphrase safe. Without both,"
                " data recovery is mathematically impossible."
            )
          else:
            st.error("❌ IPFS Gateway Timeout or Pinata Secret Invalid.")
        except Exception as e:
          st.error(f"❌ Encryption Error: {str(e)}")
    else:
      st.warning("⚠️ Please provide both target file and passphrase.")

# --- TAB 2: FETCH & DECRYPT ---
with tab_dec:
  st.write("")
  cid_input = st.text_input(
      "TARGET IPFS CID (HASH):", placeholder="Qm... or bafy...", key="cid_dec"
  )
  passphrase_dec = st.text_input(
      "PASSPHRASE MASTER KEY:", type="password", key="pass_dec"
  )

  st.write("")
  if st.button("FETCH FROM IPFS & DECRYPT 🔓", key="btn_dec"):
    if cid_input and passphrase_dec:
      with st.spinner("Fetching payload from IPFS & Decrypting..."):
        try:
          encrypted_data = fetch_from_ipfs(cid_input)
          if encrypted_data:
            # Sesuai fungsi asli ranslab_256: return is_success, decrypted_bytes, original_filename
            is_success, decrypted_bytes, orig_filename = decrypt_file_bytes(
                encrypted_data, passphrase_dec
            )

            if is_success and decrypted_bytes:
              st.success("✅ DECRYPTION & INTEGRITY VERIFIED!")
              file_label = (
                  str(orig_filename).upper()
                  if orig_filename
                  else "DECRYPTED_FILE"
              )
              file_name_download = (
                  str(orig_filename) if orig_filename else "decrypted_file.bin"
              )

              st.download_button(
                  label=f"💾 DOWNLOAD {file_label}",
                  data=decrypted_bytes,
                  file_name=file_name_download,
                  mime="application/octet-stream",
              )
            else:
              st.error(
                  "❌ Decryption Failed! Invalid Passphrase or Corrupted"
                  " Payload."
              )
          else:
            st.error("❌ Failed to fetch payload from IPFS. Check CID.")
        except Exception as e:
          st.error(f"❌ Error: {str(e)}")
    else:
      st.warning("⚠️ Please provide both CID and Master Passphrase.")