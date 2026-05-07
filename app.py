import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import io
from PIL import Image
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv

# Optional: pytesseract for OCR (requires Tesseract-OCR system package)
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    pytesseract = None

# Page configuration
st.set_page_config(
    page_title="SmartDOX - Tender Evaluation Platform",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Backend API configuration
# For Streamlit Cloud: Set in Secrets section
# For local: Use .env file or environment variable
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

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
    }
    .status-fail {
        color: #dc3545;
        font-weight: bold;
    }
    .status-review {
        color: #ffc107;
        font-weight: bold;
    }
    .evaluation-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Helper functions
def extract_text_from_file(uploaded_file):
    """Extract text from PDF or image files"""
    try:
        if uploaded_file.type == "application/pdf":
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        elif uploaded_file.type.startswith("image/"):
            if not TESSERACT_AVAILABLE:
                st.error(
                    "⚠️ **Tesseract-OCR is not installed**\n\n"
                    "To process image files, please install Tesseract-OCR:\n\n"
                    "**Windows:**\n"
                    "1. Download from: https://github.com/UB-Mannheim/tesseract/wiki\n"
                    "2. Run the installer (default path: C:\\Program Files\\Tesseract-OCR)\n"
                    "3. Restart the app\n\n"
                    "**For now:** Please upload PDF files instead, which don't require OCR."
                )
                return None
            
            image = Image.open(uploaded_file)
            # Try to find Tesseract executable
            tesseract_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            ]
            
            tesseract_found = False
            for path in tesseract_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    tesseract_found = True
                    break
            
            if not tesseract_found:
                st.error(
                    "⚠️ **Tesseract-OCR not found at expected location**\n\n"
                    "Please install from: https://github.com/UB-Mannheim/tesseract/wiki\n"
                    "Default path: C:\\Program Files\\Tesseract-OCR"
                )
                return None
            
            text = pytesseract.image_to_string(image)
            return text
        else:
            st.warning("Unsupported file type. Please upload PDF or image.")
            return None
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}\n\nFor image files, ensure Tesseract-OCR is installed.")
        return None

def signup_user(name, email, mobile, password):
    """Register a new user"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/signup",
            json={
                "name": name,
                "email": email,
                "mobile": mobile,
                "password": password
            },
            timeout=REQUEST_TIMEOUT
        )
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Backend service may be loading."}
    except requests.exceptions.ConnectionError:
        return {"error": f"Cannot connect to backend: {API_BASE_URL}"}
    except Exception as e:
        return {"error": str(e)}

def login_user(email, password):
    """Authenticate user"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/login",
            json={"email": email, "password": password},
            timeout=REQUEST_TIMEOUT
        )
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Backend service may be loading."}
    except requests.exceptions.ConnectionError:
        return {"error": f"Cannot connect to backend: {API_BASE_URL}"}
    except Exception as e:
        return {"error": str(e)}

def upload_tender(file, user_id):
    """Upload and process tender document"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(
            f"{API_BASE_URL}/upload-tender",
            files=files,
            params={"user_id": user_id},
            timeout=REQUEST_TIMEOUT
        )
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"error": f"Cannot connect to backend: {API_BASE_URL}"}
    except Exception as e:
        return {"error": str(e)}

def evaluate_bidder(file, lang="en"):
    """Evaluate bidder document"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(
            f"{API_BASE_URL}/evaluate-bidder",
            files=files,
            params={"lang": lang},
            timeout=REQUEST_TIMEOUT
        )
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"error": f"Cannot connect to backend: {API_BASE_URL}"}
    except Exception as e:
        return {"error": str(e)}

def get_file_history(user_id):
    """Retrieve file upload history"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/history/{user_id}",
            timeout=REQUEST_TIMEOUT
        )
        return response.json()
    except requests.exceptions.Timeout:
        return []
    except requests.exceptions.ConnectionError:
        return []
    except Exception as e:
        return []

def chat_with_bot(message):
    """Send message to chatbot"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"message": message},
            timeout=REQUEST_TIMEOUT
        )
        return response.json()
    except requests.exceptions.Timeout:
        return {"reply": "Request timed out. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"reply": f"Cannot connect to backend: {API_BASE_URL}"}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}

# Authentication Section
if not st.session_state.is_logged_in:
    st.markdown("""
        <div class="main-header">
            <h1>🎯 SmartDOX</h1>
            <p>AI-Powered Smart Tender Evaluation Platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Show Tesseract warning if not available
    if not TESSERACT_AVAILABLE:
        st.warning(
            "⚠️ **Optional: Tesseract-OCR not detected**\n\n"
            "You can still use the app with PDF files. To process image files, "
            "[install Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)"
        )

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Sign Up")
        with st.form("signup_form"):
            signup_name = st.text_input("Full Name", key="signup_name")
            signup_email = st.text_input("Email", key="signup_email")
            signup_mobile = st.text_input("Mobile Number", key="signup_mobile")
            signup_password = st.text_input("Password", type="password", key="signup_password")
            signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")
            
            if st.form_submit_button("Create Account"):
                if not all([signup_name, signup_email, signup_mobile, signup_password, signup_confirm]):
                    st.error("Please fill all fields")
                elif signup_password != signup_confirm:
                    st.error("Passwords don't match")
                else:
                    response = signup_user(signup_name, signup_email, signup_mobile, signup_password)
                    if "error" in response:
                        st.error(f"Signup failed: {response['error']}")
                    else:
                        st.success("✅ Account created successfully! Please login.")

    with col2:
        st.subheader("🔐 Log In")
        with st.form("login_form"):
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")
            
            if st.form_submit_button("Login"):
                if not login_email or not login_password:
                    st.error("Please enter email and password")
                else:
                    response = login_user(login_email, login_password)
                    if "error" in response or "message" not in response:
                        st.error("Invalid credentials")
                    else:
                        st.session_state.is_logged_in = True
                        st.session_state.user_id = response.get("user_id")
                        st.session_state.username = response.get("name")
                        st.rerun()

else:
    # Main Application (After Login)
    # Sidebar navigation
    sidebar = st.sidebar
    sidebar.markdown("---")
    
    col_user, col_logout = sidebar.columns([3, 1])
    with col_user:
        sidebar.write(f"👤 Welcome, **{st.session_state.username}**")
    with col_logout:
        if sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.is_logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
    
    sidebar.markdown("---")
    
    # Navigation menu
    menu_option = sidebar.radio(
        "📌 Menu",
        ["🏠 Dashboard", "📄 Process Tender", "👥 Evaluate Bidder", "📋 File History", "💬 Chatbot"]
    )

    # Dashboard
    if menu_option == "🏠 Dashboard":
        st.markdown("""
            <div class="main-header">
                <h1>🎯 SmartDOX Dashboard</h1>
                <p>Automate and Standardize Tender Evaluation</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("📄 **Process Tender Documents**\n\nExtract eligibility criteria from tender documents automatically.")
        
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
                "✅ OCR-based extraction",
                "✅ Intelligent criteria matching",
                "✅ Explainable AI decisions",
                "✅ Multilingual support",
                "✅ Audit-ready reporting"
            ]
            for feature in features:
                st.write(feature)
        
        with col2:
            st.subheader("📊 Supported File Formats")
            formats = [
                "📄 PDF documents (typed & scanned)",
                "🖼️ Images (JPG, PNG, etc.)",
                "📋 Word files",
                "📊 Tables and spreadsheets"
            ]
            for fmt in formats:
                st.write(fmt)

    # Process Tender
    elif menu_option == "📄 Process Tender":
        st.markdown("### 📄 Upload & Process Tender Document")
        st.write("Upload a tender document to extract eligibility criteria (turnover, projects, certifications, etc.)")

        uploaded_tender = st.file_uploader(
            "Choose a tender document",
            type=["pdf", "jpg", "jpeg", "png", "gif"],
            key="tender_uploader"
        )

        if uploaded_tender:
            st.info(f"📁 File: **{uploaded_tender.name}**")
            
            if st.button("🔍 Process Tender", use_container_width=True):
                with st.spinner("Processing tender document..."):
                    response = upload_tender(uploaded_tender, st.session_state.user_id)
                
                if "error" in response:
                    st.error(f"Error: {response['error']}")
                else:
                    st.success("✅ Tender processed successfully!")
                    
                    criteria = response.get("criteria", {})
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📋 Extracted Criteria")
                        criteria_df = pd.DataFrame([
                            {"Criterion": "Minimum Turnover", "Value": f"₹{criteria.get('turnover', 'N/A')} Crore"},
                            {"Criterion": "Minimum Projects", "Value": criteria.get('projects', 'N/A')},
                            {"Criterion": "GST Required", "Value": "✅ Yes" if criteria.get('gst') else "❌ No"},
                            {"Criterion": "ISO Required", "Value": "✅ Yes" if criteria.get('iso') else "❌ No"}
                        ])
                        st.dataframe(criteria_df, use_container_width=True, hide_index=True)

    # Evaluate Bidder
    elif menu_option == "👥 Evaluate Bidder":
        st.markdown("### 👥 Evaluate Bidder Document")
        st.write("Upload a bidder document to evaluate against tender criteria")

        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_bidder = st.file_uploader(
                "Choose a bidder document",
                type=["pdf", "jpg", "jpeg", "png", "gif"],
                key="bidder_uploader"
            )
        
        with col2:
            language = st.selectbox(
                "📝 Language",
                ["English", "Hindi", "Marathi"],
                key="eval_language"
            )

        if uploaded_bidder:
            st.info(f"📁 File: **{uploaded_bidder.name}**")
            
            if st.button("🔬 Evaluate Bidder", use_container_width=True):
                lang_code = {"English": "en", "Hindi": "hi", "Marathi": "mr"}.get(language, "en")
                
                with st.spinner("Evaluating bidder document..."):
                    response = evaluate_bidder(uploaded_bidder, lang=lang_code)
                
                if "error" in response:
                    st.error(f"Error: {response['error']}")
                else:
                    st.success("✅ Evaluation completed!")
                    
                    # Display Bidder Data
                    st.subheader("📊 Bidder Information")
                    bidder_data = response.get("bidder_data", {})
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Turnover", f"₹{bidder_data.get('turnover', 'N/A')} Cr")
                    with col2:
                        st.metric("Projects", bidder_data.get('projects', 'N/A'))
                    with col3:
                        st.metric("GST", "✅ Yes" if bidder_data.get('gst') else "❌ No")
                    with col4:
                        st.metric("ISO", "✅ Yes" if bidder_data.get('iso') else "❌ No")

                    # Display Evaluation Results
                    st.subheader("🎯 Evaluation Results")
                    evaluation = response.get("evaluation", {})
                    
                    results_df = pd.DataFrame([
                        {
                            "Criterion": "Turnover",
                            "Status": evaluation.get('turnover', 'N/A')
                        },
                        {
                            "Criterion": "Projects",
                            "Status": evaluation.get('projects', 'N/A')
                        },
                        {
                            "Criterion": "GST",
                            "Status": evaluation.get('gst', 'N/A')
                        },
                        {
                            "Criterion": "ISO",
                            "Status": evaluation.get('iso', 'N/A')
                        }
                    ])
                    
                    # Color code the status
                    def color_status(val):
                        if val == "PASS":
                            return "background-color: #d4edda; color: #155724;"
                        elif val == "FAIL":
                            return "background-color: #f8d7da; color: #721c24;"
                        else:
                            return "background-color: #fff3cd; color: #856404;"
                    
                    st.dataframe(
                        results_df.style.applymap(color_status, subset=["Status"]),
                        use_container_width=True,
                        hide_index=True
                    )

                    # Display Final Verdict
                    verdict = response.get("verdict", "Needs Manual Review")
                    
                    if "Not Eligible" in verdict:
                        st.error(f"❌ **Final Verdict: {verdict}**")
                    elif "Needs Manual Review" in verdict:
                        st.warning(f"⚠️ **Final Verdict: {verdict}**")
                    else:
                        st.success(f"✅ **Final Verdict: {verdict}**")

                    # Display Explanation
                    if "explanation" in response:
                        st.subheader("📝 Detailed Explanation")
                        explanation = response.get("explanation", {})
                        
                        for criterion, details in explanation.items():
                            with st.expander(f"🔍 {criterion.upper()}", expanded=False):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write(f"**Status:** {details.get('status', 'N/A')}")
                                    st.write(f"**Required:** {details.get('required', 'N/A')}")
                                with col2:
                                    st.write(f"**Found:** {details.get('found', 'N/A')}")
                                    st.write(f"**Reason:** {details.get('reason', 'N/A')}")

    # File History
    elif menu_option == "📋 File History":
        st.markdown("### 📋 Your File Upload History")
        
        with st.spinner("Loading history..."):
            history = get_file_history(st.session_state.user_id)
        
        if isinstance(history, list) and len(history) > 0:
            history_df = pd.DataFrame(history)
            
            # Format date column
            if "date" in history_df.columns:
                history_df["date"] = pd.to_datetime(history_df["date"]).dt.strftime("%Y-%m-%d %H:%M:%S")
            
            st.dataframe(
                history_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "id": st.column_config.NumberColumn("ID"),
                    "filename": st.column_config.TextColumn("File Name"),
                    "date": st.column_config.TextColumn("Upload Date")
                }
            )
        else:
            st.info("📭 No files uploaded yet. Start by processing a tender document!")

    # Chatbot
    elif menu_option == "💬 Chatbot":
        st.markdown("### 💬 SmartDOX Assistant")
        st.write("Ask questions about the tender evaluation process, criteria matching, or get help with the platform.")

        # Chat history in session state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User input
        if user_input := st.chat_input("Ask me anything..."):
            # Display user message
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # Add to history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Get bot response
            with st.spinner("Thinking..."):
                response = chat_with_bot(user_input)
            
            bot_reply = response.get("reply", "Sorry, I couldn't process that.")
            
            # Display bot message
            with st.chat_message("assistant"):
                st.markdown(bot_reply)
            
            # Add to history
            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>SmartDOX v1.0 | AI-Powered Smart Tender Evaluation Platform</p>
        <p>© 2024 SmartDOX. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)
