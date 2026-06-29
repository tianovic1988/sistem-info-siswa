import streamlit as st
import pandas as pd

# 1. Mengatur konfigurasi halaman web
st.set_page_config(page_title="Sistem Informasi Pengguna", page_icon="🔒", layout="centered")

st.title("🔑 Login Sistem Informasi")
st.write("Silakan masukkan nomor HP Anda untuk melihat informasi pribadi.")

# 2. Membaca database dari file Excel
nama_file_excel = "data_pengguna.xlsx"

try:
    # Membaca Excel dan memastikan kolom No_HP dibaca sebagai text/string
    df = pd.read_excel(nama_file_excel, dtype={'No_HP': str})
    # Membersihkan spasi yang tidak sengaja terketik di Excel
    df['No_HP'] = df['No_HP'].str.strip()
except Exception as e:
    st.error(f"Gagal membaca file '{nama_file_excel}'. Pastikan file berada di folder yang sama dengan skrip ini.")
    st.stop()

# 3. Membuat Input Form untuk Nomor HP
no_hp_input = st.text_input("Masukkan Nomor HP Anda:", placeholder="Contoh: 081234567890")

# Tombol untuk proses check
if st.button("Cek Data"):
    if no_hp_input:
        # Membersihkan spasi pada input pengguna
        no_hp_input = no_hp_input.strip()
        
        # Mencari baris data yang nomor HP-nya cocok
        hasil_pencarian = df[df['No_HP'] == no_hp_input]
        
        if not hasil_pencarian.empty:
            st.success("Data ditemukan!")
            
            # Mengambil baris pertama yang cocok
            data_user = hasil_pencarian.iloc[0]
            
            st.markdown("---")
            st.subheader(f"👋 Selamat Datang, {data_user.get('Nama', 'Pengguna')}!")
            st.write("Berikut adalah informasi terkini milik Anda:")
            
            # Menampilkan seluruh informasi kolom secara otomatis (dinamis)
            # Sistem akan menampilkan data per baris berdasarkan nama kolom di Excel
            for kolom in df.columns:
                if kolom != 'No_HP': # Menyembunyikan nomor HP agar tampilan rapi
                    nilai_data = data_user[kolom]
                    # Jika data kosong di Excel, tampilkan tanda strip (-)
                    if pd.isna(nilai_data):
                        nilai_data = "-"
                    st.info(f"**{kolom}** : {nilai_data}")
                    
        else:
            st.error("Nomor HP tidak ditemukan. Silakan periksa kembali nomor yang Anda masukkan.")
    else:
        st.warning("Silakan masukkan nomor HP terlebih dahulu.")