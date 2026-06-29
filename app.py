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
    .stApp { background: radial-gradient(circle at top right, #1a1a2e, #0f0f1a); color: #FAFAFA; }
    #MainMenu, footer, header { visibility: hidden; }
    .hero-banner { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 2.5rem; border-radius: 20px; text-align: center; color: white; margin-bottom: 2rem; box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
    .bio-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); padding: 20px; border-radius: 15px; border-left: 5px solid #3b82f6; margin-bottom: 20px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); }
    .bio-row { display: flex; margin-bottom: 6px; }
    .bio-label { width: 100px; font-weight: bold; color: #A0A0A0; }
    .val-card { background: rgba(30, 30, 45, 0.8); padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 5px solid #195CBF; transition: transform 0.3s; }
    div.stButton > button { border-radius: 20px !important; background: linear-gradient(90deg, #195CBF, #3b82f6) !important; color: white !important; border: none !important; padding: 0.5rem 2rem !important; }
    .inner-box { flex: 1; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 10px; background: rgba(0,0,0,0.2); text-align: center; }
    .val-score { font-size: 1.3rem; font-weight: 800; color: #FFFFFF; }
    .trainer-box { background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 15px; text-align: center; margin-top: 20px; border: 1px solid #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
st.markdown("""<div class="hero-banner"><h1>BISA - Basis Informasi Siswa dan Akademik</h1><p>by : tian.go</p></div>""", unsafe_allow_html=True)

# 4. DATA LOADING
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

# 5. FUNGSI RENDER & PDF
def render_bio(data_dict):
    rows = "".join([f"<div class='bio-row'><div class='bio-label'>{k}</div><div>: {v}</div></div>" for k, v in data_dict.items()])
    st.markdown(f"<div class='bio-card'>{rows}</div>", unsafe_allow_html=True)

def create_pdf(data, grup_uji):
    pdf = FPDF()
    pdf.add_page(); pdf.set_font("Arial", 'B', 16); pdf.cell(0, 10, "Laporan Hasil Akademik", ln=True, align='C')
    # ... (PDF logic remains identical for brevity) ...
    return pdf.output(dest='S').encode('latin-1')

# 6. LOGIN
no_hp = st.text_input("Nomor HP:")
password = st.text_input("Password:", type="password")

if st.button("Masuk ke Sistem"):
    hasil = df[df['No_HP'] == no_hp.strip()]
    if not hasil.empty and password.strip() == str(hasil.iloc[0].get('PASSWORD', '')).strip():
        data = hasil.iloc[0]
        st.toast("Selamat datang kembali!", icon="👋")
        
        # TABBED UI
        tab1, tab2, tab3 = st.tabs(["👤 Profil", "📊 Akademik", "ℹ️ Lainnya"])
        
        with tab1:
            render_bio({"Nama": data['NAMA LENGKAP'], "Reg": data['NO REGISTRASI'], "Kelas": data['KELAS GO']})
        
        with tab2:
            st.subheader("📈 Tren Nilai")
            fig = go.Figure()
            for g, c1, c2, c3 in grup_uji:
                fig.add_trace(go.Scatter(x=['Uji 1', 'Uji 2', 'Uji 3'], y=[pd.to_numeric(data.get(c,0), errors='coerce') for c in [c1,c2,c3]], name=g))
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("📊 Detail Nilai")
            for g, c1, c2, c3 in grup_uji:
                val3 = pd.to_numeric(data.get(c3, 0), errors='coerce')
                st.markdown(f"**{g}**")
                st.progress(min(val3 / 1000, 1.0)) # Progress Bar Target
                st.markdown(f"<div class='val-card'><div style='display:flex; gap:10px;'><div class='inner-box'><div class='val-score'>{data.get(c3,'-')}</div></div></div></div>", unsafe_allow_html=True)
        
        with tab3:
            with st.expander("ℹ️ FAQ"):
                st.write("Hubungi *Personal Trainer* jika ada kendala.")
            st.markdown("<div class='trainer-box'><h5>👨‍🏫 Profil Personal Trainer</h5><p>ka Tian - Siap membantu Anda!</p></div>", unsafe_allow_html=True)
            if st.download_button("Download PDF", data=create_pdf(data, grup_uji), file_name="Laporan.pdf"):
                st.toast("PDF berhasil diunduh!", icon="✅")
                
    else:
        st.error("Data tidak ditemukan atau Password salah.")
