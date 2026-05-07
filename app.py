"""
SmartDOX - Frontend-Only Tender Evaluation Platform
No backend server required - everything runs locally in Streamlit
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
from pathlib import Path
from PIL import Image
import io

# --- DOCUMENT PROCESSING ---
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    fitz = None
    PYMUPDF_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    pytesseract = None

# --- IMPORT LOCAL SERVICES ---
from services import (
    extract_criteria,
    extract_bidder_data,
    evaluate,
    final_verdict,
    generate_explanation,
    translate_text,
    get_supported_languages,
    get_verdict_color,
    create_report_summary,
    format_results_for_display
)

# ═══════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="SmartDOX - Tender Evaluation",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════
# CUSTOM STYLING
# ═══════════════════════════════════════════════════════════════════

<<<<<<< HEAD
# Backend API configuration
# For Streamlit Cloud: Set in Secrets section
# For local: Use .env file or environment variable
API_BASE_URL = "https://smartdox-backend.onrender.com"

# Set request timeout for cloud deployments
REQUEST_TIMEOUT = 30

# Session state initialization
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

# Custom CSS
=======
>>>>>>> contributor/main
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-pass {
        color: #28a745;
        font-weight: bold;
        font-size: 1.1em;
    }
    .status-fail {
        color: #dc3545;
        font-weight: bold;
        font-size: 1.1em;
    }
    .status-review {
        color: #ffc107;
        font-weight: bold;
        font-size: 1.1em;
    }
    .evaluation-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .verdict-pass {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 1.5rem;
        border-radius: 10px;
        color: #155724;
        font-weight: bold;
        font-size: 1.2em;
    }
    .verdict-fail {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 1.5rem;
        border-radius: 10px;
        color: #721c24;
        font-weight: bold;
        font-size: 1.2em;
    }
    .verdict-review {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1.5rem;
        border-radius: 10px;
        color: #856404;
        font-weight: bold;
        font-size: 1.2em;
    }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════

if "current_language" not in st.session_state:
    st.session_state.current_language = "en"

if "file_history" not in st.session_state:
    st.session_state.file_history = []

if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = True  # No authentication needed - frontend only

# ═══════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def extract_text_from_file(uploaded_file):
    """Extract text from PDF or image files"""
    try:
        if uploaded_file.type == "application/pdf":
            if not PYMUPDF_AVAILABLE:
                st.error(
                    "⚠️ **PyMuPDF is not installed**\n\n"
                    "Please install it with: `pip install PyMuPDF`"
                )
                return None

            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            return text

        elif uploaded_file.type.startswith("image/"):
            if not TESSERACT_AVAILABLE:
                st.warning(
                    "⚠️ **Tesseract-OCR not available for image processing**\n\n"
                    "For now, please use PDF files. To process images:\n"
                    "1. Download: https://github.com/UB-Mannheim/tesseract/wiki\n"
                    "2. Install (Windows: C:\\Program Files\\Tesseract-OCR)\n"
                    "3. Run: `pip install pytesseract`"
                )
                return None

            image = Image.open(uploaded_file)
            tesseract_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            ]

            for path in tesseract_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break

            text = pytesseract.image_to_string(image)
            return text if text.strip() else None

        else:
            st.warning("Unsupported file type. Please upload PDF or image.")
            return None

    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")
        return None


def save_to_history(filename, file_type):
    """Save file to local history"""
    entry = {
        "filename": filename,
        "type": file_type,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.file_history.append(entry)


def get_verdict_css_class(verdict):
    """Get CSS class for verdict display"""
    if "Eligible" in verdict and "Not" not in verdict:
        return "verdict-pass"
    elif "Not Eligible" in verdict:
        return "verdict-fail"
    else:
        return "verdict-review"


# ═══════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════

# Display header
st.markdown("""
    <div class="main-header">
        <h1>🎯 SmartDOX</h1>
        <p>AI-Powered Smart Tender Evaluation Platform</p>
        <p style="font-size: 0.9em; margin-top: 0.5rem;">✨ Frontend-Only • No Backend Required • Private & Local</p>
    </div>
""", unsafe_allow_html=True)

# Show availability warnings
if not PYMUPDF_AVAILABLE:
    st.warning(
        "⚠️ **PyMuPDF not installed** - PDF processing won't work.\n"
        "Install with: `pip install PyMuPDF`"
    )

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Language selector
    languages = get_supported_languages()
    language_display = [f"{v}" for k, v in languages.items()]
    language_keys = list(languages.keys())
    
    selected_lang = st.selectbox(
        "Language",
        language_keys,
        format_func=lambda x: languages[x],
        index=0
    )
    st.session_state.current_language = selected_lang
    
    st.markdown("---")
    
    # About section
    st.markdown("### ℹ️ About")
    st.info(
        "**SmartDOX** is an AI-powered tender evaluation platform that helps "
        "automatically extract criteria and evaluate bidder eligibility.\n\n"
        "✨ **Features:**\n"
        "- 📄 PDF & Image Processing\n"
        "- 🤖 Smart Criteria Extraction\n"
        "- 👥 Bidder Evaluation\n"
        "- 📊 Detailed Reports\n"
        "- 🌍 Multilingual Support\n"
        "- 💾 Local History Tracking"
    )

# Create tabs for different functions
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Dashboard", "📄 Process Tender", "👥 Evaluate Bidder", "📋 History"])

# ───────────────────────────────────────────────────────────────────
# TAB 1: DASHBOARD
# ───────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("### 🎯 SmartDOX Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📄 **Process Tender Documents**\n\nExtract eligibility criteria from tender documents automatically using AI.")
    
    with col2:
        st.success("👥 **Evaluate Bidder Submissions**\n\nMatch bidder documents against tender criteria.")
    
    with col3:
        st.warning("📊 **Get Explainable Results**\n\nReceive transparent, audit-ready evaluation reports.")

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Key Features")
        features = [
            "✅ Automated document understanding",
            "✅ OCR-based extraction from scanned PDFs",
            "✅ Intelligent criteria matching",
            "✅ Explainable AI decisions",
            "✅ Multilingual support (8+ languages)",
            "✅ Audit-ready reporting",
            "✅ Completely local & private (no backend server)"
        ]
        for feature in features:
            st.write(feature)
    
    with col2:
        st.subheader("📊 Supported File Formats")
        formats = [
            "📄 PDF documents (text & scanned)",
            "🖼️ Images (JPG, PNG, GIF)",
            "📋 Any document convertible to PDF"
        ]
        for fmt in formats:
            st.write(fmt)
        
        st.markdown("---")
        st.markdown("### 🚀 Getting Started")
        st.markdown("""
        1. **Go to "Process Tender" tab** → Upload tender document
        2. **Review extracted criteria**
        3. **Go to "Evaluate Bidder" tab** → Upload bidder document  
        4. **Get instant evaluation results**
        """)

# ───────────────────────────────────────────────────────────────────
# TAB 2: PROCESS TENDER
# ───────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("### 📄 Upload & Process Tender Document")
    st.write("Extract eligibility criteria (turnover, projects, certifications, etc.) from tender documents")
    
    st.markdown("---")
    
    uploaded_tender = st.file_uploader(
        "Choose a tender document",
        type=["pdf", "jpg", "jpeg", "png", "gif"],
        key="tender_uploader"
    )
    
    if uploaded_tender:
        st.info(f"📁 File: **{uploaded_tender.name}** ({uploaded_tender.size / 1024:.1f} KB)")
        
        if st.button("🔍 Process Tender", use_container_width=True):
            with st.spinner("🔄 Processing tender document..."):
                text = extract_text_from_file(uploaded_tender)
                
                if text:
                    criteria = extract_criteria(text)
                    save_to_history(uploaded_tender.name, "tender")
                    
                    # Display results
                    st.success("✅ Tender processed successfully!")
                    st.markdown("---")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 📋 Extracted Criteria")
                        
                        if criteria.get("turnover"):
                            st.metric(
                                "Minimum Turnover",
                                f"₹{criteria['turnover']} Crore",
                                delta="Required"
                            )
                        else:
                            st.metric(
                                "Minimum Turnover",
                                "Not Specified",
                                delta="Optional"
                            )
                        
                        if criteria.get("projects"):
                            st.metric(
                                "Minimum Projects",
                                f"{criteria['projects']} Projects",
                                delta="Required"
                            )
                        else:
                            st.metric(
                                "Minimum Projects",
                                "Not Specified",
                                delta="Optional"
                            )
                    
                    with col2:
                        st.markdown("#### 📌 Certifications")
                        
                        if criteria.get("gst"):
                            st.success("✅ GST Registration Required")
                        else:
                            st.info("➖ GST Registration Not Required")
                        
                        if criteria.get("iso"):
                            st.success("✅ ISO Certification Required")
                        else:
                            st.info("➖ ISO Certification Not Required")
                    
                    st.markdown("---")
                    
                    # Show raw extracted text
                    with st.expander("👀 View Extracted Text"):
                        st.text(text[:2000] + "..." if len(text) > 2000 else text)
                    
                    # Store criteria in session for later use
                    st.session_state.current_criteria = criteria
                    st.success("💾 Criteria saved! Go to 'Evaluate Bidder' to compare against bids.")
                else:
                    st.error("❌ Could not extract text from file. Please try another document.")

# ───────────────────────────────────────────────────────────────────
# TAB 3: EVALUATE BIDDER
# ───────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("### 👥 Upload & Evaluate Bidder Document")
    st.write("Evaluate if bidder meets the tender requirements")
    
    st.markdown("---")
    
    # Check if criteria has been extracted
    if "current_criteria" not in st.session_state:
        st.warning("⚠️ Please process a tender document first to extract criteria.")
        st.info("💡 Go to 'Process Tender' tab above to extract criteria from a tender document.")
    else:
        criteria = st.session_state.current_criteria
        
        # Show current criteria
        with st.expander("📋 View Current Criteria"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Turnover Required:**", criteria.get("turnover", "Not specified"))
                st.write("**Projects Required:**", criteria.get("projects", "Not specified"))
            with col2:
                st.write("**GST Required:**", "✅ Yes" if criteria.get("gst") else "❌ No")
                st.write("**ISO Required:**", "✅ Yes" if criteria.get("iso") else "❌ No")
        
        st.markdown("---")
        
        # Upload bidder document
        uploaded_bidder = st.file_uploader(
            "Choose a bidder document",
            type=["pdf", "jpg", "jpeg", "png", "gif"],
            key="bidder_uploader"
        )
        
        if uploaded_bidder:
            st.info(f"📁 File: **{uploaded_bidder.name}** ({uploaded_bidder.size / 1024:.1f} KB)")
            
            if st.button("🔍 Evaluate Bidder", use_container_width=True):
                with st.spinner("🔄 Processing bidder document and evaluating..."):
                    text = extract_text_from_file(uploaded_bidder)
                    
                    if text:
                        # Extract bidder data
                        bidder_data = extract_bidder_data(text)
                        
                        # Evaluate
                        results = evaluate(criteria, bidder_data)
                        verdict = final_verdict(results)
                        explanation = generate_explanation(criteria, bidder_data, results)
                        
                        # Save to history
                        save_to_history(uploaded_bidder.name, "bidder")
                        
                        # Translate if needed
                        current_lang = st.session_state.current_language
                        if current_lang != "en":
                            with st.spinner(f"🌍 Translating results to {current_lang}..."):
                                verdict = translate_text(verdict, current_lang)
                                explanation = translate_text(explanation, current_lang)
                        
                        st.success("✅ Evaluation completed!")
                        st.markdown("---")
                        
                        # Display Verdict
                        verdict_class = get_verdict_css_class(verdict)
                        st.markdown(f"""
                            <div class="{verdict_class}">
                            🎯 FINAL VERDICT: {verdict}
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("---")
                        
                        # Bidder Information
                        st.markdown("#### 📊 Bidder Information")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Company Name:**", bidder_data.get("company_name", "Unknown"))
                            st.write("**Turnover:**", f"₹{bidder_data.get('turnover')} Crore" if bidder_data.get('turnover') else "Not Found")
                        
                        with col2:
                            st.write("**Project Experience:**", f"{bidder_data.get('projects')} Projects" if bidder_data.get('projects') else "Not Found")
                            st.write("**Registration Number:**", bidder_data.get("registration_number", "Not Found"))
                        
                        st.write("**GST Status:**", "✅ Registered" if bidder_data.get("gst") else "❌ Not Registered")
                        st.write("**ISO Status:**", "✅ Certified" if bidder_data.get("iso") else "❌ Not Certified")
                        
                        st.markdown("---")
                        
                        # Evaluation Results
                        st.markdown("#### ✅ Evaluation Results")
                        
                        eval_cols = st.columns(4)
                        criteria_keys = ["turnover", "projects", "gst", "iso"]
                        criteria_names = ["Turnover", "Experience", "GST", "ISO"]
                        
                        for i, (key, name) in enumerate(zip(criteria_keys, criteria_names)):
                            with eval_cols[i]:
                                status = results.get(key, "N/A")
                                if status == "PASS":
                                    st.success(f"✅ {name}\n**PASS**")
                                elif status == "FAIL":
                                    st.error(f"❌ {name}\n**FAIL**")
                                elif status == "REVIEW":
                                    st.warning(f"⚠️ {name}\n**REVIEW**")
                                else:
                                    st.info(f"➖ {name}\n**N/A**")
                        
                        st.markdown("---")
                        
                        # Detailed Explanation
                        st.markdown("#### 📝 Detailed Explanation")
                        
                        for criteria_key, criteria_name in zip(criteria_keys, criteria_names):
                            if criteria_key in explanation:
                                exp = explanation[criteria_key]
                                
                                if exp["status"] == "PASS":
                                    color = "🟢"
                                elif exp["status"] == "FAIL":
                                    color = "🔴"
                                elif exp["status"] == "REVIEW":
                                    color = "🟡"
                                else:
                                    color = "⚪"
                                
                                with st.expander(f"{color} {criteria_name} - {exp['status']}"):
                                    st.write(f"**Status:** {exp['status']}")
                                    st.write(f"**Required:** {exp['required']}")
                                    st.write(f"**Found:** {exp['found']}")
                                    st.write(f"**Analysis:** {exp['reason']}")
                        
                        st.markdown("---")
                        
                        # Generate Report
                        st.markdown("#### 📄 Generate Report")
                        
                        report = create_report_summary(bidder_data, criteria, results, explanation, verdict)
                        
                        if st.button("📥 Download Text Report"):
                            st.download_button(
                                label="Download Report (.txt)",
                                data=report,
                                file_name=f"evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain"
                            )
                        
                        st.markdown("---")
                        
                        # Show raw text
                        with st.expander("👀 View Extracted Bidder Text"):
                            st.text(text[:2000] + "..." if len(text) > 2000 else text)
                    
                    else:
                        st.error("❌ Could not extract text from bidder document. Please try another document.")

# ───────────────────────────────────────────────────────────────────
# TAB 4: FILE HISTORY
# ───────────────────────────────────────────────────────────────────
with tab4:
    st.markdown("### 📋 File Processing History")
    
    if not st.session_state.file_history:
        st.info("📭 No files processed yet. Start by uploading a tender or bidder document.")
    else:
        history_df = pd.DataFrame(st.session_state.file_history)
        
        st.markdown(f"**Total files processed:** {len(st.session_state.file_history)}")
        
        st.dataframe(
            history_df.sort_values("timestamp", ascending=False),
            use_container_width=True,
            hide_index=True
        )
        
        if st.button("🗑️ Clear History"):
            st.session_state.file_history = []
            st.success("History cleared!")
            st.rerun()

# ═══════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.9em;'>
    <p>🎯 SmartDOX v2.0 • Frontend-Only Edition • All processing done locally on your machine</p>
    <p>💡 No backend required • No data sent to external servers • 100% Private</p>
</div>
""", unsafe_allow_html=True)
