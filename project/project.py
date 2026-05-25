import streamlit as st
import pandas as pd
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import base64 # buat encode gambar.

# ──────────────────────────────────────────────── #
#   HELPER: muat file SVG dari direktori lokal     #
# ──────────────────────────────────────────────── #
def load_svg(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

# ──────────────────────────────────────────────── #
#             KONFIGURASI HALAMAN                  #
# ──────────────────────────────────────────────── #
st.set_page_config(
    page_title="SPK Fuzzy Mamdani – Wisata Kerajinan",
    page_icon="🏺",
    layout="wide",
    initial_sidebar_state="expanded",
)

def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_img = get_base64("dashb-utama.jpg")

# ──────────────────────────────────────────────── #
#                  GLOBAL CSS                      #
# ──────────────────────────────────────────────── #
st.markdown("""
<style>

/* GLOBAL */

@import url('https://fonts.googleapis.com/css2?family=Marcellus+SC&family=Poppins:wght@300;400;500;600;700;800&display=swap');

    html, body {
    font-family:'Poppins', sans-serif;
}
            
.dash-title,
.hero-card h2,
.sidebar-logo{
    font-family:'Marcellus SC', serif !important;
}
.hero-card,
.total-card {
    width: 100%;
    box-sizing: border-box;
}
            
/* DASHBOARD UTAMA - Background */
.stApp {
            
    background-image:url("data:image/jpg;base64,%s");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: scroll;
    color: #f0fdf4;
}

/* SIDEBAR */
.sidebar-top{
    padding-top:30px;
    padding-bottom:24px;
    text-align:center;
}

.sidebar-logo{
    font-family:'Marcellus SC', serif;
    color:#F3E8CC;
    font-size:2.8rem;
    line-height:1;
    letter-spacing:1px;
    margin-bottom:10px;
}

.sidebar-sub{
    font-family:'Poppins', sans-serif;
    font-style:italic;
    font-size:0.92rem;
    font-weight:300;
    color:#F3E8CC;
    opacity:.92;
}
            
[data-testid="stSidebar"] {
    background: rgba(10,20,12,0.78) !important;
    backdrop-filter: blur(18px);
    border-right: 1px solid rgba(134,239,172,0.08);
}

/* SIDEBAR BUTTON */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.18) !important;
    color: #ffc926 !important;
    border-radius: 18px !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    height: 64px;
    width: 92%;
    margin: 0 auto 14px auto;
    display:block;
    font-size: 1rem !important;
    font-family:'Poppins',sans-serif !important;
    font-weight:600 !important;
    transition: all .25s ease;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.28) !important;
    color: #ffc926 !important;
    transform: scale(1.02);
    box-shadow:
        0 0 18px rgba(255,202,38,0.15);
}

[data-testid="stSidebar"] .stButton > button:focus {
    border: 2px solid #d52518 !important;
    box-shadow:
        0 0 0 3px rgba(213,37,24,0.2);
}
                    
/* CARD */
.card {
    background: rgba(17,25,20,0.72);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(134,239,172,0.10);
    border-radius: 20px;
    padding: 24px;
    transition: all .25s ease;
    box-shadow:
        0 8px 24px rgba(0,0,0,0.22);
}

.card:hover {
    transform: translateY(-3px);
    border: 1px solid rgba(134,239,172,0.35);
    box-shadow:
        0 10px 28px rgba(34,197,94,0.18);
}
            
.card-metric {
    background: rgba(243,232,204,0.55);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.22);
    padding: 20px;
    transition: all .28s ease;
    box-shadow:
        0 8px 24px rgba(0,0,0,0.08);
}

.card-metric:hover {
    transform: translateY(-5px);
    box-shadow:
        0 0 18px rgba(255,202,38,0.18),
        0 15px 30px rgba(0,0,0,0.14);
}

/* BUTTON */
            
/* INPUT LABEL HITUNG SPK */

.stSlider label,
.stNumberInput label,
.stSelectbox label {
    color:#19532B !important;
    font-family:'Poppins', sans-serif !important;
    font-weight:600 !important;
}
            
.stButton > button {
    background: linear-gradient(
        135deg, #22c55e, #16a34a) !important;

    color: white !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow:
        0 6px 18px rgba(34,197,94,0.22);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 10px 24px rgba(34,197,94,0.35) !important;
}


/* WARNING BOX - Proses Fuzzy*/
div[data-baseweb="notification"] {
    background:#D97706 !important;
    border: none !important;
    border-radius:14px !important;
}

div[data-baseweb="notification"] p {
    color:#F3E8CC !important;
    font-family:'Poppins', sans-serif !important;
    font-weight:600 !important;
    font-size:0.95rem !important;
}
            
/* SECTION */
.section-header {
    background: linear-gradient(
        135deg, rgba(34,197,94,0.18), rgba(134,239,172,0.08));

    border-left: 4px solid #22c55e;
    color: #f0fdf4;
    border-radius: 10px;
    padding: 14px 20px;
    font-weight: 700;
}

/* TABLE*/
thead tr th {
    background: rgba(34,197,94,0.18) !important;
    color:#f0fdf4 !important;
}

/* RESULT */
.result-box {
    background: linear-gradient(
        135deg, rgba(34,197,94,0.15), rgba(134,239,172,0.08));

    border: 2px solid #22c55e;
    border-radius: 16px;
}

.result-score {
    background: linear-gradient(
        135deg, #22c55e, #86efac);

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* PAGE TITLE */
.page-title{
    font-family:'Marcellus SC', serif;
    font-size:3rem;
    color:#F8C537;
    margin-top:-8px;
    margin-bottom:18px;
    letter-spacing:1px;
}

/* DATASET INFO */
.dataset-info{
    font-family:'Poppins', sans-serif;
    font-size:1.08rem;
    font-weight:500;
    color:#F3E8CC;
    margin-top:4px;
    margin-bottom:10px;
}

.dataset-info span{
    color:#8BB8FF;
    font-weight:600;
}

.dataset-total{
    font-family:'Poppins', sans-serif;
    font-size:1.18rem;
    font-weight:600;
    color:#F3E8CC;
    margin-bottom:18px;
}

.dataset-total span{
    color:#F8C537;
}

/* EXPORT BUTTON */
.stDownloadButton button{
    background:rgba(10,15,30,0.82) !important;
    color:#F3E8CC !important;
    border:none !important;
    border-radius:14px !important;
    padding:10px 18px !important;
    font-family:'Poppins', sans-serif !important;
    font-size:0.92rem !important;
    font-weight:500 !important;
    transition:0.25s;
    width:170px;
    height:48px;
}

.footer-card{
    margin-top:30px;
    margin-bottom:10px;
    background:#F3E8CC;
    border-radius:18px;
    padding:14px 20px;
    text-align:center;
    color:#1C4D2D;
    font-family:'Poppins', sans-serif;
    font-size:0.82rem;
    font-weight:500;
    box-shadow:
        0 8px 20px rgba(0,0,0,0.18);
}
            
.db-icon-wrap{
    width:58px;
    height:58px;
    margin-bottom:10px;
    display:flex;
    align-items:center;
    justify-content:center;
    overflow:hidden;
}

.db-icon{
    width:58px;
    height:58px;
    object-fit:contain;
    display:block;
}
            
.note-high{
    color:#00A86B;
}

/* FUZZY NOTE */
.fuzzy-note{
    margin-top:22px;
    margin-bottom:10px;
    background:#F3E8CC;
    border-radius:22px;
    padding:22px 28px;
    text-align:center;
    box-shadow:
        0 8px 22px rgba(0,0,0,0.18);
}

.fuzzy-note-title{
    font-family:'Marcellus SC', serif;
    font-size:1.35rem;
    color:#1C4D2D;
    margin-bottom:10px;
}

.fuzzy-note-text{
    font-family:'Poppins', sans-serif;
    font-size:1rem;
    font-weight:500;
    color:#244c34;
    margin-bottom:14px;
}

.fuzzy-note-tags{
    font-family:'Poppins', sans-serif;
    font-size:1rem;
    font-weight:600;
    color:#1C4D2D;
    line-height:1.9;
}

.note-low{
    color:#E53935;
}

.note-mid{
    color:#D4A017;
}

.note-high{
    color:#00A86B;
}

/* BADGE OUTPUT RULE BASE */
.badge-tinggi,
.badge-sedang,
.badge-rendah{
    font-family:'Poppins', sans-serif;
    font-size:.82rem;
    font-weight:700;
    padding:6px 14px;
    border-radius:12px;
    display:inline-block;
    min-width:78px;
    text-align:center;
    box-shadow:
        0 4px 10px rgba(0,0,0,0.12);
}

/* TINGGI */
.badge-tinggi{
    background:#F3E8CC;
    color:#1C4D2D;
}

/* SEDANG */
.badge-sedang{
    background:#F3E8CC;
    color:#8B6A00;
}

/* RENDAH */
.badge-rendah{
    background:#F3E8CC;
    color:#A61B1B;
}
     
</style>
""".replace("%s", bg_img), unsafe_allow_html=True)


# ──────────────────────────────────────────────────────── #
#   LANGKAH 1 – LOAD DATASET                               #
#   Dataset: Rural Heritage Tourism Industry Chain         #
#   Filter: Heritage_Type == "Handicraft Center"           #
# ──────────────────────────────────────────────────────── #
@st.cache_data
def load_data():
    df = pd.read_csv("rural_heritage_tourism_industry_chain_dataset.csv")
    # Filter hanya destinasi tipe Handicraft Center
    hc = df[df["Heritage_Type"] == "Handicraft Center"].copy()
    hc = hc.reset_index(drop=True)
    hc.index = hc.index + 1
    return df, hc

df_all, df_hc = load_data()


# ──────────────────────────────────────────────────────── #
#   LANGKAH 2 – DEFINISI VARIABEL FUZZY (Modul IX)        #
#                                                          #
#   Antecedent (Input):                                    #
#     - jumlah_pengunjung  → C1 Visitor Count   (Benefit) #
#     - harga_tiket        → C2 Ticket Price    (Cost)    #
#     - kepuasan_wisatawan → C3 Tourist Sat.    (Benefit) #
#     - pendapatan         → C4 Revenue         (Benefit) #
#     - biaya_operasional  → C5 Operational Cost(Cost)    #
#                                                          #
#   Consequent (Output):                                   #
#     - kinerja → Skor kinerja destinasi [0, 100]         #
#                                                          #
#   Catatan: np.arange bersifat interval setengah terbuka #
#   sehingga batas atas dilebihkan (sesuai Modul IX)      #
# ──────────────────────────────────────────────────────── #
@st.cache_resource
def bangun_sistem_fuzzy():

    # Definisikan variabel fuzzy input (Antecedent)
    jumlah_pengunjung  = ctrl.Antecedent(np.arange(52,  800, 1),      'visitor_count')
    harga_tiket        = ctrl.Antecedent(np.arange(10,  100, 1),      'ticket_price')
    kepuasan_wisatawan = ctrl.Antecedent(np.arange(0.0, 5.1, 0.1),   'tourist_sat')
    pendapatan         = ctrl.Antecedent(np.arange(5000, 100001, 100),'revenue')
    biaya_operasional  = ctrl.Antecedent(np.arange(2000, 50001, 100), 'op_cost')

    # Definisikan variabel fuzzy output (Consequent)
    # Metode defuzzifikasi: centroid (sesuai Modul IX)
    kinerja = ctrl.Consequent(np.arange(0, 101, 1), 'kinerja', defuzzify_method='centroid')

    # ── Fungsi Keanggotaan C1: Jumlah Pengunjung ─────────────────────────────
    # Rendah  → trapesium kiri  (trapmf)
    # Sedang  → segitiga tengah (trimf)
    # Tinggi  → trapesium kanan (trapmf)
    jumlah_pengunjung['rendah'] = fuzz.trapmf(jumlah_pengunjung.universe, [52,  52,  200, 400])
    jumlah_pengunjung['sedang'] = fuzz.trimf( jumlah_pengunjung.universe, [200, 425, 650])
    jumlah_pengunjung['tinggi'] = fuzz.trapmf(jumlah_pengunjung.universe, [500, 650, 799, 799])

    # ── Fungsi Keanggotaan C2: Harga Tiket ───────────────────────────────────
    harga_tiket['murah']  = fuzz.trapmf(harga_tiket.universe, [10, 10, 30, 55])
    harga_tiket['sedang'] = fuzz.trimf( harga_tiket.universe, [30, 55, 80])
    harga_tiket['mahal']  = fuzz.trapmf(harga_tiket.universe, [60, 80, 99, 99])

    # ── Fungsi Keanggotaan C3: Kepuasan Wisatawan ────────────────────────────
    kepuasan_wisatawan['rendah'] = fuzz.trapmf(kepuasan_wisatawan.universe, [0.0, 0.0, 2.0, 3.25])
    kepuasan_wisatawan['sedang'] = fuzz.trimf( kepuasan_wisatawan.universe, [2.5, 3.5, 4.5])
    kepuasan_wisatawan['tinggi'] = fuzz.trapmf(kepuasan_wisatawan.universe, [3.75, 4.5, 5.0, 5.0])

    # ── Fungsi Keanggotaan C4: Pendapatan ────────────────────────────────────
    pendapatan['rendah'] = fuzz.trapmf(pendapatan.universe, [5000,  5000,  30000, 55000])
    pendapatan['sedang'] = fuzz.trimf( pendapatan.universe, [30000, 55000, 80000])
    pendapatan['tinggi'] = fuzz.trapmf(pendapatan.universe, [60000, 80000, 100000, 100000])

    # ── Fungsi Keanggotaan C5: Biaya Operasional ─────────────────────────────
    biaya_operasional['rendah'] = fuzz.trapmf(biaya_operasional.universe, [2000,  2000,  15000, 27000])
    biaya_operasional['sedang'] = fuzz.trimf( biaya_operasional.universe, [15000, 27500, 40000])
    biaya_operasional['tinggi'] = fuzz.trapmf(biaya_operasional.universe, [30000, 40000, 50000, 50000])

    # ── Fungsi Keanggotaan Output: Kinerja ───────────────────────────────────
    kinerja['rendah'] = fuzz.trapmf(kinerja.universe, [0,  0,  25, 50])
    kinerja['sedang'] = fuzz.trimf( kinerja.universe, [25, 50, 75])
    kinerja['tinggi'] = fuzz.trapmf(kinerja.universe, [50, 75, 100, 100])

    # ──────────────────────────────────────────────────────────────────────── #
    #   LANGKAH 3 – DASAR ATURAN / RULE BASE (IF-THEN)                        #
    #   Operator "&" = AND = MIN  (penalaran min-max Mamdani, Modul IX)       #
    #   Operator "|" = OR  = MAX                                               #
    #   Total: 15 aturan fuzzy                                                 #
    # ──────────────────────────────────────────────────────────────────────── #
    aturan = [
        # R1  : IF Pengunjung Tinggi AND Kepuasan Tinggi  THEN Kinerja Tinggi
        ctrl.Rule(jumlah_pengunjung['tinggi'] & kepuasan_wisatawan['tinggi'],  kinerja['tinggi']),
        # R2  : IF Pengunjung Sedang AND Kepuasan Tinggi  THEN Kinerja Tinggi
        ctrl.Rule(jumlah_pengunjung['sedang'] & kepuasan_wisatawan['tinggi'],  kinerja['tinggi']),
        # R3  : IF Pengunjung Rendah                      THEN Kinerja Rendah
        ctrl.Rule(jumlah_pengunjung['rendah'],                                  kinerja['rendah']),
        # R4  : IF Harga Murah AND Kepuasan Tinggi        THEN Kinerja Tinggi
        ctrl.Rule(harga_tiket['murah']   & kepuasan_wisatawan['tinggi'],        kinerja['tinggi']),
        # R5  : IF Harga Mahal AND Kepuasan Rendah        THEN Kinerja Rendah
        ctrl.Rule(harga_tiket['mahal']   & kepuasan_wisatawan['rendah'],        kinerja['rendah']),
        # R6  : IF Harga Sedang AND Kepuasan Sedang       THEN Kinerja Sedang
        ctrl.Rule(harga_tiket['sedang']  & kepuasan_wisatawan['sedang'],        kinerja['sedang']),
        # R7  : IF Pendapatan Tinggi AND Biaya Rendah     THEN Kinerja Tinggi
        ctrl.Rule(pendapatan['tinggi']   & biaya_operasional['rendah'],         kinerja['tinggi']),
        # R8  : IF Pendapatan Tinggi AND Biaya Tinggi     THEN Kinerja Sedang
        ctrl.Rule(pendapatan['tinggi']   & biaya_operasional['tinggi'],         kinerja['sedang']),
        # R9  : IF Pendapatan Rendah                      THEN Kinerja Rendah
        ctrl.Rule(pendapatan['rendah'],                                          kinerja['rendah']),
        # R10 : IF Biaya Tinggi                           THEN Kinerja Rendah
        ctrl.Rule(biaya_operasional['tinggi'],                                   kinerja['rendah']),
        # R11 : IF Biaya Rendah AND Kepuasan Tinggi       THEN Kinerja Tinggi
        ctrl.Rule(biaya_operasional['rendah'] & kepuasan_wisatawan['tinggi'],   kinerja['tinggi']),
        # R12 : IF Kepuasan Rendah                        THEN Kinerja Rendah
        ctrl.Rule(kepuasan_wisatawan['rendah'],                                  kinerja['rendah']),
        # R13 : IF Kepuasan Sedang                        THEN Kinerja Sedang
        ctrl.Rule(kepuasan_wisatawan['sedang'],                                  kinerja['sedang']),
        # R14 : IF Pengunjung Tinggi AND Harga Mahal      THEN Kinerja Sedang
        ctrl.Rule(jumlah_pengunjung['tinggi'] & harga_tiket['mahal'],           kinerja['sedang']),
        # R15 : IF Pengunjung Sedang AND Harga Sedang     THEN Kinerja Sedang
        ctrl.Rule(jumlah_pengunjung['sedang'] & harga_tiket['sedang'],          kinerja['sedang']),
    ]

    # ── Bangun sistem kontrol dan simulasi ───────────────────────────────────
    sistem_kontrol = ctrl.ControlSystem(aturan)
    simulasi       = ctrl.ControlSystemSimulation(sistem_kontrol)

    return (simulasi,
            jumlah_pengunjung, harga_tiket, kepuasan_wisatawan,
            pendapatan, biaya_operasional, kinerja)


# Bangun sistem fuzzy sekali, kemudian di-cache oleh Streamlit
(simulasi_fuzzy,
 var_pengunjung, var_tiket, var_kepuasan,
 var_pendapatan, var_biaya, var_kinerja) = bangun_sistem_fuzzy()


# ──────────────────────────────────────────────────────── #
#   TEKS ATURAN (untuk tampilan tabel di halaman Rule Base)#
# ──────────────────────────────────────────────────────── #
TEKS_ATURAN = [
    "IF Visitor Tinggi AND Satisfaction Tinggi THEN Kinerja Tinggi",
    "IF Visitor Sedang AND Satisfaction Tinggi THEN Kinerja Tinggi",
    "IF Visitor Rendah THEN Kinerja Rendah",
    "IF Price Murah AND Satisfaction Tinggi THEN Kinerja Tinggi",
    "IF Price Mahal AND Satisfaction Rendah THEN Kinerja Rendah",
    "IF Price Sedang AND Satisfaction Sedang THEN Kinerja Sedang",
    "IF Revenue Tinggi AND Cost Rendah THEN Kinerja Tinggi",
    "IF Revenue Tinggi AND Cost Tinggi THEN Kinerja Sedang",
    "IF Revenue Rendah THEN Kinerja Rendah",
    "IF Cost Tinggi THEN Kinerja Rendah",
    "IF Cost Rendah AND Satisfaction Tinggi THEN Kinerja Tinggi",
    "IF Satisfaction Rendah THEN Kinerja Rendah",
    "IF Satisfaction Sedang THEN Kinerja Sedang",
    "IF Visitor Tinggi AND Price Mahal THEN Kinerja Sedang",
    "IF Visitor Sedang AND Price Sedang THEN Kinerja Sedang",
]

# Definisi aturan dalam format (nomor, antecedent dict, konsekuen)
DEFINISI_ATURAN = [
    (1,  {"visitor_count": "tinggi", "tourist_sat": "tinggi"},             "tinggi"),
    (2,  {"visitor_count": "sedang", "tourist_sat": "tinggi"},             "tinggi"),
    (3,  {"visitor_count": "rendah"},                                       "rendah"),
    (4,  {"ticket_price":  "murah",  "tourist_sat": "tinggi"},             "tinggi"),
    (5,  {"ticket_price":  "mahal",  "tourist_sat": "rendah"},             "rendah"),
    (6,  {"ticket_price":  "sedang", "tourist_sat": "sedang"},             "sedang"),
    (7,  {"revenue":       "tinggi", "op_cost":     "rendah"},             "tinggi"),
    (8,  {"revenue":       "tinggi", "op_cost":     "tinggi"},             "sedang"),
    (9,  {"revenue":       "rendah"},                                       "rendah"),
    (10, {"op_cost":       "tinggi"},                                       "rendah"),
    (11, {"op_cost":       "rendah", "tourist_sat": "tinggi"},             "tinggi"),
    (12, {"tourist_sat":   "rendah"},                                       "rendah"),
    (13, {"tourist_sat":   "sedang"},                                       "sedang"),
    (14, {"visitor_count": "tinggi", "ticket_price": "mahal"},             "sedang"),
    (15, {"visitor_count": "sedang", "ticket_price": "sedang"},            "sedang"),
]


# ──────────────────────────────────────────────────────── #
#   LANGKAH 4 – FUZZIFIKASI                                #
#   Hitung derajat keanggotaan tiap variabel input         #
#   menggunakan fuzz.interp_membership (Modul IX)          #
# ──────────────────────────────────────────────────────── #
def hitung_fuzzifikasi(c1, c2, c3, c4, c5):
    """
    Menghitung derajat keanggotaan (µ) setiap nilai input
    terhadap himpunan fuzzy yang telah didefinisikan.
    Menggunakan fuzz.interp_membership dari library scikit-fuzzy.
    """
    derajat = {
        "visitor_count": {
            "rendah": float(fuzz.interp_membership(var_pengunjung.universe,
                                                    var_pengunjung['rendah'].mf, c1)),
            "sedang": float(fuzz.interp_membership(var_pengunjung.universe,
                                                    var_pengunjung['sedang'].mf, c1)),
            "tinggi": float(fuzz.interp_membership(var_pengunjung.universe,
                                                    var_pengunjung['tinggi'].mf, c1)),
        },
        "ticket_price": {
            "murah":  float(fuzz.interp_membership(var_tiket.universe,
                                                    var_tiket['murah'].mf,  c2)),
            "sedang": float(fuzz.interp_membership(var_tiket.universe,
                                                    var_tiket['sedang'].mf, c2)),
            "mahal":  float(fuzz.interp_membership(var_tiket.universe,
                                                    var_tiket['mahal'].mf,  c2)),
        },
        "tourist_sat": {
            "rendah": float(fuzz.interp_membership(var_kepuasan.universe,
                                                    var_kepuasan['rendah'].mf, c3)),
            "sedang": float(fuzz.interp_membership(var_kepuasan.universe,
                                                    var_kepuasan['sedang'].mf, c3)),
            "tinggi": float(fuzz.interp_membership(var_kepuasan.universe,
                                                    var_kepuasan['tinggi'].mf, c3)),
        },
        "revenue": {
            "rendah": float(fuzz.interp_membership(var_pendapatan.universe,
                                                    var_pendapatan['rendah'].mf, c4)),
            "sedang": float(fuzz.interp_membership(var_pendapatan.universe,
                                                    var_pendapatan['sedang'].mf, c4)),
            "tinggi": float(fuzz.interp_membership(var_pendapatan.universe,
                                                    var_pendapatan['tinggi'].mf, c4)),
        },
        "op_cost": {
            "rendah": float(fuzz.interp_membership(var_biaya.universe,
                                                    var_biaya['rendah'].mf, c5)),
            "sedang": float(fuzz.interp_membership(var_biaya.universe,
                                                    var_biaya['sedang'].mf, c5)),
            "tinggi": float(fuzz.interp_membership(var_biaya.universe,
                                                    var_biaya['tinggi'].mf, c5)),
        },
    }
    return derajat


# ──────────────────────────────────────────────────────── #
#   LANGKAH 5 – INFERENSI / PENALARAN                      #
#   Hitung α-predikat setiap aturan dengan operator        #
#   AND = MIN  (penalaran min-max Mamdani, Modul IX)       #
# ──────────────────────────────────────────────────────── #
def hitung_inferensi(derajat_keanggotaan):
    """
    Menerapkan setiap aturan IF-THEN pada nilai derajat keanggotaan.
    Operator AND menggunakan operasi MIN sesuai penalaran Mamdani.
    Mengembalikan list (nomor_aturan, alpha, konsekuen).
    """
    hasil_inferensi = []
    for (nomor, antecedent, konsekuen) in DEFINISI_ATURAN:
        # Kumpulkan derajat keanggotaan semua anteceden dalam aturan ini
        nilai_alpha = [derajat_keanggotaan[variabel][term]
                       for variabel, term in antecedent.items()]
        # Operator AND = MIN (penalaran min-max Mamdani)
        alpha = min(nilai_alpha)
        hasil_inferensi.append((nomor, alpha, konsekuen))
    return hasil_inferensi


# ──────────────────────────────────────────────────────── #
#   LANGKAH 6 – AGREGASI                                   #
#   Gabungkan output setiap aturan menggunakan MAX         #
#   (operasi max pada konsekuen, Modul IX)                 #
# ──────────────────────────────────────────────────────── #
def hitung_agregasi(hasil_inferensi):
    """
    Melakukan agregasi himpunan fuzzy output menggunakan operasi MAX.
    Setiap kategori output (rendah/sedang/tinggi) diambil nilai alpha terbesar.
    """
    agregasi = {"tinggi": 0.0, "sedang": 0.0, "rendah": 0.0}
    for (_, alpha, konsekuen) in hasil_inferensi:
        # Operasi MAX pada output konsekuen
        agregasi[konsekuen] = max(agregasi[konsekuen], alpha)
    return agregasi


# ──────────────────────────────────────────────────────── #
#   LANGKAH 7 – DEFUZZIFIKASI & HITUNG SKOR AKHIR          #
#   Menggunakan ctrl.ControlSystemSimulation (scikit-fuzzy)#
#   Metode defuzzifikasi: centroid                         #
# ──────────────────────────────────────────────────────── #
def hitung_fuzzy_mamdani(c1, c2, c3, c4, c5):
    """
    Fungsi utama SPK Fuzzy Mamdani.
    Melakukan seluruh tahap:
      1. Fuzzifikasi (fuzz.interp_membership)
      2. Inferensi   (AND = MIN, per aturan)
      3. Agregasi    (MAX per kategori output)
      4. Defuzzifikasi (centroid via ctrl.ControlSystemSimulation)

    Parameter:
        c1 : Visitor Count
        c2 : Ticket Price
        c3 : Tourist Satisfaction
        c4 : Revenue Generated
        c5 : Operational Cost

    Return:
        skor     : nilai crisp hasil defuzzifikasi [0-100]
        kategori : label "TINGGI" / "SEDANG" / "RENDAH"
        derajat  : dict derajat keanggotaan (untuk tampilan)
        inf_res  : list hasil inferensi per aturan (untuk tampilan)
        agg      : dict nilai agregasi per kategori (untuk tampilan)
    """
    # Clamp nilai input agar berada dalam batas universe
    c1 = float(np.clip(c1, 52,   799))
    c2 = float(np.clip(c2, 10,    99))
    c3 = float(np.clip(c3,  0.0,   5.0))
    c4 = float(np.clip(c4, 5000, 100000))
    c5 = float(np.clip(c5, 2000,  50000))

    # Masukkan nilai input ke sistem simulasi
    simulasi_fuzzy.input['visitor_count'] = c1
    simulasi_fuzzy.input['ticket_price']  = c2
    simulasi_fuzzy.input['tourist_sat']   = c3
    simulasi_fuzzy.input['revenue']       = c4
    simulasi_fuzzy.input['op_cost']       = c5

    # Hitung inferensi + agregasi + defuzzifikasi (otomatis oleh scikit-fuzzy)
    simulasi_fuzzy.compute()
    skor = float(simulasi_fuzzy.output['kinerja'])

    # Hitung ulang detail tiap tahap untuk keperluan tampilan UI
    derajat  = hitung_fuzzifikasi(c1, c2, c3, c4, c5)
    inf_res  = hitung_inferensi(derajat)
    agg      = hitung_agregasi(inf_res)
    kategori = tentukan_kategori(skor)

    return skor, kategori, derajat, inf_res, agg


def tentukan_kategori(skor):
    """
    Menentukan label kategori kinerja berdasarkan nilai skor defuzzifikasi.
    Threshold dibagi rata: Rendah < 33.33 ≤ Sedang < 66.67 ≤ Tinggi
    """
    if skor >= 66.67:
        return "TINGGI"
    elif skor >= 33.33:
        return "SEDANG"
    else:
        return "RENDAH"


def get_result_style(kat):
    """Mengembalikan nama kelas CSS dan emoji sesuai kategori hasil."""
    if kat == "TINGGI":
        return "result-box", "result-score", "🥇"
    elif kat == "SEDANG":
        return "result-box-sedang", "result-score-sedang", "🥈"
    return "result-box-rendah", "result-score-rendah", "🥉"


# ──────────────────────────────────────────────────────── #
#   HITUNG SKOR SEMUA BARIS DATASET HANDICRAFT CENTER      #
#   (dijalankan sekali, di-cache Streamlit)                #
# ──────────────────────────────────────────────────────── #
@st.cache_data
def hitung_semua_skor(df):
    """
    Menjalankan fungsi hitung_fuzzy_mamdani untuk setiap baris data
    pada dataset Handicraft Center dan mengembalikan DataFrame hasil.
    """
    hasil = []
    for _, baris in df.iterrows():
        skor, kat, _, _, _ = hitung_fuzzy_mamdani(
            baris["Visitor_Count"],
            baris["Ticket_Price"],
            baris["Tourist_Satisfaction"],
            baris["Revenue_Generated"],
            baris["Operational_Cost"],
        )
        hasil.append({"Skor_Kinerja": round(skor, 2), "Kategori": kat})
    return pd.DataFrame(hasil)

skor_df    = hitung_semua_skor(df_hc)
df_hasil   = pd.concat([df_hc.reset_index(drop=True), skor_df], axis=1)
df_ranking = df_hasil.sort_values("Skor_Kinerja", ascending=False).reset_index(drop=True)
df_ranking.insert(0, "Rank", range(1, len(df_ranking) + 1))


# ──────────────────────────────────────────────────────── #
#                       S I D E B A R                      #
# ──────────────────────────────────────────────────────── #
st.sidebar.markdown(
    """
    <div class="sidebar-top">
        <div class="sidebar-logo">
            SPK<br>MAMDANI
        </div>
        <hr>
        <div class="sidebar-sub">
            Fuzzy Decision Support System
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"

daftar_menu = [
    "Dashboard",
    "Dataset",
    "Fuzzifikasi",
    "Rule Base",
    "Hitung SPK",
    "Proses Fuzzy",
    "Hasil & Ranking",
    "Visualisasi",
    "Profile Tim"
]

for item in daftar_menu:
    if st.sidebar.button(item, use_container_width=True):
        st.session_state.menu = item

menu = st.session_state.menu
st.markdown("", unsafe_allow_html=True)


# ════════════════════════════════════════════════ #
#               HALAMAN 1 – DASHBOARD              #
# ════════════════════════════════════════════════ #
if menu == "Dashboard":
    st.markdown("""
    <div class="page-title" style="color:#18542a;">
        Dashboard
    </div>
    """, unsafe_allow_html=True)

    svg_db      = load_svg("files-db.svg")
    svg_db_b64  = base64.b64encode(svg_db.encode()).decode()

    svg_visitor     = load_svg("visitor-count.svg")
    svg_visitor_b64 = base64.b64encode(svg_visitor.encode()).decode()

    svg_ticket      = load_svg("ticket.svg")
    svg_ticket_b64  = base64.b64encode(svg_ticket.encode()).decode()

    svg_rate        = load_svg("rate.svg")
    svg_rate_b64    = base64.b64encode(svg_rate.encode()).decode()

    svg_revenue     = load_svg("revenue-bag.svg")
    svg_revenue_b64 = base64.b64encode(svg_revenue.encode()).decode()

    svg_ops         = load_svg("operational.svg")
    svg_ops_b64     = base64.b64encode(svg_ops.encode()).decode()

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Marcellus&family=Poppins:wght@300;400;500;600;700&display=swap');
                
    .dash-title {
        font-family: 'Marcellus SC', serif;
        font-size: 3.8rem;
        font-weight: 400;
        color:#ffc926;
        line-height: 1.1;
        margin-bottom: 10px;
        margin-top: -20px;
        text-shadow: none;
    }
    .hero-card {
        background: rgba(243,232,204,0.38);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 28px;
        padding: 30px;
        box-shadow:
            0 8px 32px rgba(0,0,0,0.14);
        transition: all .3s ease;
    }
    .hero-card:hover {
        transform: translateY(-4px);
        box-shadow:
            0 0 22px rgba(255,202,38,0.16),
            0 18px 40px rgba(0,0,0,0.16);
    }
    .hero-card h2 {
        font-family: 'Marcellus SC', serif;
        font-size: 1.95rem;
        font-weight: 400;
        color:#ffc926;
        margin-bottom: 10px;
        line-height: 1.2;
    }
    .hero-card p {
        font-family: 'Poppins', sans-serif;
        font-size: 0.92rem;
        font-weight: 600;
        color: #19532B;
        line-height: 1.6;
        text-align: justify;
        margin: 0;
    }
    .total-card {
        background: rgba(243,232,204,0.38);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border-radius: 30px;
        border: 1px solid rgba(255,255,255,0.24);
        padding: 28px 20px;
        min-height: 220px;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        text-align:center;
        box-shadow:
            0 8px 32px rgba(0,0,0,0.14);
        transition:all .3s ease;
    }
    .total-card:hover {
        transform: translateY(-4px);
        box-shadow:
            0 0 22px rgba(255,202,38,0.16),
            0 18px 40px rgba(0,0,0,0.16);
    }
    .total-card svg {
        width: 58px;
        height: 58px;
        margin-bottom: 10px;
    }
    .total-card .total-num {
        font-family: 'Poppins', sans-serif;
        font-size: 2.4rem;
        font-weight: 700;
        color: #19532B;
        line-height: 1.1;
    }
    .total-card .total-label {
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #19532B;
        margin-top: 4px;
    }
    .dash-section-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffc926;
        margin: 28px 0 14px 0;
    }
    .dash-section-title-yellow {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #FFCA26;
        margin: 28px 0 14px 0;
    }
    .krit-card {
        background: rgba(243,232,204,0.88);
        border-radius: 22px;
        padding: 20px 12px;
        min-height: 220px;
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        text-align:center;
        transition: all .28s ease;
        border:1px solid rgba(255,255,255,0.12);
    }
    .krit-card:hover{
        transform:translateY(-5px);
        box-shadow:
            0 0 18px rgba(255,202,38,0.18),
            0 15px 30px rgba(0,0,0,0.14);
    }
    .krit-card svg {
        width: 48px;
        height: 48px;
        margin-bottom: 6px;
    }
    .krit-card .kc {
        font-family: 'Poppins', sans-serif;
        font-size: 0.82rem;
        font-weight: 600;
        color: #19532B;
        margin-bottom: 2px;
    }
    .krit-card .kname {
        font-family: 'Poppins', sans-serif;
        font-size: 0.88rem;
        font-weight: 600;
        color: #19532B;
        margin: 2px 0 3px 0;
    }
    .krit-card .krange {
        font-family: 'Poppins', sans-serif;
        font-size: 0.72rem;
        font-weight: 400;
        color: #19532B;
        margin-bottom: 8px;
    }
    .badge-benefit {
        background: #9ABC05;
        color: #fff;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 0.78rem;
        padding: 3px 14px;
        border-radius: 14px;
        display: inline-block;
    }
    .badge-cost {
        background: #D52518;
        color: #fff;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 0.78rem;
        padding: 3px 14px;
        border-radius: 14px;
        display: inline-block;
    }
    .ring-card-dark {
        background: rgba(25,83,43,0.72);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border:1px solid rgba(255,255,255,0.12);
        border-radius: 30px;
        padding: 20px 16px;
        text-align: center;
        min-height: 155px;
        transition:all .28s ease;
    }
    .ring-card-dark:hover{
        transform:translateY(-4px);
        box-shadow:
            0 0 18px rgba(255,202,38,0.15);
    }
    .ring-card-dark .rnum {
        font-family: 'Poppins', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #F3E8CC;
        line-height: 1.1;
    }
    .ring-card-dark .rlabel {
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #F3E8CC;
        margin-top: 4px;
        line-height: 1.3;
    }
    .ring-card-dark .rsub {
        font-family: 'Poppins', sans-serif;
        font-size: 0.82rem;
        font-weight: 400;
        color: #F3E8CC;
        margin-top: 6px;
    }
    .dash-footer {
        background: #F3E8CC;
        color: #19532B;
        font-family: 'Poppins', sans-serif;
        font-size: 0.82rem;
        font-weight: 500;
        text-align: center;
        padding: 14px 20px;
        margin-top: 36px;
        border-radius: 0 0 8px 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    total_semua = len(df_all)
    total_hc    = len(df_hc)

    st.markdown("<div class='dash-title'>Dashboard</div>", unsafe_allow_html=True)

    col_hero, col_total = st.columns([3, 1.6])

    with col_hero:
        st.markdown(f"""
        <div class="hero-card">
            <h2 style="font-weight:800; text-align:center;">Sistem Pendukung Keputusan</h2>
            <p style="text-align:center;">
                Pemilihan Penilaian Kinerja Destinasi Wisata Kerajinan<br>
                (Handicraft Tourism) Menggunakan Metode Fuzzy Mamdani.
            </p>
            <div style='
                color:#19532B;
                font-size:.88rem;
                line-height:1.3;
                margin:0;
                text-align:center;
            '>
                Sistem membantu menentukan peringkat kinerja destinasi wisata kerajinan (Handicraft Center)<br>
                berdasarkan 5 kriteria menggunakan metode Fuzzy Mamdani Inference System (FMIS)
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_total:
        st.markdown(f"""
        <div class="total-card">
            <div class="db-icon-wrap">
                <img src="data:image/svg+xml;base64,{svg_db_b64}" class="db-icon">
            </div>
            <div class="total-num">{total_semua}</div>
            <div class="total-label">Total Data</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='dash-section-title'>Kriteria Penilaian</div>", unsafe_allow_html=True)

    # Data kriteria: (kode, nama, range, tipe, ikon svg)
    kriteria = [
        ("C1", "Visitor Count",        "(52-799)",         "Benefit", svg_visitor),
        ("C2", "Ticket Price",         "(10-99)",          "Cost",    svg_ticket),
        ("C3", "Tourist Satisfaction", "(0-5)",            "Benefit", svg_rate),
        ("C4", "Revenue Generated",    "(5.000-100.000)",  "Benefit", svg_revenue),
        ("C5", "Operational Cost",     "(2.000-50.000)",   "Cost",    svg_ops),
    ]

    kolom_krit = st.columns(5)
    for i, (kode, nama, rentang, tipe, ikon_svg) in enumerate(kriteria):
        badge = ("<span class='badge-benefit'>Benefit</span>"
                 if tipe == "Benefit"
                 else "<span class='badge-cost'>Cost</span>")
        with kolom_krit[i]:
            st.markdown(f"""
            <div class="krit-card">
                <div style='width:48px;height:48px;margin-bottom:6px;'>{ikon_svg}</div>
                <div class="kc">{kode}</div>
                <div class="kname">{nama}</div>
                <div class="krange">{rentang}</div>
                {badge}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='dash-section-title-yellow'>Ringkasan Sistem</div>", unsafe_allow_html=True)

    kolom_ring = st.columns(4)
    data_ring = [
        (str(total_semua), "Total Data",                "(Dataset)"),
        (str(total_hc),    "Data Handicraft<br>Center", "(Setelah di Filter)"),
        ("5",              "Jumlah Kriteria",            "(Kriteria)"),
        ("Fuzzy Mamdani",  " ",                          "Inference System"),
    ]

    for i, (nilai, label, sub) in enumerate(data_ring):
        with kolom_ring[i]:
            st.markdown(f"""
            <div class="ring-card-dark">
                <div class="rnum">{nilai}</div>
                <div class="rlabel">{label}</div>
                <div class="rsub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════ #
#               HALAMAN 2 – DATASET                #
# ════════════════════════════════════════════════ #
if menu == "Dataset":
    st.markdown("""
    <div class="page-title" style="color:#18542a;">
        Dataset
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([8, 2])

    with col1:
        st.markdown("""
        <div class="dataset-info">
            Filter Heritage_Type:
            <span style="color:#19532B;">Handicraft Center</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Tombol ekspor data hasil filter
        csv_export = df_hc[
            ["Location_ID", "Heritage_Type", "Visitor_Count",
             "Ticket_Price", "Tourist_Satisfaction",
             "Revenue_Generated", "Operational_Cost"]
        ].to_csv(index=False)

        st.download_button(
            "Export CSV",
            csv_export,
            "handicraft_center.csv",
            "text/csv"
        )

    st.markdown(f"""
    <div class="dataset-total">
        Total Data Setelah Filter:
        <span>{len(df_hc)}</span> baris
    </div>
    """, unsafe_allow_html=True)

    # Tampilkan kolom yang relevan dengan label ramah pengguna
    kolom_tampil = [
        "Location_ID", "Heritage_Type", "Visitor_Count",
        "Ticket_Price", "Tourist_Satisfaction",
        "Revenue_Generated", "Operational_Cost"
    ]
    df_tampil = df_hc[kolom_tampil].copy()
    df_tampil.index = df_tampil.index + 1
    df_tampil.columns = [
        "Destinasi", "Heritage Type", "Visitor Count",
        "Ticket Price", "Tourist Satisfaction",
        "Revenue Generated", "Operational Cost"
    ]

    st.dataframe(df_tampil, use_container_width=True, height=450)


# ════════════════════════════════════════════════ #
#             HALAMAN 3 – FUZZIFIKASI              #
# ════════════════════════════════════════════════ #
if menu == "Fuzzifikasi":
    st.markdown(""" <div class="page-title" style="color:#18542a;"> Fuzzifikasi </div> """, unsafe_allow_html=True)

    warna_bg    = "#0f172a"
    warna_grid  = "#1e1b4b"
    warna_teks  = "#e2e8f0"

    def plot_fungsi_keanggotaan(ax, variabel, label_himpunan, judul, peta_warna):
        """
        Menggambar grafik fungsi keanggotaan dari variabel scikit-fuzzy.
        Menggunakan variabel.universe dan variabel[label].mf
        sesuai contoh Modul IX (Gambar 8.11, 8.12, 8.13).
        """
        ax.set_facecolor(warna_grid)
        ax.spines[['top', 'right', 'left', 'bottom']].set_color('#374151')
        ax.tick_params(colors=warna_teks, labelsize=7)
        ax.set_title(judul, color=warna_teks, fontsize=8, fontweight='bold', pad=6)
        ax.set_ylim(-0.05, 1.1)
        ax.set_xlim(variabel.universe[0], variabel.universe[-1])
        ax.grid(True, alpha=0.15, color='#6366f1')
        for lbl in label_himpunan:
            warna = peta_warna.get(lbl, "#818cf8")
            ax.plot(variabel.universe, variabel[lbl].mf,
                    color=warna, lw=2, label=lbl.capitalize())
        ax.legend(fontsize=6, framealpha=0.2, labelcolor=warna_teks,
                  facecolor=warna_grid, edgecolor='#374151')

    fig, axes = plt.subplots(2, 3, figsize=(14, 7))
    fig.patch.set_facecolor(warna_bg)
    plt.subplots_adjust(wspace=0.35, hspace=0.5)

    # Plot C1 – Jumlah Pengunjung
    plot_fungsi_keanggotaan(
        axes[0, 0], var_pengunjung,
        ["rendah", "sedang", "tinggi"],
        "C1 – Visitor Count (Benefit)",
        {"rendah": "#ef4444", "sedang": "#f59e0b", "tinggi": "#10b981"}
    )
    # Plot C2 – Harga Tiket
    plot_fungsi_keanggotaan(
        axes[0, 1], var_tiket,
        ["murah", "sedang", "mahal"],
        "C2 – Ticket Price (Cost)",
        {"murah": "#3b82f6", "sedang": "#f59e0b", "mahal": "#ef4444"}
    )
    # Plot C3 – Kepuasan Wisatawan
    plot_fungsi_keanggotaan(
        axes[0, 2], var_kepuasan,
        ["rendah", "sedang", "tinggi"],
        "C3 – Tourist Satisfaction (Benefit)",
        {"rendah": "#ef4444", "sedang": "#f59e0b", "tinggi": "#10b981"}
    )
    # Plot C4 – Pendapatan
    plot_fungsi_keanggotaan(
        axes[1, 0], var_pendapatan,
        ["rendah", "sedang", "tinggi"],
        "C4 – Revenue Generated (Benefit)",
        {"rendah": "#ef4444", "sedang": "#f59e0b", "tinggi": "#10b981"}
    )
    # Plot C5 – Biaya Operasional
    plot_fungsi_keanggotaan(
        axes[1, 1], var_biaya,
        ["rendah", "sedang", "tinggi"],
        "C5 – Operational Cost (Cost)",
        {"rendah": "#10b981", "sedang": "#f59e0b", "tinggi": "#ef4444"}
    )
    # Plot Output – Kinerja
    plot_fungsi_keanggotaan(
        axes[1, 2], var_kinerja,
        ["rendah", "sedang", "tinggi"],
        "Output – Kinerja Destinasi",
        {"rendah": "#ef4444", "sedang": "#f59e0b", "tinggi": "#10b981"}
    )

    st.pyplot(fig)
    plt.close()

    st.markdown("""
<div class='fuzzy-note'>
<div class='fuzzy-note-title'>Keterangan Fungsi Keanggotaan</div>
<div class='fuzzy-note-text'>
Diimplementasikan menggunakan <b>fuzz.trimf</b> (segitiga) dan <b>fuzz.trapmf</b> (trapesium)<br>
dari library scikit-fuzzy, didefinisikan pada <b>ctrl.Antecedent</b> (input) dan <b>ctrl.Consequent</b> (output).
</div>
<div class='fuzzy-note-tags'>
<span style='color:#E53935;'>Rendah / Murah</span> = Trapesium kiri (trapmf) &nbsp;|&nbsp;
<span style='color:#D4A017;'>Sedang</span> = Segitiga tengah (trimf) &nbsp;|&nbsp;
<span style='color:#00A86B;'>Tinggi / Mahal</span> = Trapesium kanan (trapmf)
</div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════ #
#              HALAMAN 4 – RULE BASE               #
# ════════════════════════════════════════════════ #
if menu == "Rule Base":
    st.markdown(""" <div class="page-title" style="color:#18542a;"> RULE BASE - Aturan Fuzzy (IF - THEN) </div> """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-box"
        style='font-family:Poppins,sans-serif; color:#1C4D2D; font-weight:500; font-size:.95rem;'>
        Total Rule: <b>15 aturan</b> &nbsp;|&nbsp;
        Operator: <b>AND (&amp;) = MIN</b> &nbsp;|&nbsp;
        Implementasi: <b>ctrl.Rule (scikit-fuzzy)</b>
    </div>
    """, unsafe_allow_html=True)

    # Badge warna per kategori konsekuen
    badge_html = {
        "tinggi": "<span class='badge-tinggi'>Tinggi</span>",
        "sedang": "<span class='badge-sedang'>Sedang</span>",
        "rendah": "<span class='badge-rendah'>Rendah</span>",
    }

    for teks_aturan, (nomor, ant, konsekuen) in zip(TEKS_ATURAN, DEFINISI_ATURAN):
        col_no, col_rule, col_out = st.columns([0.5, 6, 1])
        with col_no:
            st.markdown(f"""
            <div style= 'background: #1C4D2D;border-radius:50%;width:38px;height:38px;
                        display:flex;align-items:center;justify-content:center;
                        font-weight:700;color:#F8C537;font-size:.9rem;margin-top:6px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.16);'>
                {nomor}
            </div>
            """, unsafe_allow_html=True)
        with col_rule:
            st.markdown(f"""
            <div style='padding:14px 18px; background:rgba(22,40,28,0.96); backdrop-filter:blur(14px);
                        border:1px solid rgba(255,255,255,0.08); border-radius:16px; font-family:Poppins,sans-serif;
                        font-size:.94rem; font-weight:500; line-height:1.7; color:#F3E8CC; margin-top:4px;
                    box-shadow: 0 6px 20px rgba(0,0,0,0.22);'>
        {teks_aturan}
    </div>
    """, unsafe_allow_html=True)
            
        with col_out:
            st.markdown(f"""
            <div style='margin-top:10px;text-align:center;'>
                {badge_html[konsekuen]}
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════ #
#             HALAMAN 5 – HITUNG SPK               #
# ════════════════════════════════════════════════ #
if menu == "Hitung SPK":
    st.markdown(""" <div class="page-title" style="color:#18542a;"> HITUNG SPK - Input Data & Eksekusi </div> """, unsafe_allow_html=True)

    col_input, col_pilih = st.columns([3, 2])

    with col_input:
        st.markdown("""
            <h4 style='
            color:#19532B;
            font-family:Poppins,sans-serif;
            font-size:1.7rem;
            font-weight:700;
            margin-bottom:6px;
            '>
                Input Nilai Kriteria
            </h4>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box" style='font-size:.82rem;
                    font-family:Poppins,sans-serif;
                    color:#19532B;
                    font-weight:500;'>
            Masukkan nilai untuk menghitung kinerja destinasi
        </div>
        """, unsafe_allow_html=True)

        # Slider dan number_input sesuai Modul IX
        c1_val = st.slider("C1 – Visitor Count (Benefit)",         52,  799, 400,
                           help="Semakin tinggi visitor, semakin baik")
        c2_val = st.slider("C2 – Ticket Price (Cost)",             10,   99,  35,
                           help="Semakin murah, semakin baik")
        c3_val = st.slider("C3 – Tourist Satisfaction (Benefit)", 0.0,  5.0, 4.0, 0.1,
                           help="Semakin tinggi, semakin baik")
        c4_val = st.number_input("C4 – Revenue Generated (Benefit)",
                                  5000, 100000, 50000, 1000,
                                  help="Semakin besar revenue, semakin baik")
        c5_val = st.number_input("C5 – Operational Cost (Cost)",
                                  2000, 50000, 20000, 500,
                                  help="Semakin kecil cost, semakin baik")

    with col_pilih:
        st.markdown("""
            <h4 style='
            color:#19532B;
            font-family:Poppins,sans-serif;
            font-size:1.7rem;
            font-weight:700;
            margin-bottom:6px;
            '>
                Pilih Alternatif / Destinasi
            </h4>
        """, unsafe_allow_html=True)

        pilihan_dest = ["-- Input Manual --"] + df_hc["Location_ID"].tolist()
        destinasi_dipilih = st.selectbox("Pilih Destinasi dari Dataset", pilihan_dest)

        if destinasi_dipilih != "-- Input Manual --":
            baris = df_hc[df_hc["Location_ID"] == destinasi_dipilih].iloc[0]
            c1_val = int(baris["Visitor_Count"])
            c2_val = int(baris["Ticket_Price"])
            c3_val = float(baris["Tourist_Satisfaction"])
            c4_val = int(baris["Revenue_Generated"])
            c5_val = int(baris["Operational_Cost"])
            st.info(f"""
            **Data Destinasi: {destinasi_dipilih}**
            - Visitor Count: {c1_val}
            - Ticket Price: {c2_val}
            - Satisfaction: {c3_val}
            - Revenue: {c4_val:,}
            - Op. Cost: {c5_val:,}
            """)

        st.markdown("""
            <h4 style='
            color:#19532B;
            font-family:Poppins,sans-serif;
            font-size:1.7rem;
            font-weight:700;
            margin-bottom:6px;
            '>
                Keterangan Kriteria
            </h4>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box" style='font-size:.8rem;
                    font-family:Poppins,sans-serif;
                    color:#19532B;
                    font-weight:500;
                    '>
            <b>C1 Benefit:</b> Semakin besar semakin baik<br>
            <b>C2 Cost:</b> Semakin kecil semakin baik<br>
            <b>C3 Benefit:</b> Semakin besar semakin baik<br>
            <b>C4 Benefit:</b> Semakin besar semakin baik<br>
            <b>C5 Cost:</b> Semakin kecil semakin baik
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("▶ HITUNG SPK", use_container_width=True):
        skor, kat, derajat, inf_res, agg = hitung_fuzzy_mamdani(
            c1_val, c2_val, c3_val, c4_val, c5_val
        )

        # Simpan hasil ke session_state agar bisa dibaca di halaman Proses Fuzzy
        st.session_state["hasil_terakhir"] = {
            "skor": skor, "kat": kat,
            "derajat": derajat, "inf": inf_res, "agg": agg,
            "c1": c1_val, "c2": c2_val, "c3": c3_val,
            "c4": c4_val, "c5": c5_val,
        }

        box_class, score_class, emoji = get_result_style(kat)
        st.markdown(f"""
        <div class="{box_class}">
            <div style='font-size:2rem;margin-bottom:8px;'>{emoji}</div>
            <div class="{score_class}">{skor:.2f} / 100</div>
            <div class="result-kategori">Kategori: {kat}</div>
        </div>
        """, unsafe_allow_html=True)

        st.success(f"✅ Perhitungan selesai! Skor Kinerja: **{skor:.2f}** – Kategori: **{kat}**")
        st.info("💡 Lihat detail proses di menu **🔍 Proses Fuzzy**")


# ════════════════════════════════════════════════ #
#             HALAMAN 6 – PROSES FUZZY             #
# ════════════════════════════════════════════════ #
if menu == "Proses Fuzzy":
    st.markdown(""" <div class="page-title" style="color:#18542a;"> PROSES FUZZY - Detail Perhitungan (Mamdani via scikit-fuzzy) </div> """, unsafe_allow_html=True)

    if "hasil_terakhir" not in st.session_state:

        st.warning("⚠️ Belum ada perhitungan. Silakan ke menu **⚙️ Hitung SPK** terlebih dahulu.")
        st.stop()

    res   = st.session_state["hasil_terakhir"]
    skor  = res["skor"]
    kat   = res["kat"]
    derajat   = res["derajat"]
    inf   = res["inf"]
    agg   = res["agg"]

    # Tampilkan alur tahapan (sesuai Gambar 8.10 Modul IX)
    tahapan = [
        "1️⃣ Fuzzifikasi",
        "➡️ 2️⃣ Inferensi (Rule)",
        "➡️ 3️⃣ Agregasi (MAX)",
        "➡️ 4️⃣ Defuzzifikasi (Centroid)"
    ]
    st.markdown(f"""
    <div class="info-box" style='display:flex;gap:10px;align-items:center;flex-wrap:wrap;'>
        {''.join([f'<span style="font-weight:600;color:#818cf8;">{t}</span>' for t in tahapan])}
    </div>
    """, unsafe_allow_html=True)

    col_kiri, col_kanan = st.columns(2)

    with col_kiri:
        # ── Tahap 1: Fuzzifikasi ──────────────────────────────────────────────
        st.markdown("#### 1️⃣ Fuzzifikasi (Derajat Keanggotaan via fuzz.interp_membership)")

        info_variabel = {
            "visitor_count": ("Visitor Count",       res["c1"], ["Rendah", "Sedang", "Tinggi"]),
            "ticket_price":  ("Ticket Price",         res["c2"], ["Murah",  "Sedang", "Mahal"]),
            "tourist_sat":   ("Tourist Satisfaction", res["c3"], ["Rendah", "Sedang", "Tinggi"]),
            "revenue":       ("Revenue Generated",    res["c4"], ["Rendah", "Sedang", "Tinggi"]),
            "op_cost":       ("Operational Cost",     res["c5"], ["Rendah", "Sedang", "Tinggi"]),
        }

        baris_fuzz = []
        for var, (nama, nilai, terms) in info_variabel.items():
            baris = {"Kriteria": f"{nama} ({nilai})"}
            for t in terms:
                kunci = t.lower()
                baris[t] = f"{derajat[var].get(kunci, 0):.3f}"
            baris_fuzz.append(baris)

        tabel_fuzz = pd.DataFrame(baris_fuzz)
        st.dataframe(tabel_fuzz, use_container_width=True, hide_index=True)

        # ── Tahap 2: Inferensi ────────────────────────────────────────────────
        st.markdown("#### 2️⃣ Inferensi – Aturan Aktif (operator AND = MIN via ctrl.Rule)")

        aturan_aktif = [
            (nomor, teks, alpha, konsekuen)
            for (nomor, alpha, konsekuen), teks in zip(inf, TEKS_ATURAN)
            if alpha > 0
        ]

        if aturan_aktif:
            data_inf = []
            for nomor, teks, alpha, konsekuen in aturan_aktif:
                ikon = "🟢" if konsekuen == "tinggi" else ("🟡" if konsekuen == "sedang" else "🔴")
                data_inf.append({
                    "Rule":     f"R{nomor}",
                    "Aturan":   teks[:50] + "..." if len(teks) > 50 else teks,
                    "Nilai (α)": f"{alpha:.3f}",
                    "Output":   f"{ikon} {konsekuen.upper()}",
                })
            st.dataframe(pd.DataFrame(data_inf), use_container_width=True, hide_index=True)
        else:
            st.warning("Tidak ada aturan yang aktif")

    with col_kanan:
        # ── Tahap 3: Agregasi ─────────────────────────────────────────────────
        st.markdown("#### 3️⃣ Agregasi (Metode MAX – ctrl.ControlSystem)")
        st.markdown(f"""
        <div class="info-box">
            Output Kinerja (agregasi semua aturan):<br>
            🔴 <b>Rendah</b> = {agg['rendah']:.3f} &nbsp;|&nbsp;
            🟡 <b>Sedang</b> = {agg['sedang']:.3f} &nbsp;|&nbsp;
            🟢 <b>Tinggi</b> = {agg['tinggi']:.3f}
        </div>
        """, unsafe_allow_html=True)

        bg_plot = "#0f172a"
        fig2, ax2 = plt.subplots(figsize=(5.5, 3))
        fig2.patch.set_facecolor(bg_plot)
        ax2.set_facecolor("#1e1b4b")

        xo   = var_kinerja.universe
        # Potong fungsi keanggotaan output sesuai nilai alpha (fmin)
        y_rendah = np.fmin(agg["rendah"], var_kinerja['rendah'].mf)
        y_sedang = np.fmin(agg["sedang"], var_kinerja['sedang'].mf)
        y_tinggi = np.fmin(agg["tinggi"], var_kinerja['tinggi'].mf)
        # Agregasi dengan MAX
        y_agg = np.fmax(y_rendah, np.fmax(y_sedang, y_tinggi))

        ax2.fill_between(xo, y_rendah, alpha=0.4, color="#ef4444", label="Rendah")
        ax2.fill_between(xo, y_sedang, alpha=0.4, color="#f59e0b", label="Sedang")
        ax2.fill_between(xo, y_tinggi, alpha=0.4, color="#10b981", label="Tinggi")
        ax2.plot(xo, y_agg, color="#818cf8", lw=2, label="Agregasi")
        ax2.axvline(skor, color="white", lw=2, ls="--", label=f"Centroid={skor:.1f}")

        ax2.set_xlim(0, 100)
        ax2.set_ylim(0, 1.1)
        ax2.tick_params(colors="#e2e8f0", labelsize=7)
        ax2.spines[['top', 'right', 'left', 'bottom']].set_color('#374151')
        ax2.grid(True, alpha=0.1, color='#6366f1')
        ax2.legend(fontsize=7, framealpha=0.2, labelcolor="#e2e8f0",
                   facecolor="#1e1b4b", edgecolor="#374151")
        ax2.set_title("Fungsi Keanggotaan Output (Teraggregasi)",
                      color="#e2e8f0", fontsize=8)
        st.pyplot(fig2)
        plt.close()

        # ── Tahap 4: Defuzzifikasi ────────────────────────────────────────────
        st.markdown("#### 4️⃣ Defuzzifikasi (Centroid – ctrl.ControlSystemSimulation)")
        box_cls, score_cls, _ = get_result_style(kat)
        st.markdown(f"""
        <div class="{box_cls}">
            <div style='font-size:.85rem;color:#94a3b8;margin-bottom:4px;'>Nilai crisp (hasil akhir)</div>
            <div class="{score_cls}" style='font-size:3rem;'>{skor:.2f}</div>
            <div style='font-size:.85rem;color:#19532B;font-family:Poppins,sans-serif;
                    font-weight:600;'>Skor Kinerja</div>
            <div style='font-size:1.1rem;font-weight:700;color:#34d399;margin-top:8px;'>
                Kategori : <b>{kat}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════ #
#           HALAMAN 7 – HASIL & RANKING            #
# ════════════════════════════════════════════════ #
if menu == "Hasil & Ranking":
    st.markdown(""" <div class="page-title" style="color:#18542a;"> HASIL & RANKING - Peringkat Alternatif </div> """, unsafe_allow_html=True)

    col_tabel, col_best = st.columns([3, 2])

    with col_tabel:
        st.markdown("""
            <h3 style="color:#18542a;font-family:Poppins,sans-serif;font-weight:700;margin-bottom:10px;">
                        Peringkat Kinerja Destinasi
            </h3>
        """, unsafe_allow_html=True)

        df_tampil_rank = df_ranking[
            ["Rank", "Location_ID", "Skor_Kinerja", "Kategori"]
        ].copy()
        df_tampil_rank.columns = ["Rank", "Destinasi", "Skor Kinerja", "Kategori"]

        st.dataframe(
            df_tampil_rank,
            use_container_width=True,
            height=500,
            hide_index=True,
        )
        st.markdown("""
        <div style='font-size:.8rem; color:#F3E8CC; margin-top:6px;
                    font-family:Poppins,sans-serif;font-weight:500;'>
            Semakin tinggi skor, semakin baik kinerja destinasi wisata kerajinan.
        </div>
        """, unsafe_allow_html=True)

    with col_best:
        if len(df_ranking) > 0:
            terbaik = df_ranking.iloc[0]

            st.markdown(f"""
            <div class="result-box" style='margin-top:40px; background:#F3E8CC;
                        border:2px solid #19532B; backdrop-filter:none;'>
                <div style='font-size:3rem;margin-bottom:8px;'>🥇</div>
                <div style='font-size:.9rem;color:#19532B;font-family:
                            Poppins,sans-serif;font-weight:600;'>DESTINASI TERBAIK</div>
                <div style='font-size:1.5rem;font-weight:800;color:#19532B;
                            margin:8px 0;font-family:Poppins,sans-serif;'>
                    {terbaik["Location_ID"]}
                </div>

                <div style='font-size:.85rem;color:#19532B;font-family:Poppins,sans-serif;'>Skor Kinerja</div>
                <div style='font-size:2.5rem;font-weight:800;color:#19532B;font-family:Poppins,sans-serif;margin:8px 0;'>
                    {terbaik["Skor_Kinerja"]:.2f} / 100
                </div>

                <div style='font-size:.85rem;color:#19532B;font-family:Poppins,sans-serif;'>Kategori</div>
                <div style='font-size:1.3rem;font-weight:800;color:#19532B;font-family:Poppins,sans-serif;'>
                    ⭐ {terbaik["Kategori"]}
                </div>
                <div style='margin-top:12px;font-size:1.5rem;'>⭐⭐⭐⭐⭐</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
                <h4 style='color:#F3E8CC;font-family:Poppins,sans-serif;font-weight:700;margin-top:18px;'>
                    Distribusi Kategori </h4>
            """, unsafe_allow_html=True)

            distribusi = df_ranking["Kategori"].value_counts()
            for label, warna in [("TINGGI", "#059669"), ("SEDANG", "#d97706"), ("RENDAH", "#dc2626")]:
                jumlah = distribusi.get(label, 0)
                persen = jumlah / len(df_ranking) * 100
                st.markdown(f"""
                <div style='display:flex;align-items:center;gap:10px;margin-bottom:8px;'>
                    <div style='width:90px;font-size:.82rem;color:#e2e8f0;font-weight:600;'>{label}</div>
                    <div style='flex:1;background:#F3E8CC;border-radius:4px;height:16px;overflow:hidden;'>
                        <div style='width:{persen:.0f}%;height:100%;background:{warna};border-radius:4px;'></div>
                    </div>
                    <div style='width:60px;text-align:right;font-size:.82rem;color:{warna};font-weight:700;'>
                        {jumlah} ({persen:.0f}%)
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ════════════════════════════════════════════════ #
#             HALAMAN 8 – VISUALISASI              #
# ════════════════════════════════════════════════ #
if menu == "Visualisasi":
    st.markdown(""" <div class="page-title" style="color:#18542a;"> VISUALISASI - Grafik Hasil Ranking </div> """, unsafe_allow_html=True)

    warna_bg    = "#0f172a"
    warna_grid  = "#1e1b4b"
    warna_teks  = "#e2e8f0"

    jumlah_top = st.slider("Jumlah destinasi yang ditampilkan", 5, 20, 10)
    df_top     = df_ranking.head(jumlah_top)

    st.markdown("#### Grafik Peringkat Kinerja Destinasi Wisata Kerajinan (Handicraft Center)")

    fig3, ax3 = plt.subplots(figsize=(12, 5))
    fig3.patch.set_facecolor(warna_bg)
    ax3.set_facecolor(warna_grid)

    # Warna batang disesuaikan dengan kategori
    peta_warna_kat = {"TINGGI": "#059669", "SEDANG": "#d97706", "RENDAH": "#dc2626"}
    warna_batang   = [peta_warna_kat.get(k, "#ffffff") for k in df_top["Kategori"]]

    batang = ax3.bar(df_top["Location_ID"], df_top["Skor_Kinerja"],
                     color=warna_batang, width=0.6,
                     edgecolor="#1e1b4b", linewidth=0.5)

    # Label skor di atas setiap batang
    for bar, skor in zip(batang, df_top["Skor_Kinerja"]):
        ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
                 f"{skor:.1f}", ha="center", va="bottom",
                 color=warna_teks, fontsize=8, fontweight="bold")

    ax3.set_ylim(0, 110)
    ax3.set_xlabel("Destinasi",    color=warna_teks, fontsize=9)
    ax3.set_ylabel("Skor Kinerja", color=warna_teks, fontsize=9)
    ax3.set_title("Grafik Peringkat Kinerja Destinasi Wisata Kerajinan (Handicraft Center)",
                  color=warna_teks, fontsize=11, fontweight="bold", pad=10)
    ax3.tick_params(colors=warna_teks, labelsize=7)
    ax3.set_xticklabels(df_top["Location_ID"], rotation=45, ha="right")
    ax3.spines[['top', 'right', 'left', 'bottom']].set_color('#374151')
    ax3.grid(True, alpha=0.1, color="#6366f1", axis="y")

    legenda_patch = [
        mpatches.Patch(color="#059669", label="Tinggi"),
        mpatches.Patch(color="#d97706", label="Sedang"),
        mpatches.Patch(color="#dc2626", label="Rendah"),
    ]
    legenda = ax3.legend(
        handles=legenda_patch, fontsize=8, framealpha=0.2,
        labelcolor='white', facecolor=warna_grid, edgecolor='#374151',
        title="Kategori", title_fontsize=8, loc="upper right"
    )
    legenda.get_title().set_color("white")

    plt.tight_layout()
    st.pyplot(fig3)
    plt.close()

    st.markdown(f"""
    <div style='font-size:.75rem;color:#94a3b8;margin-top:4px;'>
        ℹ️ Grafik ini menunjukkan {jumlah_top} destinasi terbaik berdasarkan skor kinerja tertinggi.
    </div>
    """, unsafe_allow_html=True)

    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown("#### Distribusi Kategori Kinerja")
        fig4, ax4 = plt.subplots(figsize=(4, 4))
        fig4.patch.set_facecolor(warna_bg)
        ax4.set_facecolor(warna_bg)

        dist2       = df_ranking["Kategori"].value_counts()
        label_pie   = dist2.index.tolist()
        nilai_pie   = dist2.values.tolist()
        warna_pie   = [peta_warna_kat.get(k, "#6366f1") for k in label_pie]

        wedges, texts, autotexts = ax4.pie(
            nilai_pie, labels=label_pie, autopct='%1.1f%%',
            colors=warna_pie, startangle=90,
            textprops={'color': warna_teks, 'fontsize': 7},
        )
        for at in autotexts:
            at.set_color("white")
            at.set_fontweight("bold")
        ax4.set_title("Distribusi Kategori", color=warna_teks, fontsize=8.3, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close()

    with col_p2:
        st.markdown("#### Distribusi Skor Kinerja")
        fig5, ax5 = plt.subplots(figsize=(5, 4.72))
        fig5.patch.set_facecolor(warna_bg)
        ax5.set_facecolor(warna_grid)

        ax5.hist(df_ranking["Skor_Kinerja"], bins=20,
                 color="#6366f1", edgecolor="#1e1b4b", alpha=0.8)
        rata_rata = df_ranking["Skor_Kinerja"].mean()
        ax5.axvline(rata_rata, color="#f59e0b", lw=2, ls="--",
                    label=f"Mean: {rata_rata:.1f}")
        ax5.set_xlabel("Skor Kinerja", color=warna_teks, fontsize=9)
        ax5.set_ylabel("Frekuensi",    color=warna_teks, fontsize=9)
        ax5.set_title("Distribusi Skor Kinerja",
                      color=warna_teks, fontsize=10, fontweight="bold")
        ax5.tick_params(colors=warna_teks, labelsize=7)
        ax5.spines[['top', 'right', 'left', 'bottom']].set_color('#374151')
        ax5.grid(True, alpha=0.1, color="#6366f1")
        ax5.legend(fontsize=8, framealpha=0.2, labelcolor=warna_teks,
                   facecolor=warna_grid, edgecolor='#374151')
        plt.tight_layout()
        st.pyplot(fig5)
        plt.close()


# ════════════════════════════════════════════════ #
#             HALAMAN 9 – PROFILE TIM              #
# ════════════════════════════════════════════════ #
if menu == "Profile Tim":
    st.markdown(""" <div class="page-title" style="color:#18542a;"> PROFILE TIM </div> """, unsafe_allow_html=True)

    col_tentang, col_info = st.columns([3, 2])

    with col_tentang:
        st.markdown("""
        <div class="card">
            <h3 style='color:#818cf8;margin:0 0 12px;'>Tentang Sistem</h3>
            <p style='color:#94a3b8;font-size:.88rem;line-height:1.7;'>
                Aplikasi ini dikembangkan sebagai proyek akhir mata kuliah
                Sistem Cerdas dan Pengambilan Keputusan (SCPK)
                dengan metode Fuzzy Mamdani menggunakan library <b>scikit-fuzzy</b>
                untuk mendukung penilaian kinerja destinasi wisata kerajinan.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            "<h4 style='text-align:center;'>Anggota Kelompok</h4>",
            unsafe_allow_html=True
        )

        anggota = [
            ("👨‍💻", "Lathiva Safina Almasea",   "NIM. 123240226", "Prodi Informatika"),
            ("👩‍🔬", "Mutiara Rahmawati Zalsa",  "NIM. 123240257", "Prodi Informatika"),
        ]
        kolom_anggota = st.columns(len(anggota))
        for i, (ikon, nama, nim, prodi) in enumerate(anggota):
            with kolom_anggota[i]:
                st.markdown(f"""
                <div class="card" style='text-align:center;'>
                    <div style='font-size:3rem;margin-bottom:8px;'>{ikon}</div>
                    <div style='font-weight:700;color:#F3E8CC;font-size:.95rem;font-family:Poppins,sans-serif;'>{nama}</div>
                    <div style='font-size:.78rem;color:#a5b4fc;margin:4px 0;'>{nim}</div>
                    <div style='font-size:.75rem;color:#94a3b8;'>{prodi}</div>
                </div>
                """, unsafe_allow_html=True)

    with col_info:
        st.markdown("""
        <div class="card">
            <h4 style='color:#818cf8;text-align:center'>Informasi Sistem</h4>
        """, unsafe_allow_html=True)

        info_sistem = [
            ("Metode",  "Fuzzy Mamdani"),
            ("Bahasa",  "Python 3 (Streamlit)"),
            ("Library", "scikit-fuzzy, pandas, matplotlib, numpy"),
            ("Dataset", "Rural Heritage Tourism Industry Chain Dataset (Kaggle)"),
            ("Filter",  "Heritage_Type = Handicraft Center (784 baris)"),
            ("Tahun",   "2025/2026"),
        ]
        for label, nilai in info_sistem:
            st.markdown(f"""
            <div style='display:flex;margin-bottom:4px;align-items:flex-start;'>
                <div style='min-width:100px;padding-left:20px;font-size:.8rem;
                            color:#a5b4fc;font-weight:600;'>{label}</div>
                <div style='font-size:.8rem;color:#e2e8f0;'>: {nilai}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h4 style='color:#818cf8;'>Alur Sistem Fuzzy Mamdani (scikit-fuzzy)</h4>
            <div style='font-size:.82rem;color:#e2e8f0;line-height:1.95;'>
                1️⃣ <b>ctrl.Antecedent / ctrl.Consequent</b> – Definisi variabel<br>
                2️⃣ <b>fuzz.trimf / fuzz.trapmf</b> – Fungsi keanggotaan<br>
                3️⃣ <b>ctrl.Rule (&amp;)</b> – Aturan IF-THEN (AND = MIN)<br>
                4️⃣ <b>ctrl.ControlSystem</b> – Bangun sistem kontrol<br>
                5️⃣ <b>ctrl.ControlSystemSimulation</b> – Hitung &amp; defuzzifikasi (centroid)
            </div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════ #
#                    FOOTER                        #
# ════════════════════════════════════════════════ #
st.markdown("""
<div class="footer-card">
    SPK Kinerja Destinasi Wisata Kerajinan (Handicraft Tourism)
    Metode Fuzzy Mamdani (scikit-fuzzy) |
    © Ivaa &amp; Alsa, All I Wanna Do! Project Gacor! 2026.
</div>
""", unsafe_allow_html=True)