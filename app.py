import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="DietWise - Asisten Menu Diet Pintar",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS — MODERN HEALTHY LOOK & FEEL (DIETWISE REDESIGN)
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

    :root {
        --primary: #10B981;
        --primary-dark: #065F46;
        --primary-light: #E6F4EA;
        --bg-gradient: linear-gradient(185deg, #F0FDF4 0%, #FFFFFF 100%);
        --card-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
        --text-dark: #1E293B;
        --text-muted: #64748B;
    }

    .stApp {
        background: var(--bg-gradient);
    }

    /* ===== HERO PREMIUM ===== */
    .hero-container {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        border-radius: 24px;
        padding: 4rem 3rem;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(16,185,129,0.2);
    }
    .hero-title {
        font-size: 2.8rem; font-weight: 800; margin-bottom: 0.8rem;
        letter-spacing: -1px; line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 1.15rem; opacity: 0.9; max-width: 700px;
        margin: 0 auto; line-height: 1.6; font-weight: 400;
    }

    /* ===== CORE BOX / CARD VISUAL ===== */
    .dietwise-card {
        background: white; border-radius: 20px; padding: 2rem;
        border: 1px solid #E2E8F0; box-shadow: var(--card-shadow);
        margin-bottom: 1.5rem;
    }
    .card-title-premium {
        color: var(--primary-dark); font-weight: 700; 
        font-size: 1.4rem; margin-bottom: 0.5rem;
        display: flex; align-items: center; gap: 10px;
    }
    .card-desc-premium {
        color: var(--text-muted); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1rem;
    }

    .metric-pill {
        background: var(--primary-light); color: var(--primary-dark);
        padding: 0.4rem 1rem; border-radius: 30px; font-weight: 600; font-size: 0.85rem;
    }

    /* ===== SLIDER & CONTROL LABELS ===== */
    .slider-container {
        background: #F8FAFC; border-radius: 16px; padding: 1.2rem;
        margin-bottom: 1rem; border: 1px solid #F1F5F9;
    }
    .slider-title {
        font-weight: 700; color: var(--text-dark); font-size: 1rem; margin-bottom: 2px;
    }
    .slider-hint {
        color: var(--text-muted); font-size: 0.82rem; margin-bottom: 8px; line-height: 1.4;
    }

    /* ===== PODIUM PREMIUM FOR TOP MENU ===== */
    .podium-wrapper {
        background: white; border-radius: 20px; padding: 1.5rem;
        text-align: center; border: 1px solid #E2E8F0;
        box-shadow: var(--card-shadow); transition: transform 0.3s ease;
    }
    .podium-wrapper:hover { transform: translateY(-5px); }
    .rank-1 { border-top: 5px solid #F59E0B; }
    .rank-2 { border-top: 5px solid #94A3B8; }
    .rank-3 { border-top: 5px solid #B45309; }
    
    .badge-rank {
        display: inline-block; padding: 0.2rem 0.8rem; border-radius: 20px;
        font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.8rem;
    }
    .bg-r1 { background: #FEF3C7; color: #D97706; }
    .bg-r2 { background: #F1F5F9; color: #475569; }
    .bg-r3 { background: #FFEDD5; color: #C2410C; }

    /* ===== DATAFRAME TWEAK ===== */
    .dataframe thead tr th { background-color: #059669 !important; color: white !important; }

    /* ===== BUTTON RESKIN ===== */
    div.stButton > button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white; font-weight: 700; border: none; border-radius: 14px;
        padding: 0.8rem 2rem; font-size: 1rem; transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 25px rgba(16,185,129,0.25); width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-2px); box-shadow: 0 14px 30px rgba(16,185,129,0.35);
        background: linear-gradient(135deg, #059669 0%, #047857 100%); color: white;
    }

    .block-container { padding-top: 2rem; padding-bottom: 4rem; }
    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOGO & SIDEBAR INTEGRATION
# ============================================================
with st.sidebar:
    try:
        # Menggunakan file logo_dietwise.png yang ada di folder proyekmu
        st.image('logo_dietwise.png', use_container_width=True)
    except Exception:
        # Tampilan teks alternatif jika file logo belum terdeteksi
        st.markdown("<h2 style='text-align:center; color:#059669;'>🥗 DietWise</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("💡 **Tip Diet Hari Ini:**\nKonsumsi air putih minimal 2 Liter per hari untuk menjaga metabolisme tubuh Anda tetap optimal selama menjalani diet cerdas.")

# ============================================================
# DATASET LOADING
# ============================================================
def muat_dataset():
    try:
        df = pd.read_csv('dataset_diet.csv.csv')
        sumber_data = "Database DietWise"
    except FileNotFoundError:
        data_dummy = {
            'Nama_Menu': [
                'Nasi Ayam Rebus + Sayur Bening', 'Salad Buah Segar & Yogurt Low-Fat', 'Telur Dadar Teflon + Tumis Kangkung',
                'Oatmeal Pisang + Susu Almond', 'Nasi Merah + Tahu Tempe Bakar + Sayur',
                'Ayam Panggang Tanpa Kulit + Lalapan', 'Ikan Kembung Bakar + Nasi Merah', 'Gado-Gado Protein (Double Tahu)'
            ],
            'Harga': [15000, 18000, 12000, 10000, 13000, 20000, 17000, 12000],
            'Kalori': [420, 280, 350, 380, 450, 480, 400, 350],
            'Protein': [28, 8, 22, 15, 20, 32, 26, 12],
            'Jarak_Akses': [1.2, 0.8, 1.5, 1.0, 0.5, 1.3, 1.8, 0.6]
        }
        df = pd.DataFrame(data_dummy)
        sumber_data = "Rekomendasi Utama"
    return df, sumber_data

# ============================================================
# CORE ALGORITHM (WEIGHTED PRODUCT)
# ============================================================
def hitung_weighted_product(df, bobot_dict):
    W = [bobot_dict['Harga'], bobot_dict['Kalori'], bobot_dict['Protein'], bobot_dict['Akses']]
    total_bobot = sum(W)
    w_normal = [w / total_bobot for w in W]
    pangkat = [-w_normal[0], w_normal[1], w_normal[2], w_normal[3]]

    kolom_kriteria = ['Harga', 'Kalori', 'Protein', 'Jarak_Akses']
    daftar_S = []
    for _, row in df.iterrows():
        nilai_atribut = [row[k] for k in kolom_kriteria]
        S = 1
        for x, w in zip(nilai_atribut, pangkat):
            S *= x ** w
        daftar_S.append(S)

    total_S = sum(daftar_S)
    daftar_V = [s / total_S for s in daftar_S]

    hasil = df.copy()
    hasil['Vektor_S'] = daftar_S
    hasil['Vektor_V'] = daftar_V
    hasil['Rank'] = hasil['Vektor_V'].rank(ascending=False).astype(int)
    hasil = hasil.sort_values(by='Vektor_V', ascending=False).reset_index(drop=True)
    return hasil, w_normal

def format_rupiah(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

def bangun_tabel_tampilan(hasil_df):
    tabel = pd.DataFrame({
        'Rank': hasil_df['Rank'],
        'Rekomendasi Menu Makanan': hasil_df['Nama_Menu'],
        'Estimasi Harga': hasil_df['Harga'].apply(format_rupiah),
        'Energi (Kalori)': hasil_df['Kalori'].apply(lambda x: f"{x:.0f} kcal"),
        'Nutrisi (Protein)': hasil_df['Protein'].apply(lambda x: f"{x:.0f} gram"),
        'Jarak Warung/Resto': hasil_df['Jarak_Akses'].apply(lambda x: f"{x:.1f} km"),
        'Persentase Kecocokan (V)': hasil_df['Vektor_V'].apply(lambda x: f"{x:.4f}")
    })
    tabel.set_index('Rank', inplace=True)
    return tabel

# ============================================================
# STATE NAVIGATION
# ============================================================
if 'halaman' not in st.session_state: st.session_state.halaman = 'beranda'
if 'nama_user' not in st.session_state: st.session_state.nama_user = ''
if 'bobot' not in st.session_state: st.session_state.bobot = None

df_menu_preview, _ = muat_dataset()

# ============================================================
# TOP PRESET NAVIGATION BAR
# ============================================================
c_nav1, c_nav2 = st.columns([1, 2])
with c_nav1:
    st.markdown("<h3 style='margin:0; padding:0; color:#10B981; font-weight:800;'>🥗 DietWise</h3>", unsafe_allow_html=True)
with c_nav2:
    step_labels = {'beranda': '✨ Beranda Utama', 'input': '⚙️ Atur Preferensi Diet', 'hasil': '📊 Hasil Rekomendasi'}
    steps_html = " / ".join([f"<span style='color:{'#10B981; font-weight:700;' if st.session_state.halaman == k else '#64748B'}; font-size:0.95rem;'>{v}</span>" for k, v in step_labels.items()])
    st.markdown(f"<div style='text-align:right; padding-top:5px;'>{steps_html}</div>", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# HALAMAN 1 — BERANDA UTAMA
# ============================================================
if st.session_state.halaman == 'beranda':

    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Temukan Menu Diet Terbaikmu dengan Mudah</div>
        <div class="hero-subtitle">
            Bosan dengan kalkulator diet yang membingungkan? DietWise menganalisis berbagai variasi menu makanan secara cerdas, menyeimbangkan antara budget dompet, kebutuhan nutrisi harian, hingga kemudahan akses lokasi restoran di sekitar Anda secara instan.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dietwise-card">
        <div class="card-title-premium">🎯 Mengapa Menggunakan DietWise?</div>
        <div class="card-desc-premium">
            Diet yang sukses dimulai dari perencanaan makanan yang realistis. Banyak orang gagal mempertahankan program diet karena membeli makanan yang terlalu mahal atau sulit dicari. Sistem cerdas kami dirancang untuk mencegah hal tersebut dengan menyusun rekomendasi hidangan yang paling sesuai dengan preferensi gaya hidup pribadi Anda.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown("""
        <div class="podium-wrapper">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">💸</div>
            <div style="font-weight:700; color:#1E293B;">Hemat Finansial</div>
            <p style="font-size:0.85rem; color:#64748B; margin:0;">Membantu Anda memilah hidangan sehat berbiaya rendah tanpa menguras kantong bulanan.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_f2:
        st.markdown("""
        <div class="podium-wrapper">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">⚡</div>
            <div style="font-weight:700; color:#1E293B;">Efisiensi Waktu</div>
            <p style="font-size:0.85rem; color:#64748B; margin:0;">Menghitung jarak terdekat ke lokasi makanan agar diet tidak merepotkan rutinitas Anda.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_f3:
        st.markdown("""
        <div class="podium-wrapper">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">💪</div>
            <div style="font-weight:700; color:#1E293B;">Nutrisi Terjamin</div>
            <p style="font-size:0.85rem; color:#64748B; margin:0;">Fokus menyeimbangkan target kalori deficit dan kecukupan asupan protein tinggi harian.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    
    _, btn_center, _ = st.columns([1, 1.2, 1])
    with btn_center:
        if st.button("🚀 Mulai Personalisasi Menu Diet", use_container_width=True):
            st.session_state.halaman = 'input'
            st.rerun()

# ============================================================
# HALAMAN 2 — KUSTOMISASI PREFERENSI DIET
# ============================================================
elif st.session_state.halaman == 'input':

    st.markdown("""
    <div class="dietwise-card" style="text-align:center; background:linear-gradient(135deg, #F0FDF4 0%, #FFFFFF 100%);">
        <div class="card-title-premium" style="justify-content:center;">🎛️ Pengaturan Profil & Prioritas Diet</div>
        <div class="card-desc-premium">Silakan tentukan nama Anda dan seberapa penting aspek harga, nutrisi, serta kenyamanan akses di bawah ini untuk merumuskan menu yang ideal.</div>
    </div>
    """, unsafe_allow_html=True)

    kol_kiri, kol_kanan = st.columns([1, 1.4])

    with kol_kiri:
        st.markdown('<div class="dietwise-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown('<div class="card-title-premium">👤 Informasi Profil</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.85rem; color:#64748B; margin-bottom:1rem;">Tulis nama panggilan Anda untuk mempersonalisasi rangkuman laporan nutrisi diet.</div>', unsafe_allow_html=True)
        
        nama_input = st.text_input("Nama Anda", placeholder="Contoh: Budi, Siska, dll.")
        
        st.write("")
        st.markdown("📌 **Cara Kerja Sistem Cerdas:**")
        st.info("Sistem akan melakukan komparasi matematis silang. Kriteria 'Harga' secara otomatis disetel agar mencari nilai paling terjangkau (Cost), sedangkan Kalori, Protein, dan Akses disetel untuk mencari skor optimal (Benefit).")
        st.markdown('</div>', unsafe_allow_html=True)

    with kol_kanan:
        st.markdown('<div class="dietwise-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title-premium">⚖️ Tentukan Prioritas Aspek Makanan</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.85rem; color:#64748B; margin-bottom:1.5rem;">Geser indikator ke kanan jika aspek tersebut menjadi fokus utama program diet Anda saat ini. (Skala 1: Tidak Prioritas s.d 5: Sangat Penting)</div>', unsafe_allow_html=True)

        # SLIDER DENGAN PENJELASAN JELAS
        st.markdown("""
        <div class="slider-container">
            <div class="slider-title">💰 Anggaran & Harga Makanan</div>
            <div class="slider-hint">Semakin tinggi bobot, sistem akan semakin memprioritaskan makanan dengan harga termurah agar hemat pengeluaran.</div>
        </div>
        """, unsafe_allow_html=True)
        bobot_harga = st.slider("Harga Slider", 1, 5, 3, label_visibility="collapsed")

        st.markdown("""
        <div class="slider-container">
            <div class="slider-title">🔥 Kandungan Energi (Kalori)</div>
            <div class="slider-hint">Sangat krusial untuk mengontrol pembakaran kalori tubuh agar tidak berlebih atau kekurangan zat energi dasar.</div>
        </div>
        """, unsafe_allow_html=True)
        bobot_kalori = st.slider("Kalori Slider", 1, 5, 3, label_visibility="collapsed")

        st.markdown("""
        <div class="slider-container">
            <div class="slider-title">💪 Zat Pembangun Otot (Protein)</div>
            <div class="slider-hint">Penting diprioritaskan jika target Anda adalah mempertahankan massa otot atau mempercepat pemulihan tubuh selama olahraga.</div>
        </div>
        """, unsafe_allow_html=True)
        bobot_protein = st.slider("Protein Slider", 1, 5, 3, label_visibility="collapsed")

        st.markdown("""
        <div class="slider-container">
            <div class="slider-title">📍 Aksesibilitas Lokasi & Jarak</div>
            <div class="slider-hint">Mengukur tingkat kemudahan menjangkau makanan. Semakin tinggi bobotnya, semakin diutamakan tempat makan terdekat.</div>
        </div>
        """, unsafe_allow_html=True)
        bobot_akses = st.slider("Akses Slider", 1, 5, 3, label_visibility="collapsed")

        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    _, btn_hitug, _ = st.columns([1, 1.2, 1])
    with btn_hitug:
        if st.button("⚡ Hitung & Rekomendasikan Menu", use_container_width=True):
            if nama_input.strip() == "":
                st.error("⚠️ Silakan masukkan nama Anda terlebih dahulu sebelum memproses rekomendasi.")
            else:
                st.session_state.nama_user = nama_input
                st.session_state.bobot = {'Harga': bobot_harga, 'Kalori': bobot_kalori,
                                           'Protein': bobot_protein, 'Akses': bobot_akses}
                st.session_state.halaman = 'hasil'
                st.rerun()

# ============================================================
# HALAMAN 3 — LAPORAN REKOMENDASI
# ============================================================
elif st.session_state.halaman == 'hasil':

    df_menu, sumber_data = muat_dataset()
    bobot_user = st.session_state.bobot

    if bobot_user is None:
        st.warning("⚠️ Sesi preferensi kedaluwarsa. Silakan kembali ke beranda utama.")
        if st.button("⬅ Kembali Ke Beranda"):
            st.session_state.halaman = 'beranda'; st.rerun()
    else:
        hasil_df, w_normal = hitung_weighted_product(df_menu, bobot_user)

        st.markdown(f"""
        <div class="dietwise-card" style="border-left: 6px solid #10B981;">
            <div class="card-title-premium">🎉 Halo {st.session_state.nama_user}, Rencana Dietmu Siap!</div>
            <div class="card-desc-premium" style="margin:0;">Berdasarkan parameter prioritas yang Anda atur, di bawah ini merupakan susunan menu makanan yang paling cocok dijalankan dari segi finansial maupun nutrisi.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h4 style='color:#065F46; margin-bottom:1rem; font-weight:700;'>🥇 Peringkat Pilihan Teratas</h4>", unsafe_allow_html=True)
        top3 = hasil_df.head(3)
        p1, p2, p3 = st.columns(3)
        
        labels_medal = ["Juara 1 Optimal", "Rekomendasi 2", "Rekomendasi 3"]
        styles_badge = ["bg-r1", "bg-r2", "bg-r3"]
        border_styles = ["rank-1", "rank-2", "rank-3"]
        
        for i, col in enumerate([p1, p2, p3]):
            if i < len(top3):
                row = top3.iloc[i]
                with col:
                    st.markdown(f"""
                    <div class="podium-wrapper {border_styles[i]}">
                        <span class="badge-rank {styles_badge[i]}">{labels_medal[i]}</span>
                        <div style="font-size:1.1rem; font-weight:800; color:#1E293B; margin-bottom:0.5rem; min-height:45px;">{row['Nama_Menu']}</div>
                        <div style="font-size:0.85rem; color:#64748B;">Skor Kecocokan:</div>
                        <div style="font-size:1.6rem; font-weight:800; color:#10B981;">{row['Vektor_V'] * 100:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.write("")
        st.write("")
        
        kol_kiri, kol_kanan = st.columns([1.5, 1])

        with kol_kiri:
            st.markdown("<h4 style='color:#065F46; font-weight:700;'>📋 Daftar Opsi Pilihan Alternatif Selengkapnya</h4>", unsafe_allow_html=True)
            st.dataframe(bangun_tabel_tampilan(hasil_df), use_container_width=True, height=330)

        with kol_kanan:
            st.markdown("<h4 style='color:#065F46; font-weight:700;'>📊 Grafik Persentase Kecocokan</h4>", unsafe_allow_html=True)
            chart_data = hasil_df[['Nama_Menu', 'Vektor_V']].copy()
            chart_data['Kecocokan (%)'] = chart_data['Vektor_V'] * 100
            chart_data = chart_data[['Nama_Menu', 'Kecocokan (%)']].set_index('Nama_Menu')
            st.bar_chart(chart_data, color="#10B981", height=330)

        menu_terbaik = hasil_df.iloc[0]['Nama_Menu']
        kecocokan_terbaik = hasil_df.iloc[0]['Vektor_V'] * 100
        
        st.markdown(f"""
        <div style="background: #ECFDF5; border-radius:16px; padding:1.5rem; border:1px solid #A7F3D0; margin-top:1.5rem;">
            <h5 style="color:#065F46; margin:0 0 0.5rem 0; font-weight:700;">💡 Rekomendasi Kesimpulan DietWise</h5>
            <p style="color:#1E293B; margin:0; font-size:0.95rem; line-height:1.6;">
                Sangat disarankan untuk memilih menu <b>{menu_terbaik}</b> karena persentase kecocokannya menduduki peringkat tertinggi sebesar <b>{kecocokan_terbaik:.1f}%</b>. Pilihan ini berhasil menekan variabel yang Anda anggap kurang penting dan memaksimalkan kriteria nutrisi yang Anda butuhkan.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        with st.expander("🛠️ Klik untuk melihat catatan kalkulasi sistem"):
            st.markdown("**1. Bobot Awal Yang Anda Masukkan:**")
            st.json(bobot_user)
            st.markdown("**2. Bobot Ternormalisasi:**")
            st.table(pd.DataFrame({
                'Kriteria Evaluasi': ['Harga (Cost)', 'Kandungan Kalori (Benefit)', 'Nutrisi Protein (Benefit)', 'Jarak Aksesibilitas (Benefit)'],
                'Bobot Akhir Perhitungan': [f"{w:.4f}" for w in w_normal]
            }))

        st.write("")
        _, btn_reset, _ = st.columns([1, 1.2, 1])
        with btn_reset:
            if st.button("🔄 Atur Ulang Rencana / Cari Ulang", use_container_width=True):
                st.session_state.halaman = 'beranda'
                st.session_state.bobot = None
                st.rerun()