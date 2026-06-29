import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman (Harus diletakkan paling atas)
st.set_page_config(page_title="Sistem Informasi", page_icon="🔒", layout="centered")

# 2. Menyembunyikan menu bawaan Streamlit agar terlihat profesional (Kustom CSS)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. Header Halaman
st.title("🔑 Portal Informasi")
st.markdown("Silakan masukkan nomor HP terdaftar untuk mengakses data Anda.")
st.divider() # Garis pembatas estetik

# 4. Membaca database dari file Excel
nama_file_excel = "data_pengguna.xlsx"

try:
    df = pd.read_excel(nama_file_excel, dtype={'No_HP': str})
    df['No_HP'] = df['No_HP'].str.strip()
except Exception as e:
    st.error(f"Gagal membaca database. Pastikan file '{nama_file_excel}' tersedia.")
    st.stop()

# 5. Membuat Input Form
no_hp_input = st.text_input("📱 Nomor HP Anda:", placeholder="Contoh: 081234567890")

# Tombol dibuat melebar (use_container_width=True)
if st.button("Cek Data", use_container_width=True):
    if no_hp_input:
        no_hp_input = no_hp_input.strip()
        hasil_pencarian = df[df['No_HP'] == no_hp_input]
        
        if not hasil_pencarian.empty:
            st.success("✅ Verifikasi Berhasil!")
            data_user = hasil_pencarian.iloc[0]
            
            st.markdown(f"### 👋 Halo, {data_user.get('Nama', 'Pengguna')}!")
            st.caption("Berikut adalah rincian informasi Anda saat ini:")
            st.write("") # Memberi sedikit jarak (spasi kosong)
            
            # [BARU] Menampilkan data dalam bentuk 2 Kolom (Grid)
            kolom_kiri, kolom_kanan = st.columns(2) 
            urutan = 0
            
            for kolom in df.columns:
                if kolom != 'No_HP':
                    nilai_data = data_user[kolom]
                    if pd.isna(nilai_data):
                        nilai_data = "-"
                    
                    # Membagi data ke kolom kiri dan kanan secara bergantian
                    if urutan % 2 == 0:
                        with kolom_kiri:
                            st.info(f"**{kolom}**\n\n{nilai_data}")
                    else:
                        with kolom_kanan:
                            st.info(f"**{kolom}**\n\n{nilai_data}")
                    urutan += 1
                    
        else:
            st.error("❌ Nomor HP tidak ditemukan. Silakan periksa kembali.")
    else:
        st.warning("⚠️ Silakan masukkan nomor HP terlebih dahulu.")
