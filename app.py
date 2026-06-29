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

# 2. Desain CSS (Modern & Profesional)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    #MainMenu, footer, header, .stAppDeployButton { visibility: hidden; }
    
    .hero-banner {
        background: linear-gradient(135deg, #0A2540 0%, #195CBF 100%);
        padding: 2rem; border-radius: 12px; text-align: center; color: white; margin-bottom: 2rem;
    }
    .val-card { border: 1px solid #ddd; padding: 15px; border-radius: 10px; background: #ffffff; margin-bottom: 15px; border-left: 6px solid #195CBF; }
    .val-title { font-size: 0.75rem; color: #5a6e84; font-weight: 600; }
    .val-score { font-size: 1.25rem; font-weight: 700; color: #195CBF; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Pusat Layanan)
with st.sidebar:
    st.markdown("### 🏫 Pusat Layanan")
    st.info("Jika data tidak sesuai, hubungi tim kami:")
    st.success("👨‍💻 **Ka Tian**\n📱 [Chat WhatsApp](https://wa.me/6287771740512)")
    st.divider()
    st.caption("🕒 Jam Operasional: Senin - Jumat (08.00 - 15.00 WIB)")

# 4. Banner
st.markdown("""<div class="hero-banner"><h1>Portal Informasi Akademik</h1><p>Sistem Informasi Siswa Terpadu</p></div>""", unsafe_allow_html=True)

# 5. Load Data
@st.cache_data
def load_data():
    return pd.read_excel("data_pengguna.xlsx", dtype={'No_HP': str})

try:
    df = load_data()
    df['No_HP'] = df['No_HP'].str.strip()
except:
    st.error("File data_pengguna.xlsx tidak ditemukan!")
    st.stop()

# 6. Login & Tampilan Data
no_hp = st.text_input("Masukkan Nomor Handphone:")
if st.button("Masuk ke Sistem", type="primary", use_container_width=True):
    hasil = df[df['No_HP'] == no_hp.strip()]
    if not hasil.empty:
        data = hasil.iloc[0]
        
        # BIODATA
        st.subheader("👤 Biodata Siswa")
        kolom_nilai = ['PU 1','PU 2','PPU 1','PPU 2','PBM 1','PBM 2','PK 1','PK 2','Lit Bhs Indo 1','Lit Bhs Indo 2','Lit Bhs Ing 1','Lit Bhs Ing 2','PM 1','PM 2']
        with st.container(border=True):
            c1, c2 = st.columns(2)
            i = 0
            for col in df.columns:
                if col != 'No_HP' and col not in kolom_nilai:
                    val = data.get(col, "-")
                    if i % 2 == 0: c1.markdown(f"**{col}**: {val}")
                    else: c2.markdown(f"**{col}**: {val}")
                    i += 1
        
        # NILAI
        st.subheader("📊 Nilai Akademik")
        grup_uji = [("PU","PU 1","PU 2"), ("PPU","PPU 1","PPU 2"), ("PBM","PBM 1","PBM 2"), 
                    ("PK","PK 1","PK 2"), ("Lit Bhs Indo","Lit Bhs Indo 1","Lit Bhs Indo 2"), 
                    ("Lit Bhs Ing","Lit Bhs Ing 1","Lit Bhs Ing 2"), ("PM","PM 1","PM 2")]
        
        for g, c1_n, c2_n in grup_uji:
            val1 = data.get(c1_n, '-')
            val2 = data.get(c2_n, '-')
            st.markdown(f"""
            <div class='val-card'>
                <div style='font-weight: 600; color: #0A2540; margin-bottom: 10px; border-bottom: 1px solid #f0f0f0; padding-bottom: 5px;'>{g}</div>
                <div style='display: flex; gap: 12px;'>
                    <div style='flex: 1; border: 1px solid #eef2f7; border-radius: 8px; padding: 10px; background: #f8fbff; text-align: center;'>
                        <div class='val-title'>{c1_n}</div><div class='val-score'>{val1}</div>
                    </div>
                    <div style='flex: 1; border: 1px solid #eef2f7; border-radius: 8px; padding: 10px; background: #f8fbff; text-align: center;'>
                        <div class='val-title'>{c2_n}</div><div class='val-score'>{val2}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Nomor tidak terdaftar di sistem.")
