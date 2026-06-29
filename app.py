import streamlit as st
import pandas as pd

# 1. KONFIGURASI
st.set_page_config(page_title="Portal Akademik", page_icon="🏫", layout="centered")

# 2. CSS PROFESIONAL (Dark Mode Version)
st.markdown("""
    <style>
    /* Mengubah latar belakang aplikasi menjadi gelap */
    .stApp { background-color: #0E1117; }
    
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; color: #FAFAFA; }
    #MainMenu, footer, header { visibility: hidden; }
    
    .hero-banner { background: linear-gradient(135deg, #0A2540 0%, #195CBF 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; margin-bottom: 2rem; }
    
    /* Kartu Biodata & Nilai (Dark Mode Style) */
    .val-card { border: 1px solid #262730; padding: 15px; border-radius: 10px; background: #1C1E26; margin-bottom: 15px; border-left: 6px solid #195CBF; }
    .val-title { font-size: 0.75rem; color: #A0A0A0; font-weight: 600; }
    .val-score { font-size: 1.25rem; font-weight: 700; color: #FFFFFF; }
    
    /* Agar teks di dalam container putih tetap terlihat */
    div[data-testid="stVerticalBlock"] { color: #FAFAFA; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
st.markdown("""<div class="hero-banner"><h1>Portal Informasi Akademik</h1><p>Sistem Informasi Siswa Terpadu</p></div>""", unsafe_allow_html=True)

# 4. LOAD DATA (Disesuaikan dengan No_HP)
@st.cache_data
def load_data():
    df = pd.read_excel("data_pengguna.xlsx")
    # Memastikan kolom pertama dianggap sebagai No_HP
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
    # Pencarian berdasarkan No_HP
    hasil = df[df['No_HP'] == no_hp.strip()]
    
    if not hasil.empty:
        data = hasil.iloc[0]
        
        # --- BIODATA (Terkelompok & Eye-Catching) ---
        st.subheader("👤 Biodata Siswa")
        
        # Fungsi pembantu untuk membuat kartu biodata agar kode lebih rapi
        def render_biodata_card(title, icon, content_dict):
            # Menggunakan HTML/CSS untuk tampilan yang lebih elegan
            cols_html = ""
            for key, val in content_dict.items():
                cols_html += f"<div style='margin-bottom: 8px;'><strong>{key}:</strong> {val}</div>"
            
            st.markdown(f"""
            <div style='background: #ffffff; padding: 20px; border-radius: 12px; border-left: 8px solid #195CBF; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 20px;'>
                <h4 style='color: #0A2540; margin-top: 0;'>{icon} {title}</h4>
                <div style='color: #34495e; font-size: 0.95rem;'>
                    {cols_html}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 1. Data Siswa
        render_biodata_card("Data Siswa", "🧑‍🎓", {
            "Nama": data.get('NAMA LENGKAP', '-'),
            "No Reg": data.get('NO REGISTRASI', '-'),
            "No HP Siswa": data.get('NO HP SISWA', '-')
        })
            
        # 2. Data Orang Tua
        render_biodata_card("Data Orang Tua", "👨‍👩‍👧", {
            "Nama Ortu": data.get('NAMA ORTU', '-'),
            "No HP 1": data.get('NO HP ORTU 1', '-'),
            "No HP 2": data.get('NO HP ORTU 2', '-')
        })
            
        # 3. Data Kelas GO
        render_biodata_card("Data Kelas GO", "📚", {
            "Kelas": data.get('KELAS GO', '-'),
            "Hari": data.get('HARI', '-'),
            "Jam": data.get('JAM KBM', '-'),
            "Ruang": data.get('Ruang Kelas', '-'),
            "Lokasi": data.get('Lokasi', '-')
        })

        # --- NILAI ---
        st.subheader("📊 Nilai Akademik")
        grup_uji = [("PU","PU 1","PU 2"), ("PPU","PPU 1","PPU 2"), ("PBM","PBM 1","PBM 2"), 
                    ("PK","PK 1","PK 2"), ("Lit Bhs Indo","Lit Bhs Indo 1","Lit Bhs Indo 2"), 
                    ("Lit Bhs Ing","Lit Bhs Ing 1","Lit Bhs Ing 2"), ("PM","PM 1","PM 2")]
        
        for g, c1_n, c2_n in grup_uji:
            val1, val2 = data.get(c1_n, '-'), data.get(c2_n, '-')
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
        st.error("Nomor handphone tidak terdaftar di sistem. Silakan hubungi admin (ka Tian) di WA : 087771740512")
