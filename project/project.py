import streamlit as st
import pandas as pd
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import base64

def load_svg(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

#----------------------------#
#        PAGE CONFIG         #
#----------------------------#
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

#----------------------------#
#         GLOBAL CSS         #
#----------------------------#
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
     
</style>
""".replace("%s", bg_img), unsafe_allow_html=True)

#----------------------------#
#          LOAD DATA         #
#----------------------------#
@st.cache_data
def load_data():
    df = pd.read_csv("rural_heritage_tourism_industry_chain_dataset.csv")
    hc = df[df["Heritage_Type"] == "Handicraft Center"].copy()
    hc = hc.reset_index(drop=True)
    hc.index = hc.index + 1
    return df, hc

df_all, df_hc = load_data()

#---------------------------------------#
#    SCIKIT-FUZZY VARIABLE DEFINITIONS  #
#   (sesuai Modul IX: ctrl.Antecedent,  #
#    ctrl.Consequent, fuzz.trimf,       #
#    fuzz.trapmf, ctrl.Rule,            #
#    ctrl.ControlSystem,                #
#    ctrl.ControlSystemSimulation)      #
#---------------------------------------#

@st.cache_resource
def build_fuzzy_system():
    """
    Membangun sistem inferensi Fuzzy Mamdani menggunakan library scikit-fuzzy
    sesuai panduan Modul IX Praktikum Kecerdasan Buatan UPN Veteran Yogyakarta.

    Variabel input (ctrl.Antecedent) dan output (ctrl.Consequent) didefinisikan
    dengan universe sesuai range dataset Handicraft Center.
    Fungsi keanggotaan menggunakan fuzz.trimf (segitiga) dan fuzz.trapmf (trapesium).
    Aturan fuzzy IF-THEN dibangun menggunakan ctrl.Rule dengan operator & (AND/MIN).
    """

    # ── Definisi Antecedent (Input) ──────────────────────────────────────────
    # np.arange: interval setengah terbuka → batas atas dilebihkan 1 (sesuai Modul IX)
    visitor_count   = ctrl.Antecedent(np.arange(52,  800, 1), 'visitor_count')
    ticket_price    = ctrl.Antecedent(np.arange(10,  100, 1), 'ticket_price')
    tourist_sat     = ctrl.Antecedent(np.arange(0.0, 5.1, 0.1), 'tourist_sat')
    revenue         = ctrl.Antecedent(np.arange(5000, 100001, 100), 'revenue')
    op_cost         = ctrl.Antecedent(np.arange(2000, 50001, 100), 'op_cost')

    # ── Definisi Consequent (Output) ─────────────────────────────────────────
    kinerja = ctrl.Consequent(np.arange(0, 101, 1), 'kinerja', defuzzify_method='centroid')

    # ── Fungsi Keanggotaan – Visitor Count (C1: Benefit) ─────────────────────
    visitor_count['rendah'] = fuzz.trapmf(visitor_count.universe, [52,  52,  200, 400])
    visitor_count['sedang'] = fuzz.trimf( visitor_count.universe, [200, 425, 650])
    visitor_count['tinggi'] = fuzz.trapmf(visitor_count.universe, [500, 650, 799, 799])

    # ── Fungsi Keanggotaan – Ticket Price (C2: Cost) ─────────────────────────
    ticket_price['murah']  = fuzz.trapmf(ticket_price.universe, [10, 10, 30, 55])
    ticket_price['sedang'] = fuzz.trimf( ticket_price.universe, [30, 55, 80])
    ticket_price['mahal']  = fuzz.trapmf(ticket_price.universe, [60, 80, 99, 99])

    # ── Fungsi Keanggotaan – Tourist Satisfaction (C3: Benefit) ──────────────
    tourist_sat['rendah'] = fuzz.trapmf(tourist_sat.universe, [0.0, 0.0, 2.0, 3.25])
    tourist_sat['sedang'] = fuzz.trimf( tourist_sat.universe, [2.5, 3.5, 4.5])
    tourist_sat['tinggi'] = fuzz.trapmf(tourist_sat.universe, [3.75, 4.5, 5.0, 5.0])

    # ── Fungsi Keanggotaan – Revenue Generated (C4: Benefit) ─────────────────
    revenue['rendah'] = fuzz.trapmf(revenue.universe, [5000,  5000,  30000, 55000])
    revenue['sedang'] = fuzz.trimf( revenue.universe, [30000, 55000, 80000])
    revenue['tinggi'] = fuzz.trapmf(revenue.universe, [60000, 80000, 100000, 100000])

    # ── Fungsi Keanggotaan – Operational Cost (C5: Cost) ─────────────────────
    op_cost['rendah'] = fuzz.trapmf(op_cost.universe, [2000,  2000,  15000, 27000])
    op_cost['sedang'] = fuzz.trimf( op_cost.universe, [15000, 27500, 40000])
    op_cost['tinggi'] = fuzz.trapmf(op_cost.universe, [30000, 40000, 50000, 50000])

    # ── Fungsi Keanggotaan – Output Kinerja ──────────────────────────────────
    kinerja['rendah'] = fuzz.trapmf(kinerja.universe, [0,  0,  25, 50])
    kinerja['sedang'] = fuzz.trimf( kinerja.universe, [25, 50, 75])
    kinerja['tinggi'] = fuzz.trapmf(kinerja.universe, [50, 75, 100, 100])

    # ── Rule Base (15 aturan IF-THEN) ────────────────────────────────────────
    # Operator AND (&) = MIN, sesuai Modul IX penalaran min-max Mamdani
    rules = [
        ctrl.Rule(visitor_count['tinggi'] & tourist_sat['tinggi'],  kinerja['tinggi']),   # R1
        ctrl.Rule(visitor_count['sedang'] & tourist_sat['tinggi'],  kinerja['tinggi']),   # R2
        ctrl.Rule(visitor_count['rendah'],                           kinerja['rendah']),   # R3
        ctrl.Rule(ticket_price['murah']   & tourist_sat['tinggi'],  kinerja['tinggi']),   # R4
        ctrl.Rule(ticket_price['mahal']   & tourist_sat['rendah'],  kinerja['rendah']),   # R5
        ctrl.Rule(ticket_price['sedang']  & tourist_sat['sedang'],  kinerja['sedang']),   # R6
        ctrl.Rule(revenue['tinggi']       & op_cost['rendah'],       kinerja['tinggi']),   # R7
        ctrl.Rule(revenue['tinggi']       & op_cost['tinggi'],       kinerja['sedang']),   # R8
        ctrl.Rule(revenue['rendah'],                                 kinerja['rendah']),   # R9
        ctrl.Rule(op_cost['tinggi'],                                 kinerja['rendah']),   # R10
        ctrl.Rule(op_cost['rendah']       & tourist_sat['tinggi'],  kinerja['tinggi']),   # R11
        ctrl.Rule(tourist_sat['rendah'],                             kinerja['rendah']),   # R12
        ctrl.Rule(tourist_sat['sedang'],                             kinerja['sedang']),   # R13
        ctrl.Rule(visitor_count['tinggi'] & ticket_price['mahal'],  kinerja['sedang']),   # R14
        ctrl.Rule(visitor_count['sedang'] & ticket_price['sedang'], kinerja['sedang']),   # R15
    ]

    # ── Bangun Sistem Kontrol Fuzzy ───────────────────────────────────────────
    kinerja_ctrl = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(kinerja_ctrl)

    return sim, visitor_count, ticket_price, tourist_sat, revenue, op_cost, kinerja

# Build system once (cached)
fuzzy_sim, var_visitor, var_ticket, var_sat, var_revenue, var_op, var_kinerja = build_fuzzy_system()

#---------------------------------------#
#       FUZZY MAMDANI COMPUTE           #
#---------------------------------------#

RULE_TEXT = [
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

RULES_DEF = [
    (1,  {"visitor_count":"tinggi", "tourist_sat":"tinggi"},              "tinggi"),
    (2,  {"visitor_count":"sedang", "tourist_sat":"tinggi"},              "tinggi"),
    (3,  {"visitor_count":"rendah"},                                       "rendah"),
    (4,  {"ticket_price":"murah",   "tourist_sat":"tinggi"},              "tinggi"),
    (5,  {"ticket_price":"mahal",   "tourist_sat":"rendah"},              "rendah"),
    (6,  {"ticket_price":"sedang",  "tourist_sat":"sedang"},              "sedang"),
    (7,  {"revenue":"tinggi",       "op_cost":"rendah"},                  "tinggi"),
    (8,  {"revenue":"tinggi",       "op_cost":"tinggi"},                  "sedang"),
    (9,  {"revenue":"rendah"},                                             "rendah"),
    (10, {"op_cost":"tinggi"},                                             "rendah"),
    (11, {"op_cost":"rendah",       "tourist_sat":"tinggi"},              "tinggi"),
    (12, {"tourist_sat":"rendah"},                                         "rendah"),
    (13, {"tourist_sat":"sedang"},                                         "sedang"),
    (14, {"visitor_count":"tinggi", "ticket_price":"mahal"},              "sedang"),
    (15, {"visitor_count":"sedang", "ticket_price":"sedang"},             "sedang"),
]

def compute_fuzzification(c1, c2, c3, c4, c5):
    """Hitung derajat keanggotaan menggunakan fuzz.interp_membership sesuai scikit-fuzzy."""
    return {
        "visitor_count": {
            "rendah": float(fuzz.interp_membership(var_visitor.universe, var_visitor['rendah'].mf, c1)),
            "sedang": float(fuzz.interp_membership(var_visitor.universe, var_visitor['sedang'].mf, c1)),
            "tinggi": float(fuzz.interp_membership(var_visitor.universe, var_visitor['tinggi'].mf, c1)),
        },
        "ticket_price": {
            "murah":  float(fuzz.interp_membership(var_ticket.universe, var_ticket['murah'].mf,  c2)),
            "sedang": float(fuzz.interp_membership(var_ticket.universe, var_ticket['sedang'].mf, c2)),
            "mahal":  float(fuzz.interp_membership(var_ticket.universe, var_ticket['mahal'].mf,  c2)),
        },
        "tourist_sat": {
            "rendah": float(fuzz.interp_membership(var_sat.universe, var_sat['rendah'].mf, c3)),
            "sedang": float(fuzz.interp_membership(var_sat.universe, var_sat['sedang'].mf, c3)),
            "tinggi": float(fuzz.interp_membership(var_sat.universe, var_sat['tinggi'].mf, c3)),
        },
        "revenue": {
            "rendah": float(fuzz.interp_membership(var_revenue.universe, var_revenue['rendah'].mf, c4)),
            "sedang": float(fuzz.interp_membership(var_revenue.universe, var_revenue['sedang'].mf, c4)),
            "tinggi": float(fuzz.interp_membership(var_revenue.universe, var_revenue['tinggi'].mf, c4)),
        },
        "op_cost": {
            "rendah": float(fuzz.interp_membership(var_op.universe, var_op['rendah'].mf, c5)),
            "sedang": float(fuzz.interp_membership(var_op.universe, var_op['sedang'].mf, c5)),
            "tinggi": float(fuzz.interp_membership(var_op.universe, var_op['tinggi'].mf, c5)),
        },
    }

def compute_inference(fuzz_vals):
    """Hitung α-predikat setiap rule menggunakan operator AND (MIN)."""
    results = []
    for (rno, antecedent, consequent) in RULES_DEF:
        alphas = [fuzz_vals[var][term] for var, term in antecedent.items()]
        alpha = min(alphas)  # AND = MIN (sesuai Modul IX)
        results.append((rno, alpha, consequent))
    return results

def compute_aggregation(inf_results):
    """Agregasi menggunakan MAX per kategori output."""
    agg = {"tinggi": 0.0, "sedang": 0.0, "rendah": 0.0}
    for (_, alpha, cons) in inf_results:
        agg[cons] = max(agg[cons], alpha)
    return agg

def fuzzy_mamdani(c1, c2, c3, c4, c5):
    """
    Hitung skor kinerja menggunakan ctrl.ControlSystemSimulation (scikit-fuzzy).
    Defuzzifikasi centroid dilakukan otomatis oleh scikit-fuzzy.
    Juga mengembalikan detail fuzzifikasi, inferensi, agregasi untuk tampilan.
    """
    # Clamp inputs to universe bounds
    c1 = float(np.clip(c1, 52, 799))
    c2 = float(np.clip(c2, 10, 99))
    c3 = float(np.clip(c3, 0.0, 5.0))
    c4 = float(np.clip(c4, 5000, 100000))
    c5 = float(np.clip(c5, 2000, 50000))

    # Jalankan simulasi scikit-fuzzy (fuzzifikasi + inferensi + agregasi + defuzzifikasi)
    fuzzy_sim.input['visitor_count'] = c1
    fuzzy_sim.input['ticket_price']  = c2
    fuzzy_sim.input['tourist_sat']   = c3
    fuzzy_sim.input['revenue']       = c4
    fuzzy_sim.input['op_cost']       = c5
    fuzzy_sim.compute()

    score = float(fuzzy_sim.output['kinerja'])

    # Detail per-tahap untuk tampilan UI
    fuzz_vals = compute_fuzzification(c1, c2, c3, c4, c5)
    inf_res   = compute_inference(fuzz_vals)
    agg       = compute_aggregation(inf_res)
    kat       = get_kategori(score)

    return score, kat, fuzz_vals, inf_res, agg

def get_kategori(score):
    if score >= 66.67:
        return "TINGGI"
    elif score >= 33.33:
        return "SEDANG"
    else:
        return "RENDAH"

def get_result_style(kat):
    if kat == "TINGGI":
        return "result-box", "result-score", "🥇"
    elif kat == "SEDANG":
        return "result-box-sedang", "result-score-sedang", "🥈"
    return "result-box-rendah", "result-score-rendah", "🥉"

#----------------------------------------#
#        COMPUTE SCORES ALL ROWS         #
#----------------------------------------#
@st.cache_data
def compute_all_scores(df):
    scores = []
    for _, row in df.iterrows():
        s, k, _, _, _ = fuzzy_mamdani(
            row["Visitor_Count"],
            row["Ticket_Price"],
            row["Tourist_Satisfaction"],
            row["Revenue_Generated"],
            row["Operational_Cost"],
        )
        scores.append({"Skor_Kinerja": round(s, 2), "Kategori": k})
    result = pd.DataFrame(scores)
    return result

score_df  = compute_all_scores(df_hc)
df_result = pd.concat([df_hc.reset_index(drop=True), score_df], axis=1)
df_ranked = df_result.sort_values("Skor_Kinerja", ascending=False).reset_index(drop=True)
df_ranked.insert(0, "Rank", range(1, len(df_ranked) + 1))

#----------------------------#
#          SIDEBAR           #
#----------------------------#
st.sidebar.markdown(
    """
    <div class="sidebar-top">
        <div class="sidebar-logo">
            SPK<br>MAMDANI
        </div>
        <div class="sidebar-sub">
            Fuzzy Decision Support System
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"

menus = [
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

for item in menus:
    if st.sidebar.button(item, use_container_width=True):
        st.session_state.menu = item

menu = st.session_state.menu
st.markdown("""
    """, unsafe_allow_html=True)

# ────────────────────────────────────────────────────── #
#                   PAGE 1 – DASHBOARD                   #
# ────────────────────────────────────────────────────── #
if menu == "Dashboard":

    svg_db       = load_svg("files-db.svg")
    svg_db_b64 = base64.b64encode(svg_db.encode()).decode()

    svg_visitor  = load_svg("visitor-count.svg")
    svg_visitor_b64 = base64.b64encode(svg_visitor.encode()).decode()

    svg_ticket   = load_svg("ticket.svg")
    svg_ticket_b64 = base64.b64encode(svg_ticket.encode()).decode()

    svg_rate     = load_svg("rate.svg")
    svg_rate_b64 = base64.b64encode(svg_rate.encode()).decode()

    svg_revenue  = load_svg("revenue-bag.svg")
    svg_revenue_b64 = base64.b64encode(svg_revenue.encode()).decode()

    svg_ops      = load_svg("operational.svg")
    svg_ops_b64 = base64.b64encode(svg_ops.encode()).decode()

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

    total_all = len(df_all)
    total_hc  = len(df_hc)

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
                berdasarkan 5 kriteria menggunakan metode Fuzzy Mamdani Inference System (FMIS)<br>
                via library <b>scikit-fuzzy</b> (ctrl.Antecedent, ctrl.Consequent, fuzz.trimf, fuzz.trapmf).
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_total:
        st.markdown(f"""
        <div class="total-card">
            <div class="db-icon-wrap">
                <img src="data:image/svg+xml;base64,{svg_db_b64}" class="db-icon">
            </div>
            <div class="total-num">{total_all}</div>
            <div class="total-label">Total Data</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='dash-section-title'>Kriteria Penilaian</div>", unsafe_allow_html=True)

    kriteria = [
        ("C1", "Visitor Count",        "(52-799)",         "Benefit", svg_visitor),
        ("C2", "Ticket Price",         "(10-99)",          "Cost",    svg_ticket),
        ("C3", "Tourist Satisfaction", "(0-5)",            "Benefit", svg_rate),
        ("C4", "Revenue Generated",    "(5.000-100.000)",  "Benefit", svg_revenue),
        ("C5", "Operational Cost",     "(2.000-50.000)",   "Cost",    svg_ops),
    ]

    k_cols = st.columns(5)
    for i, (code, name, rng, btype, svg_icon) in enumerate(kriteria):
        badge = "<span class='badge-benefit'>Benefit</span>" if btype == "Benefit" else "<span class='badge-cost'>Cost</span>"
        with k_cols[i]:
            st.markdown(f"""
            <div class="krit-card">
                <div style='width:48px;height:48px;margin-bottom:6px;'>{svg_icon}</div>
                <div class="kc">{code}</div>
                <div class="kname">{name}</div>
                <div class="krange">{rng}</div>
                {badge}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='dash-section-title-yellow'>Ringkasan Sistem</div>", unsafe_allow_html=True)

    r_cols = st.columns(4)
    ring_data = [
        (str(total_all), "Total Data", "(Dataset)"),
        (str(total_hc), "Data Handicraft<br>Center", "(Setelah di Filter)"),
        ("5", "Jumlah Kriteria", "(Kriteria)"),
        ("Fuzzy Mamdani", " ", "Inference System"),
    ]

    for i, (val, label, sub) in enumerate(ring_data):
        with r_cols[i]:
            st.markdown(f"""
            <div class="ring-card-dark">
                <div class="rnum">{val}</div>
                <div class="rlabel">{label}</div>
                <div class="rsub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

# ────────────────────────────────────────────────────── #
#                    PAGE 2 – DATASET                    #
# ────────────────────────────────────────────────────── #
if menu == "Dataset":
    st.markdown("""
    <div class="page-title">
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
        csv_data = df_hc[["Location_ID","Heritage_Type","Visitor_Count","Ticket_Price",
                      "Tourist_Satisfaction","Revenue_Generated","Operational_Cost"]].to_csv(index=False)

        st.download_button(
            "Export CSV",
            csv_data,
            "handicraft_center.csv",
            "text/csv"
        )

    st.markdown(f"""
    <div class="dataset-total">
        Total Data Setelah Filter:
        <span>{len(df_hc)}</span> baris
    </div>
    """, unsafe_allow_html=True)

    display_cols = ["Location_ID","Heritage_Type","Visitor_Count","Ticket_Price",
                "Tourist_Satisfaction","Revenue_Generated","Operational_Cost"]

    show_df = df_hc[display_cols].copy()
    show_df.index = show_df.index + 1
    show_df.columns = ["Destinasi","Heritage Type","Visitor Count","Ticket Price",
                       "Tourist Satisfaction","Revenue Generated","Operational Cost"]

    st.dataframe(show_df, use_container_width=True, height=450)

# ────────────────────────────────────────────────────── #
#                  PAGE 3 – FUZZIFIKASI                  #
# ────────────────────────────────────────────────────── #
if menu == "Fuzzifikasi":
    st.markdown("""
    <div class="page-title">
        Fuzzifikasi
    </div>
    """, unsafe_allow_html=True)

    bg_color   = "#0f172a"
    grid_color = "#1e1b4b"
    text_color = "#e2e8f0"

    def plot_mf_skfuzzy(ax, variable, labels, title, colors_map):
        """Plot fungsi keanggotaan dari variabel scikit-fuzzy."""
        ax.set_facecolor(grid_color)
        ax.spines[['top','right','left','bottom']].set_color('#374151')
        ax.tick_params(colors=text_color, labelsize=7)
        ax.set_title(title, color=text_color, fontsize=8, fontweight='bold', pad=6)
        ax.set_ylim(-0.05, 1.1)
        ax.set_xlim(variable.universe[0], variable.universe[-1])
        ax.grid(True, alpha=0.15, color='#6366f1')
        for lbl in labels:
            col = colors_map.get(lbl, "#818cf8")
            ax.plot(variable.universe, variable[lbl].mf,
                    color=col, lw=2, label=lbl.capitalize())
        ax.legend(fontsize=6, framealpha=0.2, labelcolor=text_color,
                  facecolor=grid_color, edgecolor='#374151')

    fig, axes = plt.subplots(2, 3, figsize=(14, 7))
    fig.patch.set_facecolor(bg_color)
    plt.subplots_adjust(wspace=0.35, hspace=0.5)

    plot_mf_skfuzzy(axes[0,0], var_visitor,
                    ["rendah","sedang","tinggi"],
                    "C1 – Visitor Count (Benefit)",
                    {"rendah":"#ef4444","sedang":"#f59e0b","tinggi":"#10b981"})

    plot_mf_skfuzzy(axes[0,1], var_ticket,
                    ["murah","sedang","mahal"],
                    "C2 – Ticket Price (Cost)",
                    {"murah":"#3b82f6","sedang":"#f59e0b","mahal":"#ef4444"})

    plot_mf_skfuzzy(axes[0,2], var_sat,
                    ["rendah","sedang","tinggi"],
                    "C3 – Tourist Satisfaction (Benefit)",
                    {"rendah":"#ef4444","sedang":"#f59e0b","tinggi":"#10b981"})

    plot_mf_skfuzzy(axes[1,0], var_revenue,
                    ["rendah","sedang","tinggi"],
                    "C4 – Revenue Generated (Benefit)",
                    {"rendah":"#ef4444","sedang":"#f59e0b","tinggi":"#10b981"})

    plot_mf_skfuzzy(axes[1,1], var_op,
                    ["rendah","sedang","tinggi"],
                    "C5 – Operational Cost (Cost)",
                    {"rendah":"#10b981","sedang":"#f59e0b","tinggi":"#ef4444"})

    plot_mf_skfuzzy(axes[1,2], var_kinerja,
                    ["rendah","sedang","tinggi"],
                    "Output – Kinerja Destinasi",
                    {"rendah":"#ef4444","sedang":"#f59e0b","tinggi":"#10b981"})

    st.pyplot(fig)
    plt.close()

    st.markdown("""
<div class='fuzzy-note'>

<div class='fuzzy-note-title'>
    Keterangan Fungsi Keanggotaan
</div>

<div class='fuzzy-note-text'>
Diimplementasikan menggunakan <b>fuzz.trimf</b> (segitiga) dan <b>fuzz.trapmf</b> (trapesium)<br>
dari library scikit-fuzzy, didefinisikan pada <b>ctrl.Antecedent</b> (input) dan <b>ctrl.Consequent</b> (output).
</div>

<div class='fuzzy-note-tags'>
<span style='color:#E53935;'>Rendah / Murah</span>
= Trapesium kiri (trapmf)

<span style='color:#D4A017;'>Sedang</span>
= Segitiga tengah (trimf)

<span style='color:#00A86B;'>Tinggi / Mahal</span>
= Trapesium kanan (trapmf)
                
</div>

</div>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────────── #
#                   PAGE 4 – RULE BASE                   #
# ────────────────────────────────────────────────────── #
elif menu == "Rule Base":
    st.markdown("""
    <div class="section-header">
        <span class="section-num">4</span>
        RULE BASE – Aturan Fuzzy (IF – THEN)
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-box">
        📋 Total Rule: <b>15 aturan</b> &nbsp;|&nbsp; Operator: <b>AND (&amp;) = MIN</b> &nbsp;|&nbsp; Implementasi: <b>ctrl.Rule (scikit-fuzzy)</b>
    </div>
    """, unsafe_allow_html=True)

    badge = {
        "tinggi": "<span class='badge-tinggi'>Tinggi</span>",
        "sedang": "<span class='badge-sedang'>Sedang</span>",
        "rendah": "<span class='badge-rendah'>Rendah</span>",
    }

    for i, (rule_txt, (rno, ant, cons)) in enumerate(zip(RULE_TEXT, RULES_DEF)):
        col_no, col_rule, col_out = st.columns([0.5, 6, 1])
        with col_no:
            st.markdown(f"""
            <div style='background:rgba(99,102,241,0.3);border-radius:50%;width:32px;height:32px;
                        display:flex;align-items:center;justify-content:center;
                        font-weight:800;color:#818cf8;font-size:.85rem;margin-top:6px;'>{rno}</div>
            """, unsafe_allow_html=True)
        with col_rule:
            st.markdown(f"""
            <div style='padding:10px 14px;background:rgba(30,27,75,0.6);
                        border:1px solid rgba(99,102,241,0.25);border-radius:8px;
                        font-size:.85rem;color:#e2e8f0;margin-top:4px;'>
                {rule_txt}
            </div>
            """, unsafe_allow_html=True)
        with col_out:
            st.markdown(f"""
            <div style='margin-top:10px;text-align:center;'>
                {badge[cons]}
            </div>
            """, unsafe_allow_html=True)

# ────────────────────────────────────────────────────── #
#                  PAGE 5 – HITUNG SPK                   #
# ────────────────────────────────────────────────────── #
elif menu == "Hitung SPK":
    st.markdown("""
    <div class="section-header">
        <span class="section-num">5</span>
        HITUNG SPK – Input Data &amp; Eksekusi
    </div>
    """, unsafe_allow_html=True)

    col_input, col_select = st.columns([3, 2])

    with col_input:
        st.markdown("#### Input Nilai Kriteria")
        st.markdown("""
        <div class="info-box" style='font-size:.82rem;'>
            Masukkan nilai untuk menghitung kinerja destinasi
        </div>
        """, unsafe_allow_html=True)

        c1_val = st.slider("C1 – Visitor Count (Benefit)", 52, 799, 400,
                           help="Semakin tinggi visitor, semakin baik")
        c2_val = st.slider("C2 – Ticket Price (Cost)", 10, 99, 35,
                           help="Semakin murah, semakin baik")
        c3_val = st.slider("C3 – Tourist Satisfaction (Benefit)", 0.0, 5.0, 4.0, 0.1,
                           help="Semakin tinggi, semakin baik")
        c4_val = st.number_input("C4 – Revenue Generated (Benefit)", 5000, 100000, 50000, 1000,
                                  help="Semakin besar revenue, semakin baik")
        c5_val = st.number_input("C5 – Operational Cost (Cost)", 2000, 50000, 20000, 500,
                                  help="Semakin kecil cost, semakin baik")

    with col_select:
        st.markdown("#### Pilih Alternatif / Destinasi")
        dest_options = ["-- Input Manual --"] + df_hc["Location_ID"].tolist()
        selected_dest = st.selectbox("Pilih Destinasi dari Dataset", dest_options)

        if selected_dest != "-- Input Manual --":
            row = df_hc[df_hc["Location_ID"] == selected_dest].iloc[0]
            c1_val = int(row["Visitor_Count"])
            c2_val = int(row["Ticket_Price"])
            c3_val = float(row["Tourist_Satisfaction"])
            c4_val = int(row["Revenue_Generated"])
            c5_val = int(row["Operational_Cost"])
            st.info(f"""
            **Data Destinasi: {selected_dest}**
            - Visitor Count: {c1_val}
            - Ticket Price: {c2_val}
            - Satisfaction: {c3_val}
            - Revenue: {c4_val:,}
            - Op. Cost: {c5_val:,}
            """)

        st.markdown("#### Keterangan Kriteria")
        st.markdown("""
        <div class="info-box" style='font-size:.8rem;'>
            <b>C1 Benefit:</b> Semakin besar semakin baik<br>
            <b>C2 Cost:</b> Semakin kecil semakin baik<br>
            <b>C3 Benefit:</b> Semakin besar semakin baik<br>
            <b>C4 Benefit:</b> Semakin besar semakin baik<br>
            <b>C5 Cost:</b> Semakin kecil semakin baik
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("▶ HITUNG SPK", use_container_width=True):
        score, kat, fuzz_vals, inf_res, agg = fuzzy_mamdani(
            c1_val, c2_val, c3_val, c4_val, c5_val
        )

        st.session_state["last_result"] = {
            "score": score, "kat": kat, "fuzz": fuzz_vals,
            "inf": inf_res, "agg": agg,
            "c1": c1_val, "c2": c2_val, "c3": c3_val,
            "c4": c4_val, "c5": c5_val,
        }

        box_class, score_class, emoji = get_result_style(kat)

        st.markdown(f"""
        <div class="{box_class}">
            <div style='font-size:2rem;margin-bottom:8px;'>{emoji}</div>
            <div class="{score_class}">{score:.2f} / 100</div>
            <div class="result-kategori">Kategori: {kat}</div>
        </div>
        """, unsafe_allow_html=True)

        st.success(f"✅ Perhitungan selesai! Skor Kinerja: **{score:.2f}** – Kategori: **{kat}**")
        st.info("💡 Lihat detail proses di menu **🔍 Proses Fuzzy**")

# ───────────────────────────────────────────────────── #
#                 PAGE 6 – PROSES FUZZY                 #
# ───────────────────────────────────────────────────── #
elif menu == "Proses Fuzzy":
    st.markdown("""
    <div class="section-header">
        <span class="section-num">6</span>
        PROSES FUZZY – Detail Perhitungan (Mamdani via scikit-fuzzy)
    </div>
    """, unsafe_allow_html=True)

    if "last_result" not in st.session_state:
        st.warning("⚠️ Belum ada perhitungan. Silakan ke menu **⚙️ Hitung SPK** terlebih dahulu.")
        st.stop()

    res   = st.session_state["last_result"]
    score = res["score"]
    kat   = res["kat"]
    fuzz_vals = res["fuzz"]
    inf   = res["inf"]
    agg   = res["agg"]

    steps = ["1️⃣ Fuzzifikasi", "➡️ 2️⃣ Inferensi (Rule)", "➡️ 3️⃣ Agregasi (MAX)", "➡️ 4️⃣ Defuzzifikasi (Centroid)"]
    st.markdown(f"""
    <div class="info-box" style='display:flex;gap:10px;align-items:center;flex-wrap:wrap;'>
        {''.join([f'<span style="font-weight:600;color:#818cf8;">{s}</span>' for s in steps])}
    </div>
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    with col_l:
        # 1. Fuzzifikasi
        st.markdown("#### 1️⃣ Fuzzifikasi (Derajat Keanggotaan via fuzz.interp_membership)")
        var_info = {
            "visitor_count": ("Visitor Count",       res["c1"], ["Rendah","Sedang","Tinggi"]),
            "ticket_price":  ("Ticket Price",         res["c2"], ["Murah","Sedang","Mahal"]),
            "tourist_sat":   ("Tourist Satisfaction", res["c3"], ["Rendah","Sedang","Tinggi"]),
            "revenue":       ("Revenue Generated",    res["c4"], ["Rendah","Sedang","Tinggi"]),
            "op_cost":       ("Operational Cost",     res["c5"], ["Rendah","Sedang","Tinggi"]),
        }

        fuzz_rows = []
        for var, (name, val, terms) in var_info.items():
            row_data = {"Kriteria": f"{name} ({val})"}
            for t in terms:
                tk = t.lower()
                row_data[t] = f"{fuzz_vals[var].get(tk, 0):.3f}"
            fuzz_rows.append(row_data)

        fuzz_table = pd.DataFrame(fuzz_rows)
        st.dataframe(fuzz_table, use_container_width=True, hide_index=True)

        # 2. Inferensi
        st.markdown("#### 2️⃣ Inferensi – Aturan Aktif (operator AND = MIN via ctrl.Rule)")
        active_rules = [(rno, txt, alpha, cons)
                        for (rno, alpha, cons), txt in zip(inf, RULE_TEXT)
                        if alpha > 0]

        if active_rules:
            inf_data = []
            for rno, txt, alpha, cons in active_rules:
                badge_h = "🟢" if cons=="tinggi" else ("🟡" if cons=="sedang" else "🔴")
                inf_data.append({
                    "Rule": f"R{rno}",
                    "Aturan": txt[:50]+"..." if len(txt)>50 else txt,
                    "Nilai (α)": f"{alpha:.3f}",
                    "Output": f"{badge_h} {cons.upper()}",
                })
            st.dataframe(pd.DataFrame(inf_data), use_container_width=True, hide_index=True)
        else:
            st.warning("Tidak ada aturan yang aktif")

    with col_r:
        # 3. Agregasi
        st.markdown("#### 3️⃣ Agregasi (Metode MAX – ctrl.ControlSystem)")
        st.markdown(f"""
        <div class="info-box">
            Output Kinerja (agregasi semua aturan):<br>
            🔴 <b>Rendah</b> = {agg['rendah']:.3f} &nbsp;|&nbsp;
            🟡 <b>Sedang</b> = {agg['sedang']:.3f} &nbsp;|&nbsp;
            🟢 <b>Tinggi</b> = {agg['tinggi']:.3f}
        </div>
        """, unsafe_allow_html=True)

        bg = "#0f172a"
        fig2, ax2 = plt.subplots(figsize=(5.5, 3))
        fig2.patch.set_facecolor(bg)
        ax2.set_facecolor("#1e1b4b")

        xo = var_kinerja.universe
        yr = np.fmin(agg["rendah"], var_kinerja['rendah'].mf)
        ys = np.fmin(agg["sedang"], var_kinerja['sedang'].mf)
        yt = np.fmin(agg["tinggi"], var_kinerja['tinggi'].mf)
        y_agg = np.fmax(yr, np.fmax(ys, yt))

        ax2.fill_between(xo, yr,    alpha=0.4, color="#ef4444", label="Rendah")
        ax2.fill_between(xo, ys,    alpha=0.4, color="#f59e0b", label="Sedang")
        ax2.fill_between(xo, yt,    alpha=0.4, color="#10b981", label="Tinggi")
        ax2.plot(xo, y_agg, color="#818cf8", lw=2, label="Agregasi")
        ax2.axvline(score, color="white", lw=2, ls="--", label=f"Centroid={score:.1f}")

        ax2.set_xlim(0, 100)
        ax2.set_ylim(0, 1.1)
        ax2.tick_params(colors="#e2e8f0", labelsize=7)
        ax2.spines[['top','right','left','bottom']].set_color('#374151')
        ax2.grid(True, alpha=0.1, color='#6366f1')
        ax2.legend(fontsize=7, framealpha=0.2, labelcolor="#e2e8f0",
                   facecolor="#1e1b4b", edgecolor="#374151")
        ax2.set_title("Fungsi Keanggotaan Output (Teraggregasi)", color="#e2e8f0", fontsize=8)
        st.pyplot(fig2)
        plt.close()

        # 4. Defuzzifikasi
        st.markdown("#### 4️⃣ Defuzzifikasi (Centroid – ctrl.ControlSystemSimulation)")
        box_cls, score_cls, _ = get_result_style(kat)
        st.markdown(f"""
        <div class="{box_cls}">
            <div style='font-size:.85rem;color:#94a3b8;margin-bottom:4px;'>Nilai crisp (hasil akhir)</div>
            <div class="{score_cls}" style='font-size:3rem;'>{score:.2f}</div>
            <div style='font-size:.85rem;color:#94a3b8;'>Skor Kinerja</div>
            <div style='font-size:1.1rem;font-weight:700;color:#34d399;margin-top:8px;'>
                Kategori : <b>{kat}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ────────────────────────────────────────────────────── #
#               PAGE 7 – HASIL dan RANKING               #
# ────────────────────────────────────────────────────── #
elif menu == "Hasil & Ranking":
    st.markdown("""
    <div class="section-header">
        <span class="section-num">7</span>
        HASIL &amp; RANKING – Peringkat Alternatif
    </div>
    """, unsafe_allow_html=True)

    col_t, col_best = st.columns([3, 2])
    with col_t:
        st.markdown("#### Peringkat Kinerja Destinasi")

        show_rank = df_ranked[["Rank","Location_ID","Skor_Kinerja","Kategori"]].copy()
        show_rank.columns = ["Rank", "Destinasi", "Skor Kinerja", "Kategori"]

        st.dataframe(
            show_rank,
            use_container_width=True,
            height=500,
            hide_index=True,
        )
        st.markdown("""
        <div style='font-size:.75rem;color:#94a3b8;margin-top:4px;'>
            ℹ️ Semakin tinggi skor, semakin baik kinerja destinasi wisata kerajinan.
        </div>
        """, unsafe_allow_html=True)

    with col_best:
        if len(df_ranked) > 0:
            best = df_ranked.iloc[0]
            best_name  = best["Location_ID"]
            best_score = best["Skor_Kinerja"]
            best_kat   = best["Kategori"]

            st.markdown(f"""
            <div class="result-box" style='margin-top:40px;'>
                <div style='font-size:3rem;margin-bottom:8px;'>🥇</div>
                <div style='font-size:.9rem;color:#94a3b8;'>DESTINASI TERBAIK</div>
                <div style='font-size:1.5rem;font-weight:800;color:#e2e8f0;margin:8px 0;'>{best_name}</div>
                <div style='font-size:.85rem;color:#94a3b8;'>Skor Kinerja</div>
                <div class='result-score' style='font-size:2.5rem;'>{best_score:.2f} / 100</div>
                <div style='font-size:.85rem;color:#94a3b8;'>Kategori</div>
                <div style='font-size:1.3rem;font-weight:800;color:#34d399;'>⭐ {best_kat}</div>
                <div style='margin-top:12px;font-size:1.5rem;'>⭐⭐⭐⭐⭐</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("#### 📊 Distribusi Kategori")
            dist = df_ranked["Kategori"].value_counts()
            for k, c in [("TINGGI","#059669"),("SEDANG","#d97706"),("RENDAH","#dc2626")]:
                count = dist.get(k, 0)
                pct = count / len(df_ranked) * 100
                st.markdown(f"""
                <div style='display:flex;align-items:center;gap:10px;margin-bottom:8px;'>
                    <div style='width:90px;font-size:.82rem;color:#e2e8f0;font-weight:600;'>{k}</div>
                    <div style='flex:1;background:#1e1b4b;border-radius:4px;height:16px;overflow:hidden;'>
                        <div style='width:{pct:.0f}%;height:100%;background:{c};border-radius:4px;'></div>
                    </div>
                    <div style='width:60px;text-align:right;font-size:.82rem;color:{c};font-weight:700;'>
                        {count} ({pct:.0f}%)
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ────────────────────────────────────────────────────── #
#                  PAGE 8 – VISUALISASI                  #
# ────────────────────────────────────────────────────── #
elif menu == "Visualisasi":
    st.markdown("""
    <div class="section-header">
        <span class="section-num">8</span>
        VISUALISASI – Grafik Hasil Ranking
    </div>
    """, unsafe_allow_html=True)

    bg       = "#0f172a"
    grid_col = "#1e1b4b"
    txt_col  = "#e2e8f0"

    top_n  = st.slider("Jumlah destinasi yang ditampilkan", 5, 20, 10)
    top_df = df_ranked.head(top_n)

    st.markdown(f"#### Grafik Peringkat Kinerja Destinasi Wisata Kerajinan (Handicraft Center)")

    fig3, ax3 = plt.subplots(figsize=(12, 5))
    fig3.patch.set_facecolor(bg)
    ax3.set_facecolor(grid_col)

    cat_colors = {"TINGGI": "#059669", "SEDANG": "#d97706", "RENDAH": "#dc2626"}
    bar_colors = [cat_colors.get(k, "#ffffff") for k in top_df["Kategori"]]

    bars = ax3.bar(top_df["Location_ID"], top_df["Skor_Kinerja"],
                   color=bar_colors, width=0.6, edgecolor="#1e1b4b", linewidth=0.5)

    for bar, score in zip(bars, top_df["Skor_Kinerja"]):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                 f"{score:.1f}", ha="center", va="bottom",
                 color=txt_col, fontsize=8, fontweight="bold")

    ax3.set_ylim(0, 110)
    ax3.set_xlabel("Destinasi", color=txt_col, fontsize=9)
    ax3.set_ylabel("Skor Kinerja", color=txt_col, fontsize=9)
    ax3.set_title("Grafik Peringkat Kinerja Destinasi Wisata Kerajinan (Handicraft Center)",
                  color=txt_col, fontsize=11, fontweight="bold", pad=10)
    ax3.tick_params(colors=txt_col, labelsize=7)
    ax3.set_xticklabels(top_df["Location_ID"], rotation=45, ha="right")
    ax3.spines[['top','right','left','bottom']].set_color('#374151')
    ax3.grid(True, alpha=0.1, color="#6366f1", axis="y")

    patches = [
        mpatches.Patch(color="#059669", label="Tinggi"),
        mpatches.Patch(color="#d97706", label="Sedang"),
        mpatches.Patch(color="#dc2626", label="Rendah"),
    ]
    legend = ax3.legend(
        handles=patches,
        fontsize=8,
        framealpha=0.2,
        labelcolor='white',
        facecolor=grid_col,
        edgecolor='#374151',
        title="Kategori",
        title_fontsize=8,
        loc="upper right"
    )
    legend.get_title().set_color("white")

    plt.tight_layout()
    st.pyplot(fig3)
    plt.close()
    st.markdown(f"""
    <div style='font-size:.75rem;color:#94a3b8;margin-top:4px;'>
        ℹ️ Grafik ini menunjukkan {top_n} destinasi terbaik berdasarkan skor kinerja tertinggi.
    </div>
    """, unsafe_allow_html=True)

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("#### Distribusi Kategori Kinerja")
        fig4, ax4 = plt.subplots(figsize=(4, 4))
        fig4.patch.set_facecolor(bg)
        ax4.set_facecolor(bg)

        dist2      = df_ranked["Kategori"].value_counts()
        pie_labels = dist2.index.tolist()
        pie_values = dist2.values.tolist()
        pie_colors = [cat_colors.get(k, "#6366f1") for k in pie_labels]

        wedges, texts, autotexts = ax4.pie(
            pie_values, labels=pie_labels, autopct='%1.1f%%',
            colors=pie_colors, startangle=90,
            textprops={'color': txt_col, 'fontsize': 7},
        )
        for at in autotexts:
            at.set_color("white")
            at.set_fontweight("bold")
        ax4.set_title("Distribusi Kategori", color=txt_col, fontsize=8.3, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close()

    with col_p2:
        st.markdown("#### Distribusi Skor Kinerja")
        fig5, ax5 = plt.subplots(figsize=(5, 4.72))
        fig5.patch.set_facecolor(bg)
        ax5.set_facecolor(grid_col)

        ax5.hist(df_ranked["Skor_Kinerja"], bins=20, color="#6366f1",
                 edgecolor="#1e1b4b", alpha=0.8)
        ax5.axvline(df_ranked["Skor_Kinerja"].mean(), color="#f59e0b",
                    lw=2, ls="--", label=f"Mean: {df_ranked['Skor_Kinerja'].mean():.1f}")
        ax5.set_xlabel("Skor Kinerja", color=txt_col, fontsize=9)
        ax5.set_ylabel("Frekuensi",    color=txt_col, fontsize=9)
        ax5.set_title("Distribusi Skor Kinerja", color=txt_col, fontsize=10, fontweight="bold")
        ax5.tick_params(colors=txt_col, labelsize=7)
        ax5.spines[['top','right','left','bottom']].set_color('#374151')
        ax5.grid(True, alpha=0.1, color="#6366f1")
        ax5.legend(fontsize=8, framealpha=0.2, labelcolor=txt_col,
                   facecolor=grid_col, edgecolor='#374151')
        plt.tight_layout()
        st.pyplot(fig5)
        plt.close()

# ────────────────────────────────────────────────────── #
#                  PAGE 9 – PROFILE TIM                  #
# ────────────────────────────────────────────────────── #
elif menu == "Profile Tim":
    st.markdown("""
    <div class="section-header">
        <span class="section-num">9</span>
        PROFILE TIM
    </div>
    """, unsafe_allow_html=True)

    col_about, col_info = st.columns([3, 2])

    with col_about:
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
        members = [
            ("👨‍💻", "Lathiva Safina Almasea",  "NIM. 123240226", "Prodi Informatika"),
            ("👩‍🔬", "Mutiara Rahmawati Zalsa", "NIM. 123240257", "Prodi Informatika"),
        ]
        cols_m = st.columns(len(members))
        for i, (icon, name, nim, prodi) in enumerate(members):
            with cols_m[i]:
                st.markdown(f"""
                <div class="card" style='text-align:center;'>
                    <div style='font-size:3rem;margin-bottom:8px;'>{icon}</div>
                    <div style='font-weight:700;color:#e2e8f0;font-size:.95rem;'>{name}</div>
                    <div style='font-size:.78rem;color:#a5b4fc;margin:4px 0;'>{nim}</div>
                    <div style='font-size:.75rem;color:#94a3b8;'>{prodi}</div>
                </div>
                """, unsafe_allow_html=True)

    with col_info:
        st.markdown("""
        <div class="card">
            <h4 style='color:#818cf8;text-align:center'>Informasi Sistem</h4>
        """, unsafe_allow_html=True)

        info_items = [
            ("Metode",   "Fuzzy Mamdani"),
            ("Bahasa",   "Python 3 (Streamlit)"),
            ("Library",  "scikit-fuzzy, pandas, matplotlib, numpy"),
            ("Dataset",  "Rural Heritage Tourism Industry Chain Dataset (Kaggle)"),
            ("Filter",   "Heritage_Type = Handicraft Center (784 baris)"),
            ("Tahun",    "2025/2026"),
        ]
        for label, val in info_items:
            st.markdown(f"""
            <div style='display:flex;margin-bottom:4px;align-items:flex-start;'>
                <div style='min-width:100px;padding-left:20px;font-size:.8rem;color:#a5b4fc;font-weight:600;'>{label}</div>
                <div style='font-size:.8rem;color:#e2e8f0;'>: {val}</div>
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

st.markdown("""
<div class="footer-card">
    SPK Kinerja Destinasi Wisata Kerajinan (Handicraft Tourism)
    Metode Fuzzy Mamdani (scikit-fuzzy) |
    © Ivaa & Alsa, All I Wanna Do! Project Gacor! 2026.
</div>
""", unsafe_allow_html=True)