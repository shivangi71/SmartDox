import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

# IMPORT PARSER + MATCHER + explainer
from services.explainer import generate_explanation
from services.parser import extract_criteria, extract_bidder_data
from services.matcher import evaluate, final_verdict


# --- TESSERACT CONFIGURATION ---
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# FastAPI app
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# HOME ROUTE
# -----------------------------
@app.get("/")
def home():
    return {"status": "SmartDOX API is Online"}

# -----------------------------
# TENDER PROCESSING
# -----------------------------
@app.post("/upload-tender")
async def process_tender(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text = ""

        if file.filename.endswith('.pdf'):
            doc = fitz.open(stream=contents, filetype="pdf")
            for page in doc:
                page_text = page.get_text()

                # OCR fallback
                if len(page_text.strip()) < 10:
                    pix = page.get_pixmap()
                    img = Image.open(io.BytesIO(pix.tobytes()))
                    page_text = pytesseract.image_to_string(img)

                text += page_text
        else:
            image = Image.open(io.BytesIO(contents))
            text = pytesseract.image_to_string(image)

        criteria = extract_criteria(text)

        return {
            "filename": file.filename,
            "criteria": criteria,
            "preview": text[:500]
        }

    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# BIDDER EVALUATION (FULL)
# -----------------------------
@app.post("/evaluate-bidder")
async def evaluate_bidder(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text = ""

        if file.filename.endswith('.pdf'):
            doc = fitz.open(stream=contents, filetype="pdf")
            for page in doc:
                page_text = page.get_text()

                if len(page_text.strip()) < 10:
                    pix = page.get_pixmap()
                    img = Image.open(io.BytesIO(pix.tobytes()))
                    page_text = pytesseract.image_to_string(img)

                text += page_text
        else:
            image = Image.open(io.BytesIO(contents))
            text = pytesseract.image_to_string(image)

        # Extract bidder info
        bidder_data = extract_bidder_data(text)

        # TEMP criteria
        criteria = {
            "turnover": 5,
            "projects": 3,
            "gst": True,
            "iso": True
        }

        # Matching
        results = evaluate(criteria, bidder_data)
        verdict = final_verdict(results)

        # 🔥 NEW: Explanation
        explanation = generate_explanation(criteria, bidder_data, results)

        return {
            "bidder_data": bidder_data,
            "evaluation": results,
            "explanation": explanation,   # 👈 ADD THIS
            "final_status": verdict
        }

    except Exception as e:
        return {"error": str(e)}
# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)