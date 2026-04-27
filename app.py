import streamlit as st
import time
import random
import base64
from PIL import Image
import os
import glob
import database as db
import image_utils as iu
from fpdf import FPDF
import tempfile
from transformers import pipeline


try:
    page_icon_img = Image.open("d:/Study/A/epidermix/assets/logo.png")
except Exception:
    page_icon_img = None

st.set_page_config(
    page_title="Epidermix - Skin Analysis AI",
    page_icon=page_icon_img,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if "user" not in st.session_state:
    st.session_state.user = "Guest"
if "page" not in st.session_state:
    st.session_state.page = "Home"

def navigate_to(page_name):
    st.session_state.page = page_name

def logout():
    st.session_state.user = "Guest"
    st.rerun()

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_image_path(pattern):
    files = glob.glob(f"d:/Study/A/epidermix/assets/{pattern}*.png")
    if not files:
        files = glob.glob(f"assets/{pattern}*.png")
    return files[0] if files else ""

def generate_pdf_report(username, diagnosis, confidence, severity, desc, rec):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=16, style='B')
    pdf.cell(200, 10, txt="EPIDERMIX AI - Skin Analysis Report", ln=1, align='C')
    pdf.set_font("Helvetica", size=12)
    pdf.cell(200, 10, txt=f"Patient/User: {username}", ln=1)
    pdf.cell(200, 10, txt=f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
    pdf.cell(200, 10, txt="", ln=1)
    pdf.set_font("Helvetica", size=14, style='B')
    pdf.cell(200, 10, txt=f"Diagnosis: {diagnosis}", ln=1)
    pdf.set_font("Helvetica", size=12)
    pdf.cell(200, 10, txt=f"Confidence Level: {confidence}%", ln=1)
    pdf.cell(200, 10, txt=f"Severity: {severity}", ln=1)
    pdf.multi_cell(0, 10, txt=f"Description: {desc}")
    pdf.cell(200, 5, txt="", ln=1)
    pdf.multi_cell(0, 10, txt=f"Recommendation: {rec}")
    
    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, "epidermix_report.pdf")
    pdf.output(pdf_path)
    return pdf_path

label_map = {
    'benign_keratosis-like_lesions': {
        "severity": "Low",
        "description": "A non-cancerous skin growth that may look like a wart, seborrheic keratosis, or solar lentigo.",
        "recommendation": "Generally harmless, but monitor for changes and wear sunscreen.",
        "status": "success"
    },
    'basal_cell_carcinoma': {
        "severity": "High",
        "description": "A type of skin cancer that begins in the basal cells, often associated with cumulative sun exposure.",
        "recommendation": "URGENT: Please consult a dermatologist for excision and treatment.",
        "status": "danger"
    },
    'actinic_keratoses': {
        "severity": "Moderate",
        "description": "A rough, scaly patch on the skin that develops from years of sun exposure. This is considered precancerous.",
        "recommendation": "Consult a doctor for evaluation as it may evolve into squamous cell carcinoma.",
        "status": "warning"
    },
    'vascular_lesions': {
        "severity": "Low to Moderate",
        "description": "Abnormalities in blood vessels under the skin surface, indicating cherry angiomas, angiokeratomas, or pyogenic granulomas.",
        "recommendation": "Usually benign. Seek medical advice if it bleeds or grows rapidly.",
        "status": "warning"
    },
    'melanocytic_Nevi': {
        "severity": "Low",
        "description": "Commonly known as moles. These are standard benign melanocytic proliferations.",
        "recommendation": "Continue with your regular skin care routine and monitor for the ABCDE signs of melanoma.",
        "status": "success"
    },
    'melanoma': {
        "severity": "High",
        "description": "A very serious and highly aggressive type of skin cancer that develops in melanocytes. Early detection is critical.",
        "recommendation": "URGENT: Please consult a dermatologist immediately for a professional biopsy. Do not wait.",
        "status": "danger"
    },
    'dermatofibroma': {
        "severity": "Low",
        "description": "A common benign fibrous nodule usually found on the lower legs, often resulting from a minor injury like a bug bite.",
        "recommendation": "Harmless and does not require treatment unless symptomatic or bothersome.",
        "status": "success"
    }
}

@st.cache_resource
def load_hf_model():
    return pipeline("image-classification", model="Anwarkh1/Skin_Cancer-Image_Classification")

def analyse_skin_image(image):
    st.info("Initiating local scan using Vision Transformer Neural Network. (First run downloads weights)...")
    
    try:
        classifier = load_hf_model()
        results = classifier(image)
        
        best_prediction = results[0]
        label = best_prediction["label"]
        score = best_prediction["score"]
        
        mapping = label_map.get(label, {
            "severity": "Unknown",
            "description": "Unrecognized condition.",
            "recommendation": "Seek professional medical help.",
            "status": "warning"
        })
        
        st.success("Analysis Complete!")
        
        display_label = label.replace("_", " ").title()
        
        return {
            "diagnosis": display_label,
            "confidence": round(score * 100, 2),
            "severity": mapping["severity"],
            "description": mapping["description"],
            "recommendation": mapping["recommendation"],
            "status": mapping["status"]
        }
            
    except Exception as e:
        st.error(f"Error executing AI visual core: {str(e)}")
        return get_fallback_diagnosis()

def get_fallback_diagnosis():
    return {
        "diagnosis": "System Error (Fallback)",
        "confidence": 0,
        "severity": "Unknown",
        "description": "The AI vision service is currently unreachable.",
        "recommendation": "Please try again later when the connection is restored.",
        "status": "warning"
    }


def render_sidebar():
    with st.sidebar:
        st.header("Member Portal")
        if st.session_state.user == "Guest":
            st.write("Please log in to track your analysis history.")
            tab1, tab2 = st.tabs(["Login", "Register"])
            with tab1:
                l_user = st.text_input("Username", key="log_user")
                l_pass = st.text_input("Password", type="password", key="log_pass")
                if st.button("LOGIN", use_container_width=True):
                    if db.authenticate_user(l_user, l_pass):
                        st.session_state.user = l_user
                        st.success("Authenticated!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
            with tab2:
                r_user = st.text_input("New Username", key="reg_user")
                r_pass = st.text_input("New Password", type="password", key="reg_pass")
                if st.button("REGISTER", use_container_width=True):
                    if db.register_user(r_user, r_pass):
                        st.success("Registered successfully! Please log in.")
                    else:
                        st.error("Username already exists.")
        else:
            st.write(f"**Logged in as: {st.session_state.user}**")
            if st.button("LOGOUT", use_container_width=True):
                logout()
                
            st.markdown("---")
            st.subheader("Past Scans Database")
            scans = db.get_user_scans(st.session_state.user)
            if not scans:
                st.info("No past scans detected.")
            else:
                for s in scans:
                    with st.expander(f"{s['timestamp']} | {s['diagnosis']}"):
                        st.write(f"**Confidence:** {s['confidence']}%")
                        st.write(f"**Severity:** {s['severity']}")

def render_banner():
    try:
        logo_b64 = get_base64_of_bin_file("d:/Study/A/epidermix/assets/logo.png")
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width: 200px; margin-right: 60px;" />'
    except Exception:
        logo_html = '''<div style="margin-right: 60px; width: 200px;"><svg viewBox="0 0 100 100" fill="none" stroke="#111" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M60 20 L20 50 L40 80 L70 50 Z" /><circle cx="60" cy="20" r="5" fill="#111" /><circle cx="20" cy="50" r="5" fill="#111" /><circle cx="40" cy="80" r="5" fill="#111" /><circle cx="70" cy="50" r="5" fill="#111" /><path d="M40 50 L60 20 M40 50 L20 50 M40 50 L40 80 M40 50 L70 50" stroke-width="1" /><circle cx="40" cy="50" r="3" fill="#111" /><path d="M70 50 C 90 50, 90 90, 60 90 L30 90" /><rect x="25" y="65" width="20" height="8" rx="2" /></svg></div>'''

    st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300&display=swap');
.block-container {{ padding-top: 0rem !important; padding-left: 0rem !important; padding-right: 0rem !important; max-width: 100% !important; }}
.stButton {{ display: flex; justify-content: center; margin-top: 30px; margin-bottom: 50px; }}
div[data-testid="stButton"] > button {{ background-color: #002244; color: white; border-radius: 30px; padding: 15px 40px; font-size: 18px; font-weight: bold; border: none; }}
div[data-testid="stButton"] > button:hover {{ background-color: #001122; color: white; border: none; }}
</style>
<div style="background-color: #fce4ec; padding: 120px 80px; margin-bottom: 80px; display: flex; align-items: center; justify-content: center; width: 100%; border-radius: 0;">
    {logo_html}
    <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
        <h1 style="margin:0; font-size: 100px; font-family: 'Montserrat', sans-serif; font-weight: 300; letter-spacing: 10px; color: #111;">EPIDERMIX</h1>
        <p style="margin:0; font-size: 24px; font-family: 'Montserrat', sans-serif; letter-spacing: 4px; color: #333; font-weight: 300;">INTELLIGENCE FOR YOUR SKIN'S EVOLUTION.</p>
    </div>
</div>""", unsafe_allow_html=True)

def render_footer():
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888; font-family: Montserrat; font-size: 12px; margin-top: 50px; margin-bottom: 30px;'>"
        "Epidermix Intelligence &copy; 2026 | "
        "<a href='#' style='color: #888;'>Privacy Policy</a> | "
        "<a href='#' style='color: #888;'>Terms of Service</a> | "
        "<b>Medical Disclaimer:</b> For educational UI purposes only. Not professional medical advice."
        "</div>", unsafe_allow_html=True
    )

def render_home():
    render_sidebar()
    render_banner()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("ANALYSE SKIN NOW", key="btn_hero", use_container_width=True):
            navigate_to("Analysis")
            st.rerun()

    st.markdown("<h3 style='padding-left: 40px;'>Ritual Guide</h3>", unsafe_allow_html=True)
    try:
        img_acne = get_base64_of_bin_file(get_image_path("skincare_botanical_serum"))
        img_moist = get_base64_of_bin_file(get_image_path("skincare_moisturizer_marble"))
        img_drop = get_base64_of_bin_file(get_image_path("skincare_serum_drop_leaf"))
        img_cheek = get_base64_of_bin_file(get_image_path("skincare_application_cheek"))
        img_aloe = get_base64_of_bin_file(get_image_path("skincare_aloe_vera_bottles"))
        img_rose = get_base64_of_bin_file(get_image_path("skincare_rose_water_mist"))
        
        grid_html = f"""<style>
.ritual-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 20px; margin-bottom: 40px; padding: 0 40px; }}
.ritual-card {{ position: relative; border-radius: 12px; overflow: hidden; cursor: auto; aspect-ratio: 1; box-shadow: 0 4px 8px rgba(0,0,0,0.1); background-color: #fff; }}
.ritual-card img {{ width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s; }}
.ritual-overlay {{ position: absolute; bottom: 0; left: 0; right: 0; top: 0; background: rgba(0,34,68,0.95); color: white; opacity: 0; transition: opacity 0.3s; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; text-align: center; }}
.ritual-card:hover .ritual-overlay {{ opacity: 1; }}
.ritual-card:hover img {{ transform: scale(1.1); }}
.overlay-title {{ font-size: 22px; font-weight: bold; margin-bottom: 10px; }}
.overlay-text {{ font-size: 14px; line-height: 1.5; }}
</style>
<div class="ritual-grid">
    <div class="ritual-card"><img src="data:image/png;base64,{img_acne}"><div class="ritual-overlay"><div class="overlay-title">Acne Management</div><div class="overlay-text">Prioritise a gentle cleanser and non-comedogenic moisturiser. Avoid picking spots to prevent scarring.</div></div></div>
    <div class="ritual-card"><img src="data:image/png;base64,{img_moist}"><div class="ritual-overlay"><div class="overlay-title">Hydration First</div><div class="overlay-text">Apply moisturiser to damp skin to lock in hydration. Look for ingredients like ceramides.</div></div></div>
    <div class="ritual-card"><img src="data:image/png;base64,{img_drop}"><div class="ritual-overlay"><div class="overlay-title">Active Serums</div><div class="overlay-text">Integrate powerful actives such as Vitamin C in the morning and Retinol at night.</div></div></div>
    <div class="ritual-card"><img src="data:image/png;base64,{img_cheek}"><div class="ritual-overlay"><div class="overlay-title">Gentle Application</div><div class="overlay-text">Always apply skincare with upward, gentle strokes. Never pull down on your skin.</div></div></div>
    <div class="ritual-card"><img src="data:image/png;base64,{img_aloe}"><div class="ritual-overlay"><div class="overlay-title">Natural Soothing</div><div class="overlay-text">Incorporate natural anti-inflammatories like Aloe Vera to calm redness.</div></div></div>
    <div class="ritual-card"><img src="data:image/png;base64,{img_rose}"><div class="ritual-overlay"><div class="overlay-title">Refreshing Mists</div><div class="overlay-text">Use botanical toners or rose water throughout the day to rehydrate.</div></div></div>
</div>"""
        st.markdown(grid_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading images: {e}")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("ANALYSE SKIN NOW", key="btn_footer", use_container_width=True):
            navigate_to("Analysis")
            st.rerun()

    render_footer()

def render_analysis():
    render_sidebar()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Back to Home", use_container_width=True):
            navigate_to("Home")
            st.rerun()
            
    st.title("Epidermix AI Analysis")
    st.markdown("Upload a close-up picture of an anomalous skin area, and Epidermix will initiate vision processing and check diagnostic matrices.")
    st.markdown("---")
    
    st.warning("**Disclaimer**: Epidermix is for educational purposes only. Mock results should not replace professional medical diagnosis.")
    
    uploaded_file = st.file_uploader("Upload Skin Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            c1, c2 = st.columns(2)
            with c1:
                st.image(image, caption="Original Uploaded Source", use_container_width=True)
            with c2:
                augmented = iu.generate_mock_heatmap(image)
                st.image(augmented, caption="Epidermix Vision Output (Heatmap Target)", use_container_width=True)
            
            st.markdown("---")
            if st.button("EXECUTE ANALYSIS PROTOCOL", type="primary"):
                result = analyse_skin_image(image)
                
                # DB Storage
                if st.session_state.user and st.session_state.user != "Guest":
                    db.save_scan(st.session_state.user, result["diagnosis"], result["confidence"], result["severity"])
                
                st.subheader("Diagnostic Results:")
                res_c1, res_c2 = st.columns(2)
                with res_c1:
                    st.metric(label="Predicted Diagnosis", value=result["diagnosis"])
                    st.metric(label="Severity Index", value=result["severity"])
                with res_c2:
                    st.metric(label="System Confidence", value=f"{result['confidence']}%")
                
                st.markdown("#### Detail Summary")
                if result["status"] == "danger":
                    st.error(result["description"])
                    st.error(f"**Action Required**: {result['recommendation']}")
                elif result["status"] == "warning":
                    st.warning(result["description"])
                    st.warning(f"**Recommendation**: {result['recommendation']}")
                else:
                    st.success(result["description"])
                    st.success(f"**Recommendation**: {result['recommendation']}")
                
                st.markdown("---")
                pdf_path = generate_pdf_report(
                    st.session_state.user, 
                    result["diagnosis"], 
                    result["confidence"], 
                    result["severity"], 
                    result["description"], 
                    result["recommendation"]
                )
                
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📄 Download Official System Report (PDF)",
                        data=pdf_file,
                        file_name="Epidermix_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        except Exception as e:
            st.error(f"System Error: {e}")
            
    render_footer()

def main():
    if "page" not in st.session_state:
        st.session_state.page = "Home"
        
    if st.session_state.page == "Home":
        render_home()
    elif st.session_state.page == "Analysis":
        render_analysis()

if __name__ == "__main__":
    main()
