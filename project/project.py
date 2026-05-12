import streamlit as st
import pandas as pd
import numpy as np
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
            
    background-image:
        linear-gradient(
            rgba(6,15,8,0.48),
            rgba(6,15,8,0.58)
        ),

        url("data:image/jpg;base64,%s");

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
#        FUZZY MAMDANI FUNCTIONS        #
#---------------------------------------#

# MEMBERSHIP FUNCTIONS.

def mf_trapezoid(x, a, b, c, d):
    """Trapezoid membership function"""
    if x <= a or x >= d:
        return 0.0
    elif b <= x <= c:
        return 1.0
    elif a < x < b:
        return (x - a) / (b - a)
    else:  # c < x < d
        return (d - x) / (d - c)

def mf_triangle(x, a, b, c):
    """Triangle membership function"""
    if x <= a or x >= c:
        return 0.0
    elif x == b:
        return 1.0
    elif a < x <= b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)

# --- C1: Visitor Count (52-799) -> Benefit ---
def c1_rendah(x):
    return mf_trapezoid(x, 52, 52, 200, 400)

def c1_sedang(x):
    return mf_triangle(x, 200, 425, 650)

def c1_tinggi(x):
    return mf_trapezoid(x, 500, 650, 799, 799)

# --- C2: Ticket Price (10-99) -> Cost ---
def c2_murah(x):
    return mf_trapezoid(x, 10, 10, 30, 55)

def c2_sedang(x):
    return mf_triangle(x, 30, 55, 80)

def c2_mahal(x):
    return mf_trapezoid(x, 60, 80, 99, 99)

# --- C3: Tourist Satisfaction (0-5) -> Benefit ---
def c3_rendah(x):
    return mf_trapezoid(x, 0, 0, 2.0, 3.25)

def c3_sedang(x):
    return mf_triangle(x, 2.5, 3.5, 4.5)

def c3_tinggi(x):
    return mf_trapezoid(x, 3.75, 4.5, 5.0, 5.0)

# --- C4: Revenue Generated (5000-100000) -> Benefit ---
def c4_rendah(x):
    return mf_trapezoid(x, 5000, 5000, 30000, 55000)

def c4_sedang(x):
    return mf_triangle(x, 30000, 55000, 80000)

def c4_tinggi(x):
    return mf_trapezoid(x, 60000, 80000, 100000, 100000)

# --- C5: Operational Cost (2000-50000) -> Cost ---
def c5_rendah(x):
    return mf_trapezoid(x, 2000, 2000, 15000, 27500)

def c5_sedang(x):
    return mf_triangle(x, 15000, 27500, 40000)

def c5_tinggi(x):
    return mf_trapezoid(x, 30000, 40000, 50000, 50000)

# --- Output: Kinerja (0-100) ---
def out_rendah(z):
    return mf_trapezoid(z, 0, 0, 25, 50)

def out_sedang(z):
    return mf_triangle(z, 25, 50, 75)

def out_tinggi(z):
    return mf_trapezoid(z, 50, 75, 100, 100)

#-------------------------------------#
#        RULE BASE (15 rules)         #
#-------------------------------------#
RULES = [
    # No, Antecedent dict, Consequent
    (1,  {"c1":"tinggi", "c3":"tinggi"},              "tinggi"),
    (2,  {"c1":"sedang", "c3":"tinggi"},              "tinggi"),
    (3,  {"c1":"rendah"},                             "rendah"),
    (4,  {"c2":"murah",  "c3":"tinggi"},              "tinggi"),
    (5,  {"c2":"mahal",  "c3":"rendah"},              "rendah"),
    (6,  {"c2":"sedang", "c3":"sedang"},              "sedang"),
    (7,  {"c4":"tinggi", "c5":"rendah"},              "tinggi"),
    (8,  {"c4":"tinggi", "c5":"tinggi"},              "sedang"),
    (9,  {"c4":"rendah"},                             "rendah"),
    (10, {"c5":"tinggi"},                             "rendah"),
    (11, {"c5":"rendah", "c3":"tinggi"},              "tinggi"),
    (12, {"c3":"rendah"},                             "rendah"),
    (13, {"c3":"sedang"},                             "sedang"),
    (14, {"c1":"tinggi", "c2":"mahal"},               "sedang"),
    (15, {"c1":"sedang", "c2":"sedang"},              "sedang"),
]

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

RULE_COLORS = {
    "tinggi": "#059669",
    "sedang": "#d97706",
    "rendah": "#dc2626",
}

def fuzzify(c1, c2, c3, c4, c5):
    return {
        "c1": {"rendah": c1_rendah(c1), "sedang": c1_sedang(c1), "tinggi": c1_tinggi(c1)},
        "c2": {"murah":  c2_murah(c2),  "sedang": c2_sedang(c2),  "mahal":  c2_mahal(c2)},
        "c3": {"rendah": c3_rendah(c3), "sedang": c3_sedang(c3), "tinggi": c3_tinggi(c3)},
        "c4": {"rendah": c4_rendah(c4), "sedang": c4_sedang(c4), "tinggi": c4_tinggi(c4)},
        "c5": {"rendah": c5_rendah(c5), "sedang": c5_sedang(c5), "tinggi": c5_tinggi(c5)},
    }

def inferensi(fuzz):
    """Apply all rules → return list of (rule_no, alpha, consequent)"""
    results = []
    for (rno, antecedent, consequent) in RULES:
        alphas = []
        for var, term in antecedent.items():
            alphas.append(fuzz[var][term])
        alpha = min(alphas)  # AND = MIN
        results.append((rno, alpha, consequent))
    return results

def agregasi(inference_results):
    """MAX aggregation for each output term"""
    agg = {"tinggi": 0.0, "sedang": 0.0, "rendah": 0.0}
    for (_, alpha, cons) in inference_results:
        agg[cons] = max(agg[cons], alpha)
    return agg

def defuzzifikasi(agg):
    """Centroid defuzzification"""
    z_range = np.linspace(0, 100, 1000)
    numerator = 0.0
    denominator = 0.0
    for z in z_range:
        # clipped MF = min(alpha, mf(z))
        mu_r = min(agg["rendah"], out_rendah(z))
        mu_s = min(agg["sedang"], out_sedang(z))
        mu_t = min(agg["tinggi"], out_tinggi(z))
        mu = max(mu_r, mu_s, mu_t)  # MAX aggregation
        numerator   += z * mu
        denominator += mu
    if denominator == 0:
        return 0.0
    return numerator / denominator

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

def fuzzy_mamdani(c1, c2, c3, c4, c5):
    fuzz = fuzzify(c1, c2, c3, c4, c5)
    inf  = inferensi(fuzz)
    agg  = agregasi(inf)
    score= defuzzifikasi(agg)
    kat  = get_kategori(score)
    return score, kat, fuzz, inf, agg

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

score_df = compute_all_scores(df_hc)
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

    #------------------------------------#
    #        SIDEBAR MENU CUSTOM         #
    #------------------------------------#

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

    def load_svg(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()

    svg_db       = load_svg("files-db.svg")
    import base64
    svg_db_b64 = base64.b64encode(svg_db.encode()).decode()

    svg_visitor  = load_svg("visitor-count.svg")
    import base64
    svg_visitor_b64 = base64.b64encode(svg_visitor.encode()).decode()

    svg_ticket   = load_svg("ticket.svg")
    import base64
    svg_ticket_b64 = base64.b64encode(svg_ticket.encode()).decode()

    svg_rate     = load_svg("rate.svg")
    import base64
    svg_rate_b64 = base64.b64encode(svg_rate.encode()).decode()

    svg_revenue  = load_svg("revenue-bag.svg")
    import base64
    svg_revenue_b64 = base64.b64encode(svg_revenue.encode()).decode()

    svg_ops      = load_svg("operational.svg")
    import base64
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
        padding: 16px 12px 14px 14px;
        min-height: 175px;
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

    # ── JUDUL ────────────────────────────────────── #
    st.markdown("<div class='dash-title'>Dashboard</div>", unsafe_allow_html=True)

    # ── HERO ROW ─────────────────────────────────── #
    col_hero, col_total = st.columns([3, 1.6])

    with col_hero:
        st.markdown(f"""
        <div class="hero-card">
            <h2>Sistem Pendukung Keputusan</h2>
            <p>
                Pemilihan Penilaian Kinerja Destinasi Wisata Kerajinan
                (Handicraft Tourism) Menggunakan Metode Fuzzy Mamdani.
                Sistem membantu menentukan peringkat kinerja destinasi
                wisata kerajinan (Handicraft Center) berdasarkan 5 kriteria
                menggunakan metode Fuzzy Mamdani Inference System (FMIS).
            </p>
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

    # ── KRITERIA PENILAIAN ───────────────────────── #
    st.markdown("<div class='dash-section-title'>Kriteria Penilaian</div>", unsafe_allow_html=True)

    kriteria = [
        ("C1", "Visitor Count",        "(52-799)",         "Benefit", svg_visitor),
        ("C2", "Ticket Price",         "(10-99)",          "Cost",    svg_ticket),
        ("C3", "Tourist Satification", "(0-5)",            "Benefit", svg_rate),
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

    # ── RINGKASAN SISTEM ─────────────────────────── #
    st.markdown("<div class='dash-section-title-yellow'>Ringkasan Sistem</div>", unsafe_allow_html=True)

    r_cols = st.columns(4)
    ring_data = [
        (str(total_all), "Total Data",              "(Dataset)"),
        (str(total_hc),  "Data Handicraft<br>Center", "(Setelah di Filter)"),
        ("5",            "Jumlah Kriteria",          "(Kriteria)"),
        ("Fuzzy Mamdani","Metode",                   "(Inference System)"),
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
            <span>Handicraft Center</span>
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
        Fuzzifikasi - Fungsi Keanggotaan
    </div>
    """, unsafe_allow_html=True)

    bg_color = "#0f172a"
    grid_color = "#1e1b4b"
    text_color = "#e2e8f0"

    def plot_mf(ax, x_range, mf_funcs, labels, title, colors_map):
        ax.set_facecolor(grid_color)
        ax.spines[['top','right','left','bottom']].set_color('#374151')
        ax.tick_params(colors=text_color, labelsize=7)
        ax.set_title(title, color=text_color, fontsize=8, fontweight='bold', pad=6)
        ax.set_ylim(-0.05, 1.1)
        ax.set_xlim(x_range[0], x_range[-1])
        ax.grid(True, alpha=0.15, color='#6366f1')
        for i, (mf_fn, lbl) in enumerate(zip(mf_funcs, labels)):
            y = [mf_fn(xi) for xi in x_range]
            col = colors_map.get(lbl, "#818cf8")
            ax.plot(x_range, y, color=col, lw=2, label=lbl.capitalize())
        ax.legend(fontsize=6, framealpha=0.2, labelcolor=text_color,
                  facecolor=grid_color, edgecolor='#374151')

    fig, axes = plt.subplots(2, 3, figsize=(14, 7))
    fig.patch.set_facecolor(bg_color)
    plt.subplots_adjust(wspace=0.35, hspace=0.5)

    # C1
    x1 = np.linspace(52, 799, 500)
    plot_mf(axes[0,0], x1,
            [c1_rendah, c1_sedang, c1_tinggi],
            ["rendah","sedang","tinggi"],
            "C1 – Visitor Count (Benefit)",
            {"rendah":"#ef4444","sedang":"#f59e0b","tinggi":"#10b981"})

    # C2
    x2 = np.linspace(10, 99, 500)
    plot_mf(axes[0,1], x2,
            [c2_murah, c2_sedang, c2_mahal],
            ["murah","sedang","mahal"],
            "C2 – Ticket Price (Cost)",
            {"murah":"#3b82f6","sedang":"#f59e0b","mahal":"#ef4444"})

    # C3
    x3 = np.linspace(0, 5, 500)
    plot_mf(axes[0,2], x3,
            [c3_rendah, c3_sedang, c3_tinggi],
            ["rendah","sedang","tinggi"],
            "C3 – Tourist Satisfaction (Benefit)",
            {"rendah":"#ef4444","sedang":"#f59e0b","tinggi":"#10b981"})

    # C4
    x4 = np.linspace(5000, 100000, 500)
    plot_mf(axes[1,0], x4,
            [c4_rendah, c4_sedang, c4_tinggi],
            ["rendah","sedang","tinggi"],
            "C4 – Revenue Generated (Benefit)",
            {"rendah":"#ef4444","sedang":"#f59e0b","tinggi":"#10b981"})

    # C5
    x5 = np.linspace(2000, 50000, 500)
    plot_mf(axes[1,1], x5,
            [c5_rendah, c5_sedang, c5_tinggi],
            ["rendah","sedang","tinggi"],
            "C5 – Operational Cost (Cost)",
            {"rendah":"#10b981","sedang":"#f59e0b","tinggi":"#ef4444"})

    # Output
    xo = np.linspace(0, 100, 500)
    plot_mf(axes[1,2], xo,
            [out_rendah, out_sedang, out_tinggi],
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
Segitiga (trimf) dan Trapesium (trapmf) digunakan sebagai fungsi keanggotaan.
</div>

<div class='fuzzy-note-tags'>
<span style='color:#E53935;'>Rendah / Murah</span>
= Trapesium kiri

<span style='color:#D4A017;'>Sedang</span>
= Segitiga tengah

<span style='color:#00A86B;'>Tinggi / Mahal</span>
= Trapesium kanan
                
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
        📋 Total Rule: <b>15 aturan</b> &nbsp;|&nbsp; Operator: <b>AND (MIN)</b>
    </div>
    """, unsafe_allow_html=True)

    badge = {
        "tinggi": "<span class='badge-tinggi'>Tinggi</span>",
        "sedang": "<span class='badge-sedang'>Sedang</span>",
        "rendah": "<span class='badge-rendah'>Rendah</span>",
    }

    for i, (rule_txt, (rno, ant, cons)) in enumerate(zip(RULE_TEXT, RULES)):
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
        score, kat, fuzz, inf_res, agg = fuzzy_mamdani(c1_val, c2_val, c3_val, c4_val, c5_val)

        st.session_state["last_result"] = {
            "score": score, "kat": kat, "fuzz": fuzz,
            "inf": inf_res, "agg": agg,
            "c1": c1_val, "c2": c2_val, "c3": c3_val,
            "c4": c4_val, "c5": c5_val,
        }

        # Result display
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
        PROSES FUZZY – Detail Perhitungan (Mamdani)
    </div>
    """, unsafe_allow_html=True)

    if "last_result" not in st.session_state:
        st.warning("⚠️ Belum ada perhitungan. Silakan ke menu **⚙️ Hitung SPK** terlebih dahulu.")
        st.stop()

    res   = st.session_state["last_result"]
    score = res["score"]
    kat   = res["kat"]
    fuzz  = res["fuzz"]
    inf   = res["inf"]
    agg   = res["agg"]

    # Step indicator
    steps = ["1️⃣ Fuzzifikasi", "➡️ 2️⃣ Inferensi (Rule)", "➡️ 3️⃣ Agregasi (MAX)", "➡️ 4️⃣ Defuzzifikasi"]
    st.markdown(f"""
    <div class="info-box" style='display:flex;gap:10px;align-items:center;flex-wrap:wrap;'>
        {''.join([f'<span style="font-weight:600;color:#818cf8;">{s}</span>' for s in steps])}
    </div>
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    with col_l:
        # 1. Fuzzifikasi
        st.markdown("#### 1️⃣ Fuzzifikasi (Derajat Keanggotaan)")
        var_info = {
            "c1": ("Visitor Count", res["c1"], ["Rendah","Sedang","Tinggi"]),
            "c2": ("Ticket Price",  res["c2"], ["Murah","Sedang","Mahal"]),
            "c3": ("Tourist Satisfaction", res["c3"], ["Rendah","Sedang","Tinggi"]),
            "c4": ("Revenue Generated",    res["c4"], ["Rendah","Sedang","Tinggi"]),
            "c5": ("Operational Cost",     res["c5"], ["Rendah","Sedang","Tinggi"]),
        }

        fuzz_rows = []
        for var, (name, val, terms) in var_info.items():
            row_data = {"Kriteria": f"{name} ({val})", "Nilai Input": val}
            for t in terms:
                tk = t.lower()
                row_data[t] = f"{fuzz[var].get(tk, 0):.3f}"
            fuzz_rows.append(row_data)

        fuzz_table = pd.DataFrame(fuzz_rows)
        st.dataframe(fuzz_table, use_container_width=True, hide_index=True)

        # 2. Inferensi
        st.markdown("#### 2️⃣ Inferensi – Aturan yang Aktif (MIN)")
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
        st.markdown("#### 3️⃣ Agregasi (Metode MAX)")
        st.markdown(f"""
        <div class="info-box">
            Output Kinerja (agregasi semua aturan):<br>
            🔴 <b>Rendah</b> = {agg['rendah']:.3f} &nbsp;|&nbsp;
            🟡 <b>Sedang</b> = {agg['sedang']:.3f} &nbsp;|&nbsp;
            🟢 <b>Tinggi</b> = {agg['tinggi']:.3f}
        </div>
        """, unsafe_allow_html=True)

        # Aggregation graph
        bg = "#0f172a"
        fig2, ax2 = plt.subplots(figsize=(5.5, 3))
        fig2.patch.set_facecolor(bg)
        ax2.set_facecolor("#1e1b4b")

        xo = np.linspace(0, 100, 1000)
        yr = [min(agg["rendah"], out_rendah(z)) for z in xo]
        ys = [min(agg["sedang"], out_sedang(z)) for z in xo]
        yt = [min(agg["tinggi"], out_tinggi(z)) for z in xo]
        y_agg = [max(r, s, t) for r,s,t in zip(yr,ys,yt)]

        ax2.fill_between(xo, yr, alpha=0.4, color="#ef4444", label="Rendah")
        ax2.fill_between(xo, ys, alpha=0.4, color="#f59e0b", label="Sedang")
        ax2.fill_between(xo, yt, alpha=0.4, color="#10b981", label="Tinggi")
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
        st.markdown("#### 4️⃣ Defuzzifikasi (Centroid)")
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

        # Show table with color-coded kategori
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
            best_name = best["Location_ID"]
            best_score = best["Skor_Kinerja"]
            best_kat = best["Kategori"]

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

            # Kategori distribution
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

    bg = "#0f172a"
    grid_col = "#1e1b4b"
    txt_col = "#e2e8f0"

    top_n = st.slider("Jumlah destinasi yang ditampilkan", 5, 20, 10)
    top_df = df_ranked.head(top_n)

    # Bar chart ranking
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

    # Pie chart
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("#### Distribusi Kategori Kinerja")
        fig4, ax4 = plt.subplots(figsize=(4, 4))
        fig4.patch.set_facecolor(bg)
        ax4.set_facecolor(bg)

        dist2 = df_ranked["Kategori"].value_counts()
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
        ax5.set_ylabel("Frekuensi", color=txt_col, fontsize=9)
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
                dengan metode Fuzzy Mamdani untuk mendukung penilaian kinerja destinasi
                wisata kerajinan.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            "<h4 style='text-align:center;'>Anggota Kelompok</h4>",
            unsafe_allow_html=True
        )
        members = [
            ("👨‍💻", "Lathiva Safina Almasea", "NIM. 123240226", "Prodi Informatika"),
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
            ("Metode", "Fuzzy Mamdani"),
            ("Bahasa", "Python (Streamlit)"),
            ("Library", "scikit-fuzzy, pandas, matplotlib, numpy"),
            ("Dataset", "Rural Heritage Tourism Industry Chain Dataset (CSV – Online)"),
            ("Tahun", "2025/2026"),
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
            <h4 style='color:#818cf8;'>Alur Sistem Fuzzy Mamdani</h4>
            <div style='font-size:.82rem;color:#e2e8f0;line-height:1.95;'>
                1️⃣ <b>Fuzzifikasi</b> – Nilai crisp → derajat keanggotaan<br>
                2️⃣ <b>Inferensi</b> – Evaluasi rule IF-THEN (MIN)<br>
                3️⃣ <b>Agregasi</b> – Kombinasi output rule (MAX)<br>
                4️⃣ <b>Defuzzifikasi</b> – Centroid → skor kinerja
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="footer-card">
    SPK Kinerja Destinasi Wisata Kerajinan (Handicraft Tourism)
    Metode Fuzzy Mamdani |
    © Ivaa & Alsa, All I Wanna Do! Project Gacor! 2026.
</div>
""", unsafe_allow_html=True)