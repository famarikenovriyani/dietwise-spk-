import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os

# ===================== KONFIGURASI HALAMAN =====================
st.set_page_config(
    page_title="DietWise - Rekomendasi Menu Diet Sehat",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===================== CSS KUSTOM (AMAN UNTUK LIGHT/DARK) =====================
# Hanya untuk background dan aksen, tanpa mengubah warna teks menjadi transparan
st.markdown(
    """
    <style>
    /* Gradasi hijau untuk header dan sidebar (hanya pada mode terang) */
    .main-header {
        background: linear-gradient(90deg, #2e7d32, #66bb6a);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .main-header h1 {
        color: white !important;
        font-weight: 700;
    }
    .main-header p {
        color: #f0f0f0 !important;
        font-size: 1.1rem;
    }
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #e8f5e9, #ffffff);
    }
    /* Card shadow */
    .stContainer {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-radius: 12px;
        padding: 1rem;
        background-color: rgba(255,255,255,0.8);
    }
    /* Tombol utama */
    .stButton button {
        background-color: #2e7d32;
        color: white;
        font-weight: 600;
        border-radius: 30px;
        padding: 0.5rem 2rem;
        border: none;
        transition: 0.3s;
    }
    .stButton button:hover {
        background-color: #1b5e20;
        color: white;
        transform: scale(1.02);
    }
    /* Metrik */
    .stMetric {
        background: #f1f8e9;
        border-radius: 12px;
        padding: 0.5rem;
    }
    /* Badge skor */
    .badge-wp {
        background: #ffb300;
        color: #1e1e1e;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ===================== LOGO =====================
# Asumsikan file logo.png berada di direktori yang sama dengan app.py
logo_path = "logo_dietwise.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.sidebar.image(logo, width=200)
else:
    st.sidebar.markdown("## 🥗 DietWise")
    st.sidebar.caption("(Tambahkan file logo.png untuk logo)")

# ===================== INISIALISASI SESSION STATE =====================
if "page" not in st.session_state:
    st.session_state.page = "beranda"
if "nama" not in st.session_state:
    st.session_state.nama = "Pengguna"
if "filter" not in st.session_state:
    st.session_state.filter = "Semua"
if "bobot_harga" not in st.session_state:
    st.session_state.bobot_harga = 3
if "bobot_kalori" not in st.session_state:
    st.session_state.bobot_kalori = 4
if "bobot_protein" not in st.session_state:
    st.session_state.bobot_protein = 5
if "bobot_jarak" not in st.session_state:
    st.session_state.bobot_jarak = 2
if "rekomendasi" not in st.session_state:
    st.session_state.rekomendasi = {}

# ===================== DATASET INTERNAL (20+ MENU) =====================
menu_data = [
    # ---------- PAGI ----------
    {
        "Nama Menu": "Nasi Goreng Spesial",
        "Waktu": "Pagi",
        "Harga": 25000,
        "Kalori": 450,
        "Protein": 15,
        "Karbo": 60,
        "Lemak": 20,
        "Jarak": 2.0,
        "Kategori": "Halal",
        "Deskripsi": "Nasi goreng dengan telur, ayam, dan sayuran segar.",
        "Gambar": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400",
    },
    {
        "Nama Menu": "Bubur Ayam",
        "Waktu": "Pagi",
        "Harga": 20000,
        "Kalori": 350,
        "Protein": 12,
        "Karbo": 40,
        "Lemak": 10,
        "Jarak": 1.5,
        "Kategori": "Halal",
        "Deskripsi": "Bubur hangat dengan suwiran ayam, cakue, dan kacang.",
        "Gambar": "https://images.unsplash.com/photo-1574486741799-6a2f5aedb0e2?w=400",
    },
    {
        "Nama Menu": "Omelet Sayur",
        "Waktu": "Pagi",
        "Harga": 18000,
        "Kalori": 300,
        "Protein": 10,
        "Karbo": 20,
        "Lemak": 15,
        "Jarak": 1.0,
        "Kategori": "Vegetarian",
        "Deskripsi": "Telur dadar padat dengan campuran sayuran hijau.",
        "Gambar": "https://images.unsplash.com/photo-1525351484168-05f3f3b64ba2?w=400",
    },
    {
        "Nama Menu": "Sereal Susu",
        "Waktu": "Pagi",
        "Harga": 15000,
        "Kalori": 250,
        "Protein": 8,
        "Karbo": 30,
        "Lemak": 5,
        "Jarak": 0.5,
        "Kategori": "Vegetarian",
        "Deskripsi": "Sereal gandum utuh dengan susu segar dan potongan buah.",
        "Gambar": "https://images.unsplash.com/photo-1550461716-d0be6a6d729c?w=400",
    },
    {
        "Nama Menu": "Roti Bakar",
        "Waktu": "Pagi",
        "Harga": 12000,
        "Kalori": 280,
        "Protein": 9,
        "Karbo": 35,
        "Lemak": 8,
        "Jarak": 0.8,
        "Kategori": "Vegetarian",
        "Deskripsi": "Roti gandum panggang dengan selai kacang dan pisang.",
        "Gambar": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400",
    },
    {
        "Nama Menu": "Smoothie Bowl",
        "Waktu": "Pagi",
        "Harga": 22000,
        "Kalori": 320,
        "Protein": 12,
        "Karbo": 45,
        "Lemak": 6,
        "Jarak": 1.2,
        "Kategori": "Vegetarian",
        "Deskripsi": "Mangkuk smoothie dengan topping granola, buah, dan biji chia.",
        "Gambar": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400",
    },
    # ---------- SIANG ----------
    {
        "Nama Menu": "Ayam Bakar",
        "Waktu": "Siang",
        "Harga": 35000,
        "Kalori": 550,
        "Protein": 30,
        "Karbo": 50,
        "Lemak": 25,
        "Jarak": 3.0,
        "Kategori": "Halal",
        "Deskripsi": "Ayam bakar dengan bumbu rempah dan sambal terasi.",
        "Gambar": "https://images.unsplash.com/photo-1587593810168-94b0f55fb9f4?w=400",
    },
    {
        "Nama Menu": "Nasi Padang",
        "Waktu": "Siang",
        "Harga": 30000,
        "Kalori": 500,
        "Protein": 25,
        "Karbo": 70,
        "Lemak": 30,
        "Jarak": 2.5,
        "Kategori": "Halal",
        "Deskripsi": "Nasi dengan lauk khas Padang: rendang, ayam, dan sayur.",
        "Gambar": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=400",
    },
    {
        "Nama Menu": "Salad Buah",
        "Waktu": "Siang",
        "Harga": 25000,
        "Kalori": 200,
        "Protein": 5,
        "Karbo": 30,
        "Lemak": 10,
        "Jarak": 1.0,
        "Kategori": "Vegetarian",
        "Deskripsi": "Salad buah segar dengan yogurt rendah lemak.",
        "Gambar": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400",
    },
    {
        "Nama Menu": "Sandwich Tahu",
        "Waktu": "Siang",
        "Harga": 20000,
        "Kalori": 280,
        "Protein": 12,
        "Karbo": 35,
        "Lemak": 8,
        "Jarak": 1.5,
        "Kategori": "Vegetarian",
        "Deskripsi": "Roti isi tahu, selada, tomat, dan saus rendah kalori.",
        "Gambar": "https://images.unsplash.com/photo-1550507992-eb63ffee0847?w=400",
    },
    {
        "Nama Menu": "Mie Ayam",
        "Waktu": "Siang",
        "Harga": 28000,
        "Kalori": 520,
        "Protein": 28,
        "Karbo": 65,
        "Lemak": 20,
        "Jarak": 2.0,
        "Kategori": "Halal",
        "Deskripsi": "Mie kenyal dengan ayam cincang, sawi, dan kuah gurih.",
        "Gambar": "https://images.unsplash.com/photo-1552611052-33e04de081de?w=400",
    },
    {
        "Nama Menu": "Gado-gado",
        "Waktu": "Siang",
        "Harga": 27000,
        "Kalori": 450,
        "Protein": 18,
        "Karbo": 40,
        "Lemak": 25,
        "Jarak": 1.8,
        "Kategori": "Vegetarian",
        "Deskripsi": "Sayuran rebus dengan bumbu kacang dan kerupuk.",
        "Gambar": "https://images.unsplash.com/photo-1565557623262-b5a9e0b3450a?w=400",
    },
    # ---------- MALAM ----------
    {
        "Nama Menu": "Steak Daging",
        "Waktu": "Malam",
        "Harga": 50000,
        "Kalori": 700,
        "Protein": 40,
        "Karbo": 30,
        "Lemak": 35,
        "Jarak": 4.0,
        "Kategori": "Halal",
        "Deskripsi": "Steak daging sapi panggang dengan saus jamur dan kentang.",
        "Gambar": "https://images.unsplash.com/photo-1544025162-d76694265947?w=400",
    },
    {
        "Nama Menu": "Ikan Bakar",
        "Waktu": "Malam",
        "Harga": 40000,
        "Kalori": 600,
        "Protein": 35,
        "Karbo": 40,
        "Lemak": 20,
        "Jarak": 3.0,
        "Kategori": "Halal",
        "Deskripsi": "Ikan kakap bakar dengan sambal dan lalapan.",
        "Gambar": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400",
    },
    {
        "Nama Menu": "Pasta Sayur",
        "Waktu": "Malam",
        "Harga": 30000,
        "Kalori": 400,
        "Protein": 15,
        "Karbo": 50,
        "Lemak": 15,
        "Jarak": 2.0,
        "Kategori": "Vegetarian",
        "Deskripsi": "Pasta penne dengan saus tomat, zucchini, dan paprika.",
        "Gambar": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=400",
    },
    {
        "Nama Menu": "Tahu Tempe Bacem",
        "Waktu": "Malam",
        "Harga": 20000,
        "Kalori": 300,
        "Protein": 18,
        "Karbo": 25,
        "Lemak": 12,
        "Jarak": 1.5,
        "Kategori": "Vegetarian",
        "Deskripsi": "Tahu dan tempe bacem manis dengan nasi hangat.",
        "Gambar": "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=400",
    },
    {
        "Nama Menu": "Pizza Sayur",
        "Waktu": "Malam",
        "Harga": 45000,
        "Kalori": 600,
        "Protein": 20,
        "Karbo": 70,
        "Lemak": 28,
        "Jarak": 3.5,
        "Kategori": "Vegetarian",
        "Deskripsi": "Pizza tipis dengan topping jamur, paprika, dan keju mozzarella.",
        "Gambar": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400",
    },
    {
        "Nama Menu": "Sushi",
        "Waktu": "Malam",
        "Harga": 55000,
        "Kalori": 450,
        "Protein": 22,
        "Karbo": 60,
        "Lemak": 10,
        "Jarak": 4.5,
        "Kategori": "Halal",
        "Deskripsi": "Sushi roll dengan isian salmon, timun, dan nasi sushi.",
        "Gambar": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=400",
    },
    {
        "Nama Menu": "Sup Krim Jagung",
        "Waktu": "Malam",
        "Harga": 25000,
        "Kalori": 350,
        "Protein": 12,
        "Karbo": 40,
        "Lemak": 18,
        "Jarak": 2.0,
        "Kategori": "Vegetarian",
        "Deskripsi": "Sup krim jagung dengan potongan wortel dan kentang.",
        "Gambar": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400",
    },
]

df_menu = pd.DataFrame(menu_data)

# ===================== FUNGSI ALGORITMA WEIGHTED PRODUCT =====================
def hitung_wp(df, bobot):
    total_bobot = sum(bobot)
    w_normal = [b / total_bobot for b in bobot]
    kriteria = df[["Harga", "Kalori", "Protein", "Jarak"]].values
    S = np.ones(len(df))
    for i, row in enumerate(kriteria):
        S[i] *= row[0] ** (-w_normal[0])
        S[i] *= row[1] ** (w_normal[1])
        S[i] *= row[2] ** (w_normal[2])
        S[i] *= row[3] ** (-w_normal[3])
    V = S / np.sum(S)
    return V, w_normal

def get_rekomendasi(df, bobot, filter_kategori="Semua"):
    if filter_kategori != "Semua":
        df_filter = df[df["Kategori"] == filter_kategori].copy()
    else:
        df_filter = df.copy()
    if df_filter.empty:
        return df_filter, None, None
    V, w_normal = hitung_wp(df_filter, bobot)
    df_filter["Skor_WP"] = V
    df_filter = df_filter.sort_values("Skor_WP", ascending=False)
    return df_filter, V, w_normal

# ===================== FUNGSI RENDER HALAMAN =====================
def render_beranda():
    # Header dengan gradasi hijau (CSS sudah disisipkan)
    st.markdown(
        """
        <div class="main-header">
            <h1>🍽️ DietWise</h1>
            <p>Sistem Pendukung Keputusan Rekomendasi Menu Diet Harian</p>
            <p style="font-size:0.9rem; opacity:0.9;">Temukan menu terbaik untuk sarapan, makan siang, dan makan malam sesuai preferensi Anda.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Tiga kartu keunggulan dengan ikon dan warna
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown("### 🧠 Cerdas")
            st.write("Metode Weighted Product memberikan rekomendasi objektif berdasarkan bobot kriteria yang Anda tentukan.")
    with col2:
        with st.container(border=True):
            st.markdown("### ⚖️ Fleksibel")
            st.write("Atur bobot Harga, Kalori, Protein, dan Jarak sesuai skala prioritas pribadi Anda.")
    with col3:
        with st.container(border=True):
            st.markdown("### 🥗 Lengkap")
            st.write("Lebih dari 20 pilihan menu dengan filter Halal/Vegetarian untuk semua waktu makan.")

    st.markdown("---")

    # Tombol mulai dengan animasi CSS
    if st.button("🚀 Mulai Cari Rekomendasi Menu", use_container_width=True):
        st.session_state.page = "form"
        st.rerun()

    # Tambahan tips sehat di footer
    with st.expander("💡 Tips Diet Sehat"):
        st.write(
            """
            - **Konsumsi protein** setiap kali makan untuk menjaga rasa kenyang.
            - **Perbanyak serat** dari sayuran dan buah-buahan.
            - **Batasi gula** dan lemak jenuh.
            - **Minum air putih** minimal 8 gelas sehari.
            - **Pilih karbohidrat kompleks** seperti nasi merah atau roti gandum.
            """
        )

def render_form():
    # Header
    st.markdown(
        """
        <div class="main-header">
            <h1>📝 Atur Kriteria Diet Anda</h1>
            <p>Sesuaikan filter dan bobot untuk mendapatkan rekomendasi yang paling sesuai.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.subheader("👤 Identitas")
        nama = st.text_input("Nama Pengguna", value=st.session_state.nama)
        st.session_state.nama = nama

    with st.container(border=True):
        st.subheader("🔍 Filter Menu")
        filter_kategori = st.selectbox(
            "Pilih Jenis Makanan",
            options=["Semua", "Halal", "Vegetarian"],
            index=["Semua", "Halal", "Vegetarian"].index(st.session_state.filter),
        )
        st.session_state.filter = filter_kategori

    with st.container(border=True):
        st.subheader("⚖️ Bobot Kriteria (1–5)")
        st.caption("Semakin tinggi angka, semakin penting kriteria tersebut bagi Anda.")

        col1, col2 = st.columns(2)
        with col1:
            bh = st.slider("💰 Harga (Cost)", 1, 5, st.session_state.bobot_harga, key="sl_harga")
            bk = st.slider("🔥 Kalori (Benefit)", 1, 5, st.session_state.bobot_kalori, key="sl_kalori")
        with col2:
            bp = st.slider("💪 Protein (Benefit)", 1, 5, st.session_state.bobot_protein, key="sl_protein")
            bj = st.slider("📍 Jarak (Cost)", 1, 5, st.session_state.bobot_jarak, key="sl_jarak")

        st.session_state.bobot_harga = bh
        st.session_state.bobot_kalori = bk
        st.session_state.bobot_protein = bp
        st.session_state.bobot_jarak = bj

    if st.button("✨ Hitung Rekomendasi Sekarang", use_container_width=True):
        bobot = [bh, bk, bp, bj]
        rekomendasi = {}
        for waktu in ["Pagi", "Siang", "Malam"]:
            df_waktu = df_menu[df_menu["Waktu"] == waktu]
            df_rek, _, _ = get_rekomendasi(df_waktu, bobot, filter_kategori)
            rekomendasi[waktu] = df_rek
        st.session_state.rekomendasi = rekomendasi
        st.session_state.page = "hasil"
        st.rerun()

    st.markdown("---")
    if st.button("🔙 Kembali ke Beranda"):
        st.session_state.page = "beranda"
        st.rerun()

def render_hasil():
    st.markdown(
        """
        <div class="main-header">
            <h1>📊 Hasil Rekomendasi Menu</h1>
            <p>Berikut menu terbaik untuk setiap waktu makan berdasarkan preferensi Anda.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(f"👤 {st.session_state.nama}  |  🍽️ Filter: {st.session_state.filter}")

    tabs = st.tabs(["🌅 Makan Pagi", "☀️ Makan Siang", "🌙 Makan Malam"])
    waktu_list = ["Pagi", "Siang", "Malam"]

    for tab, waktu in zip(tabs, waktu_list):
        with tab:
            df_rek = st.session_state.rekomendasi.get(waktu, pd.DataFrame())
            if df_rek.empty:
                st.info("Tidak ada menu yang sesuai dengan filter yang dipilih untuk waktu ini.")
                continue

            # Menu terbaik (#1)
            st.subheader("🏆 Menu Terbaik")
            menu_terbaik = df_rek.iloc[0]

            col_img, col_info = st.columns([1, 2])
            with col_img:
                st.image(menu_terbaik["Gambar"], use_container_width=True)
            with col_info:
                with st.container(border=True):
                    st.markdown(f"### {menu_terbaik['Nama Menu']}")
                    st.markdown(f"*{menu_terbaik['Deskripsi']}*")
                    st.markdown(f"**Kategori:** {menu_terbaik['Kategori']}")

                    # Nutrisi dengan metrik
                    col_metrik = st.columns(4)
                    with col_metrik[0]:
                        st.metric("💰 Harga", f"Rp {menu_terbaik['Harga']:,.0f}")
                    with col_metrik[1]:
                        st.metric("🔥 Kalori", f"{menu_terbaik['Kalori']} kkal")
                    with col_metrik[2]:
                        st.metric("💪 Protein", f"{menu_terbaik['Protein']} g")
                    with col_metrik[3]:
                        st.metric("📍 Jarak", f"{menu_terbaik['Jarak']} km")

                    # Badge skor WP
                    skor = menu_terbaik["Skor_WP"]
                    st.markdown(f"**Skor WP:** <span class='badge-wp'>{skor:.6f}</span>", unsafe_allow_html=True)

            # Menu alternatif (peringkat #2 dst)
            if len(df_rek) > 1:
                st.subheader("🔄 Menu Alternatif")
                for i, (idx, row) in enumerate(df_rek.iloc[1:].iterrows(), start=2):
                    with st.container(border=True):
                        col_alt1, col_alt2 = st.columns([1, 3])
                        with col_alt1:
                            st.image(row["Gambar"], use_container_width=True)
                        with col_alt2:
                            st.markdown(f"**#{i} {row['Nama Menu']}**")
                            st.write(row["Deskripsi"])
                            st.caption(f"Kategori: {row['Kategori']}")
                            col_metrik2 = st.columns(4)
                            with col_metrik2[0]:
                                st.metric("Harga", f"Rp {row['Harga']:,.0f}")
                            with col_metrik2[1]:
                                st.metric("Kalori", f"{row['Kalori']} kkal")
                            with col_metrik2[2]:
                                st.metric("Protein", f"{row['Protein']} g")
                            with col_metrik2[3]:
                                st.metric("Jarak", f"{row['Jarak']} km")
                            st.markdown(f"**Skor WP:** `{row['Skor_WP']:.6f}`")

            # Expander detail perhitungan WP
            with st.expander("📐 Lihat Detail Perhitungan Weighted Product"):
                bobot = [
                    st.session_state.bobot_harga,
                    st.session_state.bobot_kalori,
                    st.session_state.bobot_protein,
                    st.session_state.bobot_jarak,
                ]
                df_waktu_original = df_menu[df_menu["Waktu"] == waktu]
                df_calc = df_waktu_original.copy()
                if st.session_state.filter != "Semua":
                    df_calc = df_calc[df_calc["Kategori"] == st.session_state.filter]
                if df_calc.empty:
                    st.info("Tidak ada data perhitungan.")
                else:
                    V, w_normal = hitung_wp(df_calc, bobot)
                    S_vals = []
                    for i, row in df_calc.iterrows():
                        S_i = (
                            row["Harga"] ** (-w_normal[0])
                            * row["Kalori"] ** (w_normal[1])
                            * row["Protein"] ** (w_normal[2])
                            * row["Jarak"] ** (-w_normal[3])
                        )
                        S_vals.append(S_i)
                    df_calc["S"] = S_vals
                    df_calc["V"] = V
                    df_calc = df_calc.sort_values("V", ascending=False)

                    st.write("**Bobot Normalisasi:**")
                    st.write({
                        "Harga": f"{w_normal[0]:.4f}",
                        "Kalori": f"{w_normal[1]:.4f}",
                        "Protein": f"{w_normal[2]:.4f}",
                        "Jarak": f"{w_normal[3]:.4f}",
                    })
                    st.write("**Tabel S (vektor S) dan V (vektor V) per menu:**")
                    st.dataframe(
                        df_calc[["Nama Menu", "Harga", "Kalori", "Protein", "Jarak", "S", "V"]],
                        use_container_width=True,
                    )
                    st.caption("Cost (Harga, Jarak) dipangkat negatif, Benefit (Kalori, Protein) dipangkat positif.")

    if st.button("🔄 Ulangi & Atur Kriteria Baru", use_container_width=True):
        st.session_state.page = "form"
        st.rerun()

# ===================== NAVIGASI =====================
def main():
    # Sidebar dengan informasi tambahan
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🥗 Tentang DietWise")
    st.sidebar.write(
        "DietWise membantu Anda memilih menu diet harian terbaik "
        "menggunakan metode Weighted Product. Sesuaikan kriteria dan "
        "dapatkan rekomendasi yang personal."
    )
    st.sidebar.markdown("---")
    st.sidebar.caption("Dibuat dengan ❤️ oleh Tim DietWise")

    if st.session_state.page == "beranda":
        render_beranda()
    elif st.session_state.page == "form":
        render_form()
    elif st.session_state.page == "hasil":
        render_hasil()
    else:
        st.error("Halaman tidak ditemukan.")

if __name__ == "__main__":
    main()
