import streamlit as st
from ranslab_256 import encrypt_file_bytes, decrypt_file_bytes
from ipfs_engine import push_to_ipfs, fetch_from_ipfs

# Streamlit Page Config
st.set_page_config(
    page_title="RANSLAB-256 Vault",
    page_icon="🔰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Cyberpunk CSS (Nemesis Style)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Share+Tech+Mono&display=swap');
    
    .stApp {
        background-color: #050811 !important;
        background-image: 
            linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px) !important;
        background-size: 30px 30px !important;
        color: #e2e8f0 !important;
    }
    
    h1, h2, h3, h4, .stCaption {
        font-family: 'Orbitron', sans-serif !important;
    }
    
    p, input, button {
        font-family: 'Share Tech Mono', monospace !important;
    }
    
    .cyber-header {
        text-align: center;
        padding: 20px 0 30px 0;
    }
    
    .cyber-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.8rem;
        font-weight: 900;
        letter-spacing: 5px;
        color: #ffffff;
        text-shadow: 0 0 15px rgba(0, 240, 255, 0.6), 0 0 30px rgba(0, 240, 255, 0.2);
    }
    
    .cyber-subtitle {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.8rem;
        color: #00f0ff;
        letter-spacing: 3px;
        margin-top: 5px;
    }
    
    /* Input Styling */
    label {
        color: #00f0ff !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.78rem !important;
        letter-spacing: 1px !important;
    }
    
    div[data-baseweb="input"] {
        background-color: #0b1329 !important;
        border: 1px solid #1e293b !important;
        border-radius: 6px !important;
    }
    
    div[data-baseweb="input"]:focus-within {
        border-color: #00f0ff !important;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.4) !important;
    }
    
    input {
        color: #00f0ff !important;
    }
    
    /* Button Styling */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #0b1736 0%, #082046 100%) !important;
        color: #00f0ff !important;
        border: 1px solid #00f0ff !important;
        padding: 12px 20px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: 2px !important;
        border-radius: 6px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.2) !important;
    }
    
    div.stButton > button:hover {
        background: #00f0ff !important;
        color: #05070c !important;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.8) !important;
    }
    
    /* Tab Styling */
    button[data-baseweb="tab"] {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.85rem !important;
        color: #94a3b8 !important;
    }
    
    button[aria-selected="true"] {
        color: #00f0ff !important;
        border-bottom-color: #00f0ff !important;
    }
</style>
""", unsafe_allow_html=True)

# Cyber Header
st.markdown("""
<div class="cyber-header">
    <div class="cyber-title">RANS🔰LAB-256</div>
    <div class="cyber-subtitle">// QUANTUM-RESISTANT ZERO-KNOWLEDGE IPFS VAULT</div>
</div>
""", unsafe_allow_html=True)

# Tabs
tab_enc, tab_dec = st.tabs(["🔒 ENCRYPT & PUSH TO IPFS", "🔓 FETCH FROM IPFS & DECRYPT"])

with tab_enc:
    st.write("")
    uploaded_file = st.file_uploader("SELECT TARGET FILE (ANY BINARY FORMAT)", key="file_enc")
    passphrase_enc = st.text_input("PASSPHRASE MASTER KEY (MEMORIZED ONLY):", type="password", key="pass_enc")
    
    st.write("")
    if st.button("EXECUTE ENCRYPTION & PUSH TO IPFS 🚀", key="btn_enc"):
        if uploaded_file and passphrase_enc:
            with st.spinner("Locking file & Pushing payload to IPFS..."):
                try:
                    file_bytes = uploaded_file.read()
                    encrypted_payload = encrypt_file_bytes(file_bytes, passphrase_enc)
                    filename_ranslab = f"{uploaded_file.name}.ranslab"
                    
                    cid = push_to_ipfs(encrypted_payload, filename_ranslab)
                    
                    st.success("✅ ENCRYPTION & IPFS PINNING SUCCESSFUL!")
                    st.code(cid, language="text")
                    st.caption("☝️ Copy & simpan Kode CID IPFS di atas untuk dekripsi nanti.")
                except Exception as e:
                    st.error(f"❌ ERROR: {str(e)}")
        else:
            st.warning("⚠️ Masukkan file dan Passphrase!")

with tab_dec:
    st.write("")
    input_cid = st.text_input("INPUT IPFS CID HASH:", placeholder="Qm... / bafy...", key="cid_dec")
    passphrase_dec = st.text_input("PASSPHRASE DECRYPTION KEY:", type="password", key="pass_dec")
    
    # TAMBAHAN: Input Nama & Ekstensi File Output (Default .jpg)
    output_filename = st.text_input("SAVE RESTORED FILE AS:", value=".File.txt.PNG.jpg.Mp3.Mp4.Etc", key="out_filename")
    
    st.write("")
    if st.button("FETCH FROM IPFS & DECRYPT 🔓", key="btn_dec"):
        if input_cid and passphrase_dec:
            with st.spinner("Fetching payload from IPFS Gateway & Decrypting..."):
                try:
                    payload_bytes = fetch_from_ipfs(input_cid)
                    decrypted_bytes = decrypt_file_bytes(payload_bytes, passphrase_dec)
                    
                    st.success("✅ DECRYPTION SUCCESS: Binary Restored 100%!")
                    
                    # File name menggunakan input dari user
                    st.download_button(
                        label=f"📥 DOWNLOAD {output_filename}",
                        data=decrypted_bytes,
                        file_name=output_filename,
                        mime="application/octet-stream",
                        key="btn_dl"
                    )
                except Exception as e:
                    st.error(f"❌ DECRYPTION FAILED: Passphrase salah atau CID tidak ditemukan.")
        else:
            st.warning("⚠️ Input CID dan Passphrase!")