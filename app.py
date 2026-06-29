import streamlit as st
import pandas as pd

# 1. KONFIGURASI
st.set_page_config(page_title="Portal Akademik", page_icon="🏫", layout="centered")

# 2. CSS PROFESIONAL (Dark Mode & Biru Muda)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    #MainMenu, footer, header { visibility: hidden; }
    
    .hero-banner { background: linear-gradient(135deg, #0A2540 0%, #195CBF 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; margin-bottom: 2rem; }
    
    /* Kartu Biodata Biru Muda */
    .bio-card { 
        background: #3498db; 
        color: #ffffff; 
        padding: 20px; 
        border-radius: 12px; 
        border-left: 8px solid #2980b9; 
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .bio-card h4, .bio-card strong { color: #ffffff !important; }
    .bio-card div { color: #f0f0f0 !important; }
    
    /* Kartu Nilai Dark Mode */
    .val-card { background: #1C1E26; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 6px solid #195CBF; }
    .inner-box { flex: 1; border: 1px solid #333; border-radius: 8px; padding: 10px; background: #262730; text-align: center; }
    .val-title { font-size: 0.8rem; color: #A0A0A0; font-weight: 600; }
    .val-score { font-size: 1.4rem; font-weight: 700; color: #FFFFFF; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
st.markdown("""<div class="hero-banner"><h1>Portal Informasi Akademik</h1><p>Sistem Informasi Siswa Terpadu</p></div>""", unsafe_allow_html=True)

# 4. LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_excel("data_pengguna.xlsx")
    df.rename(columns={df.columns[0]: 'No_HP'}, inplace=True)
    df['No_HP'] = df['No_HP'].astype(str).str.strip()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error memuat file: {e}")
    st.stop()

# 5. INPUT LOGIN
no_hp = st.text_input("Masukkan Nomor Handphone:")

if st.button("Masuk ke Sistem", type="primary", use_container_width=True):
    hasil = df[df['No_HP'] == no_hp.strip()]
    
    if not hasil.empty:
        data = hasil.iloc[0]
        
        # Fungsi render kartu biodata
        def render_biodata_card(title, icon, content_dict):
            cols_html = ""
            for key, val in content_dict.items():
                cols_html += f"<div style='margin-bottom: 8px;'><strong>{key}:</strong> {val}</div>"
            st.markdown(f"<div class='bio-card'><h4>{icon} {title}</h4><div>{cols_html}</div></div>", unsafe_allow_html=True)

        # ... (kode sebelumnya sampai bagian BIODATA)

        # BIODATA
        st.subheader("👤 Biodata Siswa")
        render_biodata_card("Data Siswa", "🧑‍🎓", {"Nama": data.get('NAMA LENGKAP', '-'), "No Reg": data.get('NO REGISTRASI', '-'), "No HP Siswa": data.get('NO HP SISWA', '-')})
        render_biodata_card("Data Orang Tua", "👨‍👩‍👧", {"Nama Ortu": data.get('NAMA ORTU', '-'), "No HP 1": data.get('NO HP ORTU 1', '-'), "No HP 2": data.get('NO HP ORTU 2', '-')})
        render_biodata_card("Data Kelas GO", "📚", {"Kelas": data.get('KELAS GO', '-'), "Hari": data.get('HARI', '-'), "Jam": data.get('JAM KBM', '-'), "Ruang": data.get('Ruang Kelas', '-'), "Lokasi": data.get('Lokasi', '-')})

        # --- NILAI HARUS BERADA DI DALAM BLOK IF ---
        st.subheader("📊 Nilai Akademik")

        grup_uji = [
            ("PU", "PU 1", "PU 2", "PU 3"), 
            ("PPU", "PPU 1", "PPU 2", "PPU 3"), 
            ("PBM", "PBM 1", "PBM 2", "PBM 3"), 
            ("PK", "PK 1", "PK 2", "PK 3"), 
            ("Lit Bhs Indo", "Lit Bhs Indo 1", "Lit Bhs Indo 2", "Lit Bhs Indo 3"), 
            ("Lit Bhs Ing", "Lit Bhs Ing 1", "Lit Bhs Ing 2", "Lit Bhs Ing 3"), 
            ("PM", "PM 1", "PM 2", "PM 3")
        ]

        for g, c1_n, c2_n, c3_n in grup_uji:
            val1, val2, val3 = data.get(c1_n, '-'), data.get(c2_n, '-'), data.get(c3_n, '-')
            
            st.markdown(f"""
            <div class='val-card'>
                <div style='color:#195CBF; font-weight:bold; border-bottom:1px solid #333; margin-bottom:10px; padding-bottom:5px;'>{g}</div>
                <div style='display:flex; gap:12px;'>
                    <div class='inner-box'><div class='val-title'>{c1_n}</div><div class='val-score'>{val1}</div></div>
                    <div class='inner-box'><div class='val-title'>{c2_n}</div><div class='val-score'>{val2}</div></div>
                    <div class='inner-box'><div class='val-title'>{c3_n}</div><div class='val-score'>{val3}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    else: # --- ELSE INI HARUS SEJAJAR DENGAN IF NOT HASIL.EMPTY ---
        st.error("Nomor handphone tidak terdaftar di sistem. Silakan hubungi admin (ka Tian) di WA : 087771740512")
