# 🔧 Tesseract-OCR Installation Guide

**Required for:** Processing image files (JPG, PNG, etc.)  
**Optional for:** PDF-only workflows (Tesseract not needed)

## ⚡ Quick Fix - Windows

### Method 1: Automatic Installation (Recommended)
```bash
# Double-click this file to install Tesseract
install_tesseract.bat
```

### Method 2: Manual Installation
1. Download latest installer from: https://github.com/UB-Mannheim/tesseract/wiki
   - Look for: `tesseract-ocr-w64-v5.x.exe` (64-bit) or `tesseract-ocr-w32-v5.x.exe` (32-bit)

2. Run the installer
   - Default installation path: `C:\Program Files\Tesseract-OCR`
   - Accept all defaults or customize if needed

3. Restart Streamlit app:
   ```bash
   streamlit run app.py
   ```

### Method 3: Using Chocolatey (If Installed)
```powershell
choco install tesseract -y
```

### Method 4: Using Scoop (If Installed)
```powershell
scoop install tesseract
```

---

## 🍎 macOS Installation

```bash
# Using Homebrew
brew install tesseract
```

---

## 🐧 Linux Installation

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr
```

### CentOS/RHEL
```bash
sudo yum install -y tesseract
```

### Fedora
```bash
sudo dnf install -y tesseract
```

---

## ✅ Verify Installation

### Windows PowerShell
```powershell
tesseract --version
```

### macOS/Linux
```bash
tesseract --version
```

**Expected output:**
```
tesseract 5.x.x
```

---

## 🔧 Troubleshooting

### Issue: "Tesseract is not installed or cannot be found"

**Solution 1: Check installation path**
```powershell
# Windows: Verify Tesseract exists at
Test-Path "C:\Program Files\Tesseract-OCR\tesseract.exe"
```

**Solution 2: Add to System PATH (Advanced)**

If Tesseract is installed in a non-standard location:

**Windows:**
1. Right-click "This PC" → Properties
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "System variables", find or create `PATH`
5. Add the path to Tesseract (e.g., `C:\Custom\Path\Tesseract-OCR`)
6. Click OK and restart your terminal

**macOS/Linux:**
```bash
# Add to ~/.zshrc or ~/.bash_profile
export PATH="/usr/local/bin:$PATH"
```

**Solution 3: Specify path in app.py**

If app still can't find Tesseract, edit `app.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Your\Custom\Path\tesseract.exe'
```

---

## 📊 Why Two Packages?

**PyTesseract** (Python package):
- Interface to call Tesseract from Python code
- Installed via: `pip install pytesseract`
- Already included in `requirements_streamlit.txt`

**Tesseract-OCR** (System library):
- The actual OCR engine that does text recognition
- Must be installed separately on your system
- Download from: https://github.com/UB-Mannheim/tesseract/wiki

**Both are needed** for image file processing!

---

## 🎯 Using SmartDOX Without Tesseract

**You CAN still use SmartDOX without Tesseract for:**
- ✅ PDF documents (typed PDFs work great)
- ✅ Tender evaluation
- ✅ Bidder assessment
- ✅ All other features

**You NEED Tesseract ONLY for:**
- ❌ Processing JPG/PNG images
- ❌ Scanned PDF processing (may be better with Tesseract)

**Workaround:** Convert image files to PDF:
```bash
# Using ImageMagick (optional)
convert image.jpg document.pdf

# Or use online tools:
# https://smallpdf.com/jpg-to-pdf
```

---

## 🚀 For Production Deployment

### Docker
```dockerfile
# Dockerfile already includes Tesseract installation
FROM python:3.10-slim

RUN apt-get update && apt-get install -y tesseract-ocr
```

### Cloud Platforms
- **Streamlit Cloud**: Tesseract not available by default
  - Solution: Upload PDFs only or use PDF conversion
- **Google Cloud Run**: Include in Dockerfile (done)
- **Azure Container**: Include in Dockerfile (done)

---

## 📝 Additional Language Data (Optional)

Tesseract supports multiple languages beyond English.

### Download Additional Languages

**Windows:**
1. Find your Tesseract installation: `C:\Program Files\Tesseract-OCR\`
2. Go to: `tessdata` folder
3. Download language files from: https://github.com/UB-Mannheim/tessdata
4. Place .traineddata files in tessdata folder

**macOS/Linux:**
```bash
# Language files are usually auto-installed
# To verify:
tesseract --list-langs

# Common languages already included:
# eng (English), fra (French), spa (Spanish), deu (German), etc.
```

---

## 🔐 Uninstall Tesseract

### Windows
1. Control Panel → Programs → Programs and Features
2. Find "Tesseract OCR"
3. Click "Uninstall"

### macOS
```bash
brew uninstall tesseract
```

### Linux
```bash
# Ubuntu/Debian
sudo apt-get remove -y tesseract-ocr

# CentOS/RHEL
sudo yum remove -y tesseract
```

---

## 📚 Resources

- **Official GitHub**: https://github.com/UB-Mannheim/tesseract/wiki
- **Tesseract Docs**: https://tesseract-ocr.github.io/
- **PyTesseract Docs**: https://pytesseract.readthedocs.io/

---

## 💡 Next Steps

1. **Install Tesseract** using method above
2. **Verify** installation with: `tesseract --version`
3. **Restart** Streamlit app
4. **Test** by uploading an image file
5. **Report** any issues

Happy document processing! 🎉
