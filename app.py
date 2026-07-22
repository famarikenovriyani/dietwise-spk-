import streamlit as st
import pandas as pd
import numpy as np
import os
import base64

# ==========================================
# 1. KONFIGURASI HALAMAN & PAGE TITLE
# ==========================================
st.set_page_config(
    page_title="DietWise — Smart Healthy Meal Planner",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. STYLING CSS (AESTHETIC, CLEAN & MODERN)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Sembunyikan Header & Sidebar Bawaan Streamlit */
[data-testid="stSidebar"], header, footer, .stDeployButton {
    display: none !important;
}

.stApp {
    background: linear-gradient(135deg, #F0FDF4 0%, #F8FAFC 50%, #EFF6FF 100%);
}

.main-container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 10px;
}

/* Navbar Custom */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #FFFFFF;
    padding: 12px 25px;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    margin-bottom: 25px;
    border: 1px solid #E2E8F0;
}

.navbar-brand {
    font-size: 1.3rem;
    font-weight: 800;
    color: #10B981;
    display: flex;
    align-items: center;
    gap: 8px;
}

.navbar-badge {
    background-color: #E0E7FF;
    color: #3730A3;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 20px;
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
    max-width: 650px;
    margin: 0 auto;
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

/* Food Card Container */
.food-card-wrapper {
    background: #FFFFFF;
    border-radius: 18px;
    border: 1px solid #E2E8F0;
    padding: 18px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.04);
    margin-bottom: 20px;
}

div[data-testid="stImage"] img {
    border-radius: 14px !important;
    max-height: 200px !important;
    object-fit: cover !important;
    width: 100% !important;
}

.rank-badge {
    background-color: #10B981;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.8rem;
    display: inline-block;
    margin-bottom: 8px;
}

.tag-badge {
    background-color: #F1F5F9;
    color: #475569;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-right: 5px;
}

/* Custom Button */
div.stButton > button {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    border: none !important;
    box-shadow: 0 8px 15px rgba(16, 185, 129, 0.25) !important;
}

div.stButton > button:hover {
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. DATASET MENU MAKANAN (LENGKAP)
# ==========================================
@st.cache_data
def get_menu_data():
    data = [
        # MEAL PAGI
        {"Nama Menu": "Oatmeal Pisang & Chia Seed", "Waktu": "Pagi", "Harga": 15000, "Kalori": 250, "Protein": 10, "Karbo": 42, "Lemak": 5, "Jarak": 0.5, "Kategori": "Halal / Vegetarian", "Gambar": "https://images.unsplash.com/photo-1517673400267-0251440c45dc?w=600"},
        {"Nama Menu": "Roti Gandum Alpukat & Telur", "Waktu": "Pagi", "Harga": 18000, "Kalori": 310, "Protein": 14, "Karbo": 30, "Lemak": 12, "Jarak": 1.0, "Kategori": "Halal / Vegetarian", "Gambar": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=600"},
        {"Nama Menu": "Smoothie Bowl Fruit Crunch", "Waktu": "Pagi", "Harga": 28000, "Kalori": 290, "Protein": 9, "Karbo": 48, "Lemak": 6, "Jarak": 2.1, "Kategori": "Halal / Vegetarian", "Gambar": "https://images.unsplash.com/photo-1590301157890-4810ed352733?w=600"},
        
        # MEAL SIANG
        {"Nama Menu": "Dada Ayam Panggang & Salad", "Waktu": "Siang", "Harga": 25000, "Kalori": 380, "Protein": 38, "Karbo": 15, "Lemak": 8, "Jarak": 1.2, "Kategori": "Halal", "Gambar": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=600"},
        {"Nama Menu": "Ikan Salmon Panggang Lemon", "Waktu": "Siang", "Harga": 45000, "Kalori": 430, "Protein": 42, "Karbo": 10, "Lemak": 18, "Jarak": 3.0, "Kategori": "Halal", "Gambar": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=600"},
        {"Nama Menu": "Nasi Merah Tumis Ayam Brokoli", "Waktu": "Siang", "Harga": 22000, "Kalori": 410, "Protein": 30, "Karbo": 45, "Lemak": 7, "Jarak": 0.9, "Kategori": "Halal", "Gambar": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600"},

        # MEAL MALAM
        {"Nama Menu": "Tumis Tahu Tempe Brokoli", "Waktu": "Malam", "Harga": 12000, "Kalori": 220, "Protein": 16, "Karbo": 20, "Lemak": 6, "Jarak": 0.4, "Kategori": "Halal / Vegetarian", "Gambar": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600"},
        {"Nama Menu": "Salad Alpukat & Telur Rebus", "Waktu": "Malam", "Harga": 20000, "Kalori": 270, "Protein": 18, "Karbo": 12, "Lemak": 15, "Jarak": 0.8, "Kategori": "Halal / Vegetarian", "Gambar": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600"},
        {"Nama Menu": "Sup Daging Sapi Bening & Sayur", "Waktu": "Malam", "Harga": 27000, "Kalori": 320, "Protein": 25, "Karbo": 18, "Lemak": 9, "Jarak": 1.5, "Kategori": "Halal", "Gambar": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=600"}
    ]
    return pd.DataFrame(data)

df_menu = get_menu_data()

if 'halaman' not in st.session_state:
    st.session_state.halaman = 'beranda'

# Container Pembatas Utama
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# NAVBAR ATAS
st.markdown("""
    <div class="navbar">
        <div class="navbar-brand">🥗 DietWise</div>
        <div><span class="navbar-badge">SPK Weighted Product (WP)</span></div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 4. HALAMAN 1: BERANDA
# ==========================================
if st.session_state.halaman == 'beranda':
    
    st.markdown("""
        <div class="hero-card">
            <div class="hero-title">Rencanakan Menu Diet Sehari-Hari ✨</div>
            <div class="hero-subtitle">
                Sistem pendukung keputusan pintar untuk menyusun kombinasi paket Makan Pagi, Siang, dan Malam yang paling pas dengan nutrisi, budget, serta lokasi terdekatmu!
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
            <div class="feature-card">
                <div style="font-size: 2rem;">🗓️</div>
                <h4 style="color: #0F172A; margin: 8px 0;">Paket Pagi-Siang-Malam</h4>
                <p style="color: #64748B; font-size: 0.85rem; margin: 0;">Rekomendasi spesifik disesuaikan dengan waktu makan harianmu.</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="feature-card">
                <div style="font-size: 2rem;">🥗</div>
                <h4 style="color: #0F172A; margin: 8px 0;">Nutrisi Makro Lengkap</h4>
                <p style="color: #64748B; font-size: 0.85rem; margin: 0;">Menghitung Kalori, Protein, Karbohidrat, hingga Lemak secara transparan.</p>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="feature-card">
                <div style="font-size: 2rem;">📐</div>
                <h4 style="color: #0F172A; margin: 8px 0;">Metode Matematika WP</h4>
                <p style="color: #64748B; font-size: 0.85rem; margin: 0;">Menggunakan pembobotan kriteria Weighted Product yang akurat.</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    
    st.markdown('<div style="display: flex; justify-content: center; margin-top: 20px;">', unsafe_allow_html=True)
    if st.button("🚀 Mulai Cari Rekomendasi Menu", key="btn_start"):
        st.session_state.halaman = 'kriteria'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. HALAMAN 2: FORM KRITERIA & FILTER
# ==========================================
elif st.session_state.halaman == 'kriteria':
    
    st.markdown("""
        <div style="text-align: center; margin-bottom: 25px;">
            <h2 style="color: #0F172A; font-weight: 800;">⚙️ Atur Profil & Kriteria Diet Anda</h2>
            <p style="color: #64748B;">Isi data diri dan tentukan prioritas penting untuk makanan harian Anda.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_input1, col_input2 = st.columns([1, 1.2])
    
    with col_input1:
        st.markdown("### 👤 Data Pengguna & Filter")
        nama = st.text_input("Nama Lengkap / Panggilan:", value="", max_chars=25, placeholder="Contoh: Siti Aisyah")
        diet_filter = st.selectbox("Preferensi Kategori Makanan:", ["Semua Kategori", "Halal / Vegetarian Only"])
        
        st.info("""
        💡 **Petunjuk Nilai Prioritas:**
        * **1:** Kurang Diprioritaskan
        * **5:** Paling Diprioritaskan
        """)
        
    with col_input2:
        st.markdown("### ⚖️ Tingkat Prioritas Kriteria (Skala 1 - 5)")
        w_harga = st.slider("💰 Prioritas Harga Murah", 1, 5, 3)
        w_kalori = st.slider("🔥 Prioritas Kecukupan Kalori", 1, 5, 3)
        w_protein = st.slider("💪 Prioritas Protein Tinggi", 1, 5, 4)
        w_jarak = st.slider("📍 Prioritas Jarak Dekat", 1, 5, 2)

    st.write("")
    btn_back, btn_calc = st.columns([1, 2])
    
    with btn_back:
        if st.button("⬅️ Kembali"):
            st.session_state.halaman = 'beranda'
            st.rerun()
            
    with btn_calc:
        if st.button("✨ Hitung Rekomendasi Menu Sekarang"):
            st.session_state.nama = nama if nama.strip() != "" else "Pengguna"
            st.session_state.diet_filter = diet_filter
            st.session_state.weights = [w_harga, w_kalori, w_protein, w_jarak]
            st.session_state.halaman = 'hasil'
            st.rerun()

# ==========================================
# 6. HALAMAN 3: HASIL REKOMENDASI (SISTEM WP)
# ==========================================
elif st.session_state.halaman == 'hasil':
    
    nama_user = st.session_state.get('nama', 'Pengguna')
    diet_pref = st.session_state.get('diet_filter', 'Semua Kategori')
    
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 25px;">
            <h2 style="color: #0F172A; font-weight: 800;">🎉 Rekomendasi Menu Harian Untuk {nama_user}</h2>
            <p style="color: #64748B;">Urutan kombinasi menu makanan terbaik berdasarkan hasil kalkulasi algoritma <b>Weighted Product (WP)</b></p>
        </div>
    """, unsafe_allow_html=True)
    
    # PERHITUNGAN WP
    df_calc = df_menu.copy()
    if diet_pref == "Halal / Vegetarian Only":
        df_calc = df_calc[df_calc['Kategori'].str.contains("Vegetarian")].reset_index(drop=True)
        
    weights = st.session_state.get('weights', [3, 3, 4, 2])
    w = np.array(weights, dtype=float)
    w_norm = w / np.sum(w)  # Normalisasi Bobot
    
    # Cost (-) & Benefit (+)
    # [Harga (Cost), Kalori (Benefit), Protein (Benefit), Jarak (Cost)]
    w_cost = [-w_norm[0], w_norm[1], w_norm[2], -w_norm[3]]
    
    S_list = []
    for idx, row in df_calc.iterrows():
        val = (row['Harga'] ** w_cost[0]) * (row['Kalori'] ** w_cost[1]) * (row['Protein'] ** w_cost[2]) * (row['Jarak'] ** w_cost[3])
        S_list.append(val)
        
    df_calc['S'] = S_list
    total_S = sum(S_list)
    df_calc['Skor V'] = df_calc['S'] / total_S if total_S > 0 else 0
    df_calc = df_calc.sort_values(by='Skor V', ascending=False).reset_index(drop=True)
    
    # TAB NAVIGASI WAKTU MAKAN
    tab_pagi, tab_siang, tab_malam = st.tabs(["🌅 Makan Pagi", "☀️ Makan Siang", "🌙 Makan Malam"])
    
    def render_meal_section(waktu_makan):
        df_sub = df_calc[df_calc['Waktu'] == waktu_makan].reset_index(drop=True)
        if len(df_sub) == 0:
            st.warning(f"Tidak ada menu untuk waktu {waktu_makan} sesuai filter Anda.")
            return
            
        top = df_sub.iloc[0]
        st.markdown(f"### 🏆 Menu {waktu_makan} Pilihan Utama (Peringkat #1)")
        
        st.markdown('<div class="food-card-wrapper">', unsafe_allow_html=True)
        c_img, c_detail = st.columns([1, 1.4])
        with c_img:
            st.image(top['Gambar'], use_column_width=True)
        with c_detail:
            st.markdown(f'<span class="rank-badge">SKOR AKHIR WP: {top["Skor V"]:.4f}</span>', unsafe_allow_html=True)
            st.markdown(f'<span class="tag-badge">{top["Kategori"]}</span>', unsafe_allow_html=True)
            st.markdown(f"<h3 style='margin:8px 0; color:#0F172A;'>{top['Nama Menu']}</h3>", unsafe_allow_html=True)
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("💰 Harga", f"Rp {top['Harga']:,}")
            m2.metric("🔥 Kalori", f"{top['Kalori']} kcal")
            m3.metric("💪 Protein", f"{top['Protein']}g")
            m4.metric("📍 Jarak", f"{top['Jarak']} km")
            
            st.caption(f"📊 **Nutrisi Makro Lainnya:** Karbohidrat: **{top['Karbo']}g** | Lemak: **{top['Lemak']}g**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # MENAMPILKAN ALTERNATIF LAIN
        if len(df_sub) > 1:
            st.markdown(f"#### 🥗 Alternatif Menu {waktu_makan} Lainnya")
            grid = st.columns(2)
            for i in range(1, len(df_sub)):
                row = df_sub.iloc[i]
                with grid[(i-1) % 2]:
                    st.markdown('<div class="food-card-wrapper">', unsafe_allow_html=True)
                    st.markdown(f"**{row['Nama Menu']}** *(Rp {row['Harga']:,})*")
                    st.caption(f"Kalori: {row['Kalori']} kcal | Protein: {row['Protein']}g | Skor WP: {row['Skor V']:.4f}")
                    st.markdown('</div>', unsafe_allow_html=True)

    with tab_pagi:
        render_meal_section("Pagi")
    with tab_siang:
        render_meal_section("Siang")
    with tab_malam:
        render_meal_section("Malam")
        
    st.write("")
    
    # TRANSPARANSI PERHITUNGAN MATEMATIS WP
    with st.expander("📐 Lihat Detail Transparansi Perhitungan Algoritma WP"):
        st.markdown("#### 1. Normalisasi Bobot Kriteria ($W_j$)")
        st.write(f"Bobot Input: `[Harga={weights[0]}, Kalori={weights[1]}, Protein={weights[2]}, Jarak={weights[3]}]`")
        st.write(f"Hasil Normalisasi ($W_j$): `[Harga={w_norm[0]:.4f}, Kalori={w_norm[1]:.4f}, Protein={w_norm[2]:.4f}, Jarak={w_norm[3]:.4f}]`")
        
        st.markdown("#### 2. Matriks Vektor S & Vektor V Seluruh Alternatif")
        st.dataframe(
            df_calc[['Nama Menu', 'Waktu', 'Harga', 'Kalori', 'Protein', 'Jarak', 'S', 'Skor V']],
            use_container_width=True
        )

    st.write("")
    st.markdown('<div style="display: flex; justify-content: center; margin-top: 15px;">', unsafe_allow_html=True)
    if st.button("🔄 Ulangi & Atur Kriteria Baru"):
        st.session_state.halaman = 'beranda'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
