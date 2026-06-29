import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime
import pytz

# 1. KONFIGURASI
st.set_page_config(page_title="Portal Akademik BISA", page_icon="🏫", layout="centered")

# 2. CSS MODERN & PROFESIONAL
st.markdown("""
    <style>
    /* Latar Belakang & Layout */
    .stApp { background: radial-gradient(circle at top right, #1a1a2e, #0f0f1a); color: #FAFAFA; }
    #MainMenu, footer, header { visibility: hidden; }
    
    /* Hero Banner */
    .hero-banner { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 2.5rem; border-radius: 20px; text-align: center; color: white; margin-bottom: 2rem; box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
    
    /* Glassmorphism Cards */
    .bio-card { 
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); 
        padding: 20px; border-radius: 15px; border-left: 5px solid #3b82f6; 
        margin-bottom: 20px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Nilai Card Hover Effect */
    .val-card { 
        background: rgba(30, 30, 45, 0.8); padding: 15px; border-radius: 12px; margin-bottom: 15px; 
        border-left: 5px solid #195CBF; transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .val-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(59, 130, 246, 0.2); }
    
    /* Tombol Modern */
    div.stButton > button { border-radius: 20px !important; background: linear-gradient(90deg, #195CBF, #3b82f6) !important; color: white !important; border: none !important; padding: 0.5rem 2rem !important; }
    
    .inner-box { flex: 1; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 10px; background: rgba(0,0,0,0.2); text-align: center; }
    .val-title { font-size: 0.65rem; color: #A0A0A0; text-transform: uppercase; letter-spacing: 1px; }
    .val-score { font-size: 1.3rem; font-weight: 800; color: #FFFFFF; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
st.markdown("""<div class="hero-banner"><h1>BISA SYSTEM</h1><p>Basis Informasi Siswa dan Akademik - by tian.go</p></div>""", unsafe_allow_html=True)

# 4. LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_excel("data_pengguna.xlsx", dtype=str)
    df.columns = df.columns.str.strip()
    df.rename(columns={df.columns[0]: 'No_HP'}, inplace=True)
    return df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

try:
    df = load_data()
except:
    st.error("File data tidak ditemukan.")
    st.stop()

# 5. DATA GLOBAL
grup_uji = [
    ("PU", "PU 1", "PU 2", "PU 3"), ("PPU", "PPU 1", "PPU 2", "PPU 3"), 
    ("PBM", "PBM 1", "PBM 2", "PBM 3"), ("PK", "PK 1", "PK 2", "PK 3"), 
    ("Lit Bhs Indo", "Lit Bhs Indo 1", "Lit Bhs Indo 2", "Lit Bhs Indo 3"), 
    ("Lit Bhs Ing", "Lit Bhs Ing 1", "Lit Bhs Ing 2", "Lit Bhs Ing 3"), ("PM", "PM 1", "PM 2", "PM 3")
]

# 6. FUNGSI PDF
def create_pdf(data, grup_uji):
    pdf = FPDF()
    pdf.set_left_margin(20)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Laporan Hasil Akademik", ln=True, align='C')
    pdf.ln(10)
    
    # Biodata
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Biodata Siswa", ln=True)
    pdf.set_font("Arial", '', 11)
    for label, key in [("Nama", 'NAMA LENGKAP'), ("Reg", 'NO REGISTRASI'), ("Kelas", 'KELAS GO'), ("Ortu", 'NAMA ORTU')]:
        pdf.cell(30, 8, label + ":", 0)
        pdf.cell(0, 8, str(data.get(key, '-')), ln=True)
    
    pdf.ln(10)
    
    # Tabel Nilai
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Detail Nilai Akademik", ln=True)
    pdf.set_fill_color(200, 220, 255)
    
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(50, 10, "Mata Uji", 1, 0, 'C', 1)
    for i in range(1,4): pdf.cell(30, 10, f"Uji {i}", 1, 0, 'C', 1)
    pdf.ln(10)
    
    pdf.set_font("Arial", '', 11)
    for g, c1, c2, c3 in grup_uji:
        pdf.cell(50, 10, g, 1)
        for c in [c1, c2, c3]: pdf.cell(30, 10, str(data.get(c, '-')), 1, 0, 'C')
        pdf.ln(10)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 9)
    waktu = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%d %B %Y, %H:%M:%S")
    pdf.cell(0, 10, f"Dicetak dari BISA SYSTEM - by tian.go pada {waktu}", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# 7. INPUT LOGIN
no_hp = st.text_input("Nomor HP (Contoh: 81234567890)")
password = st.text_input("Password (Tanggal Lahir: DDMMYYYY)", type="password")

if st.button("Masuk ke Sistem"):
    hasil = df[df['No_HP'] == no_hp.strip()]
    if not hasil.empty and password.strip() == str(hasil.iloc[0].get('PASSWORD', '')).strip():
        data = hasil.iloc[0]
        st.link_button("Chat Admin", "https://wa.me/6287771740512")
        
        # Grid layout untuk biodata
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='bio-card'><h4>🧑‍🎓 Siswa</h4>Nama: <strong>{data['NAMA LENGKAP']}</strong><br>Reg: {data['NO REGISTRASI']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='bio-card'><h4>📚 Kelas</h4>Kelas: {data['KELAS GO']}<br>Ruang: {data.get('Ruang Kelas', '-')}</div>", unsafe_allow_html=True)
        
        # Grafik
        st.subheader("📈 Tren Nilai")
        fig = go.Figure()
        for g, c1, c2, c3 in grup_uji:
            fig.add_trace(go.Scatter(x=['Uji 1', 'Uji 2', 'Uji 3'], y=[pd.to_numeric(data.get(c,0), errors='coerce') for c in [c1,c2,c3]], name=g))
        st.plotly_chart(fig, use_container_width=True)
        
        # Nilai
        st.subheader("📊 Nilai Akademik")
        for g, c1, c2, c3 in grup_uji:
            st.markdown(f"""<div class='val-card'><div style='font-weight:bold; margin-bottom:5px;'>{g}</div>
            <div style='display:flex; gap:10px;'><div class='inner-box'><div class='val-title'>Uji 1</div><div class='val-score'>{data.get(c1,'-')}</div></div>
            <div class='inner-box'><div class='val-title'>Uji 2</div><div class='val-score'>{data.get(c2,'-')}</div></div>
            <div class='inner-box'><div class='val-title'>Uji 3</div><div class='val-score'>{data.get(c3,'-')}</div></div></div></div>""", unsafe_allow_html=True)
        
        st.download_button("Download Laporan PDF", data=create_pdf(data, grup_uji), file_name="Laporan_Akademik.pdf", mime="application/pdf")
    else:
        st.error("Data tidak ditemukan atau Password salah.")
        st.link_button("Hubungi Admin (ka Tian) untuk Bantuan", "https://wa.me/6287771740512")
