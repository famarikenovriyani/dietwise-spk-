import streamlit as st
import pandas as pd
import numpy as np
import os
import base64

# ============================================================
# KONFIGURASI HALAMAN METODE SPK
# ============================================================
st.set_page_config(
    page_title="DietWise — SPK Pemilihan Menu Diet",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM STYLING (MODERN UI/UX DESIGN)
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Sembunyikan Sidebar Bawaan */
    [data-testid="stSidebar"] {
        display: none !important;
    }

    /* Sembunyikan Header Bawaan Streamlit dalam iframe */
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }

    .stApp {
        background: #F8FAFC;
    }

    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 1000px !important;
    }

    /* ===== HERO LOGO STYLING ===== */
    .logo-hero-wrapper {
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }
    .logo-hero-img {
        width: 170px;
        height: 170px;
        object-fit: contain;
        border-radius: 50%;
        background: #FFFFFF;
        padding: 12px;
        box-shadow: 0 15px 35px rgba(16, 185, 129, 0.2);
        border: 3px solid #10B981;
        transition: transform 0.3s ease;
    }
    .logo-hero-img:hover {
        transform: scale(1.05);
    }

    /* ===== BANNER UTAMA ===== */
    .hero-banner {
        background: linear-gradient(135deg, #065F46 0%, #059669 50%, #10B981 100%);
        border-radius: 24px;
        padding: 2.5rem 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px rgba(5, 150, 105, 0.2);
        margin-bottom: 2rem;
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.8rem;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.95;
        max-width: 750px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* ===== CARD UI ===== */
    .custom-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.5rem;
    }
    .card-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #065F46;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }

    /* ===== BOX TIPS ===== */
    .tips-box {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 16px;
        padding: 1.2rem;
        color: #166534;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 2rem;
        text-align: center;
    }

    /* ===== PODIUM BOX ===== */
    .podium-box {
        background: white;
        border-radius: 18px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #E2E8F0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.04);
    }
    .rank-1 { border-top: 6px solid #F59E0B; }
    .rank-2 { border-top: 6px solid #94A3B8; }
    .rank-3 { border-top: 6px solid #D97706; }

    /* ===== CUSTOM BUTTON ===== */
    div.stButton > button {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.9rem 2rem !important;
        font-size: 1.1rem !important;
        box-shadow: 0 10px 20px rgba(16, 185, 129, 0.25) !important;
        width: 100%;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #047857 0%, #059669 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 14px 28px rgba(16, 185, 129, 0.35) !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPER DATA & ALGORITMA WP
# ============================================================
def muat_dataset():
    try:
        df = pd.read_csv('dataset_diet.csv.csv')
    except FileNotFoundError:
        data_dummy = {
            'Nama_Menu': [
                'Nasi Ayam Rebus + Sayur Bening', 'Salad Buah Segar & Yogurt Low-Fat', 
                'Telur Dadar Teflon + Tumis Kangkung', 'Oatmeal Pisang + Susu Almond', 
                'Nasi Merah + Tahu Tempe Bakar', 'Ayam Panggang Tanpa Kulit', 
                'Ikan Kembung Bakar + Nasi Merah', 'Gado-Gado Protein (Double Tahu)'
            ],
            'Harga': [15000, 18000, 12000, 10000, 13000, 20000, 17000, 12000],
            'Kalori': [420, 280, 350, 380, 450, 480, 400, 350],
            'Protein': [28, 8, 22, 15, 20, 32, 26, 12],
            'Jarak_Akses': [1.2, 0.8, 1.5, 1.0, 0.5, 1.3, 1.8, 0.6]
        }
        df = pd.DataFrame(data_dummy)
    return df

def hitung_weighted_product(df, bobot_dict):
    W = [bobot_dict['Harga'], bobot_dict['Kalori'], bobot_dict['Protein'], bobot_dict['Akses']]
    total_bobot = sum(W)
    w_normal = [w / total_bobot for w in W]
    
    pangkat = [-w_normal[0], w_normal[1], w_normal[2], w_normal[3]]

    kolom_kriteria = ['Harga', 'Kalori', 'Protein', 'Jarak_Akses']
    daftar_S = []
    for _, row in df.iterrows():
        S = 1
        for x, w in zip([row[k] for k in kolom_kriteria], pangkat):
            S *= (x ** w)
        daftar_S.append(S)

    total_S = sum(daftar_S)
    daftar_V = [s / total_S for s in daftar_S]

    hasil = df.copy()
    hasil['Vektor_S'] = daftar_S
    hasil['Vektor_V'] = daftar_V
    hasil['Rank'] = hasil['Vektor_V'].rank(ascending=False).astype(int)
    return hasil.sort_values(by='Vektor_V', ascending=False).reset_index(drop=True), w_normal

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return None

# ============================================================
# STATE MANAGEMENT
# ============================================================
if 'halaman' not in st.session_state: st.session_state.halaman = 'beranda'
if 'nama_user' not in st.session_state: st.session_state.nama_user = ''
if 'bobot' not in st.session_state: st.session_state.bobot = None


# ============================================================
# HALAMAN 1: BERANDA UTAMA (DEPAN)
# ============================================================
if st.session_state.halaman == 'beranda':

    # LOGO UTAMA
    img_b64 = get_image_base64('logo_dietwise.png')
    if img_b64:
        st.markdown(f"""
        <div class="logo-hero-wrapper">
            <img src="data:image/png;base64,{img_b64}" class="logo-hero-img">
        </div>
        """, unsafe_allow_html=True)

    # HERO HEADER
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Sistem Pendukung Keputusan Menu Diet</div>
        <div class="hero-subtitle">
            Implementasi Metode <b>Weighted Product (WP)</b> untuk Penentuan Rekomendasi Menu Makanan Sehat Berdasarkan Anggaran, Nutrisi, dan Aksesibilitas.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # TIPS DIET
    st.markdown("""
    <div class="tips-box">
        <b>💡 Tips Diet Hari Ini:</b> Konsumsi air putih minimal 2 Liter per hari untuk menjaga metabolisme tubuh Anda tetap optimal selama menjalani diet cerdas.
    </div>
    """, unsafe_allow_html=True)

    # TOMBOL TRANSISI KE FORM REKOMENDASI
    _, col_btn, _ = st.columns([1, 1.5, 1])
    with col_btn:
        if st.button("🚀 Mulai Rekomendasi Menu", use_container_width=True):
            st.session_state.halaman = 'input'
            st.rerun()


# ============================================================
# HALAMAN 2: FORM PREFERENSI DIET
# ============================================================
elif st.session_state.halaman == 'input':

    # LOGO KECIL DI ATAS FORM
    img_b64 = get_image_base64('logo_dietwise.png')
    if img_b64:
        st.markdown(f"""
        <div style="text-align:center; margin-bottom: 1rem;">
            <img src="data:image/png;base64,{img_b64}" style="width:80px; height:80px; object-fit:contain;">
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="custom-card">
        <div class="card-title">⚙️ Atur Profil & Kriteria Diet Anda</div>
        <p style="text-align:center; color:#64748B;">Tentukan tingkat kepentingan kriteria sesuai dengan kondisi Anda saat ini.</p>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1.3])

    with col_a:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('### 👤 Data Responden')
        nama_input = st.text_input("Nama Lengkap", placeholder="Masukkan nama Anda...")
        st.write("")
        st.info("ℹ️ **Kriteria Cost:** Harga (Makin murah makin bagus)\n\nℹ️ **Kriteria Benefit:** Kalori, Protein, dan Aksesibilitas Jarak.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('### ⚖️ Prioritas Kriteria (Skala 1 - 5)')
        bobot_harga = st.slider("💰 Prioritas Harga Murah", 1, 5, 3)
        bobot_kalori = st.slider("🔥 Prioritas Target Kalori", 1, 5, 3)
        bobot_protein = st.slider("💪 Prioritas Asupan Protein", 1, 5, 3)
        bobot_akses = st.slider("📍 Prioritas Jarak Lokasi Dekat", 1, 5, 3)
        st.markdown('</div>', unsafe_allow_html=True)

    c_back, c_sub = st.columns([1, 2])
    with c_back:
        if st.button("⬅️ Kembali", use_container_width=True):
            st.session_state.halaman = 'beranda'
            st.rerun()
    with c_sub:
        if st.button("⚡ Hitung Rekomendasi (Weighted Product)", use_container_width=True):
            if not nama_input.strip():
                st.error("⚠️ Mohon isi Nama Anda terlebih dahulu!")
            else:
                st.session_state.nama_user = nama_input
                st.session_state.bobot = {
                    'Harga': bobot_harga, 'Kalori': bobot_kalori,
                    'Protein': bobot_protein, 'Akses': bobot_akses
                }
                st.session_state.halaman = 'hasil'
                st.rerun()


# ============================================================
# HALAMAN 3: HASIL REKOMENDASI (LAPORAN SPK)
# ============================================================
elif st.session_state.halaman == 'hasil':

    df_menu = muat_dataset()
    bobot_user = st.session_state.bobot

    hasil_df, w_normal = hitung_weighted_product(df_menu, bobot_user)

    st.markdown(f"""
    <div class="custom-card" style="border-left: 6px solid #10B981;">
        <div class="card-title" style="justify-content: flex-start;">🎉 Hasil Rekomendasi Menu — {st.session_state.nama_user}</div>
        <p style="color:#64748B; margin:0;">Berikut adalah urutan preferensi terbaik hasil perhitungan Algoritma Weighted Product.</p>
    </div>
    """, unsafe_allow_html=True)

    # PODIUM TOP 3
    st.markdown("<h3 style='color:#065F46; font-weight:700;'>🥇 3 Menu Teratas Rekomendasi</h3>", unsafe_allow_html=True)
    top3 = hasil_df.head(3)
    p1, p2, p3 = st.columns(3)
    labels = ["Pilihan Utama (Rank 1)", "Pilihan Kedua (Rank 2)", "Pilihan Ketiga (Rank 3)"]
    ranks = ["rank-1", "rank-2", "rank-3"]

    for i, col in enumerate([p1, p2, p3]):
        if i < len(top3):
            row = top3.iloc[i]
            with col:
                st.markdown(f"""
                <div class="podium-box {ranks[i]}">
                    <div style="font-size:0.8rem; font-weight:700; color:#059669; text-transform:uppercase;">{labels[i]}</div>
                    <div style="font-size:1.1rem; font-weight:800; color:#1E293B; margin: 0.5rem 0;">{row['Nama_Menu']}</div>
                    <div style="font-size:0.85rem; color:#64748B;">Nilai Vektor V:</div>
                    <div style="font-size:1.6rem; font-weight:800; color:#10B981;">{row['Vektor_V'] * 100:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

    st.write("")
    
    # TABEL & GRAFIK
    col_tabel, col_grafik = st.columns([1.3, 1])

    with col_tabel:
        st.markdown("<h4 style='color:#065F46;'>📋 Tabel Peringkat Lengkap</h4>", unsafe_allow_html=True)
        tabel_view = pd.DataFrame({
            'Rank': hasil_df['Rank'],
            'Nama Menu': hasil_df['Nama_Menu'],
            'Harga': hasil_df['Harga'].apply(lambda x: f"Rp {x:,.0f}".replace(",", ".")),
            'Kalori': hasil_df['Kalori'].apply(lambda x: f"{x:.0f} kcal"),
            'Protein': hasil_df['Protein'].apply(lambda x: f"{x:.0f} g"),
            'Skor V': hasil_df['Vektor_V'].apply(lambda x: f"{x:.4f}")
        }).set_index('Rank')
        st.dataframe(tabel_view, use_container_width=True, height=280)

    with col_grafik:
        st.markdown("<h4 style='color:#065F46;'>📊 Visualisasi Persentase Skor V</h4>", unsafe_allow_html=True)
        chart_data = hasil_df[['Nama_Menu', 'Vektor_V']].copy()
        chart_data['Skor (%)'] = chart_data['Vektor_V'] * 100
        chart_data = chart_data[['Nama_Menu', 'Skor (%)']].set_index('Nama_Menu')
        st.bar_chart(chart_data, color="#10B981", height=280)

    st.write("")
    _, col_reset, _ = st.columns([1, 1.5, 1])
    with col_reset:
        if st.button("🔄 Ulangi Perhitungan", use_container_width=True):
            st.session_state.halaman = 'beranda'
            st.session_state.bobot = None
            st.rerun()
