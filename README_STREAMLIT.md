# 🎯 SmartDOX Streamlit Web Interface

A modern, user-friendly Streamlit-based web application for the SmartDOX AI-powered tender evaluation platform.

## 🌟 Features

### 🔐 User Authentication
- User registration with email verification
- Secure login system
- Session management
- User profile tracking

### 📄 Tender Processing
- Upload tender documents (PDF, images)
- Automatic criteria extraction:
  - Minimum turnover requirements
  - Required projects count
  - Mandatory certifications (GST, ISO)
- Structured output of eligibility criteria

### 👥 Bidder Evaluation
- Upload bidder submission documents
- Automatic evaluation against tender criteria
- Multi-language results (English, Hindi, Marathi)
- Detailed evaluation breakdown:
  - Individual criterion status (PASS/FAIL/REVIEW)
  - Final verdict (Eligible/Not Eligible/Needs Review)
  - Reason for each evaluation decision

### 📊 Results & Reports
- Color-coded evaluation results
- Explainable AI decisions
- Detailed criterion-wise analysis
- Audit-ready output format

### 📋 File Management
- Upload history tracking
- File search and filtering
- Timestamp recording (IST timezone)

### 💬 AI Assistant Chatbot
- Real-time chat interface
- Questions about platform features
- Guidance on tender evaluation
- Multilingual support

### 🎨 Modern UI/UX
- Responsive design
- Gradient headers and themed elements
- Intuitive navigation
- Real-time status updates
- Data visualization with tables and metrics

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB

### Required Software
1. **Python 3.8+**
   - Download: https://www.python.org/

2. **Tesseract-OCR** (for document scanning)
   - **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

3. **Backend API** (SmartDOX FastAPI Server)
   - Must be running on `http://localhost:8000`
   - See backend README for setup instructions

## 🚀 Installation & Setup

### Option 1: Quick Start (Windows)
```bash
# 1. Double-click run_streamlit.bat
# OR
# 2. Run from command prompt:
run_streamlit.bat
```

### Option 2: Quick Start (Linux/macOS)
```bash
# 1. Make script executable
chmod +x run_streamlit.sh

# 2. Run the script
./run_streamlit.sh
```

### Option 3: Manual Installation
```bash
# 1. Install dependencies
pip install -r requirements_streamlit.txt

# 2. Create .env file
cp .env.example .env

# 3. Configure .env (set API_BASE_URL)
# Edit .env with your favorite editor

# 4. Ensure backend is running
# In another terminal: python backend/main.py

# 5. Launch Streamlit
streamlit run app.py

# 6. Open browser
# Navigate to http://localhost:8501
```

## 📁 Project Structure

```
SmartDox/
├── app.py                          # Main Streamlit application
├── requirements_streamlit.txt      # Python dependencies
├── .env.example                    # Environment variables template
├── STREAMLIT_SETUP_GUIDE.md       # Detailed setup guide
├── run_streamlit.bat              # Windows launcher
├── run_streamlit.sh               # Linux/macOS launcher
├── backend/
│   ├── main.py                    # FastAPI backend
│   ├── database.py                # Database models
│   └── services/                  # Business logic services
└── frontend/                       # Legacy HTML frontend
```

## 🎯 How to Use

### 1. Create Account
- Click "Sign Up" tab
- Enter full name, email, mobile, and password
- Click "Create Account"

### 2. Login
- Click "Log In" tab
- Enter email and password
- Click "Login"

### 3. Process Tender Document
- Click "📄 Process Tender" in menu
- Upload tender document (PDF or image)
- Click "🔍 Process Tender"
- View extracted criteria in structured table

### 4. Evaluate Bidder Document
- Click "👥 Evaluate Bidder" in menu
- Upload bidder document (PDF or image)
- Select output language
- Click "🔬 Evaluate Bidder"
- Review evaluation results:
  - Bidder information (metrics)
  - Evaluation status per criterion
  - Final verdict with explanation

### 5. View File History
- Click "📋 File History" in menu
- See all documents uploaded by your account
- Track evaluation activities

### 6. Chat with Assistant
- Click "💬 Chatbot" in menu
- Type questions in chat box
- Get instant AI-powered responses

## 📊 Supported File Formats

| Type | Formats | Notes |
|------|---------|-------|
| **Documents** | PDF | Typed and scanned PDFs supported |
| **Images** | JPG, PNG, GIF, JPEG | OCR applied for text extraction |
| **Converted** | Word, Excel | Convert to PDF/image first |

## ⚙️ Configuration

### Environment Variables (.env)
```env
# Backend API endpoint
API_BASE_URL=http://localhost:8000

# Optional: Add your own keys
GROQ_API_KEY=your_key_here
```

### Tesseract Path (Windows)
If Tesseract is installed in a different location, update in `app.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Your\Path\To\tesseract.exe'
```

### Streamlit Configuration
Create `~/.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#f0f2f6"
secondaryBackgroundColor = "#e0e1ff"
textColor = "#262730"
```

## 🔒 Security Features

- Password-based authentication
- User session management
- Email validation for signup
- Secure file upload handling
- Database protection (SQLite)

## 🐛 Troubleshooting

### Issue: "Connection Error: Cannot reach API"
**Solution:**
```bash
# Terminal 1: Start backend
cd backend
python main.py

# Terminal 2: Start Streamlit
streamlit run app.py
```

### Issue: "Tesseract is not installed"
**Solution:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Update tesseract path in `app.py`
- Restart Streamlit

### Issue: "File format not supported"
**Solution:**
- Supported formats: PDF, JPG, PNG, GIF, JPEG
- Convert to supported format before uploading

### Issue: "OCR not reading text correctly"
**Solution:**
- Ensure document is clear and high-contrast
- Use typed PDF instead of scanned when possible
- Pre-process image if needed

### Issue: "Port 8501 already in use"
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

## 📈 Performance Tips

1. **Optimize Documents**
   - Use clear, high-contrast images
   - Keep file sizes reasonable (<50MB)
   - Typed PDFs process faster than scanned

2. **Network**
   - Ensure stable internet connection
   - Keep backend and frontend on same network
   - Use localhost for best performance

3. **System**
   - Close unnecessary applications
   - Allocate sufficient RAM for app
   - Use SSD for faster file operations

## 🎨 Customization

### Change Theme Colors
Edit CSS section in `app.py`:
```python
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
    }
    </style>
""", unsafe_allow_html=True)
```

### Add New Menu Items
```python
menu_option = sidebar.radio(
    "📌 Menu",
    ["🏠 Dashboard", "📄 Process Tender", "👥 Evaluate Bidder", 
     "📋 File History", "💬 Chatbot", "🆕 Your New Feature"]
)
```

### Modify Evaluation Criteria
Update the criteria in `/backend/services/matcher.py`

## 📚 API Integration

The Streamlit app connects to the FastAPI backend:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/signup` | POST | Register user |
| `/login` | POST | Authenticate user |
| `/upload-tender` | POST | Process tender |
| `/evaluate-bidder` | POST | Evaluate bidder |
| `/history/{user_id}` | GET | Get file history |
| `/chat` | POST | Chat with AI |

## 🚦 Status Codes

### Evaluation Statuses
- **✅ PASS**: Criterion met/satisfied
- **❌ FAIL**: Criterion not met
- **⚠️ REVIEW**: Data unclear, needs manual review

### Final Verdicts
- **✅ Eligible**: All criteria passed
- **⚠️ Needs Manual Review**: Some criteria need review
- **❌ Not Eligible**: One or more criteria failed

## 📞 Support & Help

1. **Check Documentation**: See `STREAMLIT_SETUP_GUIDE.md`
2. **Verify Setup**: Run checklist:
   - [ ] Python 3.8+ installed
   - [ ] Dependencies installed
   - [ ] Backend running
   - [ ] Tesseract installed
   - [ ] .env configured
3. **Debug**: Check console for error messages
4. **Report Issues**: Create GitHub issue with:
   - Error message
   - Steps to reproduce
   - System information

## 🔄 Workflow Example

```
1. User Signs Up → Creates Account
2. User Logs In → Accesses Dashboard
3. User Uploads Tender → Extracts Criteria
4. User Uploads Bidder Doc → System Evaluates
5. System Shows Results → Pass/Fail/Review
6. User Reviews Explanation → Makes Decision
7. User Checks History → Tracks Activity
```

## 📝 File Description

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application with all UI/logic |
| `requirements_streamlit.txt` | Python package dependencies |
| `.env.example` | Template for environment variables |
| `STREAMLIT_SETUP_GUIDE.md` | Detailed setup and usage documentation |
| `run_streamlit.bat` | Quick launcher for Windows |
| `run_streamlit.sh` | Quick launcher for Linux/macOS |
| `README_STREAMLIT.md` | This file |

## 🎯 Future Enhancements

- [ ] Batch document processing
- [ ] Advanced filtering and search
- [ ] PDF/Excel report export
- [ ] Real-time collaboration
- [ ] Machine learning feedback loop
- [ ] Enhanced analytics dashboard
- [ ] API key management
- [ ] Role-based access control

## 📄 License

SmartDOX - AI-Powered Smart Tender Evaluation Platform

## 👥 Contributors

- Frontend: Streamlit UI Development
- Backend: FastAPI + ML Services
- DevOps: Deployment & Infrastructure

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
- [Python Best Practices](https://pep8.org)

---

**Made with ❤️ for Government Procurement Automation**
