import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# 1. KONFIGURASI HALAMAN & THEME
# ============================================================
st.set_page_config(
    page_title="DietWise — Rekomendasi Menu Diet Smart SPK",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Injection CSS Modern (Terisolasi agar kontras teks selalu jelas)
st.markdown("""
<style>
    /* Styling Dasar & Kontras Teks */
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Custom Navbar Header */
    .nav-header {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        padding: 20px 30px;
        border-radius: 16px;
        color: white !important;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.3);
        margin-bottom: 25px;
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .nav-logo-icon {
        background: white;
        width: 50px;
        height: 50px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .nav-title {
        font-size: 26px;
        font-weight: 800;
        margin: 0;
        color: #ffffff !important;
        letter-spacing: -0.5px;
    }
    .nav-subtitle {
        font-size: 13px;
        margin: 0;
        color: #D1FAE5 !important;
    }

    /* Card Component Modern */
    .custom-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    
    /* Menu Card Styling */
    .menu-card-title {
        font-size: 22px;
        font-weight: 700;
        color: #0F172A !important;
        margin-bottom: 8px;
    }
    .badge-wp {
        background: #FEF3C7;
        color: #B45309 !important;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 14px;
        display: inline-block;
        border: 1px solid #FDE68A;
    }
    .badge-category {
        background: #E0E7FF;
        color: #4338CA !important;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        margin-left: 8px;
    }

    /* Metric Grid Box */
    .metric-box {
        background: #F8FAFC;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        border: 1px solid #F1F5F9;
    }
    .metric-label {
        font-size: 12px;
        color: #64748B !important;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 16px;
        font-weight: 700;
        color: #1E293B !important;
        margin-top: 4px;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #FFFFFF;
        border-radius: 10px;
        color: #475569;
        font-weight: 600;
        border: 1px solid #E2E8F0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #10B981 !important;
        color: white !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 2. NAVBAR & HEADER DENGAN LOGO TERINTEGRASI
# ============================================================
def tampilkan_navbar():
    st.markdown("""
    <div class="nav-header">
        <div class="nav-brand">
            <div class="nav-logo-icon">🥗</div>
            <div>
                <p class="nav-title">DietWise</p>
                <p class="nav-subtitle">Sistem Rekomendasi Menu Diet Harian — Weighted Product (WP)</p>
            </div>
        </div>
        <div>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 14px; border-radius: 20px; font-size: 12px; color: white; font-weight: 600;">SPK Smart Engine</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 3. DATASET DENGAN GAMBAR ACCURATE 100% (DIRECT UNSPLASH IDs)
# ============================================================
def muat_dataset():
    data = {
        'Nama Menu': [
            'Oatmeal Pisang & Susu Rendah Lemak',
            'Telur Dadar & Tumis Kangkung',
            'Roti Gandum Selai Kacang',
            'Bubur Kacang Hijau Manis',
            'Nasi Ayam Rebus & Sayur Bening',
            'Gado-Gado Surabaya Khas',
            'Nasi Merah & Tumis Tahu Tempe Brokoli',
            'Soto Ayam Bening Madura',
            'Ikan Salmon Panggang & Kentang',
            'Sup Ayam Sayuran Segar',
            'Capcay Seafood Kuah Kental',
            'Dada Ayam Panggang & Brokoli'
        ],
        'Waktu': [
            'Pagi', 'Pagi', 'Pagi', 'Pagi',
            'Siang', 'Siang', 'Siang', 'Siang',
            'Malam', 'Malam', 'Malam', 'Malam'
        ],
        'Harga': [10000, 12000, 8000, 7000, 15000, 12000, 13000, 15000, 28000, 14000, 18000, 22000],
        'Kalori': [380, 350, 300, 280, 420, 320, 380, 350, 410, 300, 280, 320],
        'Protein': [12, 22, 10, 8, 28, 12, 20, 18, 32, 18, 20, 35],
        'Karbo': [55, 5, 40, 45, 60, 30, 55, 40, 20, 15, 25, 8],
        'Lemak': [8, 15, 12, 3, 10, 14, 9, 8, 22, 6, 7, 5],
        'Jarak': [1.0, 1.5, 0.8, 0.6, 1.2, 1.0, 0.9, 1.6, 2.0, 1.1, 1.4, 1.3],
        'Kategori': [
            'Vegetarian', 'Halal', 'Vegetarian', 'Vegetarian',
            'Halal', 'Vegetarian', 'Vegetarian', 'Halal',
            'Halal', 'Halal', 'Halal', 'Halal'
        ],
        # Direct Verified Image URLs (Resized & Crop Optimized)
        'Gambar': [
            'https://images.unsplash.com/photo-1517673400267-0251440c45dc?auto=format&fit=crop&w=600&q=80',  # Oatmeal
            'https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=600&q=80',  # Omelette/Telur
            'https://images.unsplash.com/photo-1509722747041-616f39b57569?auto=format&fit=crop&w=600&q=80',  # Toast
            'https://images.unsplash.com/photo-1541832676-9b763b0239ab?auto=format&fit=crop&w=600&q=80',  # Porridge/Bubur
            'https://images.unsplash.com/photo-1598515213692-5f252be82273?auto=format&fit=crop&w=600&q=80',  # Chicken Rice
            'https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=600&q=80',  # Salad/Gado-gado
            'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80',  # Healthy Bowl
            'https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=600&q=80',  # Soup/Soto
            'https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=600&q=80',  # Salmon
            'https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=600&q=80',  # Vegetable Soup
            'https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=600&q=80',  # Capcay/Stirfry
            'https://images.unsplash.com/photo-1532550907401-a500c9a57435?auto=format&fit=crop&w=600&q=80'   # Grilled Chicken
        ],
        'Deskripsi': [
            'Serat tinggi dari oat dan pisang untuk energi tahan lama di pagi hari.',
            'Sumber protein praktis dipadu serat kangkung yang segar.',
            'Karbohidrat kompleks yang mengenyangkan dan cepat disiapkan.',
            'Bubur hangat kayak protein nabati dan serat alami.',
            'Kombinasi klasik kaya protein tanpa lemak berlebih.',
            'Sayuran segar dengan saus kacang tinggi gizi.',
            'Nasi merah kaya serat dipadu kebaikan tahu, tempe, dan brokoli.',
            'Soto hangat yang kaya rempah alami pembakar metabolisme.',
            'Tinggi Omega-3 dan protein premium untuk pemulihan jaringan tubuh.',
            'Sup hangat rendah kalori yang kaya vitamin & mineral.',
            'Aneka aneka sayur dan seafood segar tinggi protein.',
            'Menu diet paling efektif: dada ayam tinggi protein & brokoli serat.'
        ]
    }
    return pd.DataFrame(data)

# ============================================================
# 4. ALGORITMA WEIGHTED PRODUCT (WP)
# ============================================================
def hitung_wp(df_subset, bobot_dict):
    W = [bobot_dict['Harga'], bobot_dict['Kalori'], bobot_dict['Protein'], bobot_dict['Jarak']]
    total_bobot = sum(W)
    w_normal = [w / total_bobot for w in W]
    pangkat = [-w_normal[0], w_normal[1], w_normal[2], -w_normal[3]]  # Harga & Jarak = Cost

    kolom_kriteria = ['Harga', 'Kalori', 'Protein', 'Jarak']
    daftar_S = []
    for _, row in df_subset.iterrows():
        nilai = [row[k] for k in kolom_kriteria]
        S = 1
        for x, w in zip(nilai, pangkat):
            S *= (x ** w)
        daftar_S.append(S)

    total_S = sum(daftar_S)
    daftar_V = [s / total_S for s in daftar_S]

    hasil = df_subset.copy()
    hasil['Vektor_S'] = daftar_S
    hasil['Vektor_V'] = daftar_V
    hasil['Rank'] = hasil['Vektor_V'].rank(ascending=False).astype(int)
    hasil = hasil.sort_values(by='Vektor_V', ascending=False).reset_index(drop=True)

    detail = {
        'kriteria': ['Harga (Cost)', 'Kalori (Benefit)', 'Protein (Benefit)', 'Jarak (Cost)'],
        'bobot_mentah': W,
        'bobot_normal': w_normal
    }
    return hasil, detail

# ============================================================
# 5. INITIALIZATION STATE
# ============================================================
if 'halaman' not in st.session_state: st.session_state.halaman = 'beranda'
if 'nama_user' not in st.session_state: st.session_state.nama_user = ''
if 'bobot' not in st.session_state: st.session_state.bobot = None
if 'filter_kategori' not in st.session_state: st.session_state.filter_kategori = 'Semua'

df_menu = muat_dataset()
tampilkan_navbar()

# ============================================================
# HALAMAN 1 — BERANDA MODERN
# ============================================================
if st.session_state.halaman == 'beranda':
    
    st.markdown("""
    <div style="text-align: center; padding: 30px 10px;">
        <h1 style="font-size: 38px; font-weight: 800; color: #0F172A; margin-bottom: 10px;">
            Rencanakan Menu Diet Sehatmu Secara Presisi ✨
        </h1>
        <p style="font-size: 16px; color: #64748B; max-width: 700px; margin: 0 auto;">
            Sistem Pendukung Keputusan pintar yang menghitung kombinasi <b>Makan Pagi, Siang, dan Malam</b> paling ideal berdasarkan anggaran, nutrisi, dan jarak terdekatmu.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 40px; margin-bottom: 10px;">📅</div>
            <h3 style="color: #1E293B; font-size: 18px; margin-bottom: 8px;">Paket Pagi-Siang-Malam</h3>
            <p style="color: #64748B; font-size: 13px;">Rekomendasi spesifik disesuaikan dengan waktu makan harianmu secara lengkap.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 40px; margin-bottom: 10px;">🥗</div>
            <h3 style="color: #1E293B; font-size: 18px; margin-bottom: 8px;">Nutrisi Makro Lengkap</h3>
            <p style="color: #64748B; font-size: 13px;">Kalkulasi Kalori, Protein, Karbohidrat, hingga Lemak secara transparan.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 40px; margin-bottom: 10px;">📐</div>
            <h3 style="color: #1E293B; font-size: 18px; margin-bottom: 8px;">Metode Matematika WP</h3>
            <p style="color: #64748B; font-size: 13px;">Menggunakan pembobotan kriteria Weighted Product yang akurat & objektif.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    _, col_btn, _ = st.columns([1, 1.5, 1])
    with col_btn:
        if st.button("🚀 Mulai Cari Rekomendasi Menu", use_container_width=True, type="primary"):
            st.session_state.halaman = 'kriteria'
            st.rerun()

# ============================================================
# HALAMAN 2 — FORM PREFERENSI & KRITERIA
# ============================================================
elif st.session_state.halaman == 'kriteria':

    st.markdown("## 🎛️ Atur Kriteria & Preferences")
    st.write("Isi identitas dan tentukan seberapa penting masing-masing faktor bagi dietmu.")

    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### 👤 Data Diri Pengguna")
        col_a, col_b = st.columns(2)
        with col_a:
            nama_input = st.text_input("Nama Lengkap Kamu", placeholder="Contoh: Budi Santoso")
        with col_b:
            filter_kategori = st.selectbox("Filter Jenis Makanan", ["Semua", "Halal", "Vegetarian"])
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### ⚖️ Bobot Prioritas Kriteria (Skala 1 - 5)")
        st.info("💡 **Petunjuk:** Angka 1 = Tidak Terlalu Penting | Angka 5 = Sangat Penting & Prioritas Utama")

        col1, col2 = st.columns(2)
        with col1:
            bobot_harga = st.slider("💰 Prioritas Harga (Murah)", 1, 5, 3)
            bobot_kalori = st.slider("🔥 Prioritas Kalori (Optimal)", 1, 5, 4)
        with col2:
            bobot_protein = st.slider("💪 Prioritas Protein (Tinggi)", 1, 5, 5)
            bobot_jarak = st.slider("📍 Prioritas Jarak Akses (Dekat)", 1, 5, 2)
        st.markdown('</div>', unsafe_allow_html=True)

    _, col_btn, _ = st.columns([1, 1.5, 1])
    with col_btn:
        if st.button("✨ Hitung Rekomendasi Sekarang", use_container_width=True, type="primary"):
            if not nama_input.strip():
                st.warning("⚠️ Silakan isi nama kamu terlebih dahulu.")
            else:
                st.session_state.nama_user = nama_input
                st.session_state.filter_kategori = filter_kategori
                st.session_state.bobot = {
                    'Harga': bobot_harga, 'Kalori': bobot_kalori,
                    'Protein': bobot_protein, 'Jarak': bobot_jarak
                }
                st.session_state.halaman = 'hasil'
                st.rerun()

# ============================================================
# HALAMAN 3 — HASIL REKOMENDASI LENGKAP & VISUAL
# ============================================================
elif st.session_state.halaman == 'hasil':

    if not st.session_state.bobot:
        st.warning("⚠️ Data preferensi tidak ditemukan.")
        if st.button("⬅ Kembali ke Beranda"):
            st.session_state.halaman = 'beranda'
            st.rerun()
    else:
        st.markdown(f"""
        <div style="background: #ECFDF5; border: 1px solid #A7F3D0; padding: 16px 20px; border-radius: 12px; margin-bottom: 20px;">
            <h3 style="color: #065F46; margin:0; font-size: 20px;">🎉 Rekomendasi Menu Harian Untuk <b>{st.session_state.nama_user}</b></h3>
            <p style="color: #047857; margin: 4px 0 0 0; font-size: 13px;">Urutan kombinasi menu makanan terbaik berdasarkan hasil kalkulasi algoritma Weighted Product (WP)</p>
        </div>
        """, unsafe_allow_html=True)

        df_filtered = df_menu.copy()
        if st.session_state.filter_kategori != "Semua":
            df_filtered = df_filtered[df_filtered['Kategori'] == st.session_state.filter_kategori]

        tab_pagi, tab_siang, tab_malam = st.tabs(["🌅 Makan Pagi", "☀️ Makan Siang", "🌙 Makan Malam"])
        tab_map = {"Pagi": tab_pagi, "Siang": tab_siang, "Malam": tab_malam}

        for waktu, tab in tab_map.items():
            with tab:
                subset = df_filtered[df_filtered['Waktu'] == waktu].reset_index(drop=True)

                if len(subset) == 0:
                    st.warning(f"Tidak ada menu {waktu.lower()} yang sesuai dengan filter kategori '{st.session_state.filter_kategori}'.")
                    continue

                hasil, detail = hitung_wp(subset, st.session_state.bobot)
                terbaik = hasil.iloc[0]

                # MENU PERINGKAT PERTAMA (WINNER CARD)
                st.markdown(f"#### 🏆 Menu {waktu} Terbaik (Peringkat #1)")
                
                with st.container():
                    col_img, col_detail = st.columns([1.2, 2])
                    
                    with col_img:
                        st.image(terbaik['Gambar'], use_container_width=True)
                    
                    with col_detail:
                        st.markdown(f"""
                        <div class="menu-card-title">{terbaik['Nama Menu']}</div>
                        <div>
                            <span class="badge-wp">SKOR AKHIR WP: {terbaik['Vektor_V']:.4f}</span>
                            <span class="badge-category">{terbaik['Kategori']}</span>
                        </div>
                        <p style="color: #475569; font-size: 14px; margin-top: 12px;">{terbaik['Deskripsi']}</p>
                        """, unsafe_allow_html=True)

                        st.write("")
                        m1, m2, m3, m4 = st.columns(4)
                        with m1:
                            st.markdown(f"""
                            <div class="metric-box">
                                <div class="metric-label">💰 Harga</div>
                                <div class="metric-value">Rp {terbaik['Harga']:,}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with m2:
                            st.markdown(f"""
                            <div class="metric-box">
                                <div class="metric-label">🔥 Kalori</div>
                                <div class="metric-value">{terbaik['Kalori']} kcal</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with m3:
                            st.markdown(f"""
                            <div class="metric-box">
                                <div class="metric-label">💪 Protein</div>
                                <div class="metric-value">{terbaik['Protein']}g</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with m4:
                            st.markdown(f"""
                            <div class="metric-box">
                                <div class="metric-label">📍 Jarak</div>
                                <div class="metric-value">{terbaik['Jarak']} km</div>
                            </div>
                            """, unsafe_allow_html=True)

                # MENU ALTERNATIF LAINNYA
                if len(hasil) > 1:
                    st.write("")
                    st.markdown("#### 📋 Alternatif Menu Lainnya")
                    for i in range(1, len(hasil)):
                        row = hasil.iloc[i]
                        with st.container():
                            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                            c_img2, c_txt2 = st.columns([0.8, 3])
                            with c_img2:
                                st.image(row['Gambar'], use_container_width=True)
                            with c_txt2:
                                st.markdown(f"""
                                <div style="display: flex; justify-content: space-between; align-items: start;">
                                    <div>
                                        <h4 style="margin:0; color: #1E293B;">#{row['Rank']} {row['Nama Menu']}</h4>
                                        <p style="color: #64748B; font-size: 13px; margin-top: 4px;">
                                            Rp {row['Harga']:,} • {row['Kalori']} kcal • {row['Protein']}g Protein • {row['Jarak']} km
                                        </p>
                                    </div>
                                    <span style="background: #F1F5F9; color: #334155; font-weight: 700; padding: 4px 10px; border-radius: 8px; font-size: 13px;">
                                        Skor WP: {row['Vektor_V']:.4f}
                                    </span>
                                </div>
                                """, unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)

                # TRANSPARANSI PERHITUNGAN MATHEMATICS
                with st.expander("📐 Transparansi & Detail Kalkulasi Algoritma WP"):
                    st.markdown("**1. Bobot Ternormalisasi (Wj):**")
                    st.dataframe(pd.DataFrame({
                        'Kriteria': detail['kriteria'],
                        'Bobot Input': detail['bobot_mentah'],
                        'Bobot Normalisasi': [f"{w:.4f}" for w in detail['bobot_normal']]
                    }), use_container_width=True)

                    st.markdown("**2. Matriks Hasil Perhitungan (Vektor S & Vektor V):**")
                    tabel_detail = hasil[['Nama Menu', 'Vektor_S', 'Vektor_V', 'Rank']].copy()
                    tabel_detail['Vektor_S'] = tabel_detail['Vektor_S'].apply(lambda x: f"{x:.6f}")
                    tabel_detail['Vektor_V'] = tabel_detail['Vektor_V'].apply(lambda x: f"{x:.6f}")
                    st.dataframe(tabel_detail, use_container_width=True, hide_index=True)

        st.write("")
        _, col_btn, _ = st.columns([1, 1.5, 1])
        with col_btn:
            if st.button("🔄 Ulangi & Atur Kriteria Baru", use_container_width=True, type="primary"):
                st.session_state.halaman = 'kriteria'
                st.rerun()
