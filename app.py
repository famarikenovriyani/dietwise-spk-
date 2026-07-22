import streamlit as st
import pandas as pd
import numpy as np
import os
import base64

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="DietWise — Smart Healthy Food",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CUSTOM CSS UTAMA (DESIGN PROFESSIONAL & KONTRAST)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #0F172A !important;
}

/* Sembunyikan elemen bawaan Streamlit */
[data-testid="stSidebar"], header, footer, .stDeployButton {
    display: none !important;
}

.stApp {
    background-color: #F8FAFC !important;
}

.main-container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 10px;
}

/* HERO BANNER BERANDA */
.hero-box {
    background: linear-gradient(135deg, #059669 0%, #10B981 100%);
    border-radius: 24px;
    padding: 45px 35px;
    color: #FFFFFF !important;
    text-align: center;
    box-shadow: 0 20px 35px rgba(16, 185, 129, 0.25);
    margin-bottom: 30px;
}

.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: #FFFFFF !important;
    margin-bottom: 12px;
    letter-spacing: -0.5px;
}

.hero-subtitle {
    font-size: 1.1rem;
    color: #ECFDF5 !important;
    max-width: 750px;
    margin: 0 auto;
    line-height: 1.6;
}

/* CARDS STATISTIK */
.stat-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}

.stat-number {
    font-size: 1.8rem;
    font-weight: 800;
    color: #10B981;
}

.stat-label {
    font-size: 0.88rem;
    color: #64748B;
    font-weight: 600;
}

/* SECTION CARDS (BERANDA & STEPS) */
.step-card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 25px 20px;
    border: 2px solid #E2E8F0;
    text-align: center;
    height: 100%;
    transition: all 0.3s ease;
}

.step-number {
    background: #10B981;
    color: #FFFFFF;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    margin: 0 auto 15px auto;
}

.step-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0F172A !important;
    margin-bottom: 8px;
}

.step-desc {
    font-size: 0.9rem;
    color: #475569 !important;
    line-height: 1.5;
}

/* FORM STYLING (HALAMAN KRITERIA) */
.stSlider label, .stTextInput label, label {
    color: #0F172A !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
}

.stTextInput input {
    color: #0F172A !important;
    background-color: #FFFFFF !important;
    border: 2px solid #CBD5E1 !important;
    border-radius: 12px !important;
    padding: 12px 15px !important;
}

.info-guide-box {
    background: #EFF6FF;
    border-left: 5px solid #3B82F6;
    border-radius: 16px;
    padding: 20px;
    color: #1E3A8A !important;
    margin-bottom: 20px;
}

/* FOOD CARD STYLING (HASIL REKOMENDASI) */
.food-card {
    background: #FFFFFF;
    border-radius: 20px;
    border: 1px solid #E2E8F0;
    padding: 22px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
    margin-bottom: 25px;
}

div[data-testid="stImage"] img {
    border-radius: 16px !important;
    max-height: 230px !important;
    object-fit: cover !important;
    width: 100% !important;
}

.nutrition-badge {
    background: #F1F5F9;
    border-radius: 10px;
    padding: 10px 14px;
    color: #0F172A !important;
    font-weight: 700;
    font-size: 0.9rem;
    border: 1px solid #CBD5E1;
    margin-bottom: 8px;
}

.rank-badge-primary {
    background: #10B981;
    color: #FFFFFF !important;
    padding: 6px 16px;
    border-radius: 30px;
    font-weight: 800;
    font-size: 0.85rem;
    display: inline-block;
    margin-bottom: 12px;
}

.rank-badge-secondary {
    background: #475569;
    color: #FFFFFF !important;
    padding: 5px 14px;
    border-radius: 30px;
    font-weight: 700;
    font-size: 0.8rem;
    display: inline-block;
    margin-bottom: 10px;
}

/* BUTTON STYLING */
div.stButton > button {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 1.05rem !important;
    border-radius: 14px !important;
    padding: 14px 32px !important;
    border: none !important;
    box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3) !important;
}

div.stButton > button:hover {
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LOGO & DATASET DEKONTAMINASI GAMBAR
# ==========================================
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return None

logo_b64 = get_base64_image("logo_dietwise.png")

@st.cache_data
def get_menu_data():
    # Gambar dipastikan presisi sesuai dengan nama menu
    data = [
        {
            "Nama Menu": "Dada Ayam Panggang & Salad",
            "Harga": 25000, "Kalori": 350, "Protein": 35, "Jarak": 1.2,
            "Deskripsi": "Potongan dada ayam panggang rendah lemak disajikan dengan salad sayur segar dan saus olive oil.",
            "Gambar": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=600"
        },
        {
            "Nama Menu": "Salad Alpukat & Telur Rebus",
            "Harga": 20000, "Kalori": 280, "Protein": 18, "Jarak": 0.8,
            "Deskripsi": "Kombinasi serat alpukat segar, telur rebus kaya protein, dan sayuran hijau pilihan.",
            "Gambar": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600"
        },
        {
            "Nama Menu": "Smoothie Bowl Fruit Crunch",
            "Harga": 30000, "Kalori": 310, "Protein": 12, "Jarak": 2.5,
            "Deskripsi": "Mangkuk smoothie buah naga dan pisang segar ditaburi topping granola dan biji chia.",
            "Gambar": "https://images.unsplash.com/photo-1590301157890-4810ed352733?w=600"
        },
        {
            "Nama Menu": "Ikan Salmon Panggang Lemon",
            "Harga": 45000, "Kalori": 420, "Protein": 40, "Jarak": 3.0,
            "Deskripsi": "Ikan salmon panggang lembut dengan perasan lemon kaya Omega-3 dan protein tinggi.",
            "Gambar": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=600"
        },
        {
            "Nama Menu": "Oatmeal Pisang & Chia Seed",
            "Harga": 15000, "Kalori": 250, "Protein": 10, "Jarak": 0.5,
            "Deskripsi": "Oatmeal hangat sehat dikombinasikan dengan potongan pisang manis alami dan chia seed.",
            "Gambar": "https://images.unsplash.com/photo-1517673400267-0251440c45dc?w=600"
        },
        {
            "Nama Menu": "Tumis Tahu Tempe Brokoli",
            "Harga": 12000, "Kalori": 210, "Protein": 16, "Jarak": 0.4,
            "Deskripsi": "Tumisan sehat tahu, tempe, dan brokoli hijau tanpa minyak berlebih, cocok untuk budget hemat.",
            "Gambar": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600"
        }
    ]
    return pd.DataFrame(data)

df_menu = get_menu_data()

if 'halaman' not in st.session_state:
    st.session_state.halaman = 'beranda'

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ==========================================
# 4. HALAMAN 1: BERANDA INTERAKTIF & RAMAI
# ==========================================
if st.session_state.halaman == 'beranda':
    
    if logo_b64:
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{logo_b64}" style="width: 140px; height: auto;">
            </div>
        """, unsafe_allow_html=True)
    
    # Hero Box
    st.markdown("""
        <div class="hero-box">
            <div class="hero-title">Rekomendasi Makanan Diet Pintar & Sesuai Budget</div>
            <div class="hero-subtitle">
                Bingung menentukan menu makan sehat harian? DietWise memanfaatkan kalkulasi Decision Support System untuk merekomendasikan menu terbaik berdasarkan budget, target kalori, protein, dan lokasi terdekat dari Anda.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # STATISTIK APLIKASI
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown('<div class="stat-card"><div class="stat-number">100%</div><div class="stat-label">Personalisasi Kriteria</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="stat-card"><div class="stat-number">Akurat</div><div class="stat-label">Algoritma Weighted Product</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div class="stat-card"><div class="stat-number">Cepat</div><div class="stat-label">Rekomendasi Seketika</div></div>', unsafe_allow_html=True)
        
    st.write("")
    st.write("")
    
    # PENJELASAN CARA KERJA (STEP BY STEP)
    st.markdown("<h3 style='text-align: center; color: #0F172A; font-weight: 800; margin-bottom: 25px;'>Bagaimana DietWise Membantu Anda?</h3>", unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown("""
            <div class="step-card">
                <div class="step-number">1</div>
                <div class="step-title">Masukkan Profil</div>
                <div class="step-desc">Tentukan nama Anda dan tentukan kriteria utama (misal: lebih butuh murah, atau butuh protein tinggi).</div>
            </div>
        """, unsafe_allow_html=True)
    with col_s2:
        st.markdown("""
            <div class="step-card">
                <div class="step-number">2</div>
                <div class="step-title">Perhitungan Matematika</div>
                <div class="step-desc">Sistem memproses seluruh pilihan makanan menggunakan metode Weighted Product (WP) secara akurat.</div>
            </div>
        """, unsafe_allow_html=True)
    with col_s3:
        st.markdown("""
            <div class="step-card">
                <div class="step-number">3</div>
                <div class="step-title">Hasil Rekomendasi</div>
                <div class="step-desc">Dapatkan urutan peringkat menu makanan sehat terbaik lengkap dengan perincian gizi dan harganya.</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    st.write("")
    
    # Tombol Utama di Tengah
    st.markdown('<div style="display: flex; justify-content: center; margin-top: 10px;">', unsafe_allow_html=True)
    if st.button("🚀 Mulai Cari Rekomendasi Menu Sekarang", key="btn_home"):
        st.session_state.halaman = 'kriteria'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. HALAMAN 2: ATUR KRITERIA (LENGKAP & RAMAH AWAM)
# ==========================================
elif st.session_state.halaman == 'kriteria':
    
    st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h2 style="color: #0F172A; font-weight: 800; font-size: 2.2rem;">Atur Profil & Prioritas Makanan Anda</h2>
            <p style="color: #475569; font-size: 1.05rem; max-width: 700px; margin: 0 auto;">
                Setiap orang memiliki kebutuhan diet yang berbeda. Atur tingkat kepentingan kriteria di bawah ini agar sistem dapat menyajikan rekomendasi yang paling cocok untuk Anda.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_input1, col_input2 = st.columns([1, 1.2], gap="large")
    
    with col_input1:
        st.markdown("<h3 style='color: #0F172A; font-weight: 800;'>1. Identitas Pengguna</h3>", unsafe_allow_html=True)
        nama = st.text_input("Nama Lengkap atau Panggilan Anda:", value="", placeholder="Contoh: Budi Prasetyo")
        
        st.markdown("""
        <div class="info-guide-box">
            <h4 style="margin: 0 0 10px 0; font-weight: 800; color: #1E3A8A;">📘 Panduan Pengisian Tingkat Prioritas:</h4>
            <p style="margin-0; font-size: 0.92rem; line-height: 1.6; color: #1E3A8A;">
                <b>Skala 1 (Kurang Penting):</b> Anda tidak terlalu memikirkan poin kriteria tersebut.<br>
                <b>Skala 5 (Sangat Penting):</b> Kriteria tersebut wajib menjadi prioritas paling utama dalam pemilihan makanan Anda.<br><br>
                <i>Contoh: Jika tanggal tua dan budget terbatas, geser slider <b>Harga Murah</b> ke angka <b>5</b>.</i>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_input2:
        st.markdown("<h3 style='color: #0F172A; font-weight: 800;'>2. Tentukan Bobot Prioritas (Skala 1 - 5)</h3>", unsafe_allow_html=True)
        
        w_harga = st.slider("💰 Prioritas Harga Murah", 1, 5, 3, help="Semakin tinggi angka, semakin sistem memprioritaskan makanan berharga terjangkau.")
        w_kalori = st.slider("🔥 Prioritas Kecukupan Kalori", 1, 5, 3, help="Semakin tinggi angka, semakin sistem memprioritaskan makanan yang mengenyangkan.")
        w_protein = st.slider("💪 Prioritas Kadar Protein Tinggi", 1, 5, 4, help="Semakin tinggi angka, semakin sistem memprioritaskan makanan bernutrisi tinggi.")
        w_jarak = st.slider("📍 Prioritas Jarak Resto Terdekat", 1, 5, 2, help="Semakin tinggi angka, semakin sistem memprioritaskan resto terdekat dari tempat tinggal Anda.")

    st.write("")
    st.write("")
    btn_back, btn_calc = st.columns([1, 2])
    
    with btn_back:
        if st.button("⬅️ Kembali ke Beranda"):
            st.session_state.halaman = 'beranda'
            st.rerun()
            
    with btn_calc:
        if st.button("✨ Hitung Rekomendasi Menu Terbaik"):
            st.session_state.nama = nama if nama.strip() != "" else "Sahabat DietWise"
            st.session_state.weights = [w_harga, w_kalori, w_protein, w_jarak]
            st.session_state.halaman = 'hasil'
            st.rerun()

# ==========================================
# 6. HALAMAN 3: HASIL REKOMENDASI (GAMBAR PAS & BERSIH)
# ==========================================
elif st.session_state.halaman == 'hasil':
    
    nama_user = st.session_state.get('nama', 'Sahabat DietWise')
    
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <h2 style="color: #0F172A; font-weight: 800; font-size: 2.2rem;">Hasil Rekomendasi Menu Untuk {nama_user}</h2>
            <p style="color: #475569; font-size: 1rem;">
                Berikut adalah daftar makanan yang diurutkan secara matematis menggunakan kalkulasi <b>Weighted Product (WP)</b> berdasarkan prioritas Anda.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # MATEMATIKA WEIGHTED PRODUCT (WP)
    weights = st.session_state.get('weights', [3, 3, 4, 2])
    w = np.array(weights, dtype=float)
    w = w / np.sum(w) # Normalisasi Bobot
    
    # Harga & Jarak = Cost (-), Kalori & Protein = Benefit (+)
    w_cost = [-w[0], w[1], w[2], -w[3]]
    
    S = []
    for idx, row in df_menu.iterrows():
        val = (row['Harga'] ** w_cost[0]) * (row['Kalori'] ** w_cost[1]) * (row['Protein'] ** w_cost[2]) * (row['Jarak'] ** w_cost[3])
        S.append(val)
        
    df_result = df_menu.copy()
    df_result['S'] = S
    df_result['Skor V'] = df_result['S'] / sum(S)
    df_result = df_result.sort_values(by='Skor V', ascending=False).reset_index(drop=True)
    df_result['Rank'] = df_result.index + 1
    
    # REKOMENDASI UTAMA (PERINGKAT #1)
    top = df_result.iloc[0]
    
    st.markdown("<h3 style='color: #0F172A; font-weight: 800; margin-bottom: 12px;'>🏆 Rekomendasi Makanan Utama (Peringkat #1)</h3>", unsafe_allow_html=True)
    
    st.markdown('<div class="food-card">', unsafe_allow_html=True)
    c_img, c_detail = st.columns([1, 1.4], gap="large")
    with c_img:
        st.image(top['Gambar'], use_column_width=True)
    with c_detail:
        st.markdown(f'<span class="rank-badge-primary">REKOMENDASI TERBAIK (SKOR WP: {top["Skor V"]:.4f})</span>', unsafe_allow_html=True)
        st.markdown(f"<h2 style='margin:0 0 8px 0; color:#0F172A; font-weight:800;'>{top['Nama Menu']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#475569; margin-bottom: 15px; font-size: 0.95rem;'>{top['Deskripsi']}</p>", unsafe_allow_html=True)
        
        # Grid Detail Kriteria
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
            <div class="nutrition-badge">Harga: Rp {top['Harga']:,}</div>
            <div class="nutrition-badge">Kandungan Kalori: {top['Kalori']} kcal</div>
            <div class="nutrition-badge">Kandungan Protein: {top['Protein']} gram</div>
            <div class="nutrition-badge">Jarak Restoran: {top['Jarak']} km</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 12px; padding: 14px 18px; color: #065F46; font-size: 0.92rem; line-height: 1.5;">
            <b>Alasan Penilaian Terbaik:</b><br>
            Menu <b>{top['Nama Menu']}</b> menempati urutan teratas karena memiliki nilai paling seimbang antara tingkat kecukupan gizi dan efisiensi biaya sebesar Rp {top['Harga']:,} sesuai dengan batas prioritas yang diset oleh <b>{nama_user}</b>.
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    st.markdown("<h3 style='color: #0F172A; font-weight: 800; margin-bottom: 15px;'>🥗 Pilihan Menu Alternatif Lainnya</h3>", unsafe_allow_html=True)
    
    # GRID KARTU MENU LAINNYA (PERINGKAT 2 DSB)
    cols = st.columns(2, gap="large")
    for i in range(1, len(df_result)):
        row = df_result.iloc[i]
        with cols[(i-1) % 2]:
            st.markdown('<div class="food-card">', unsafe_allow_html=True)
            img_col, info_col = st.columns([1, 1.2])
            with img_col:
                st.image(row['Gambar'], use_column_width=True)
            with info_col:
                st.markdown(f'<span class="rank-badge-secondary">Peringkat #{row["Rank"]}</span>', unsafe_allow_html=True)
                st.markdown(f"<h4 style='margin: 0 0 6px 0; color:#0F172A; font-weight: 700;'>{row['Nama Menu']}</h4>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:#64748B; font-size: 0.8rem; margin-bottom: 8px;'>{row['Deskripsi']}</p>", unsafe_allow_html=True)
                st.markdown(f"<div class='nutrition-badge' style='font-size:0.82rem;'>Harga: Rp {row['Harga']:,}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='nutrition-badge' style='font-size:0.82rem;'>Gizi: {row['Kalori']} kcal | Protein {row['Protein']}g</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='nutrition-badge' style='font-size:0.82rem;'>Jarak Resto: {row['Jarak']} km</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div style="display: flex; justify-content: center; margin-top: 20px;">', unsafe_allow_html=True)
    if st.button("🔄 Ulangi & Hitung Kriteria Baru"):
        st.session_state.halaman = 'beranda'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
