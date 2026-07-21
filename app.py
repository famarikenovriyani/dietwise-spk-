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
# 2. CUSTOM CSS (AESTHETIC & BALANCED)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Sembunyikan Sidebar & Header Bawaan */
[data-testid="stSidebar"], header, footer, .stDeployButton {
    display: none !important;
}

.stApp {
    background: linear-gradient(135deg, #F0FDF4 0%, #F8FAFC 50%, #EFF6FF 100%);
}

/* Container Pembatas Agar Tidak Terlalu Lebar */
.main-container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 10px;
}

/* Hero Section */
.hero-card {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
    border-radius: 20px;
    padding: 35px 25px;
    color: white;
    text-align: center;
    box-shadow: 0 10px 25px rgba(16, 185, 129, 0.2);
    margin-bottom: 20px;
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 1rem;
    opacity: 0.95;
    max-width: 600px;
    margin: 0 auto;
}

/* Tip Box */
.tip-box {
    background-color: #FFFFFF;
    border-left: 5px solid #10B981;
    border-radius: 12px;
    padding: 14px 20px;
    color: #334155;
    font-size: 0.95rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    margin-bottom: 25px;
}

/* Feature Cards */
.feature-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    text-align: center;
}

/* Label Styling Fix */
.stSlider label, .stTextInput label {
    color: #0F172A !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
}

/* Button Customizing */
div.stButton > button {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    border: none !important;
    box-shadow: 0 8px 15px rgba(16, 185, 129, 0.25) !important;
    width: 100%;
}

div.stButton > button:hover {
    transform: translateY(-2px);
}

/* Food Card Container */
.food-card-wrapper {
    background: #FFFFFF;
    border-radius: 18px;
    border: 1px solid #E2E8F0;
    padding: 16px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.04);
    margin-bottom: 20px;
}

/* Batasi Tinggi Gambar Makanan */
div[data-testid="stImage"] img {
    border-radius: 14px !important;
    max-height: 220px !important;
    object-fit: cover !important;
    width: 100% !important;
}

.rank-badge {
    background-color: #10B981;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.85rem;
    display: inline-block;
    margin-bottom: 8px;
}

.metric-box {
    background: #F8FAFC;
    border-radius: 10px;
    padding: 8px 12px;
    text-align: center;
    border: 1px solid #E2E8F0;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HELPER FUNCTIONS & DATASET
# ==========================================
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return None

logo_b64 = get_base64_image("logo_dietwise.png")

@st.cache_data
def get_menu_data():
    data = [
        {"Nama Menu": "Dada Ayam Panggang & Salad", "Harga": 25000, "Kalori": 350, "Protein": 35, "Jarak": 1.2, "Gambar": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600"},
        {"Nama Menu": "Salad Alpukat & Telur Rebus", "Harga": 20000, "Kalori": 280, "Protein": 18, "Jarak": 0.8, "Gambar": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600"},
        {"Nama Menu": "Smoothie Bowl Fruit Crunch", "Harga": 30000, "Kalori": 310, "Protein": 12, "Jarak": 2.5, "Gambar": "https://images.unsplash.com/photo-1590301157890-4810ed352733?w=600"},
        {"Nama Menu": "Ikan Salmon Panggang Lemon", "Harga": 45000, "Kalori": 420, "Protein": 40, "Jarak": 3.0, "Gambar": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=600"},
        {"Nama Menu": "Oatmeal Pisang & Chia Seed", "Harga": 15000, "Kalori": 250, "Protein": 10, "Jarak": 0.5, "Gambar": "https://images.unsplash.com/photo-1517673400267-0251440c45dc?w=600"},
        {"Nama Menu": "Tumis Tahu Tempe Brokoli", "Harga": 12000, "Kalori": 210, "Protein": 16, "Jarak": 0.4, "Gambar": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600"}
    ]
    return pd.DataFrame(data)

df_menu = get_menu_data()

if 'halaman' not in st.session_state:
    st.session_state.halaman = 'beranda'

# Wrap All Content in Centered Container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

   # ==========================================
# 4. HALAMAN 1: BERANDA ESTETIK
# ==========================================
if st.session_state.halaman == 'beranda':
    
    if logo_b64:
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 15px;">
                <img src="data:image/png;base64,{logo_b64}" style="width: 120px; height: auto;">
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="hero-card">
            <div class="hero-title">Temukan Menu Diet Idealmu ✨</div>
            <div class="hero-subtitle">
                Bingung memilih makanan sehat harian? Rekomendasi pintar kami menyesuaikan pilihan menu berdasarkan budget, kalori, protein, dan lokasi terdekatmu!
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="tip-box">
            💡 <b>Tips Diet Hari Ini:</b> Konsumsi air putih minimal 2 Liter per hari untuk menjaga metabolisme tubuh Anda tetap optimal selama menjalani diet cerdas.
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
            <div class="feature-card">
                <div style="font-size: 2.2rem;">💰</div>
                <h4 style="color: #0F172A; margin: 8px 0;">Ramah Kantong</h4>
                <p style="color: #64748B; font-size: 0.85rem; margin: 0;">Sesuaikan preferensi menu sehat berdasarkan isi dompet harianmu.</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="feature-card">
                <div style="font-size: 2.2rem;">🥗</div>
                <h4 style="color: #0F172A; margin: 8px 0;">Target Nutrisi</h4>
                <p style="color: #64748B; font-size: 0.85rem; margin: 0;">Hitung keseimbangan kalori dan asupan protein yang tepat.</p>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="feature-card">
                <div style="font-size: 2.2rem;">📍</div>
                <h4 style="color: #0F172A; margin: 8px 0;">Jarak Terdekat</h4>
                <p style="color: #64748B; font-size: 0.85rem; margin: 0;">Cari resto terdekat agar perjalanan kuliner sehat lebih mudah.</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    st.write("")
    
    # TOMBOL PRESISI DI TENGAH
    st.markdown('<div style="display: flex; justify-content: center; margin-top: 20px;">', unsafe_allow_html=True)
    if st.button("🚀 Mulai Cari Rekomendasi Menu", key="btn_center"):
        st.session_state.halaman = 'kriteria'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. HALAMAN 2: FORM KRITERIA
# ==========================================
elif st.session_state.halaman == 'kriteria':
    
    st.markdown("""
        <div style="text-align: center; margin-bottom: 25px;">
            <h2 style="color: #0F172A; font-weight: 800;">⚙️ Atur Profil & Kriteria Diet Anda</h2>
            <p style="color: #64748B;">Isi nama Anda dan tentukan tingkat prioritas makanan yang Anda inginkan saat ini.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_input1, col_input2 = st.columns([1, 1.2])
    
    with col_input1:
        st.markdown("### 👤 Informasi Pengguna")
        nama = st.text_input("Silakan Masukkan Nama Lengkap / Panggilan Anda:", value="", placeholder="Contoh: Budi Prasetyo")
        
        st.info("""
        💡 **Petunjuk Pengisian Slider:**
        * **Nilai 1:** Kurang Diprioritaskan
        * **Nilai 5:** Sangat Diprioritaskan (Paling Penting)
        
        Sistem Weighted Product (WP) akan otomatis menghitung makanan mana yang paling cocok dengan prioritas nilai yang Anda tentukan.
        """)
        
    with col_input2:
        st.markdown("### ⚖️ Tingkat Prioritas (Skala 1 - 5)")
        w_harga = st.slider("💰 Utamakan Harga Murah", 1, 5, 3)
        w_kalori = st.slider("🔥 Utamakan Kecukupan Kalori", 1, 5, 3)
        w_protein = st.slider("💪 Utamakan Protein Tinggi", 1, 5, 4)
        w_jarak = st.slider("📍 Utamakan Jarak Dekat", 1, 5, 2)

    st.write("")
    btn_back, btn_calc = st.columns([1, 2])
    
    with btn_back:
        if st.button("⬅️ Kembali"):
            st.session_state.halaman = 'beranda'
            st.rerun()
            
    with btn_calc:
        if st.button("✨ Hitung Rekomendasi Menu Sekarang"):
            st.session_state.nama = nama if nama.strip() != "" else "Sahabat DietWise"
            st.session_state.weights = [w_harga, w_kalori, w_protein, w_jarak]
            st.session_state.halaman = 'hasil'
            st.rerun()

# ==========================================
# 6. HALAMAN 3: HASIL REKOMENDASI (RAPI & LENGKAP)
# ==========================================
elif st.session_state.halaman == 'hasil':
    
    nama_user = st.session_state.get('nama', 'Sahabat DietWise')
    
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 25px;">
            <h2 style="color: #0F172A; font-weight: 800;">🎉 Rekomendasi Menu Diet Untuk {nama_user}</h2>
            <p style="color: #64748B;">Hasil kalkulasi perangkingan menggunakan algoritma <b>Weighted Product (WP)</b></p>
        </div>
    """, unsafe_allow_html=True)
    
    # PERHITUNGAN WP
    weights = st.session_state.get('weights', [3, 3, 4, 2])
    w = np.array(weights, dtype=float)
    w = w / np.sum(w)
    
    # Cost (Harga, Jarak) & Benefit (Kalori, Protein)
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
    
    # 🏆 MENU TERBAIK (RANK #1)
    top = df_result.iloc[0]
    st.markdown("### 🏆 Rekomendasi Utama (Peringkat #1)")
    
    st.markdown('<div class="food-card-wrapper">', unsafe_allow_html=True)
    c_img, c_detail = st.columns([1, 1.5])
    with c_img:
        st.image(top['Gambar'], use_column_width=True)
    with c_detail:
        st.markdown(f'<span class="rank-badge">SKOR AKHIR WP: {top["Skor V"]:.4f}</span>', unsafe_allow_html=True)
        st.markdown(f"<h2 style='margin:0 0 10px 0; color:#0F172A;'>{top['Nama Menu']}</h2>", unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("💰 Harga", f"Rp {top['Harga']:,}")
        m2.metric("🔥 Kalori", f"{top['Kalori']} kcal")
        m3.metric("💪 Protein", f"{top['Protein']} g")
        m4.metric("📍 Jarak", f"{top['Jarak']} km")
        
        st.success(f"**Kenapa Pilihan Ini Terbaik?**\nMenu **{top['Nama Menu']}** memiliki kombinasi paling optimal antara nilai gizi dan harga Rp {top['Harga']:,} sesuai dengan bobot prioritas yang {nama_user} tentukan!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    st.markdown("### 🥗 Pilihan Alternatif Lainnya")
    
    # GRID KARTU UNTUK MENU PERINGKAT DUA DSB.
    cols = st.columns(2)
    for i in range(1, len(df_result)):
        row = df_result.iloc[i]
        with cols[(i-1) % 2]:
            st.markdown('<div class="food-card-wrapper">', unsafe_allow_html=True)
            img_col, info_col = st.columns([1, 1.2])
            with img_col:
                st.image(row['Gambar'], use_column_width=True)
            with info_col:
                st.markdown(f'<span class="rank-badge" style="background:#64748B;">Peringkat #{row["Rank"]}</span>', unsafe_allow_html=True)
                st.markdown(f"<h4 style='margin: 0 0 5px 0; color:#0F172A;'>{row['Nama Menu']}</h4>", unsafe_allow_html=True)
                st.markdown(f"**💰 Harga:** Rp {row['Harga']:,}")
                st.markdown(f"**🔥 Kalori:** {row['Kalori']} kcal | **💪 Protein:** {row['Protein']}g")
                st.markdown(f"**📍 Jarak Lokasi:** {row['Jarak']} km")
                st.caption(f"Skor WP: {row['Skor V']:.4f}")
            st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    _, col_reset, _ = st.columns([1, 1.5, 1])
    with col_reset:
        if st.button("🔄 Ulangi & Atur Kriteria Baru"):
            st.session_state.halaman = 'beranda'
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
