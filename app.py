import streamlit as st
import pandas as pd

# 1. KONFIGURASI
st.set_page_config(page_title="Portal Akademik", page_icon="🏫", layout="centered")

# 2. CSS PROFESIONAL
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    #MainMenu, footer, header { visibility: hidden; }
    .hero-banner { background: linear-gradient(135deg, #0A2540 0%, #195CBF 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; margin-bottom: 2rem; }
    
    .bio-card { background: #3498db; color: #ffffff; padding: 20px; border-radius: 12px; border-left: 8px solid #2980b9; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .bio-card h4, .bio-card strong { color: #ffffff !important; }
    .bio-card div { color: #f0f0f0 !important; }
    
    .bio-row { display: flex; margin-bottom: 8px; }
    .bio-label { width: 120px; font-weight: bold; flex-shrink: 0; }
    .bio-colon { width: 20px; }
    
    .val-card { background: #1C1E26; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 6px solid #195CBF; }
    .inner-box { flex: 1; border: 1px solid #333; border-radius: 8px; padding: 10px; background: #262730; text-align: center; }
    .val-title { font-size: 0.7rem; color: #A0A0A0; font-weight: 600; }
    .val-score { font-size: 1.2rem; font-weight: 700; color: #FFFFFF; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
st.markdown("""<div class="hero-banner"><h1>Portal Informasi Akademik</h1><p>Sistem Informasi Siswa Terpadu</p></div>""", unsafe_allow_html=True)

# 4. LOAD DATA (DIPERBAIKI: Memaksa semua data menjadi string agar format tetap terjaga)
@st.cache_data
def load_data():
    # dtype=str memastikan '04041994' tidak terbaca jadi angka '4041994'
    df = pd.read_excel("data_pengguna.xlsx", dtype=str)
    df.columns = df.columns.str.strip()
    df.rename(columns={df.columns[0]: 'No_HP'}, inplace=True)
    
    # Bersihkan semua data dari spasi yang tidak sengaja terbawa
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error memuat file: {e}")
    st.stop()

# 5. INPUT LOGIN
no_hp = st.text_input("Masukkan Nomor Handphone (tanpa 0, contoh: 81234567890):")
password = st.text_input("Masukkan Password (format tanggal bulan tahun, contoh: 01011990):", type="password")

if st.button("Masuk ke Sistem", type="primary", use_container_width=True):
    hasil = df[df['No_HP'] == no_hp.strip()]
    
    if not hasil.empty:
        data = hasil.iloc[0]
        db_password = str(data.get('PASSWORD', '')).strip()
        
        # Validasi Password
        if password.strip() == db_password:
            # --- TAMPILAN DATA JIKA LOGIN BERHASIL ---
            def render_biodata_card(title, icon, content_dict):
                rows_html = ""
                for key, val in content_dict.items():
                    rows_html += f"""
                    <div class='bio-row'>
                        <div class='bio-label'>{key}</div>
                        <div class='bio-colon'>:</div>
                        <div>{val}</div>
                    </div>"""
                st.markdown(f"<div class='bio-card'><h4>{icon} {title}</h4>{rows_html}</div>", unsafe_allow_html=True)

            st.subheader("👤 Biodata Siswa")
            render_biodata_card("Data Siswa", "🧑‍🎓", {"Nama": data.get('NAMA LENGKAP', '-'), "No Reg": data.get('NO REGISTRASI', '-'), "No HP Siswa": data.get('NO HP SISWA', '-')})
            render_biodata_card("Data Orang Tua", "👨‍👩‍👧", {"Nama Ortu": data.get('NAMA ORTU', '-'), "No HP 1": data.get('NO HP ORTU 1', '-'), "No HP 2": data.get('NO HP ORTU 2', '-')})
            render_biodata_card("Data Kelas GO", "📚", {"Kelas": data.get('KELAS GO', '-'), "Hari": data.get('HARI', '-'), "Jam": data.get('JAM KBM', '-'), "Ruang": data.get('Ruang Kelas', '-'), "Lokasi": data.get('Lokasi', '-')})

            st.subheader("📊 Nilai Akademik")
            grup_uji = [
                ("PU", "PU 1", "PU 2", "PU 3"), ("PPU", "PPU 1", "PPU 2", "PPU 3"), 
                ("PBM", "PBM 1", "PBM 2", "PBM 3"), ("PK", "PK 1", "PK 2", "PK 3"), 
                ("Lit Bhs Indo", "Lit Bhs Indo 1", "Lit Bhs Indo 2", "Lit Bhs Indo 3"), 
                ("Lit Bhs Ing", "Lit Bhs Ing 1", "Lit Bhs Ing 2", "Lit Bhs Ing 3"), ("PM", "PM 1", "PM 2", "PM 3")
            ]

            for g, c1, c2, c3 in grup_uji:
                v1 = data[c1] if c1 in data and pd.notnull(data[c1]) else '-'
                v2 = data[c2] if c2 in data and pd.notnull(data[c2]) else '-'
                v3 = data[c3] if c3 in data and pd.notnull(data[c3]) else '-'
                
                st.markdown(f"""
                <div class='val-card'>
                    <div style='color:#195CBF; font-weight:bold; border-bottom:1px solid #333; margin-bottom:10px; padding-bottom:5px;'>{g}</div>
                    <div style='display:flex; gap:12px;'>
                        <div class='inner-box'><div class='val-title'>{c1}</div><div class='val-score'>{v1}</div></div>
                        <div class='inner-box'><div class='val-title'>{c2}</div><div class='val-score'>{v2}</div></div>
                        <div class='inner-box'><div class='val-title'>{c3}</div><div class='val-score'>{v3}</div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        else:
            st.error("Password salah. Silakan periksa kembali format tanggal (DDMMYYYY).")
            
    else:
        st.error("Nomor handphone tidak terdaftar di sistem. Silakan hubungi admin (ka Tian) di WA : 087771740512")
