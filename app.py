import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime
import pytz # Memastikan waktu menggunakan zona WIB

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
st.markdown("""<div class="hero-banner"><h1>BISA - Basis Informasi Siswa dan Akademik</h1><p>created by tian.go</p></div>""", unsafe_allow_html=True)

# 4. LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_excel("data_pengguna.xlsx", dtype=str)
    df.columns = df.columns.str.strip()
    df.rename(columns={df.columns[0]: 'No_HP'}, inplace=True)
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error memuat file: {e}")
    st.stop()

# 5. DATA GLOBAL
grup_uji = [
    ("PU", "PU 1", "PU 2", "PU 3"), ("PPU", "PPU 1", "PPU 2", "PPU 3"), 
    ("PBM", "PBM 1", "PBM 2", "PBM 3"), ("PK", "PK 1", "PK 2", "PK 3"), 
    ("Lit Bhs Indo", "Lit Bhs Indo 1", "Lit Bhs Indo 2", "Lit Bhs Indo 3"), 
    ("Lit Bhs Ing", "Lit Bhs Ing 1", "Lit Bhs Ing 2", "Lit Bhs Ing 3"), ("PM", "PM 1", "PM 2", "PM 3")
]

# 6. FUNGSI PDF (REVISI MARGIN & WAKTU WIB)
def create_pdf(data, grup_uji):
    pdf = FPDF()
    pdf.set_left_margin(20) # Margin kiri ditingkatkan agar tidak mepet
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Laporan Hasil Akademik", ln=True, align='C')
    pdf.ln(10)
    
    # Biodata
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Biodata Siswa", ln=True)
    pdf.set_font("Arial", '', 11)
    fields = [("Nama", 'NAMA LENGKAP'), ("Reg", 'NO REGISTRASI'), ("Kelas", 'KELAS GO'), ("Ortu", 'NAMA ORTU')]
    for label, key in fields:
        pdf.cell(30, 8, label + ":", 0)
        pdf.cell(0, 8, str(data.get(key, '-')), ln=True)
    
    pdf.ln(10)
    
    # Tabel Nilai
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Detail Nilai Akademik", ln=True)
    pdf.set_fill_color(200, 220, 255)
    pdf.set_font("Arial", 'B', 11)
    
    # Header Tabel
    pdf.cell(50, 10, "Mata Uji", 1, 0, 'C', 1)
    pdf.cell(30, 10, "Uji 1", 1, 0, 'C', 1)
    pdf.cell(30, 10, "Uji 2", 1, 0, 'C', 1)
    pdf.cell(30, 10, "Uji 3", 1, 1, 'C', 1)
    
    # Isi Tabel
    pdf.set_font("Arial", '', 11)
    for g, c1, c2, c3 in grup_uji:
        pdf.cell(50, 10, g, 1)
        pdf.cell(30, 10, str(data.get(c1, '-')), 1, 0, 'C')
        pdf.cell(30, 10, str(data.get(c2, '-')), 1, 0, 'C')
        pdf.cell(30, 10, str(data.get(c3, '-')), 1, 1, 'C')
    
    # Footer Waktu WIB
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 9)
    wib = pytz.timezone('Asia/Jakarta')
    waktu_wib = datetime.now(wib).strftime("%d %B %Y, %H:%M:%S")
    pdf.cell(0, 10, f"Dicetak dari BISA SYSTEM - by tian.go pada {waktu_wib}", ln=True, align='C')
        
    return pdf.output(dest='S').encode('latin-1')

# 7. INPUT LOGIN
no_hp = st.text_input("Masukkan Nomor Handphone (tanpa 0, contoh: 81234567890):")
password = st.text_input("Masukkan Password (format tanggal bulan tahun, contoh: 01011990):", type="password")

if st.button("Masuk ke Sistem", type="primary", use_container_width=True):
    hasil = df[df['No_HP'] == no_hp.strip()]
    if not hasil.empty:
        data = hasil.iloc[0]
        db_password = str(data.get('PASSWORD', '')).strip()
        
        if password.strip() == db_password:
            st.link_button("Chat Admin (ka Tian) untuk Bantuan", "https://wa.me/6287771740512")
            
            # Biodata
            def render_biodata_card(title, icon, content_dict):
                rows_html = "".join([f"<div class='bio-row'><div class='bio-label'>{k}</div><div class='bio-colon'>:</div><div>{v}</div></div>" for k, v in content_dict.items()])
                st.markdown(f"<div class='bio-card'><h4>{icon} {title}</h4>{rows_html}</div>", unsafe_allow_html=True)

            render_biodata_card("Data Siswa", "🧑‍🎓", {"Nama": data.get('NAMA LENGKAP', '-'), "No Reg": data.get('NO REGISTRASI', '-'), "No HP": data.get('NO HP SISWA', '-')})
            render_biodata_card("Data Orang Tua", "👨‍👩‍👧", {"Nama Ortu": data.get('NAMA ORTU', '-'), "HP 1": data.get('NO HP ORTU 1', '-'), "HP 2": data.get('NO HP ORTU 2', '-')})
            render_biodata_card("Data Kelas GO", "📚", {"Kelas": data.get('KELAS GO', '-'), "Hari": data.get('HARI', '-'), "Jam": data.get('JAM KBM', '-'), "Ruang": data.get('Ruang Kelas', '-'), "Lokasi": data.get('Lokasi', '-')})
            
            # Tren
            st.subheader("📈 Tren Nilai")
            fig = go.Figure()
            for g, c1, c2, c3 in grup_uji:
                scores = [pd.to_numeric(data.get(c1, 0), errors='coerce'), pd.to_numeric(data.get(c2, 0), errors='coerce'), pd.to_numeric(data.get(c3, 0), errors='coerce')]
                fig.add_trace(go.Scatter(x=['Uji 1', 'Uji 2', 'Uji 3'], y=scores, name=g))
            st.plotly_chart(fig, use_container_width=True)
            
            # Nilai
            st.subheader("📊 Nilai Akademik")
            for g, c1, c2, c3 in grup_uji:
                v1, v2, v3 = data.get(c1, '-'), data.get(c2, '-'), data.get(c3, '-')
                st.markdown(f"""<div class='val-card'><div style='color:#195CBF; font-weight:bold; margin-bottom:5px;'>{g}</div>
                <div style='display:flex; gap:10px;'><div class='inner-box'><div class='val-title'>{c1}</div><div class='val-score'>{v1}</div></div>
                <div class='inner-box'><div class='val-title'>{c2}</div><div class='val-score'>{v2}</div></div>
                <div class='inner-box'><div class='val-title'>{c3}</div><div class='val-score'>{v3}</div></div></div></div>""", unsafe_allow_html=True)
            
            # PDF
            st.download_button("Download Laporan (PDF)", data=create_pdf(data, grup_uji), file_name="Laporan_Akademik.pdf", mime="application/pdf")
        else:
            st.error("Password salah. Silakan hubungi admin (ka Tian) di WA : 087771740512")
    else:
        st.error("Nomor tidak terdaftar. Silakan hubungi admin (ka Tian) di WA : 087771740512")
