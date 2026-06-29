import streamlit as st
import pandas as pd
import time  # Untuk efek animasi loading

# 1. Konfigurasi Halaman 
st.set_page_config(page_title="Portal Siswa Profesional", page_icon="🎓", layout="centered")

# 2. Modifikasi CSS (Menyembunyikan menu & menambahkan Footer Hak Cipta)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Membuat tulisan footer sendiri di bawah */
    .custom-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #888888;
        text-align: center;
        font-size: 12px;
        padding: 10px;
    }
    </style>
    <div class="custom-footer">
        &copy; 2026 Sistem Informasi Siswa. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

# 3. Membuat Sidebar (Panel Samping)
with st.sidebar:
    # Anda bisa mengganti URL gambar ini dengan link logo sekolah Anda nanti
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135823.png", width=100)
    st.title("Pusat Bantuan")
    st.info("Jika nomor HP Anda tidak terdaftar atau data akademik tidak sesuai, silakan hubungi bagian Tata Usaha Sekolah.")
    st.divider()
    st.caption("Jam Layanan: 08.00 - 15.00 WIB")

# 4. Header Utama dengan Banner
# URL di bawah adalah gambar buku/edukasi dari Unsplash
st.image("https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=1000&auto=format&fit=crop", use_container_width=True)
st.title("🎓 Portal Informasi Siswa")
st.markdown("Silakan masukkan nomor HP terdaftar untuk mengakses data Anda.")
st.divider()

# 5. Membaca Database (Menggunakan Cache agar web tidak lemot)
@st.cache_data
def load_data():
    return pd.read_excel("data_pengguna.xlsx", dtype={'No_HP': str})

try:
    df = load_data()
    df['No_HP'] = df['No_HP'].str.strip()
except Exception as e:
    st.error("Gagal membaca database. Pastikan file Excel tersedia.")
    st.stop()

# 6. Form Input
no_hp_input = st.text_input("📱 Nomor HP Anda:", placeholder="Contoh: 081234567890")

# Tombol menggunakan type="primary" agar warnanya menyala
if st.button("Cek Data", use_container_width=True, type="primary"):
    if no_hp_input:
        
        # Efek Animasi Loading
        with st.spinner("Memverifikasi data di server..."):
            time.sleep(1.5)  # Jeda buatan selama 1.5 detik
            no_hp_input = no_hp_input.strip()
            hasil_pencarian = df[df['No_HP'] == no_hp_input]
        
        if not hasil_pencarian.empty:
            # Notifikasi Pop-up di pojok kanan bawah
            st.toast('Verifikasi Berhasil!', icon='✅')
            
            data_user = hasil_pencarian.iloc[0]
            st.success(f"Selamat datang, **{data_user.get('Nama', 'Siswa')}**!")
            
            # Membungkus data di dalam kotak Expander
            with st.expander("📄 Klik untuk melihat rincian data Anda", expanded=True):
                kolom_kiri, kolom_kanan = st.columns(2) 
                urutan = 0
                
                for kolom in df.columns:
                    if kolom != 'No_HP':
                        nilai_data = data_user[kolom]
                        if pd.isna(nilai_data):
                            nilai_data = "-"
                        
                        # Format tampilan agar lebih padat dan rapi
                        if urutan % 2 == 0:
                            kolom_kiri.markdown(f"**{kolom}**<br>{nilai_data}", unsafe_allow_html=True)
                            kolom_kiri.write("") # spasi
                        else:
                            kolom_kanan.markdown(f"**{kolom}**<br>{nilai_data}", unsafe_allow_html=True)
                            kolom_kanan.write("") # spasi
                        urutan += 1
        else:
            st.error("❌ Nomor HP tidak ditemukan di sistem kami.")
    else:
        st.warning("⚠️ Kolom nomor HP tidak boleh kosong.")
