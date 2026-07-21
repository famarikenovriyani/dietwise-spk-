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
# 2. CUSTOM CSS & AESTHETIC STYLING
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #F8FAFC;
}

/* Sembunyikan Sidebar & Header Bawaan Streamlit */
[data-testid="stSidebar"], header, footer, .stDeployButton {
    display: none !important;
}

.stApp {
    background: linear-gradient(135deg, #F0FDF4 0%, #F8FAFC 50%, #EFF6FF 100%);
}

/* Hero Section Styling */
.hero-card {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
    border-radius: 24px;
    padding: 45px 30px;
    color: white;
    text-align: center;
    box-shadow: 0 20px 25px -5px rgba(16, 185, 129, 0.25);
    margin-bottom: 25px;
}

.hero-title {
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: 1.1rem;
    opacity: 0.95;
    max-width: 650px;
    margin: 0 auto;
    line-height: 1.6;
}

/* Tip Badge */
.tip-box {
    background-color: #FFFFFF;
    border-left: 5px solid #10B981;
    border-radius: 12px;
    padding: 14px 20px;
    color: #334155;
    font-size: 0.95rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    margin-bottom: 30px;
}

/* Card Section */
.feature-card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 24px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.03);
    text-align: center;
    transition: transform 0.2s ease;
}

/* Custom Slider Label Color Fix */
.stSlider label {
    color: #1E293B !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
}

/* Button Customizing */
div.stButton > button {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    padding: 14px 28px !important;
    border: none !important;
    box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.3) !important;
    width: 100%;
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 20px -3px rgba(16, 185, 129, 0.4) !important;
}

/* Food Card Styling */
.food-card {
    background: #FFFFFF;
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid #E2E8F0;
    box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

.badge-rank {
    background: #10B981;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 800;
    font-size: 0.85rem;
    display: inline-block;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HELPER FUNCTIONS & LOGO LOAD
# ==========================================
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return None

logo_b64 = get_base64_image("logo_dietwise.png")

# Dataset Menu Makanan + URL Gambar Estetik (Unsplash)
@st.cache_data
def get_menu_data():
    data = [
        {"Nama Menu": "Dada Ayam Panggang & Salad", "Harga": 25000, "Kalori": 350, "Protein": 35, "Jarak": 1.2, "Gambar": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500"},
        {"Nama Menu": "Salad Alpukat & Telur Rebus", "Harga": 20000, "Kalori": 280, "Protein": 18, "Jarak": 0.8, "Gambar": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=500"},
        {"Nama Menu": "Smoothie Bowl Fruit Crunch", "Harga": 30000, "Kalori": 310, "Protein": 12, "Jarak": 2.5, "Gambar": "https://images.unsplash.com/photo-1590301157890-4810ed352733?w=500"},
        {"Nama Menu": "Ikan Salmon Panggang Lemon", "Harga": 45000, "Kalori": 420, "Protein": 40, "Jarak": 3.0, "Gambar": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=500"},
        {"Nama Menu": "Oatmeal Pisang & Chia Seed", "Harga": 15000, "Kalori": 250, "Protein": 10, "Jarak": 0.5, "Gambar": "https://images.unsplash.com/photo-1517673400267-0251440c45dc?w=500"},
        {"Nama Menu": "Tumis Tahu Tempe Brokoli", "Harga": 12000, "Kalori": 210, "Protein": 16, "Jarak": 0.4, "Gambar": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=500"}
    ]
    return pd.DataFrame(data)

df_menu = get_menu_data()

# Session State Setup
if 'halaman' not in st.session_state:
    st.session_state.halaman = 'beranda'

# ==========================================
# 4. HALAMAN 1: BERANDA ESTETIK
# ==========================================
if st.session_state.halaman == 'beranda':
    
    # Logo Header
    if logo_b64:
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{logo_b64}" style="width: 130px; height: auto;">
            </div>
        """, unsafe_allow_html=True)
    
    # Hero Banner Modern
    st.markdown("""
        <div class="hero-card">
            <div class="hero-title">Temukan Menu Diet Idealmu ✨</div>
            <div class="hero-subtitle">
                Bingung mau makan sehat apa hari ini? Kami bantu hitungkan rekomendasi menu terbaik yang pas dengan budget, target nutrisi, dan jarak terdekatmu!
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Tip Box
    st.markdown("""
        <div class="tip-box">
            💡 <b>Tips Diet Hari Ini:</b> Konsumsi air putih minimal 2 Liter per hari untuk menjaga metabolisme tubuh Anda tetap optimal selama menjalani diet cerdas.
        </div>
    """, unsafe_allow_html=True)
    
    # Feature Showcase Grid
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
            <div class="feature-card">
                <div style="font-size: 2.5rem;">💸</div>
                <h4 style="color: #0F172A; margin: 10px 0 5px 0;">Hemat Anggaran</h4>
                <p style="color: #64748B; font-size: 0.9rem;">Rekomendasi disesuaikan dengan isi kantong harianmu.</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="feature-card">
                <div style="font-size: 2.5rem;">🥗</div>
                <h4 style="color: #0F172A; margin: 10px 0 5px 0;">Nutrisi Optimal</h4>
                <p style="color: #64748B; font-size: 0.9rem;">Seimbangkan kalori dan kecukupan protein tinggi.</p>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="feature-card">
                <div style="font-size: 2.5rem;">📍</div>
                <h4 style="color: #0F172A; margin: 10px 0 5px 0;">Aksesibilitas</h4>
                <p style="color: #64748B; font-size: 0.9rem;">Cari lokasi resto terdekat agar diet tidak repot.</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    st.write("")
    
    # CTA Button
    _, col_btn, _ = st.columns([1, 1.5, 1])
    with col_btn:
        if st.button("🚀 Mulai Cari Rekomendasi Menu"):
            st.session_state.halaman = 'kriteria'
            st.rerun()

# ==========================================
# 5. HALAMAN 2: FORM KRITERIA
# ==========================================
elif st.session_state.halaman == 'kriteria':
    
    st.markdown("""
        <div style="text-align: center; margin-bottom: 25px;">
            <h2 style="color: #0F172A; font-weight: 800;">⚙️ Atur Prioritas Diet Anda</h2>
            <p style="color: #64748B;">Geser slider di bawah untuk menentukan mana kriteria yang paling penting bagi Anda (Skala 1 - 5)</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.markdown("### 👤 Data Diri")
        nama = st.text_input("Nama Anda", value="Sahabat DietWise", placeholder="Masukkan nama...")
        
        st.info("""
        📌 **Keterangan Bobot:**
        * **Harga (Cost):** Makin tinggi angka, makin memprioritaskan makanan Murah.
        * **Kalori, Protein, Aksesibilitas (Benefit):** Makin tinggi angka, makin memprioritaskan nilai yang tinggi/dekat.
        """)
        
    with col_input2:
        st.markdown("### ⚖️ Tingkat Kepentingan (Bobot)")
        w_harga = st.slider("💰 Prioritas Harga Murah", 1, 5, 3)
        w_kalori = st.slider("🔥 Prioritas Kecukupan Kalori", 1, 5, 3)
        w_protein = st.slider("💪 Prioritas Kandungan Protein Tinggi", 1, 5, 4)
        w_jarak = st.slider("📍 Prioritas Jarak Dekat (Km)", 1, 5, 2)

    st.write("")
    btn_back, btn_calc = st.columns([1, 2])
    
    with btn_back:
        if st.button("⬅️ Kembali"):
            st.session_state.halaman = 'beranda'
            st.rerun()
            
    with btn_calc:
        if st.button("✨ Hitung Rekomendasi Menu Sekarang"):
            st.session_state.nama = nama
            st.session_state.weights = [w_harga, w_kalori, w_protein, w_jarak]
            st.session_state.halaman = 'hasil'
            st.rerun()

# ==========================================
# 6. HALAMAN 3: HASIL REKOMENDASI + FOTO
# ==========================================
elif st.session_state.halaman == 'hasil':
    
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <h2 style="color: #0F172A; font-weight: 800;">🎉 Rekomendasi Menu Terbaik Untuk {st.session_state.get('nama', 'Anda')}</h2>
            <p style="color: #64748B;">Berikut adalah urutan makanan sehat teratas yang dihitung khusus menggunakan algoritma Weighted Product (WP)</p>
        </div>
    """, unsafe_allow_html=True)
    
    # HITUNG WEIGHTED PRODUCT (WP)
    weights = st.session_state.get('weights', [3, 3, 4, 2])
    w = np.array(weights, dtype=float)
    w = w / np.sum(w) # Normalisasi bobot
    
    # Cost = Harga (-), Benefit = Kalori, Protein, Jarak (-)
    # (Jarak dibuat minus karena semakin kecil jarak semakin bagus)
    w_cost = [-w[0], w[1], w[2], -w[3]]
    
    # Hitung Vektor S
    S = []
    for idx, row in df_menu.iterrows():
        val = (row['Harga'] ** w_cost[0]) * (row['Kalori'] ** w_cost[1]) * (row['Protein'] ** w_cost[2]) * (row['Jarak'] ** w_cost[3])
        S.append(val)
        
    df_result = df_menu.copy()
    df_result['S'] = S
    df_result['Skor V'] = df_result['S'] / sum(S)
    df_result = df_result.sort_values(by='Skor V', ascending=False).reset_index(drop=True)
    df_result['Rank'] = df_result.index + 1
    
    # DISPLAY REKOMENDASI PERTAMA (TOP PICK CARD)
    top = df_result.iloc[0]
    st.markdown("### 🏆 Pilihan Terbaik No. 1")
    
    c_img, c_detail = st.columns([1.2, 2])
    with c_img:
        st.image(top['Gambar'], use_column_width=True, caption=top['Nama Menu'])
    with c_detail:
        st.markdown(f"## {top['Nama Menu']}")
        st.markdown(f"<span class='badge-rank'>Skor Kesesuaian WP: {top['Skor V']:.4f}</span>", unsafe_allow_html=True)
        st.write("")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("💰 Harga", f"Rp {top['Harga']:,}")
        m2.metric("🔥 Kalori", f"{top['Kalori']} kcal")
        m3.metric("💪 Protein", f"{top['Protein']} g")
        m4.metric("📍 Jarak", f"{top['Jarak']} km")
        
        st.success(f"✅ **Alasan Direkomendasikan:** Memiliki keseimbangan terbaik antara harga Rp {top['Harga']:,} dan kandungan protein tinggi ({top['Protein']}g) sesuai bobot preferensimu!")

    st.write("---")
    st.markdown("### 🥗 Pilihan Menu Lainnya")
    
    # DISPLAY CARDS UNTUK MENU LAINNYA
    cols = st.columns(3)
    for i in range(1, len(df_result)):
        row = df_result.iloc[i]
        with cols[(i-1) % 3]:
            st.image(row['Gambar'], use_column_width=True)
            st.markdown(f"#### #{row['Rank']} {row['Nama Menu']}")
            st.markdown(f"**💰 Harga:** Rp {row['Harga']:,}")
            st.markdown(f"**🔥 Kalori:** {row['Kalori']} kcal | **💪 Protein:** {row['Protein']}g")
            st.markdown(f"**📍 Jarak:** {row['Jarak']} km")
            st.caption(f"Skor WP: {row['Skor V']:.4f}")
            st.write("---")

    st.write("")
    _, col_reset, _ = st.columns([1, 1.5, 1])
    with col_reset:
        if st.button("🔄 Ulangi / Atur Ulang Kriteria"):
            st.session_state.halaman = 'beranda'
            st.rerun()
