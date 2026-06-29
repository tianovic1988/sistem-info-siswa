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
    
    /* Card Biodata dengan titik dua sejajar */
    .bio-card { 
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); 
        padding: 20px; border-radius: 15px; border-left: 5px solid #3b82f6; 
        margin-bottom: 20px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .bio-row { display: flex; margin-bottom: 6px; }
    .bio-label { width: 100px; font-weight: bold; color: #A0A0A0; }
    .bio-colon { width: 20px; }
    
    .val-card { background: rgba(30, 30, 45, 0.8); padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 5px solid #195CBF; transition: transform 0.3s; }
    .val-card:hover { transform: translateY(-5px); }
    div.stButton > button { border-radius: 20px !important; background: linear-gradient(90deg, #195CBF, #3b82f6) !important; color: white !important; border: none !important; padding: 0.5rem 2rem !important; }
    .inner-box { flex: 1; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 10px; background: rgba(0,0,0,0.2); text-align: center; }
    .val-title { font-size: 0.65rem; color: #A0A0A0; text-transform: uppercase; letter-spacing: 1px; }
    .val-score { font-size: 1.3rem; font-weight: 800; color: #FFFFFF; }
    .trainer-box { background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 15px; text-align: center; margin-top: 20px; border: 1px solid #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
st.markdown("""<div class="hero-banner"><h1>BISA - Basis Informasi Siswa dan Akademik</h1><p>by : tian.go</p></div>""", unsafe_allow_html=True)

# 4. LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_excel("data_pengguna.xlsx", dtype=str)
    df.columns = df.columns.str.strip()
    df.rename(columns={df.columns[0]: 'No_HP'}, inplace=True)
    return df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

df = load_data()

grup_uji = [
    ("PU", "PU 1", "PU 2", "PU 3"), ("PPU", "PPU 1", "PPU 2", "PPU 3"), 
    ("PBM", "PBM 1", "PBM 2", "PBM 3"), ("PK", "PK 1", "PK 2", "PK 3"), 
    ("Lit Bhs Indo", "Lit Bhs Indo 1", "Lit Bhs Indo 2", "Lit Bhs Indo 3"), 
    ("Lit Bhs Ing", "Lit Bhs Ing 1", "Lit Bhs Ing 2", "Lit Bhs Ing 3"), ("PM", "PM 1", "PM 2", "PM 3")
]

# 5. FUNGSI RENDER
def render_bio(title, icon, data_dict):
    rows = "".join([f"<div class='bio-row'><div class='bio-label'>{k}</div><div class='bio-colon'>:</div><div>{v}</div></div>" for k, v in data_dict.items()])
    st.markdown(f"<div class='bio-card'><h4>{icon} {title}</h4>{rows}</div>", unsafe_allow_html=True)

# 6. PDF
def create_pdf(data, grup_uji):
    pdf = FPDF()
    pdf.set_left_margin(20)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Laporan Hasil Akademik", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Biodata Siswa", ln=True)
    pdf.set_font("Arial", '', 11)
    for label, key in [("Nama", 'NAMA LENGKAP'), ("Reg", 'NO REGISTRASI'), ("Kelas", 'KELAS GO'), ("Ortu", 'NAMA ORTU')]:
        pdf.cell(30, 8, label + ":", 0)
        pdf.cell(0, 8, str(data.get(key, '-')), ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Detail Nilai Akademik", ln=True)
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

# 7. LOGIN
no_hp = st.text_input("Nomor HP (Contoh: 81234567890)")
password = st.text_input("Password (Tanggal Lahir: DDMMYYYY)", type="password")

if st.button("Masuk ke Sistem"):
    hasil = df[df['No_HP'] == no_hp.strip()]
    if not hasil.empty and password.strip() == str(hasil.iloc[0].get('PASSWORD', '')).strip():
        data = hasil.iloc[0]
        st.link_button("Chat *Personal Trainer*", "https://wa.me/6287771740512")
        
        st.subheader("👤 Biodata Lengkap")
        render_bio("Siswa", "🧑‍🎓", {"Nama": data['NAMA LENGKAP'], "Reg": data['NO REGISTRASI'], "HP": data['NO HP SISWA']})
        render_bio("Orang Tua", "👨‍👩‍👧", {"Nama": data['NAMA ORTU'], "HP 1": data['NO HP ORTU 1'], "HP 2": data['NO HP ORTU 2']})
        render_bio("Kelas GO", "📚", {"Kelas": data['KELAS GO'], "Hari": data['HARI'], "Jam": data['JAM KBM'], "Ruang": data['Ruang Kelas'], "Lokasi": data['Lokasi']})
        
        with st.expander("ℹ️ FAQ: Cara Membaca Hasil Akademik"):
            st.write("1. **Uji 1, 2, 3**: Menampilkan skor dari setiap sesi ujian yang telah diikuti.\n2. **Grafik Tren**: Memudahkan Anda melihat perkembangan performa secara visual.\n3. **Kendala**: Jika ada nilai yang tidak sesuai atau butuh jadwal tambahan, segera hubungi *Personal Trainer* Anda.")

        st.subheader("📈 Tren Nilai")
        fig = go.Figure()
        for g, c1, c2, c3 in grup_uji:
            fig.add_trace(go.Scatter(x=['Uji 1', 'Uji 2', 'Uji 3'], y=[pd.to_numeric(data.get(c,0), errors='coerce') for c in [c1,c2,c3]], name=g))
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📊 Nilai Akademik")
        for g, c1, c2, c3 in grup_uji:
            st.markdown(f"""<div class='val-card'><div style='font-weight:bold; margin-bottom:5px;'>{g}</div>
            <div style='display:flex; gap:10px;'><div class='inner-box'><div class='val-title'>Uji 1</div><div class='val-score'>{data.get(c1,'-')}</div></div>
            <div class='inner-box'><div class='val-title'>Uji 2</div><div class='val-score'>{data.get(c2,'-')}</div></div>
            <div class='inner-box'><div class='val-title'>Uji 3</div><div class='val-score'>{data.get(c3,'-')}</div></div></div></div>""", unsafe_allow_html=True)
        
        st.download_button("Download Laporan PDF", data=create_pdf(data, grup_uji), file_name="Laporan_Akademik.pdf", mime="application/pdf")
        
        st.markdown("<div class='trainer-box'><h5>👨‍🏫 Profil Personal Trainer</h5><p><strong>ka Tian</strong><br>Siap mendampingi dan memberikan arahan strategis agar Anda mencapai target akademik terbaik!</p></div>", unsafe_allow_html=True)
    else:
        st.error("Data tidak ditemukan atau Password salah.")
        st.link_button("Hubungi *Personal Trainer* (ka Tian) untuk Bantuan", "https://wa.me/6287771740512")
