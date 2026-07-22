import streamlit as st
import pandas as pd
import numpy as np
import os
import base64

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="DietWise",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# FUNGSI TAMPILKAN LOGO (DENGAN FALLBACK AMAN)
# ============================================================
def tampilkan_navbar():
    col_logo, col_judul = st.columns([1, 6])
    with col_logo:
        if os.path.exists("logo_dietwise.png"):
            st.image("logo_dietwise.png", width=70)
        else:
            st.markdown("## 🥗")
    with col_judul:
        st.markdown("### DietWise")
        st.caption("Sistem Pendukung Keputusan Rekomendasi Menu Diet — Metode Weighted Product")
    st.divider()


# ============================================================
# FUNGSI TAMPILKAN GAMBAR MENU (DENGAN FALLBACK IKON EMOJI)
# ============================================================
def tampilkan_gambar_menu(url_gambar, emoji_fallback, tinggi=180):
    """
    Mencoba menampilkan gambar dari URL. Apabila gambar gagal dimuat
    (link rusak/tidak ditemukan), sistem menampilkan kartu ikon emoji
    besar sebagai pengganti, agar tidak menampilkan gambar yang salah/acak.
    """
    try:
        st.image(url_gambar, use_container_width=True)
    except Exception:
        st.markdown(
            f"""
            <div style="background:#F1F5F9; border-radius:12px; height:{tinggi}px;
                        display:flex; align-items:center; justify-content:center;
                        font-size:4rem;">
                {emoji_fallback}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# DATASET MENU MAKANAN (12 MENU, 3 WAKTU MAKAN)
# ============================================================
def muat_dataset():
    data = {
        'Nama Menu': [
            'Oatmeal Pisang & Susu Rendah Lemak',
            'Telur Dadar + Tumis Kangkung',
            'Roti Gandum + Selai Kacang',
            'Bubur Kacang Hijau',
            'Nasi Ayam Rebus + Sayur',
            'Gado-Gado Sayur',
            'Nasi Merah + Tumis Tahu Tempe Brokoli',
            'Soto Ayam Bening',
            'Ikan Salmon Panggang + Kentang',
            'Sup Ayam Sayuran',
            'Capcay Seafood',
            'Dada Ayam Panggang + Brokoli'
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
        'Gambar': [
            'https://images.unsplash.com/photo-1517673400267-0251440c45dc?w=500',   # oatmeal
            'https://images.unsplash.com/photo-1607532941433-304659e8198a?w=500',   # telur dadar
            'https://images.unsplash.com/photo-1509722747041-616f39b57569?w=500',   # roti gandum
            'https://images.unsplash.com/photo-1626202157943-19f3e9d9d0a1?w=500',   # bubur
            'https://images.unsplash.com/photo-1598515213692-5f252be82273?w=500',   # nasi ayam
            'https://images.unsplash.com/photo-1540914124281-342587941389?w=500',   # gado-gado/salad sayur
            'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500',      # tahu tempe brokoli
            'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=500',      # soto/soup
            'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=500',   # salmon panggang
            'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=500',      # sup ayam
            'https://images.unsplash.com/photo-1512058564366-18510be2db19?w=500',   # capcay seafood
            'https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=500',   # dada ayam panggang
        ],
        'Emoji': ['🥣','🍳','🥪','🥣','🍛','🥗','🥦','🍜','🐟','🍲','🥘','🍗']
    }
    return pd.DataFrame(data)


# ============================================================
# FUNGSI INTI ALGORITMA WEIGHTED PRODUCT
# ============================================================
def hitung_wp(df_subset, bobot_dict):
    """
    Menjalankan metode Weighted Product pada subset data (per waktu makan).
    Mengembalikan DataFrame hasil beserta detail transparansi perhitungan.
    """
    W = [bobot_dict['Harga'], bobot_dict['Kalori'], bobot_dict['Protein'], bobot_dict['Jarak']]
    total_bobot = sum(W)
    w_normal = [w / total_bobot for w in W]
    pangkat = [-w_normal[0], w_normal[1], w_normal[2], -w_normal[3]]  # Harga & Jarak = cost

    kolom_kriteria = ['Harga', 'Kalori', 'Protein', 'Jarak']
    daftar_S = []
    for _, row in df_subset.iterrows():
        nilai_atribut = [row[k] for k in kolom_kriteria]
        S = 1
        for x, w in zip(nilai_atribut, pangkat):
            S *= x ** w
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
# SESSION STATE
# ============================================================
if 'halaman' not in st.session_state: st.session_state.halaman = 'beranda'
if 'nama_user' not in st.session_state: st.session_state.nama_user = ''
if 'bobot' not in st.session_state: st.session_state.bobot = None
if 'filter_kategori' not in st.session_state: st.session_state.filter_kategori = 'Semua'

df_menu = muat_dataset()

tampilkan_navbar()

# ============================================================
# HALAMAN 1 — BERANDA
# ============================================================
if st.session_state.halaman == 'beranda':

    st.title("🥗 Rekomendasi Menu Diet Sehat Harian")
    st.markdown(
        "Sistem ini membantu Anda menentukan menu **makan pagi, siang, dan malam** "
        "yang paling sesuai dengan preferensi Anda, menggunakan metode **Weighted Product (WP)** "
        "— mempertimbangkan harga, kalori, protein, dan jarak akses secara objektif."
    )

    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("### 🍽️ Paket Pagi–Siang–Malam")
            st.write("Rekomendasi terpisah untuk tiap waktu makan, sesuai kebutuhan harian Anda.")
    with c2:
        with st.container(border=True):
            st.markdown("### 📊 Nutrisi Lengkap")
            st.write("Setiap menu dilengkapi info kalori, protein, karbohidrat, dan lemak.")
    with c3:
        with st.container(border=True):
            st.markdown("### 🧮 Metode Ilmiah (WP)")
            st.write("Perhitungan transparan dan dapat ditelusuri, bukan sekadar tebakan.")

    st.write("")
    st.write("")
    _, col_tombol, _ = st.columns([1, 1.5, 1])
    with col_tombol:
        if st.button("🚀 Mulai Cari Rekomendasi Menu", use_container_width=True, type="primary"):
            st.session_state.halaman = 'kriteria'
            st.rerun()


# ============================================================
# HALAMAN 2 — KRITERIA & FILTER
# ============================================================
elif st.session_state.halaman == 'kriteria':

    st.header("🎛️ Atur Preferensi Anda")

    with st.container(border=True):
        st.subheader("👤 Data Diri")
        nama_input = st.text_input("Nama Lengkap", placeholder="Contoh: Budi Santoso")
        filter_kategori = st.selectbox(
            "Filter Jenis Menu",
            options=["Semua", "Halal", "Vegetarian"],
            help="Pilih 'Semua' untuk melihat seluruh menu, atau pilih kategori tertentu untuk menyaring."
        )

    st.write("")
    with st.container(border=True):
        st.subheader("⚖️ Bobot Tingkat Kepentingan")
        st.info(
            "💡 **Cara mengisi:** geser slider ke angka yang lebih besar (mendekati 5) apabila "
            "kriteria tersebut **sangat penting** bagi Anda. Geser ke angka kecil (mendekati 1) "
            "apabila kriteria tersebut **kurang penting**.",
            icon="💡"
        )

        col_a, col_b = st.columns(2)
        with col_a:
            bobot_harga = st.slider("💰 Harga Makanan (semakin murah semakin baik)", 1, 5, 3)
            bobot_kalori = st.slider("🔥 Kandungan Kalori (semakin tinggi semakin baik)", 1, 5, 3)
        with col_b:
            bobot_protein = st.slider("💪 Kandungan Protein (semakin tinggi semakin baik)", 1, 5, 3)
            bobot_jarak = st.slider("📍 Jarak Akses (semakin dekat semakin baik)", 1, 5, 3)

    st.write("")
    _, col_tombol, _ = st.columns([1, 1.5, 1])
    with col_tombol:
        if st.button("✨ Hitung Rekomendasi Menu Sekarang", use_container_width=True, type="primary"):
            if nama_input.strip() == "":
                st.warning("⚠️ Nama lengkap wajib diisi terlebih dahulu.")
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
# HALAMAN 3 — HASIL REKOMENDASI (3 TAB WAKTU MAKAN)
# ============================================================
elif st.session_state.halaman == 'hasil':

    bobot_user = st.session_state.bobot
    if bobot_user is None:
        st.warning("⚠️ Data preferensi tidak ditemukan. Silakan ulangi dari Beranda.")
        if st.button("⬅ Kembali ke Beranda"):
            st.session_state.halaman = 'beranda'; st.rerun()
    else:
        st.success(f"✅ Halo, **{st.session_state.nama_user}**! Berikut rekomendasi menu diet harian Anda.")

        # Terapkan filter kategori
        df_filtered = df_menu.copy()
        if st.session_state.filter_kategori != "Semua":
            df_filtered = df_filtered[df_filtered['Kategori'] == st.session_state.filter_kategori]

        tab_pagi, tab_siang, tab_malam = st.tabs(["🌅 Makan Pagi", "☀️ Makan Siang", "🌙 Makan Malam"])
        tab_map = {"Pagi": tab_pagi, "Siang": tab_siang, "Malam": tab_malam}

        for waktu, tab in tab_map.items():
            with tab:
                subset = df_filtered[df_filtered['Waktu'] == waktu].reset_index(drop=True)

                if len(subset) == 0:
                    st.warning(f"Tidak ada menu {waktu.lower()} yang sesuai filter kategori Anda.")
                    continue

                hasil, detail = hitung_wp(subset, bobot_user)
                terbaik = hasil.iloc[0]

                # ---------- MENU PERINGKAT #1 ----------
                st.subheader(f"🏆 Rekomendasi Terbaik — {waktu}")
                with st.container(border=True):
                    col_img, col_info = st.columns([1, 2])
                    with col_img:
                        tampilkan_gambar_menu(terbaik['Gambar'], terbaik['Emoji'])
                    with col_info:
                        st.markdown(f"### {terbaik['Nama Menu']}")
                        st.markdown(f"**Skor WP: `{terbaik['Vektor_V']:.4f}`** 🥇")

                        m1, m2, m3 = st.columns(3)
                        m1.metric("💰 Harga", f"Rp {terbaik['Harga']:,.0f}".replace(",", "."))
                        m2.metric("🔥 Kalori", f"{terbaik['Kalori']:.0f} kcal")
                        m3.metric("💪 Protein", f"{terbaik['Protein']:.0f} gr")

                        m4, m5, m6 = st.columns(3)
                        m4.metric("🌾 Karbo", f"{terbaik['Karbo']:.0f} gr")
                        m5.metric("🧈 Lemak", f"{terbaik['Lemak']:.0f} gr")
                        m6.metric("📍 Jarak", f"{terbaik['Jarak']:.1f} km")

                        st.info(
                            f"**Alasan Penilaian:** Menu ini memperoleh skor preferensi tertinggi "
                            f"karena kombinasi harga, kalori, protein, dan jarak aksesnya paling "
                            f"sesuai dengan bobot kepentingan yang Anda tentukan.",
                            icon="🎯"
                        )

                # ---------- ALTERNATIF LAINNYA ----------
                if len(hasil) > 1:
                    st.write("")
                    st.markdown("#### 📋 Menu Alternatif Lainnya")
                    for i in range(1, len(hasil)):
                        row = hasil.iloc[i]
                        with st.container(border=True):
                            col_img2, col_info2 = st.columns([1, 4])
                            with col_img2:
                                st.markdown(f"<div style='font-size:2.5rem; text-align:center;'>{row['Emoji']}</div>", unsafe_allow_html=True)
                            with col_info2:
                                cA, cB = st.columns([2, 1])
                                with cA:
                                    st.markdown(f"**#{row['Rank']} {row['Nama Menu']}**")
                                    st.caption(
                                        f"Rp {row['Harga']:,.0f}".replace(",", ".") +
                                        f" • {row['Kalori']:.0f} kcal • {row['Protein']:.0f}g protein • {row['Jarak']:.1f} km"
                                    )
                                with cB:
                                    st.metric("Skor WP", f"{row['Vektor_V']:.4f}")

                # ---------- TRANSPARANSI PERHITUNGAN ----------
                st.write("")
                with st.expander("📐 Lihat Detail Transparansi Perhitungan Algoritma WP"):
                    st.markdown("**① Normalisasi Bobot Kriteria**")
                    st.table(pd.DataFrame({
                        'Kriteria': detail['kriteria'],
                        'Bobot Mentah': detail['bobot_mentah'],
                        'Bobot Ternormalisasi': [f"{w:.4f}" for w in detail['bobot_normal']]
                    }))

                    st.markdown("**② Matriks Vektor S dan Vektor V per Alternatif**")
                    tabel_detail = hasil[['Nama Menu', 'Vektor_S', 'Vektor_V', 'Rank']].copy()
                    tabel_detail['Vektor_S'] = tabel_detail['Vektor_S'].apply(lambda x: f"{x:.6f}")
                    tabel_detail['Vektor_V'] = tabel_detail['Vektor_V'].apply(lambda x: f"{x:.6f}")
                    st.dataframe(tabel_detail, use_container_width=True, hide_index=True)

        st.write("")
        st.divider()
        _, col_tombol, _ = st.columns([1, 1.5, 1])
        with col_tombol:
            if st.button("🔄 Ulangi dari Awal", use_container_width=True, type="primary"):
                st.session_state.halaman = 'beranda'
                st.session_state.bobot = None
                st.rerun()
