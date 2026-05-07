# SmartDOX Streamlit App Setup & Usage Guide

## 📋 Overview

This is a Streamlit-based web interface for the SmartDOX platform - an AI-powered tender evaluation system. The app provides a user-friendly interface to:

- ✅ Register and authenticate users
- 📄 Upload and process tender documents
- 👥 Evaluate bidder submissions
- 📊 View detailed evaluation reports with explanations
- 📋 Track file upload history
- 💬 Chat with an AI assistant

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** installed
- **Tesseract-OCR** installed (for document processing)
- **Backend API** (FastAPI server) running on `http://localhost:8000`

### Installation Steps

1. **Install Tesseract-OCR** (Required for document processing)
   - **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements_streamlit.txt
   ```

3. **Configure Environment Variables**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env and set the API_BASE_URL (default is localhost:8000)
   ```

4. **Start the Backend (in separate terminal)**
   ```bash
   # From the backend directory
   python main.py
   
   # Or with uvicorn
   uvicorn main:app --reload
   ```

5. **Launch the Streamlit App**
   ```bash
   streamlit run app.py
   ```

6. **Access the Application**
   - Open browser and go to `http://localhost:8501`
   - Sign up for a new account or login with existing credentials

## 📱 Features & Usage

### 🏠 Dashboard
- Overview of all SmartDOX features
- Quick links to main functionality
- List of supported file formats

### 📄 Process Tender
1. Upload a tender document (PDF or image)
2. Click "Process Tender" button
3. View extracted eligibility criteria:
   - Minimum turnover required
   - Minimum projects required
   - Required certifications (GST, ISO)

### 👥 Evaluate Bidder
1. Upload a bidder document (PDF or image)
2. Select output language (English, Hindi, Marathi)
3. Click "Evaluate Bidder" button
4. View comprehensive evaluation results:
   - **Bidder Information**: Extracted financial and certification data
   - **Evaluation Results**: Pass/Fail status for each criterion
   - **Final Verdict**: Eligible / Not Eligible / Needs Manual Review
   - **Detailed Explanation**: Reason for each evaluation decision

### 📋 File History
- View all documents uploaded by your account
- Timestamps of each upload
- Track your evaluation activities

### 💬 Chatbot
- Ask questions about the platform
- Get help with tender evaluation process
- Understand criteria matching
- Real-time chat interface

## 📊 Supported File Formats

- **PDF**: Typed PDFs and scanned documents
- **Images**: JPG, PNG, GIF, JPEG
- **Other**: Word files, Excel sheets (via conversion to PDF/image)

## 🔐 Authentication

The app includes built-in user management:

### Sign Up
- Create new account with name, email, mobile, and password
- Account stored securely in SQLite database

### Login
- Email and password authentication
- Session maintained throughout the app

## ⚙️ Configuration

### Environment Variables (.env)
```env
# API endpoint for backend server
API_BASE_URL=http://localhost:8000

# Optional: Add your own API keys if needed
GROQ_API_KEY=your_api_key_here
```

### Tesseract Configuration
The app is configured for Windows by default:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

For other systems, update this path accordingly in `app.py`.

## 🎨 UI/UX Features

- **Modern Design**: Gradient headers, color-coded status indicators
- **Responsive Layout**: Adapts to different screen sizes
- **Interactive Components**: Forms, file uploaders, expandable sections
- **Real-time Feedback**: Spinners during processing, success/error messages
- **Data Visualization**: Tables, metrics, and structured data display

## 📊 Evaluation Criteria

The system evaluates bidders on four main criteria:

| Criterion | Evaluation Type | Status Options |
|-----------|-----------------|-----------------|
| **Turnover** | Numeric Comparison | PASS / FAIL / REVIEW |
| **Projects** | Numeric Comparison | PASS / FAIL / REVIEW |
| **GST** | Document Presence | PASS / FAIL |
| **ISO** | Document Presence | PASS / FAIL |

### Verdict Logic
- **Eligible**: All criteria are PASS
- **Needs Manual Review**: Contains REVIEW status
- **Not Eligible**: Contains FAIL status

## 🐛 Troubleshooting

### "Connection Error: Cannot reach API"
- Ensure backend server is running (`python main.py`)
- Verify `API_BASE_URL` in `.env` is correct
- Default: `http://localhost:8000`

### "Tesseract is not installed or cannot be found"
- Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
- Update the tesseract path in `app.py` if installed in different location

### "File format not supported"
- Supported: PDF, JPG, PNG, GIF, JPEG
- Convert other formats to these types before uploading

### "OCR is not reading text correctly"
- Ensure document is clear and high contrast
- Try using typed PDF instead of scanned if available
- Scanned documents may require image preprocessing

## 🔧 Development & Customization

### Add New Pages
Create a new section in the menu:
```python
elif menu_option == "📌 New Feature":
    st.markdown("### Your Feature Title")
    # Add your code here
```

### Modify Colors & Styles
Update the CSS in the `st.markdown()` section at the top of the file.

### Add New Languages
Update the language selection in Evaluate Bidder section:
```python
language = st.selectbox(
    "📝 Language",
    ["English", "Hindi", "Marathi", "Your Language"],  # Add here
)
```

## 📝 API Integration

The app communicates with the FastAPI backend through these endpoints:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/signup` | Register new user |
| POST | `/login` | Authenticate user |
| POST | `/upload-tender` | Process tender document |
| POST | `/evaluate-bidder` | Evaluate bidder document |
| GET | `/history/{user_id}` | Get file history |
| POST | `/chat` | Send message to chatbot |

## 💡 Best Practices

1. **Before Uploading**: Ensure documents are clear and readable
2. **File Size**: Keep files under 50MB for optimal performance
3. **Format**: Use PDF for better OCR accuracy
4. **Language**: Set language before evaluation for accurate translation
5. **Review Results**: Always review AI decisions for critical decisions

## 📱 System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.8+
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB
- **Browser**: Any modern browser (Chrome, Firefox, Safari, Edge)

## 🤝 Support & Contribution

For issues, feature requests, or contributions:
1. Check existing issues on GitHub
2. Create detailed bug reports
3. Submit pull requests with improvements

## 📄 License

SmartDOX is built for government procurement automation.

## 🎯 Future Enhancements

- [ ] Multi-document batch processing
- [ ] Advanced reporting and analytics
- [ ] Document comparison tools
- [ ] Integration with more languages
- [ ] Advanced filtering and search
- [ ] Export reports to PDF/Excel
- [ ] Real-time collaboration features

---

**Need Help?** Check the FAQ or contact the SmartDOX team.
