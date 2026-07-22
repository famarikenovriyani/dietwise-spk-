import streamlit as st
import pandas as pd
import numpy as np

# ===================== KONFIGURASI HALAMAN =====================
st.set_page_config(page_title="DietWise - Rekomendasi Menu Diet", layout="wide")

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

# ===================== DATASET INTERNAL =====================
menu_data = [
    # Pagi
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
        "Deskripsi": "Nasi goreng dengan telur, ayam, dan sayuran.",
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
        "Deskripsi": "Bubur dengan suwiran ayam, cakue, dan kacang.",
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
        "Deskripsi": "Telur dadar dengan sayuran segar.",
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
        "Deskripsi": "Sereal gandum dengan susu segar.",
        "Gambar": "https://images.unsplash.com/photo-1550461716-d0be6a6d729c?w=400",
    },
    # Siang
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
        "Deskripsi": "Ayam bakar dengan bumbu rempah.",
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
        "Deskripsi": "Nasi dengan lauk khas Padang.",
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
        "Deskripsi": "Salad buah segar dengan yogurt.",
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
        "Deskripsi": "Roti isi tahu dan sayuran.",
        "Gambar": "https://images.unsplash.com/photo-1550507992-eb63ffee0847?w=400",
    },
    # Malam
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
        "Deskripsi": "Steak daging sapi dengan saus.",
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
        "Deskripsi": "Ikan bakar dengan sambal.",
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
        "Deskripsi": "Pasta dengan saus sayuran.",
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
        "Deskripsi": "Tahu dan tempe bacem manis.",
        "Gambar": "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=400",
    },
]

df_menu = pd.DataFrame(menu_data)

# ===================== FUNGSI ALGORITMA WEIGHTED PRODUCT =====================
def hitung_wp(df, bobot):
    """
    Menghitung skor Weighted Product untuk setiap menu dalam df.
    bobot: list [bobot_harga, bobot_kalori, bobot_protein, bobot_jarak]
    """
    total_bobot = sum(bobot)
    w_normal = [b / total_bobot for b in bobot]  # normalisasi bobot

    # Kolom kriteria: Harga (cost), Kalori (benefit), Protein (benefit), Jarak (cost)
    kriteria = df[["Harga", "Kalori", "Protein", "Jarak"]].values
    S = np.ones(len(df))

    for i, row in enumerate(kriteria):
        # Harga (cost) -> pangkat negatif
        S[i] *= row[0] ** (-w_normal[0])
        # Kalori (benefit) -> pangkat positif
        S[i] *= row[1] ** (w_normal[1])
        # Protein (benefit) -> pangkat positif
        S[i] *= row[2] ** (w_normal[2])
        # Jarak (cost) -> pangkat negatif
        S[i] *= row[3] ** (-w_normal[3])

    V = S / np.sum(S)  # normalisasi vektor V
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
    # Banner utama
    st.title("🍽️ DietWise")
    st.markdown(
        """
        ### Sistem Pendukung Keputusan Rekomendasi Menu Diet Harian
        Temukan menu makanan terbaik untuk sarapan, makan siang, dan makan malam 
        sesuai dengan preferensi dan kebutuhan gizi Anda.
        """
    )

    # Tiga kartu keunggulan
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.subheader("🧠 Cerdas")
            st.write("Menggunakan metode Weighted Product untuk memberikan rekomendasi yang objektif.")
    with col2:
        with st.container(border=True):
            st.subheader("⚖️ Fleksibel")
            st.write("Sesuaikan bobot kriteria (Harga, Kalori, Protein, Jarak) sesuai keinginan Anda.")
    with col3:
        with st.container(border=True):
            st.subheader("🍱 Lengkap")
            st.write("Tersedia 12 menu pilihan untuk setiap waktu makan, dengan filter Halal/Vegetarian.")

    st.markdown("---")

    if st.button("🚀 Mulai Cari Rekomendasi Menu", use_container_width=True):
        st.session_state.page = "form"
        st.rerun()


def render_form():
    st.title("📝 Atur Kriteria Diet Anda")

    with st.container(border=True):
        st.subheader("Identitas")
        nama = st.text_input("Nama Pengguna", value=st.session_state.nama)
        st.session_state.nama = nama

    with st.container(border=True):
        st.subheader("Filter Menu")
        filter_kategori = st.selectbox(
            "Pilih Jenis Makanan",
            options=["Semua", "Halal", "Vegetarian"],
            index=["Semua", "Halal", "Vegetarian"].index(st.session_state.filter),
        )
        st.session_state.filter = filter_kategori

    with st.container(border=True):
        st.subheader("Bobot Kriteria (1–5)")
        st.caption("Seret slider untuk menentukan seberapa penting kriteria bagi Anda.")

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
        # Simpan bobot ke session
        bobot = [bh, bk, bp, bj]

        # Hitung rekomendasi untuk setiap waktu
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
    st.title("📊 Hasil Rekomendasi Menu")

    # Tampilkan nama pengguna dan filter yang digunakan
    st.caption(f"👤 {st.session_state.nama}  |  🍽️ Filter: {st.session_state.filter}")

    # Tab untuk setiap waktu makan
    tabs = st.tabs(["🌅 Makan Pagi", "☀️ Makan Siang", "🌙 Makan Malam"])
    waktu_list = ["Pagi", "Siang", "Malam"]

    for tab, waktu in zip(tabs, waktu_list):
        with tab:
            df_rek = st.session_state.rekomendasi.get(waktu, pd.DataFrame())

            if df_rek.empty:
                st.info("Tidak ada menu yang sesuai dengan filter yang dipilih.")
                continue

            # Tampilkan menu peringkat #1 (terbaik)
            st.subheader("🏆 Menu Terbaik")
            menu_terbaik = df_rek.iloc[0]

            # Layout: gambar di kiri, info di kanan
            col_img, col_info = st.columns([1, 2])
            with col_img:
                st.image(menu_terbaik["Gambar"], use_container_width=True)
            with col_info:
                with st.container(border=True):
                    st.markdown(f"### {menu_terbaik['Nama Menu']}")
                    st.markdown(f"*{menu_terbaik['Deskripsi']}*")
                    st.markdown(f"**Kategori:** {menu_terbaik['Kategori']}")

                    # Nutrisi dalam metrik
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
                    st.markdown(f"**Skor WP:** `{skor:.6f}`")

            # Daftar alternatif (peringkat #2 dan seterusnya)
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
                # Kita perlu mendapatkan bobot normal dan vektor S, V dari fungsi
                # Untuk itu, hitung ulang (efisien karena data kecil)
                bobot = [
                    st.session_state.bobot_harga,
                    st.session_state.bobot_kalori,
                    st.session_state.bobot_protein,
                    st.session_state.bobot_jarak,
                ]
                df_waktu_original = df_menu[df_menu["Waktu"] == waktu]
                _, _, w_normal = get_rekomendasi(
                    df_waktu_original, bobot, st.session_state.filter
                )
                # Kita tampilkan tabel perhitungan S dan V untuk setiap menu
                df_calc = df_waktu_original.copy()
                if st.session_state.filter != "Semua":
                    df_calc = df_calc[df_calc["Kategori"] == st.session_state.filter]
                if df_calc.empty:
                    st.info("Tidak ada data perhitungan.")
                else:
                    V, w_normal = hitung_wp(df_calc, bobot)
                    # S dihitung di dalam fungsi, kita perlu menghitung ulang
                    # Buat kolom S
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
                    st.write(
                        {
                            "Harga": f"{w_normal[0]:.4f}",
                            "Kalori": f"{w_normal[1]:.4f}",
                            "Protein": f"{w_normal[2]:.4f}",
                            "Jarak": f"{w_normal[3]:.4f}",
                        }
                    )
                    st.write("**Tabel S (vektor S) dan V (vektor V) per menu:**")
                    st.dataframe(
                        df_calc[["Nama Menu", "Harga", "Kalori", "Protein", "Jarak", "S", "V"]],
                        use_container_width=True,
                    )
                    st.caption("Catatan: Cost (Harga, Jarak) dipangkat negatif, Benefit (Kalori, Protein) dipangkat positif.")

    # Tombol ulangi
    if st.button("🔄 Ulangi & Atur Kriteria Baru", use_container_width=True):
        st.session_state.page = "form"
        st.rerun()


# ===================== NAVIGASI HALAMAN =====================
def main():
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
