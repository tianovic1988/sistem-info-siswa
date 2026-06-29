import streamlit as st
import pandas as pd

# Konfigurasi Halaman (Harus di baris paling atas)
st.set_page_config(page_title="Portal Akademik", page_icon="🏫", layout="centered")

# --- SIDEBAR (Diletakkan di posisi paling atas setelah konfigurasi) ---
with st.sidebar:
    st.markdown("### 🏫 Pusat Layanan")
    st.info("Jika data tidak sesuai, hubungi tim kami:")
    st.success("👨‍💻 **Ka Tian**\n📱 [Chat WhatsApp](https://wa.me/6287771740512)")
    st.divider()
    st.caption("🕒 Jam Operasional: Senin - Jumat (08.00 - 15.00 WIB)")

# --- CSS ---
st.markdown("""
    <style>
    .hero-banner { background: linear-gradient(135deg, #0A2540 0%, #195CBF 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; margin-bottom: 2rem; }
    .val-card { border: 1px solid #ddd; padding: 15px; border-radius: 10px; background: #ffffff; margin-bottom: 15px; border-left: 6px solid #195CBF; }
    .val-title { font-size: 0.75rem; color: #5a6e84; font-weight: 600; }
    .val-score { font-size: 1.25rem; font-weight: 700; color: #195CBF; }
    </style>
    """, unsafe_allow_html=True)

# --- APP ---
st.markdown("""<div class="hero-banner"><h1>Portal Informasi Akademik</h1><p>Sistem Informasi Siswa Terpadu</p></div>""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_excel("data_pengguna.xlsx", dtype={'No_HP': str})

try:
    df = load_data()
    df['No_HP'] = df['No_HP'].str.strip()
except:
    st.error("File data tidak ditemukan.")
    st.stop()

no_hp = st.text_input("Masukkan Nomor Handphone:")
if st.button("Masuk ke Sistem", type="primary"):
    hasil = df[df['No_HP'] == no_hp.strip()]
    if not hasil.empty:
        data = hasil.iloc[0]
       # BIODATA (Terkelompok)
        st.subheader("👤 Biodata Siswa")
        
        # 1. Kartu Biodata Siswa
        with st.container(border=True):
            st.markdown("#### 🧑‍🎓 Data Siswa")
            c1, c2 = st.columns(2)
            c1.write(f"**Nama**: {data.get('NAMA LENGKAP', '-')}")
            c2.write(f"**No Reg**: {data.get('NO REGISTRASI', '-')}")
            st.write(f"**No HP Siswa**: {data.get('NO HP SISWA', '-')}")
            
        # 2. Kartu Data Orang Tua
        with st.container(border=True):
            st.markdown("#### 👨‍👩‍👧 Data Orang Tua")
            st.write(f"**Nama Ortu**: {data.get('NAMA ORTU', '-')}")
            c1, c2 = st.columns(2)
            c1.write(f"**No HP 1**: {data.get('NO HP ORTU 1', '-')}")
            c2.write(f"**No HP 2**: {data.get('NO HP ORTU 2', '-')}")
            
        # 3. Kartu Data Kelas GO
        with st.container(border=True):
            st.markdown("#### 📚 Data Kelas GO")
            st.write(f"**Kelas**: {data.get('KELAS GO', '-')}")
            st.write(f"**Hari**: {data.get('HARI', '-')}")
            c1, c2 = st.columns(2)
            c1.write(f"**Jam**: {data.get('JAM KBM', '-')}")
            c2.write(f"**Ruang**: {data.get('RUANG KELAS', '-')}")
            st.write(f"**Lokasi**: {data.get('LOKASI', '-')}")
        
        st.subheader("📊 Nilai Akademik")
        grup_uji = [("PU","PU 1","PU 2"), ("PPU","PPU 1","PPU 2"), ("PBM","PBM 1","PBM 2"), 
                    ("PK","PK 1","PK 2"), ("Lit Bhs Indo","Lit Bhs Indo 1","Lit Bhs Indo 2"), 
                    ("Lit Bhs Ing","Lit Bhs Ing 1","Lit Bhs Ing 2"), ("PM","PM 1","PM 2")]
        
        for g, c1_n, c2_n in grup_uji:
            val1, val2 = data.get(c1_n, '-'), data.get(c2_n, '-')
            st.markdown(f"""
            <div class='val-card'>
                <div style='font-weight: 600; color: #0A2540; border-bottom: 1px solid #f0f0f0; margin-bottom: 5px;'>{g}</div>
                <div style='display: flex; gap: 10px;'>
                    <div style='flex: 1; padding: 5px; background: #f8fbff; text-align: center;'>
                        <div class='val-title'>{c1_n}</div><div class='val-score'>{val1}</div>
                    </div>
                    <div style='flex: 1; padding: 5px; background: #f8fbff; text-align: center;'>
                        <div class='val-title'>{c2_n}</div><div class='val-score'>{val2}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Nomor tidak terdaftar.")
