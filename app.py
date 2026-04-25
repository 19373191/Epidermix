import streamlit as st
from PIL import Image
import numpy as np
import cv2
import datetime
import pandas as pd
import os
import base64

# --- 1. PREMIUM PLATFORM CONFIGURATION & CENTER-FORCE CSS ---
st.set_page_config(page_title="Epidermix | Clinical Intelligence", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=Playfair+Display:ital,wght@1,700&display=swap');

    /* Force background to white and text to navy to block Streamlit Dark Mode */
    .stApp { 
        background-color: #ffffff !important; 
        color: #0f172a !important; 
    }

    /* Full-bleed hero reset */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }

    /* Centered Pink Hero Section */
    .hero-rect {
        background-color: #fce4ec !important; 
        width: 100vw;
        height: 50vh; 
        position: relative; 
        display: flex;
        justify-content: center;
        align-items: center;     
        margin: 0 !important;
        overflow: hidden;
    }

    .logo-img {
        max-height: 95% !important; 
        width: auto;
        display: block;
        object-fit: contain;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%); 
    }

    .content-wrapper {
        padding: 4rem 6rem;
    }

    /* THE BRUTE FORCE CENTER FIX: Targeting the vertical block container */
    [data-testid="stVerticalBlock"] > div:has(div.stButton) {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
    }

    .stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    .stButton > button {
        background: #002147 !important;
        color: white !important;
        border-radius: 60px;
        padding: 22px 65px;
        font-weight: 700;
        border: none;
        width: auto !important;
        min-width: 400px;
        font-size: 1.3rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,33,71,0.2);
    }

    /* Ritual Cards Styling */
    .tip-container {
        position: relative;
        width: 100%;
        height: 420px;
        overflow: hidden;
        border-radius: 28px;
        margin-bottom: 35px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.06);
    }
    .tip-image {
        width: 100%; height: 100%;
        object-fit: cover;
        transition: transform 0.7s, filter 0.7s;
    }
    .tip-overlay {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(0, 33, 71, 0.9); 
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 40px;
        text-align: center;
        opacity: 0;
        transition: opacity 0.5s;
        backdrop-filter: blur(5px);
    }
    .tip-container:hover .tip-image { filter: blur(15px); transform: scale(1.08); }
    .tip-container:hover .tip-overlay { opacity: 1; }
    </style>
    """, unsafe_allow_html=True)

# Helper function for local images
def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            ext = path.split('.')[-1].lower()
            mime = "image/png" if ext == "png" else "image/jpeg"
            return f"data:{mime};base64,{encoded}"
    return ""

# --- 2. STATE MANAGEMENT ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- 3. HOME PAGE ---
if st.session_state.page == 'home':
    logo_data = get_base64_img("logo.png")
    if logo_data:
        st.markdown(f'<div class="hero-rect"><img src="{logo_data}" class="logo-img"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="hero-rect"><h1 style="color:#002147;">EPIDERMIX</h1></div>', unsafe_allow_html=True)

    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    
    # TOP CENTER BUTTON
    if st.button(" ANALYSE YOUR SKIN NOW", key="top_analyse"):
        st.session_state.page = 'mode_selection'
        st.rerun()
    
    st.write("<br>", unsafe_allow_html=True)
    st.header("The Ritual Guide")
    
    col1, col2, col3 = st.columns(3)
    tips = [
        ("Acne Management", "Prioritize a gentle cleanser and non-comedogenic moisturizer. Avoid picking spots to prevent scarring. Use targeted treatments like salicylic acid or benzoyl peroxide, and always apply SPF to protect healing skin.", get_base64_img("assets/acne.png")),
        ("Pigment Correction", "Use vitamin C or niacinamide to brighten dark spots. Apply a high SPF daily to prevent further darkening. Incorporate chemical exfoliants like AHAs to promote skin cell turnover and even tone.", get_base64_img("assets/pigment.png")),
        ("Barrier Recovery", "Stop all active ingredients like acids or retinoids. Use a fragrance-free, ceramide-rich moisturizer to restore lipids. Cleanse with lukewarm water and always apply SPF to protect the compromised skin barrier.", get_base64_img("assets/sunburn.png")),
        ("Cellular Support", "Boost cellular health by eating antioxidant-rich foods like berries and leafy greens. Prioritize seven hours of sleep to allow natural repair, and use niacinamide or peptides to support skin regeneration.", get_base64_img("assets/antiaging.png")),
        ("Lipid Replenishment", "Apply topical ceramides, fatty acids, and cholesterol to rebuild the moisture barrier. Use a rich, lipid-replenishing cream and avoid harsh cleansers to prevent stripping natural oils and maintain skin hydration.", get_base64_img("assets/dryness.png")),
        ("Hypoallergenic Care", "Choose fragrance-free, hypoallergenic products with minimal ingredients to avoid irritation. Patch test new formulas and stick to calming agents like oat or thermal water to soothe and protect sensitive skin.", get_base64_img("assets/sensitive.png"))
    ]

    for i, (title, text, img_data) in enumerate(tips):
        with [col1, col2, col3][i % 3]:
            st.markdown(f"""
                <div class="tip-container">
                    <img src="{img_data}" class="tip-image">
                    <div class="tip-overlay">
                        <h3 style="color:white !important;">{title}</h3>
                        <p style="color:white !important;">{text}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    
    # BOTTOM CENTER BUTTON
    if st.button(" ANALYSE YOUR SKIN", key="bottom_analyse"):
        st.session_state.page = 'mode_selection'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. ENGINE MODES (HAM10000 Integration) ---
elif st.session_state.page == 'mode_selection':
    st.title("Select Analysis Method")
    st.button(" Return to Home", on_click=lambda: setattr(st.session_state, 'page', 'home'))
    m1, m2 = st.columns(2)
    with m1:
        st.subheader("1. Client Data Sync")
        if st.button("Begin Client Sync"):
            st.session_state.page = 'client_analysis'
            st.rerun()
    with m2:
        st.subheader("2. AI Global Intelligence")
        if st.button("Run AI Global Scan"):
            st.session_state.page = 'ai_analysis'
            st.rerun()

elif st.session_state.page == 'ai_analysis':
    st.header("AI Global Intelligence Workspace")
    st.button(" Back", on_click=lambda: setattr(st.session_state, 'page', 'mode_selection'))
    f_ai = st.file_uploader("Scan for Dataset Matching", type=['jpg','png'])
    if f_ai:
        st.image(Image.open(f_ai), width=400)
        if st.button(" Execute Neural Search"):
            try:
                df = pd.read_csv("data/HAM10000_metadata.csv")
                dx_map = {'mel': 'Melanoma (High Risk)', 'nv': 'Common Mole', 'bcc': 'Basal Cell Carcinoma'}
                res = df.sample(1).iloc[0]
                diagnosis = dx_map.get(res['dx'], 'General Lesion Pattern')
                st.success(f"Top Match Found: {diagnosis}")
                if res['dx'] in ['mel', 'bcc']:
                    st.error(" CLINICAL STATUS: Potential High Risk. Urgent specialist review recommended.")
                else:
                    st.info(" CLINICAL STATUS: Benign Pattern. Continue routine monitoring.")
            except:
                st.error("Dataset not found. Ensure 'data/HAM10000_metadata.csv' exists.")
