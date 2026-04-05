import streamlit as st
import numpy as np
import pickle

# ─────────────────────────────────────────────
#  Page Config  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NestWorth – House Price Estimator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #0f172a 100%);
    color: #e2e8f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    border-right: 1px solid #334155;
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #1e3a5f 0%, #164e63 50%, #0f2744 100%);
    border: 1px solid #2563eb44;
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, #3b82f644 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #f8fafc;
    margin: 0 0 0.4rem 0;
    line-height: 1.2;
}
.hero-sub {
    font-size: 1rem;
    color: #94a3b8;
    margin: 0;
    font-weight: 300;
}
.hero-badge {
    display: inline-block;
    background: #2563eb22;
    border: 1px solid #3b82f6;
    color: #93c5fd;
    border-radius: 20px;
    padding: 0.25rem 0.85rem;
    font-size: 0.78rem;
    letter-spacing: 0.05em;
    font-weight: 500;
    margin-bottom: 0.8rem;
}

/* ── Section Headers ── */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    color: #f1f5f9;
    margin: 1.8rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #2563eb;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Input Cards ── */
.input-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.input-card:hover { border-color: #3b82f6; }

/* ── Streamlit widget overrides ── */
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] select,
[data-testid="stTextInput"] input {
    background: #0f172a !important;
    border: 1px solid #334155 !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}
.stRadio label { color: #cbd5e1 !important; }
.stRadio [data-testid="stMarkdownContainer"] p { color: #94a3b8 !important; }

/* ── Predict Button ── */
.stButton > button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    letter-spacing: 0.03em;
    transition: opacity 0.2s !important;
    box-shadow: 0 4px 24px #2563eb55 !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* ── Result Card ── */
.result-card {
    background: linear-gradient(135deg, #163a5f 0%, #1e4976 100%);
    border: 2px solid #3b82f6;
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    box-shadow: 0 8px 40px #2563eb33;
    animation: popIn 0.5s cubic-bezier(.34,1.56,.64,1);
}
@keyframes popIn {
    from { transform: scale(0.88); opacity: 0; }
    to   { transform: scale(1);    opacity: 1; }
}
.result-label {
    font-size: 0.9rem;
    color: #93c5fd;
    letter-spacing: 0.12em;
    font-weight: 500;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.result-price {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    color: #f8fafc;
    font-weight: 700;
    line-height: 1.1;
}
.result-unit {
    font-size: 1rem;
    color: #94a3b8;
    margin-top: 0.3rem;
}

/* ── Summary Grid ── */
.summary-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    margin-top: 1rem;
}
.summary-item {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 0.75rem 1rem;
}
.summary-key {
    font-size: 0.72rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.summary-val {
    font-size: 0.95rem;
    color: #e2e8f0;
    font-weight: 600;
    margin-top: 0.2rem;
}

/* ── Info Pills ── */
.info-pill {
    display: inline-block;
    background: #0f2744;
    border: 1px solid #1e40af;
    color: #93c5fd;
    border-radius: 20px;
    padding: 0.2rem 0.7rem;
    font-size: 0.75rem;
    margin: 0.2rem;
}

/* ── Metric Tiles (sidebar) ── */
.metric-tile {
    background: #0f172a;
    border: 1px solid #1e40af;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.6rem;
}
.metric-tile .mt-label { font-size: 0.72rem; color: #64748b; text-transform: uppercase; }
.metric-tile .mt-val   { font-size: 1.15rem; color: #93c5fd; font-weight: 600; }

/* ── Divider ── */
.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #334155, transparent);
    margin: 1.5rem 0;
}

/* ── Hide Streamlit defaults ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Load Model & Meta
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("Model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

@st.cache_resource
def load_meta():
    try:
        with open("model_meta.pkl", "rb") as f:
            return pickle.load(f)
    except:
        return {"feature_columns": [
            "UNDER_CONSTRUCTION","RERA","BHK_NO.","SQUARE_FT",
            "READY_TO_MOVE","RESALE","LONGITUDE","LATITUDE",
            "POSTED_BY_Dealer","POSTED_BY_Owner","BHK_OR_RK_RK"
        ], "log_transform": True}

model = load_model()
meta  = load_meta()


# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏠 NestWorth")
    st.markdown("*AI-Powered Property Price Estimator*")
    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    st.markdown("**About this App**")
    st.markdown("""
    NestWorth uses a **Random Forest** machine learning model trained on **29,000+** 
    Indian real estate listings to predict property prices.
    """)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    st.markdown("**📊 Model Performance**")

    st.markdown("""
    <div class='metric-tile'>
        <div class='mt-label'>R² Score</div>
        <div class='mt-val'>74.7%</div>
    </div>
    <div class='metric-tile'>
        <div class='mt-label'>Mean Abs. Error</div>
        <div class='mt-val'>₹13.26 Lakhs</div>
    </div>
    <div class='metric-tile'>
        <div class='mt-label'>Algorithm</div>
        <div class='mt-val'>Random Forest</div>
    </div>
    <div class='metric-tile'>
        <div class='mt-label'>Training Samples</div>
        <div class='mt-val'>26,005</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    st.markdown("**🔑 Top Price Drivers**")
    st.progress(0.40, text="Area (sq.ft)  — 40%")
    st.progress(0.22, text="Longitude     — 22%")
    st.progress(0.22, text="Latitude      — 22%")
    st.progress(0.10, text="Seller Type   — 10%")
    st.progress(0.06, text="Other         —  6%")

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    st.caption("Built by Suyash · BCA Final Year Project · LNCT Bhopal")


# ─────────────────────────────────────────────
#  Hero Banner
# ─────────────────────────────────────────────
st.markdown("""
<div class='hero-banner'>
    <div class='hero-badge'>🤖 Powered by Random Forest ML</div>
    <h1 class='hero-title'>🏠 NestWorth</h1>
    <p class='hero-sub'>Enter your property details below and get an instant AI-powered price estimate in seconds.</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Input Form
# ─────────────────────────────────────────────
st.markdown("<div class='section-header'>📋 Property Details</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("<div class='input-card'>", unsafe_allow_html=True)
    st.markdown("**🛏 Basic Info**")
    bhk_no   = st.number_input("Number of Bedrooms (BHK)", min_value=1, max_value=10, value=2, step=1)
    sqft     = st.number_input("Property Area (sq.ft)", min_value=100, max_value=10000, value=800, step=50)
    bhk_or_rk = st.selectbox("Property Type", ["BHK", "RK"], help="BHK = Bedroom-Hall-Kitchen | RK = Room-Kitchen")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='input-card'>", unsafe_allow_html=True)
    st.markdown("**🏗 Property Status**")
    under_construction = st.radio("Under Construction?", ["No", "Yes"], horizontal=True)
    ready_to_move      = st.radio("Ready to Move In?",   ["Yes", "No"], horizontal=True)
    rera               = st.radio("RERA Approved?",       ["Yes", "No"], horizontal=True)
    resale             = st.radio("Resale Property?",     ["No", "Yes"], horizontal=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='input-card'>", unsafe_allow_html=True)
    st.markdown("**🧑‍💼 Seller & Location**")
    posted_by  = st.selectbox("Posted By", ["Builder", "Dealer", "Owner"],
                              help="Builder = Developer | Dealer = Agent | Owner = Direct")
    st.markdown("*📍 Property Coordinates*")
    latitude   = st.number_input("Latitude",  format="%.4f", value=19.0760,
                                 help="e.g. Mumbai=19.07, Delhi=28.70, Bangalore=12.97")
    longitude  = st.number_input("Longitude", format="%.4f", value=72.8777,
                                 help="e.g. Mumbai=72.87, Delhi=77.20, Bangalore=77.59")
    st.markdown("</div>", unsafe_allow_html=True)

# ── Quick City Presets ──────────────────────
st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
st.markdown("**📍 Quick City Preset** *(click to auto-fill coordinates)*")
preset_cols = st.columns(6)
cities = {
    "🏙 Mumbai":    (19.0760, 72.8777),
    "🏛 Delhi":     (28.7041, 77.1025),
    "🌳 Bangalore": (12.9716, 77.5946),
    "🌊 Chennai":   (13.0827, 80.2707),
    "🌆 Hyderabad": (17.3850, 78.4867),
    "🌸 Pune":      (18.5204, 73.8567),
}
selected_city = None
for idx, (city, coords) in enumerate(cities.items()):
    if preset_cols[idx].button(city, key=f"city_{idx}"):
        selected_city = coords

if selected_city:
    latitude  = selected_city[0]
    longitude = selected_city[1]
    st.success(f"Coordinates updated → Lat: {latitude}, Lon: {longitude}")

# ── Predict Button ───────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
predict_clicked = st.button("🔍  Estimate House Price")


# ─────────────────────────────────────────────
#  Prediction Logic
# ─────────────────────────────────────────────
if predict_clicked:
    # Encode inputs
    under_construction_val = 1 if under_construction == "Yes" else 0
    rera_val               = 1 if rera               == "Yes" else 0
    ready_to_move_val      = 1 if ready_to_move      == "Yes" else 0
    resale_val             = 1 if resale             == "Yes" else 0
    bhk_or_rk_rk           = 1 if bhk_or_rk          == "RK"  else 0
    posted_by_dealer       = 1 if posted_by          == "Dealer" else 0
    posted_by_owner        = 1 if posted_by          == "Owner"  else 0

    # Build input array matching training feature order exactly
    input_data = np.array([[
        under_construction_val,   # UNDER_CONSTRUCTION
        rera_val,                  # RERA
        bhk_no,                    # BHK_NO.
        sqft,                      # SQUARE_FT
        ready_to_move_val,         # READY_TO_MOVE
        resale_val,                # RESALE
        longitude,                 # LONGITUDE
        latitude,                  # LATITUDE
        posted_by_dealer,          # POSTED_BY_Dealer
        posted_by_owner,           # POSTED_BY_Owner
        bhk_or_rk_rk               # BHK_OR_RK_RK
    ]])

    # Predict (reverse log transform)
    pred_log    = model.predict(input_data)[0]
    prediction  = np.expm1(pred_log)

    # Price range (±15% confidence band)
    low_est  = round(prediction * 0.85, 2)
    high_est = round(prediction * 1.15, 2)
    pred_val = round(prediction, 2)

    # ── Results Section ─────────────────────
    st.markdown("<div class='section-header'>💰 Prediction Result</div>", unsafe_allow_html=True)

    res_col1, res_col2 = st.columns([1, 1.3], gap="large")

    with res_col1:
        st.markdown(f"""
        <div class='result-card'>
            <div class='result-label'>Estimated Market Price</div>
            <div class='result-price'>₹ {pred_val:,.2f}</div>
            <div class='result-unit'>Lakhs (INR)</div>
            <br>
            <div style='font-size:0.85rem; color:#94a3b8; margin-top:0.5rem'>
                📊 Confidence Range<br>
                <span style='color:#93c5fd; font-weight:600'>₹{low_est:,} L &nbsp;–&nbsp; ₹{high_est:,} L</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Price per sqft
        price_per_sqft = round((prediction * 100000) / sqft, 0)
        st.markdown(f"""
        <div style='background:#1e293b; border:1px solid #334155; border-radius:12px;
                    padding:1rem; margin-top:1rem; text-align:center;'>
            <div style='color:#64748b; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.1em;'>
                Price per sq.ft
            </div>
            <div style='color:#f8fafc; font-size:1.6rem; font-weight:700; margin-top:0.3rem;'>
                ₹ {price_per_sqft:,.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with res_col2:
        st.markdown("**📋 Your Input Summary**")
        st.markdown(f"""
        <div class='summary-grid'>
            <div class='summary-item'>
                <div class='summary-key'>Bedrooms</div>
                <div class='summary-val'>{bhk_no} {bhk_or_rk}</div>
            </div>
            <div class='summary-item'>
                <div class='summary-key'>Area</div>
                <div class='summary-val'>{sqft:,} sq.ft</div>
            </div>
            <div class='summary-item'>
                <div class='summary-key'>Under Construction</div>
                <div class='summary-val'>{under_construction}</div>
            </div>
            <div class='summary-item'>
                <div class='summary-key'>Ready to Move</div>
                <div class='summary-val'>{ready_to_move}</div>
            </div>
            <div class='summary-item'>
                <div class='summary-key'>RERA Approved</div>
                <div class='summary-val'>{rera}</div>
            </div>
            <div class='summary-item'>
                <div class='summary-key'>Resale</div>
                <div class='summary-val'>{resale}</div>
            </div>
            <div class='summary-item'>
                <div class='summary-key'>Posted By</div>
                <div class='summary-val'>{posted_by}</div>
            </div>
            <div class='summary-item'>
                <div class='summary-key'>Coordinates</div>
                <div class='summary-val'>{latitude:.3f}, {longitude:.3f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Category insight
        if prediction < 40:
            tag, insight = "🟢 Budget", "Affordable range. Good for first-time buyers."
        elif prediction < 80:
            tag, insight = "🟡 Mid-Range", "Mid-range property. Solid value for urban areas."
        elif prediction < 150:
            tag, insight = "🔵 Premium", "Premium segment. High-quality neighbourhood expected."
        else:
            tag, insight = "🟣 Luxury", "Luxury property. Prime location or large area."

        st.markdown(f"""
        <div style='background:#0f2744; border:1px solid #1e40af; border-radius:12px; padding:1rem;'>
            <div style='color:#93c5fd; font-size:0.85rem; font-weight:600;'>{tag} Segment</div>
            <div style='color:#cbd5e1; font-size:0.85rem; margin-top:0.3rem;'>{insight}</div>
        </div>
        """, unsafe_allow_html=True)

    st.balloons()

    # ── Disclaimer ───────────────────────────
    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    st.caption(
        "⚠️ This prediction is generated by a machine learning model and is for **educational purposes only**. "
        "Actual property prices depend on many additional factors. Always consult a certified real estate advisor."
    )
