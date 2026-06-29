import streamlit as st
import pandas as pd
import time 

# 1. Konfigurasi Halaman 
st.set_page_config(
    page_title="Portal Akademik", 
    page_icon="🏫", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Injeksi CSS Khusus (Desain UI)
st.markdown("""
    <style>
    /* Mengimpor Font Modern 'Poppins' dari Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    /* Menerapkan font ke seluruh halaman */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Menyembunyikan elemen bawaan Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display:none;}
    
    /* Desain Banner Utama (Gradien Biru Sekolah) */
    .hero-banner {
        background: linear-gradient(135deg, #0A2540 0%, #195CBF 100%);
        padding: 2.5rem 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .hero-banner h1 {
        color: white !important;
        font-size: 2rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem;
        padding: 0;
    }
    .hero-banner p {
        font-size: 0.95rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Footer Kustom */
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
        &copy; 2026 Portal Informasi Akademik. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

# 3. Sidebar (Pusat Layanan)
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-bottom: 0;'>🏫</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #195CBF;'>Pusat Layanan</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.9rem;'>Sistem Informasi Siswa Terpadu</p>", unsafe_allow_html=True)
    st.divider()
    
    st.info("Bagi orang tua atau siswa yang tidak bisa login atau mengalami ketidaksesuaian data, silakan hubungi tim kami:")
    st.success("👨‍💻 **Ka Tian**\n\n📱 [Chat WhatsApp (087771740512)](https://wa.me/6287771740512)")
    
    st.divider()
    st.caption("🕒 Jam Operasional: Senin - Jumat (08.00 - 15.00 WIB)")

# 4. Memanggil Banner Buatan (CSS)
st.markdown("""
    <div class="hero-banner">
        <h1>Portal Informasi Akademik</h1>
        <p>Silakan masukkan nomor telepon yang terdaftar di database sekolah untuk mengakses data secara aman.</p>
    </div>
""", unsafe_allow_html=True)

# 5. Membaca Database 
@st.cache_data
def load_data():
    return pd.read_excel("data_pengguna.xlsx", dtype={'No_HP': str})

try:
    df = load_data()
    df['No_HP'] = df['No_HP'].str.strip()
except Exception as e:
    st.error("Gagal membaca database. Pastikan file 'data_pengguna.xlsx' tersedia.")
    st.stop()

# 6. Form Input & Logika Pencarian
st.markdown("### 🔐 Verifikasi Identitas")
no_hp_input = st.text_input("Nomor Handphone (Siswa / Orang Tua):", placeholder="Contoh: 081234567890")

if st.button("Masuk ke Sistem", use_container_width=True, type="primary"):
    if no_hp_input:
        
        with st.spinner("Mencocokkan data dengan server sekolah..."):
            time.sleep(1.5) 
            no_hp_input = no_hp_input.strip()
            hasil_pencarian = df[df['No_HP'] == no_hp_input]
        
        if not hasil_pencarian.empty:
            st.toast('Akses Diberikan!', icon='🔓')
            data_user = hasil_pencarian.iloc[0]
            
            # Pesan Sambutan
            st.success(f"🎉 Verifikasi Berhasil! Selamat datang, **{data_user.get('Nama', 'Siswa')}**.")
            
            # Rincian Data (Gaya Dashboard / Metric)
            st.markdown("### 📄 Rincian Data Siswa")
            
            # Menggunakan st.container dengan border agar terlihat seperti ID Card digital
            with st.container(border=True):
                kolom_kiri, kolom_kanan = st.columns(2) 
                urutan = 0
                
                for kolom in df.columns:
                    if kolom != 'No_HP':
                        nilai_data = data_user[kolom]
                        if pd.isna(nilai_data):
                            nilai_data = "-"
                        
                        # Menampilkan data dengan fitur 'metric' Streamlit agar elegan
                        if urutan % 2 == 0:
                            kolom_kiri.metric(label=kolom, value=str(nilai_data))
                        else:
                            kolom_kanan.metric(label=kolom, value=str(nilai_data))
                        urutan += 1
                        
            st.caption("Jika terdapat kesalahan pada data di atas, harap segera melaporkannya ke Pusat Layanan di menu samping.")
        else:
            st.error("❌ Akses Ditolak: Nomor HP tidak terdaftar di sistem sekolah.")
    else:
        st.warning("⚠️ Kolom verifikasi kosong. Silakan isi nomor handphone Anda.")
