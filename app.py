import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime
import pytz

# 1. KONFIGURASI
st.set_page_config(page_title="Portal Akademik BISA", page_icon="🏫", layout="centered")

# 2. CSS MODERN
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1a1a2e, #0f0f1a); color: #FAFAFA; }
    .hero-banner { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 2.5rem; border-radius: 20px; text-align: center; color: white; margin-bottom: 2rem; }
    .bio-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); padding: 20px; border-radius: 15px; border-left: 5px solid #3b82f6; margin-bottom: 20px; }
    .bio-row { display: flex; margin-bottom: 6px; }
    .bio-label { width: 100px; font-weight: bold; color: #A0A0A0; }
    .val-card { background: rgba(30, 30, 45, 0.8); padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 5px solid #195CBF; }
    div.stButton > button { border-radius: 20px !important; background: linear-gradient(90deg, #195CBF, #3b82f6) !important; color: white !important; }
    .inner-box { flex: 1; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 10px; background: rgba(0,0,0,0.2); text-align: center; }
    .val-title { font-size: 0.65rem; color: #A0A0A0; text-transform: uppercase; }
    .val-score { font-size: 1.3rem; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
st.markdown("""<div class="hero-banner"><h1>BISA - Basis Informasi Siswa dan Akademik</h1><p>by : tian.go</p></div>""", unsafe_allow_html=True)

# 4. DATA & FUNGSI PDF
@st.cache_data
def load_data():
    df = pd.read_excel("data_pengguna.xlsx", dtype=str)
    df.columns = df.columns.str.strip()
    df.rename(columns={df.columns[0]: 'No_HP'}, inplace=True)
    return df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

df = load_data()
grup_uji = [("PU", "PU 1", "PU 2", "PU 3"), ("PPU", "PPU 1", "PPU 2", "PPU 3"), 
            ("PBM", "PBM 1", "PBM 2", "PBM 3"), ("PK", "PK 1", "PK 2", "PK 3"), 
            ("Lit Bhs Indo", "Lit Bhs Indo 1", "Lit Bhs Indo 2", "Lit Bhs Indo 3"), 
            ("Lit Bhs Ing", "Lit Bhs Ing 1", "Lit Bhs Ing 2", "Lit Bhs Ing 3"), ("PM", "PM 1", "PM 2", "PM 3")]

def create_pdf(data, grup_uji):
    pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Laporan Hasil Akademik", ln=True, align='C'); pdf.ln(10)
    pdf.set_font("Arial", 'B', 12); pdf.cell(0, 10, "Biodata Lengkap", ln=True); pdf.set_font("Arial", '', 11)
    for k, v in [("Nama", 'NAMA LENGKAP'), ("Reg", 'NO REGISTRASI'), ("Kelas", 'KELAS GO')]:
        pdf.cell(40, 8, k + ":", 0); pdf.cell(0, 8, str(data.get(v, '-')), ln=True)
    pdf.ln(5); pdf.set_font("Arial", 'B', 12); pdf.cell(0, 10, "Detail Nilai", ln=True); pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 10, "Mata Uji", 1); pdf.cell(20, 10, "Uji 1", 1); pdf.cell(20, 10, "Uji 2", 1); pdf.cell(20, 10, "Uji 3", 1, ln=True)
    pdf.set_font("Arial", '', 10)
    for g, c1, c2, c3 in grup_uji:
        pdf.cell(40, 10, g, 1); pdf.cell(20, 10, str(data.get(c1, '-')), 1); pdf.cell(20, 10, str(data.get(c2, '-')), 1); pdf.cell(20, 10, str(data.get(c3, '-')), 1, ln=True)
    return pdf.output(dest='S').encode('latin-1')

# 5. LOGIN & UI UTAMA
no_hp = st.text_input("Nomor HP:")
password = st.text_input("Password:", type="password")

if st.button("Masuk ke Sistem"):
    hasil = df[df['No_HP'] == no_hp.strip()]
    if not hasil.empty and password.strip() == str(hasil.iloc[0].get('PASSWORD', '')).strip():
        data = hasil.iloc[0]
        tab1, tab2, tab3, tab4 = st.tabs(["👤 Profil", "📊 Akademik", "👨‍🏫 Personal Trainer", "📥 Download PDF"])
        
        with tab1: # Profil
            st.markdown(f"<div class='bio-card'><h4>🧑‍🎓 Siswa</h4><div class='bio-row'><div class='bio-label'>Nama</div>: {data['NAMA LENGKAP']}</div><div class='bio-row'><div class='bio-label'>Reg</div>: {data['NO REGISTRASI']}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='bio-card'><h4>👨‍👩‍👧 Orang Tua</h4><div class='bio-row'><div class='bio-label'>Nama</div>: {data['NAMA ORTU']}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='bio-card'><h4>📚 Kelas GO</h4><div class='bio-row'><div class='bio-label'>Kelas</div>: {data['KELAS GO']}</div></div>", unsafe_allow_html=True)
        
        with tab2: # Akademik (Grafik + Nilai)
            st.subheader("📈 Tren Nilai")
            fig = go.Figure()
            for g, c1, c2, c3 in grup_uji:
                fig.add_trace(go.Scatter(x=['Uji 1', 'Uji 2', 'Uji 3'], y=[pd.to_numeric(data.get(c,0), errors='coerce') for c in [c1,c2,c3]], name=g))
            st.plotly_chart(fig, use_container_width=True)
            st.subheader("📊 Detail Nilai")
            for g, c1, c2, c3 in grup_uji:
                st.markdown(f"**{g}**")
                st.markdown(f"""<div class='val-card'><div style='display:flex; gap:10px;'><div class='inner-box'><div class='val-title'>Uji 1</div><div class='val-score'>{data.get(c1,'-')}</div></div><div class='inner-box'><div class='val-title'>Uji 2</div><div class='val-score'>{data.get(c2,'-')}</div></div><div class='inner-box'><div class='val-title'>Uji 3</div><div class='val-score'>{data.get(c3,'-')}</div></div></div></div>""", unsafe_allow_html=True)
        
        with tab3: # Personal Trainer
            st.markdown("<h5>👨‍🏫 Profil Personal Trainer</h5><p>ka Tian - Siap membantu Anda!</p>", unsafe_allow_html=True)
            st.link_button("Hubungi ka Tian via WhatsApp", "https://wa.me/6287771740512")
            
        with tab4: # Download
            st.download_button("Klik untuk Download Laporan PDF Utuh", data=create_pdf(data, grup_uji), file_name="Laporan_Akademik.pdf")
            
    else:
        st.error("Data tidak ditemukan atau Password salah.")
        st.link_button("Hubungi ka Tian untuk Bantuan", "https://wa.me/6287771740512")
