import streamlit as st
import pandas as pd
import time 

st.set_page_config(page_title="Portal Akademik", page_icon="🏫", layout="centered")

# CSS Tambahan untuk kartu nilai
st.markdown("""
    <style>
    .val-card { border: 1px solid #ddd; padding: 10px; border-radius: 10px; background: #f9f9f9; text-align: center; }
    .val-title { font-weight: bold; color: #195CBF; margin-bottom: 5px; }
    .val-score { font-size: 1.2rem; font-weight: bold; color: #333; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar & Header (Sama seperti sebelumnya)
with st.sidebar:
    st.info("Pusat Bantuan: Hubungi [Ka Tian](https://wa.me/6287771740512)")

st.title("🎓 Portal Informasi Siswa")
st.divider()

# Load Data
@st.cache_data
def load_data():
    return pd.read_excel("data_pengguna.xlsx", dtype={'No_HP': str})

df = load_data()
df['No_HP'] = df['No_HP'].str.strip()

no_hp_input = st.text_input("Nomor HP:")

if st.button("Cari Data", type="primary"):
    hasil = df[df['No_HP'] == no_hp_input.strip()]
    if not hasil.empty:
        data = hasil.iloc[0]
        
        # 1. BIODATA
        st.subheader("👤 Biodata Siswa")
        with st.container(border=True):
            col1, col2 = st.columns(2)
            # Tentukan kolom mana saja yang masuk Biodata
            biodata_cols = ['NAMA LENGKAP', 'NO REGISTRASI', 'RUANG KELAS'] 
            for i, col in enumerate(biodata_cols):
                val = data.get(col, "-")
                if i % 2 == 0: col1.write(f"**{col}**: {val}")
                else: col2.write(f"**{col}**: {val}")

        # 2. NILAI AKADEMIK (Dikelompokkan)
        st.subheader("📊 Nilai Akademik")
        # Daftar grup mata uji
        grup_uji = [
            ("PU", "PU 1", "PU 2"),
            ("PPU", "PPU 1", "PPU 2"),
            ("PBM", "PBM 1", "PBM 2"),
            ("PK", "PK 1", "PK 2"),
            ("Lit Bhs Indo", "Lit Bhs Indo 1", "Lit Bhs Indo 2"),
            ("Lit Bhs Ing", "Lit Bhs Ing 1", "Lit Bhs Ing 2"),
            ("PM", "PM 1", "PM 2")
        ]
        
        for nama_grup, col1_name, col2_name in grup_uji:
            st.markdown(f"**{nama_grup}**")
            c1, c2 = st.columns(2)
            # Kartu kiri
            with c1:
                st.markdown(f"<div class='val-card'><div class='val-title'>{col1_name}</div><div class='val-score'>{data.get(col1_name, '-')}</div></div>", unsafe_allow_html=True)
            # Kartu kanan
            with c2:
                st.markdown(f"<div class='val-card'><div class='val-title'>{col2_name}</div><div class='val-score'>{data.get(col2_name, '-')}</div></div>", unsafe_allow_html=True)
            st.write("") # spasi
    else:
        st.error("Data tidak ditemukan.")
