import streamlit as st
from streamlit_lottie import st_lottie
import requests
from PIL import Image
import os

# Set page config first
st.set_page_config(page_title="حاسبة تقسيط BAIC", page_icon="🚗", layout="wide")

# Function to load lottie
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load assets
# Try to load local logo, otherwise generic
logo = None
if os.path.exists("assets/logo.png"):
    try:
        logo = Image.open("assets/logo.png")
    except:
        pass
elif os.path.exists("logo.png"):
    try:
        logo = Image.open("logo.png")
    except:
        pass

lottie_car_url = "https://lottie.host/5a0c3065-5c1a-472e-8481-224419e75550/123456.json" 
# Using a fallback reliable URL or a placeholder if this fails. 
# actually let's use a very standard one from lottiefiles public urls if possible
lottie_car = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_ym83vnmq.json") 
if not lottie_car:
    lottie_car = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_u4jjb9bd.json")

# Custom CSS for styling
st.markdown("""
<style>
    /* Main App Styling */
    .stApp {
        background-color: #ffffff;
        color: #31333F;
        direction: rtl; /* Set functionality to Right-to-Left */
    }
    
    /* Headers */
    h1, h2, h3, p, div {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: right;
    }

    /* Custom Classes */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#00ADB5, #31333F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .card {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #dee2e6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        border-color: #00ADB5;
    }

    .metric-label {
        font-size: 1.1rem;
        color: #666;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00ADB5;
        text-shadow: none;
    }
    
    /* Streamlit Input Styling Override for Light Mode */
    .stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div > div {
        background-color: #ffffff;
        color: #31333F;
        border-radius: 8px;
        border: 1px solid #ced4da;
    }
    
    /* Fix Slider in RTL */
    .stSlider {
        direction: ltr;
        text-align: right; 
    }
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
col_logo, col_title, col_empty = st.columns([1, 4, 1])

with col_logo:
    if logo:
        st.image(logo, width=150)
    else:
        # Fallback if logo not found
        st.markdown("# 🚗")

with col_title:
    st.markdown('<div class="main-title">تمويل BAIC</div>', unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; color: #aaa;'>أحسب قسطك بسهولة</div>", unsafe_allow_html=True)

st.markdown("---")

# --- Content ---
# --- Content ---
st.markdown("### 🔢 أحسب القسط")

with st.container():

    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # Category Logic
    category = st.selectbox(
        "اختار الفئة",
        ("فئة اولى", "فئة تانيه", "فئة تالته"),
        index=0
    )
    
    col_inp1, col_inp2 = st.columns(2)
    with col_inp1:
        down_payment = st.number_input("المقدم (جنيه)", min_value=0.0, value=250000.0, step=5000.0, format="%.0f")
    with col_inp2:
        years_installment = st.slider("عدد السنين (تقسيط)", min_value=1, max_value=7, value=3)

    interest_rate = st.slider("الفائدة السنوية (%)", min_value=0.0, max_value=30.0, value=15.0, step=0.5)

    st.markdown('</div>', unsafe_allow_html=True)

# --- Calculation Logic ---
price = 0
if category == "فئة اولى":
    price = 725000
elif category == "فئة تانيه":
    price = 770000
elif category == "فئة تالته":
    price = 855000

# Formula: ((price - down_payment) * interest * years + (price - down_payment)) / (years * 12)
try:
    final_interest = interest_rate / 100.0
    principal = price - down_payment
    if principal < 0:
        principal = 0 # Handle overpayment
    
    total_interest_amount = principal * final_interest * years_installment
    total_repayment = principal + total_interest_amount
    monthly_payment = total_repayment / (years_installment * 12)
    
except Exception as e:
    monthly_payment = 0
    principal = 0

# --- Results Section ---
st.markdown("### 📊 ملخص التقسيط")

r_col1, r_col2, r_col3 = st.columns(3)

with r_col1:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">سعر العربية</div>
        <div class="metric-value">{price:,.0f} ج.م</div>
    </div>
    """, unsafe_allow_html=True)

with r_col2:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">المبلغ المتقسط</div>
        <div class="metric-value">{principal:,.0f} ج.م</div>
        <div style="font-size:0.8rem; color:#aaa;">(السعر - المقدم)</div>
    </div>
    """, unsafe_allow_html=True)

with r_col3:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label" style="color: #FFD700;">القسط الشهري</div>
        <div class="metric-value" style="color: #FFD700;">{monthly_payment:,.2f} ج.م</div>
    </div>
    """, unsafe_allow_html=True)

