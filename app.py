import streamlit as st
import pandas as pd

# 1. KONFIGURASI
st.set_page_config(page_title="Portal Akademik", page_icon="🏫", layout="centered")

# 2. CSS PROFESIONAL
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
    .hero-banner { background: linear-gradient(135deg, #0A2540 0%, #195CBF 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; margin-bottom: 2rem; }
    .val-card { border: 1px solid #ddd; padding: 15px; border-radius: 10px; background: #ffffff; margin-bottom: 15px; border-left: 6px solid #195CBF; }
    .val-title { font-size: 0.75rem; color: #5a6e84; font-weight: 600; }
    .val-score { font-size: 1.25rem; font-weight: 700; color: #195CBF; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
st.markdown("""<div class="hero-banner"><h1>Portal Informasi Akademik</h1><p>Sistem Informasi Siswa Terpadu</p></div>""", unsafe_allow_html=True)

# 4. LOAD DATA
@st.cache_data
def load_data():
    return pd.read_excel("data_pengguna.xlsx", dtype={'_HP': str})

try:
    df = load_data()
    df['_HP'] = df['_HP'].str.strip()
except Exception as e:
    st.error(f"Error memuat file: {e}")
    st.stop()

# 5. INPUT LOGIN
no_hp = st.text_input("Masukkan Nomor Handphone:")

if st.button("Masuk ke Sistem", type="primary", use_container_width=True):
    hasil = df[df['_HP'] == no_hp.strip()]
    
    if not hasil.empty:
        data = hasil.iloc[0]
        
        # --- BIODATA ---
        st.subheader("👤 Biodata Siswa")
        with st.container(border=True):
            st.markdown("#### 🧑‍🎓 Data Siswa")
            c1, c2 = st.columns(2)
            c1.write(f"**Nama**: {data.get('NAMA LENGKAP', '-')}")
            c2.write(f"**No Reg**: {data.get('NO REGISTRASI', '-')}")
            st.write(f"**No HP Siswa**: {data.get('NO HP SISWA', '-')}")
            
        with st.container(border=True):
            st.markdown("#### 👨‍👩‍👧 Data Orang Tua")
            st.write(f"**Nama Ortu**: {data.get('NAMA ORTU', '-')}")
            c1, c2 = st.columns(2)
            c1.write(f"**No HP 1**: {data.get('NO HP ORTU 1', '-')}")
            c2.write(f"**No HP 2**: {data.get('NO HP ORTU 2', '-')}")
            
        with st.container(border=True):
            st.markdown("#### 📚 Data Kelas GO")
            st.write(f"**Kelas**: {data.get('KELAS GO', '-')}")
            st.write(f"**Hari**: {data.get('HARI', '-')}")
            st.write(f"**Jam**: {data.get('JAM KBM', '-')}")
            c1, c2 = st.columns(2)
            c1.write(f"**Ruang**: {data.get('Ruang Kelas', '-')}")
            c2.write(f"**Lokasi**: {data.get('Lokasi', '-')}")

        # --- NILAI ---
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
            """, unsafe_html=True)
            
    else:
        st.error("Nomor handphone tidak terdaftar di sistem. Silakan hubungi admin (ka Tian) di WA : 087771740512")
