# 🎯 SmartDOX v2.0 - Redeveloped Frontend-Only Edition

**AI-Powered Tender Evaluation Platform • No Backend Server Required**

---

## ✨ What's New in v2.0?

**SmartDOX has been completely redeveloped as a frontend-only application!**

✅ **No FastAPI backend to run**  
✅ **No database needed**  
✅ **All processing local (private)**  
✅ **Single Streamlit app**  
✅ **Instant setup & deployment**  
✅ **100% free (no paid APIs)**  

---

## 🚀 Quick Start (30 seconds)

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the App
```bash
streamlit run app.py
```

### 3️⃣ Open in Browser
```
http://localhost:8501
```

**That's it! 🎉**

---

## 📋 What You Can Do

### 1. **Process Tender Documents** 📄
- Upload PDF or image of tender document
- Automatically extract:
  - Minimum turnover requirement
  - Minimum project experience
  - GST certification requirement
  - ISO certification requirement

### 2. **Evaluate Bidders** 👥
- Upload bidder's document/proposal
- Automatically extract bidder information:
  - Company turnover
  - Project experience
  - GST status
  - ISO certifications
- Get instant evaluation verdict:
  - ✅ **Eligible** - Meets all criteria
  - ❌ **Not Eligible** - Failed some criteria
  - ⚠️ **Needs Manual Review** - Unclear data

### 3. **Get Detailed Reports** 📊
- Explanation for each criterion
- Required vs Found values
- Pass/Fail/Review status
- Download text reports

### 4. **Multilingual Support** 🌍
- Results in 8+ languages:
  - English, Hindi, Marathi, Gujarati, Tamil, Telugu, Kannada, Malayalam
- Automatic translation using Google Translate

---

## 📁 Project Structure

```
SmartDox/
├── app.py                          # ✨ NEW: Frontend-only Streamlit app
├── services.py                     # ✨ NEW: All business logic (local)
├── requirements.txt                # ✨ UPDATED: Simplified dependencies
├── MIGRATION_GUIDE.md              # Detailed upgrade guide
├── README.md                       # This file
│
├── [DEPRECATED] backend/           # Old FastAPI server (not needed)
├── [DEPRECATED] docker-compose.yml
├── [DEPRECATED] Dockerfile
└── [DEPRECATED] Procfile
```

---

## 🔧 System Requirements

| Requirement | Details |
|-------------|---------|
| **Python** | 3.8 or higher |
| **RAM** | 2GB minimum (4GB recommended) |
| **Storage** | 500MB for packages |
| **Internet** | For translation feature (Google Translate) |

---

## ⚙️ Optional Setup

### Install Tesseract for Image OCR (Optional)
To process scanned documents as images, install Tesseract-OCR:

**Windows:**
1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer (default: `C:\Program Files\Tesseract-OCR`)
3. Restart the app

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

---

## 📊 Usage Examples

### Example 1: Process a Tender
1. Open SmartDOX
2. Go to **"Process Tender"** tab
3. Upload a tender PDF
4. View extracted criteria

### Example 2: Evaluate a Bidder
1. First process a tender (to get criteria)
2. Go to **"Evaluate Bidder"** tab
3. Upload bidder document
4. See instant evaluation with verdict
5. View detailed explanations
6. Download report

### Example 3: Get Results in Hindi
1. Select "🇮🇳 Hindi" from language dropdown (sidebar)
2. Results will be automatically translated

---

## 🎯 How It Works

### Architecture

```
User Upload (PDF/Image)
         ↓
    Text Extraction (PyMuPDF + Tesseract)
         ↓
    Parse with Regex Patterns
         ↓
    Extract Criteria & Bidder Data
         ↓
    Evaluation Logic (Match vs Requirements)
         ↓
    Generate Explanation
         ↓
    Optional: Translate to Other Languages
         ↓
    Display Results + Generate Report
```

### Key Technologies

| Component | Technology | Why |
|-----------|-----------|-----|
| UI | Streamlit | Simple, fast, Pythonic |
| PDF Processing | PyMuPDF | Fast, reliable text extraction |
| OCR | Tesseract | Industry standard, open-source |
| Translation | Google Translate API | Free, supports 100+ languages |
| Pattern Matching | RegEx | Rule-based, interpretable extraction |
| Data Handling | Pandas | Easy manipulation and display |

---

## 💻 Key Files Explained

### `app.py` - Main Application
- Streamlit interface
- File upload and processing
- Tab-based navigation
- Results display and reporting

### `services.py` - Business Logic
All the core functions:
- `extract_criteria()` - Parse tender requirements
- `extract_bidder_data()` - Extract bidder information
- `evaluate()` - Match bidder vs criteria
- `final_verdict()` - Determine eligibility
- `generate_explanation()` - Explain results
- `translate_text()` - Multilingual support

---

## 🌟 Features

### ✅ Currently Supported
- PDF text extraction (typed & scanned)
- Image processing (OCR)
- Criteria extraction (turnover, projects, GST, ISO)
- Bidder evaluation
- Detailed explanations
- Report generation
- 8+ language translations
- File history tracking

### 🔮 Potential Enhancements
- Machine learning for better extraction
- Support for .docx, .xlsx files
- Custom evaluation rules
- Batch processing
- Export to PDF reports
- User authentication (optional)

---

## 🔐 Privacy & Security

✅ **All data stays on your machine**
- No data sent to any external server (except Google Translate)
- No user accounts or logins required
- No database storage
- No tracking or analytics
- Complete local processing

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'services'"
**Solution:** Make sure `services.py` is in the same directory as `app.py`

### Issue: "PyMuPDF is not installed"
**Solution:** 
```bash
pip install PyMuPDF
```

### Issue: "Tesseract-OCR not found"
**Solution:** Install Tesseract (see Optional Setup section above)

### Issue: "Translation not working"
**Solution:** 
- Check internet connection
- Check if Google Translate is accessible in your region
- Try a different language

### Issue: "PDF not being read correctly"
**Solution:**
- Try converting PDF to text format first
- Or use image OCR (scan/screenshot)
- Try a different PDF

### Issue: Slow processing
**Solution:**
- Large scanned PDFs take longer
- Close other applications
- Try smaller documents first

---

## 🚀 Deployment

### Option 1: Streamlit Cloud (Free & Easy)
1. Push to GitHub
2. Visit https://streamlit.io/cloud
3. Connect your repository
4. Deploy in one click!

### Option 2: Docker
```bash
docker build -t smartdox .
docker run -p 8501:8501 smartdox
```

### Option 3: Traditional Server
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 📚 API Usage (Python)

If you want to use the services programmatically:

```python
from services import *
import fitz

# Step 1: Extract text from PDF
doc = fitz.open("tender.pdf")
tender_text = "".join([page.get_text() for page in doc])

# Step 2: Extract criteria
criteria = extract_criteria(tender_text)
print(criteria)
# Output: {'turnover': 5.0, 'projects': 3, 'gst': True, 'iso': False}

# Step 3: Process bidder document
bidder_doc = fitz.open("bidder.pdf")
bidder_text = "".join([page.get_text() for page in bidder_doc])
bidder = extract_bidder_data(bidder_text)

# Step 4: Evaluate
results = evaluate(criteria, bidder)
verdict = final_verdict(results)
explanation = generate_explanation(criteria, bidder, results)

# Step 5: Get results
print(f"Verdict: {verdict}")
print(f"Results: {results}")
print(f"Explanation: {explanation}")

# Step 6: Translate (optional)
translated = translate_text(verdict, 'hi')
print(f"Hindi: {translated}")
```

---

## ❓ FAQ

**Q: Do I need a backend server?**  
A: No! Everything runs locally in Streamlit.

**Q: Is my data private?**  
A: Yes, 100% private. Data stays on your machine.

**Q: Can I use this offline?**  
A: Yes, except for the translation feature (which uses Google Translate).

**Q: How accurate is the extraction?**  
A: Uses regex patterns for rule-based extraction. For complex documents, some manual review may be needed.

**Q: Can I customize evaluation rules?**  
A: Yes! Modify the `evaluate()` function in `services.py` to add your own logic.

**Q: Can I use this for production?**  
A: Yes! It's stable and all processing is local and fast.

---

## 📞 Support & Documentation

- **Streamlit Docs**: https://docs.streamlit.io
- **PyMuPDF Docs**: https://pymupdf.readthedocs.io
- **Google Translate**: https://translate.google.com
- **This Guide**: See `MIGRATION_GUIDE.md`

---

## 📝 Version History

### v2.0 (Current) - Frontend-Only Edition ✨
- Removed FastAPI backend
- Moved all logic to local services
- Simplified setup
- Better performance
- Added multilingual support

### v1.0 - Original Edition
- FastAPI backend
- Database authentication
- Groq API for chatbot
- Requires server setup

---

## 🎯 Next Steps

1. **Install:** `pip install -r requirements.txt`
2. **Run:** `streamlit run app.py`
3. **Test:** Upload sample documents
4. **Customize:** Modify `services.py` for your needs
5. **Deploy:** Share with your team!

---

## 💡 Tips for Best Results

1. **Clear documents** - Use clear, high-quality PDFs/images
2. **Structured format** - Better extraction with well-formatted documents
3. **Manual review** - Always verify automated results
4. **Set standards** - Define your own evaluation criteria in `services.py`
5. **Test first** - Start with sample documents

---

## 📄 License

SmartDOX is provided as-is for tender evaluation purposes.

---

**Made with ❤️ for Tender Evaluation**

🎯 SmartDOX - Making Tender Evaluation Simple, Fast & Transparent

**Version 2.0 • Frontend-Only • No Backend Required • All Local Processing**
