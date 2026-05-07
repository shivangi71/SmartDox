"""
SmartDOX - Local Services Module (No Backend Required)
All business logic for tender evaluation is here.
"""

import re
from deep_translator import GoogleTranslator

# ============================================================
# 1. TEXT EXTRACTION & PARSING
# ============================================================

def extract_criteria(text):
    """Extract evaluation criteria from tender document"""
    text = text.lower()
    criteria = {}

    # Turnover (e.g., "5 crore", "Rs. 5 crore")
    turnover_match = re.search(r'(?:rs\.?|₹)?\s*(\d+(?:\.\d+)?)\s*(?:crore|cr)', text)
    if turnover_match:
        criteria["turnover"] = float(turnover_match.group(1))
    else:
        criteria["turnover"] = None

    # Projects/Experience (e.g., "3 projects", "3+ similar projects")
    project_match = re.search(r'(\d+)\s*(?:\+)?\s*(?:projects|similar\s+projects|project\s+experience)', text)
    if project_match:
        criteria["projects"] = int(project_match.group(1))
    else:
        criteria["projects"] = None

    # GST Registration (keyword presence)
    criteria["gst"] = bool(re.search(r'\bgst\b|\bgst\s+registration\b', text))

    # ISO Certification (keyword presence)
    criteria["iso"] = bool(re.search(r'\biso\b|\biso\s+certification\b|\biso\s+certified\b', text))

    # Additional certifications
    criteria["has_certification_requirement"] = bool(
        re.search(r'certification|certified|iso|quality', text)
    )

    return criteria


def extract_bidder_data(text):
    """Extract bidder information from bid document"""
    text = text.lower()
    data = {}

    # Turnover
    turnover_match = re.search(r'(?:turnover|annual\s+turnover|revenue)[\s:]*(?:rs\.?|₹)?\s*(\d+(?:\.\d+)?)\s*(?:crore|cr)', text)
    if turnover_match:
        data["turnover"] = float(turnover_match.group(1))
    else:
        data["turnover"] = None

    # Projects/Experience
    project_match = re.search(r'(?:projects|experience|completed)[\s:]*(\d+)\s*(?:projects|similar\s+projects)', text)
    if project_match:
        data["projects"] = int(project_match.group(1))
    else:
        data["projects"] = None

    # GST Registration
    data["gst"] = bool(re.search(r'\bgst\b|\bgst\s+(?:registration|number|id)|gstin\b', text))

    # ISO Certification
    data["iso"] = bool(re.search(r'\biso\b|\biso\s+certification\b|\biso\s+certified\b', text))

    # Extract company name
    company_match = re.search(r'(?:company|firm|organization|entity)\s*[:\s]+([a-z\s&.,-]+)', text)
    data["company_name"] = company_match.group(1).strip() if company_match else "Unknown"

    # Extract registration number if available
    registration_match = re.search(r'(?:cin|registration|reg\.?\s+no\.?)\s*[:\s]*([a-z0-9]+)', text)
    data["registration_number"] = registration_match.group(1) if registration_match else None

    return data


# ============================================================
# 2. EVALUATION & MATCHING
# ============================================================

def evaluate(criteria, bidder):
    """
    Evaluate if bidder meets tender criteria
    Returns: {"field": "PASS"|"FAIL"|"REVIEW", ...}
    """
    result = {}

    # Turnover check
    if bidder.get("turnover") is None:
        result["turnover"] = "REVIEW"
    elif criteria.get("turnover") is None:
        result["turnover"] = "PASS"
    elif bidder["turnover"] >= criteria["turnover"]:
        result["turnover"] = "PASS"
    else:
        result["turnover"] = "FAIL"

    # Projects/Experience check
    if bidder.get("projects") is None:
        result["projects"] = "REVIEW"
    elif criteria.get("projects") is None:
        result["projects"] = "PASS"
    elif bidder["projects"] >= criteria["projects"]:
        result["projects"] = "PASS"
    else:
        result["projects"] = "FAIL"

    # GST check
    if criteria.get("gst"):
        result["gst"] = "PASS" if bidder.get("gst") else "FAIL"
    else:
        result["gst"] = "N/A"

    # ISO check
    if criteria.get("iso"):
        result["iso"] = "PASS" if bidder.get("iso") else "FAIL"
    else:
        result["iso"] = "N/A"

    return result


def final_verdict(results):
    """
    Determine final eligibility verdict
    Returns: "Eligible" | "Not Eligible" | "Needs Manual Review"
    """
    # Count failures
    failures = [v for v in results.values() if v == "FAIL"]
    reviews = [v for v in results.values() if v == "REVIEW"]

    if failures:
        return "Not Eligible"
    elif reviews:
        return "Needs Manual Review"
    else:
        return "Eligible"


def get_verdict_color(verdict):
    """Return color for verdict display"""
    if verdict == "Eligible":
        return "✅ green"
    elif verdict == "Not Eligible":
        return "❌ red"
    else:
        return "⚠️ orange"


# ============================================================
# 3. EXPLANATION & REPORTING
# ============================================================

def generate_explanation(criteria, bidder, results):
    """Generate detailed explanation for evaluation results"""
    explanation = {}

    # Turnover explanation
    explanation["turnover"] = {
        "status": results.get("turnover", "N/A"),
        "required": f">= {criteria.get('turnover')} crore" if criteria.get("turnover") else "No requirement",
        "found": f"{bidder.get('turnover')} crore" if bidder.get("turnover") else "Not Found",
        "reason": get_reason("Turnover", results.get("turnover", "N/A"))
    }

    # Projects explanation
    explanation["projects"] = {
        "status": results.get("projects", "N/A"),
        "required": f">= {criteria.get('projects')} projects" if criteria.get("projects") else "No requirement",
        "found": f"{bidder.get('projects')} projects" if bidder.get("projects") else "Not Found",
        "reason": get_reason("Project Experience", results.get("projects", "N/A"))
    }

    # GST explanation
    if results.get("gst") != "N/A":
        explanation["gst"] = {
            "status": results.get("gst", "N/A"),
            "required": "GST Registration Required",
            "found": "Available" if bidder.get("gst") else "Not Found",
            "reason": get_reason("GST Registration", results.get("gst", "N/A"))
        }

    # ISO explanation
    if results.get("iso") != "N/A":
        explanation["iso"] = {
            "status": results.get("iso", "N/A"),
            "required": "ISO Certification Required",
            "found": "Available" if bidder.get("iso") else "Not Found",
            "reason": get_reason("ISO Certification", results.get("iso", "N/A"))
        }

    return explanation


def get_reason(field, status):
    """Generate reason message based on status"""
    if status == "PASS":
        return f"✅ {field} requirement satisfied"
    elif status == "FAIL":
        return f"❌ {field} requirement not met"
    elif status == "REVIEW":
        return f"⚠️ {field} data unclear, needs manual review"
    else:
        return f"➖ {field} not evaluated"


# ============================================================
# 4. TRANSLATION
# ============================================================

def translate_text(text, target_lang='hi'):
    """
    Translate text to target language using Google Translate
    Supported: 'en', 'hi', 'mr', 'gu', 'ta', 'te', etc.
    """
    if target_lang == 'en' or not text:
        return text
    
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        
        # Handle dict translations
        if isinstance(text, dict):
            translated_dict = {}
            for key, value in text.items():
                if isinstance(value, str):
                    translated_dict[key] = translator.translate(value)
                elif isinstance(value, dict):
                    translated_dict[key] = translate_text(value, target_lang)
                else:
                    translated_dict[key] = value
            return translated_dict
        
        # Handle string translations
        translated = translator.translate(str(text))
        return translated
    
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original if translation fails


def get_supported_languages():
    """Return dictionary of supported languages"""
    return {
        "en": "🇬🇧 English",
        "hi": "🇮🇳 Hindi",
        "mr": "🇮🇳 Marathi",
        "gu": "🇮🇳 Gujarati",
        "ta": "🇮🇳 Tamil",
        "te": "🇮🇳 Telugu",
        "kn": "🇮🇳 Kannada",
        "ml": "🇮🇳 Malayalam",
    }


# ============================================================
# 5. UTILITY FUNCTIONS
# ============================================================

def format_results_for_display(bidder_data, criteria, results, explanation, verdict):
    """Format results for nice display"""
    return {
        "bidder_info": bidder_data,
        "criteria": criteria,
        "evaluation_results": results,
        "explanation": explanation,
        "final_verdict": verdict
    }


def create_report_summary(bidder_data, criteria, results, explanation, verdict):
    """Create a text summary for PDF export or display"""
    summary = f"""
    ╔════════════════════════════════════════════════════════════════╗
    ║              TENDER EVALUATION REPORT - SmartDOX              ║
    ╚════════════════════════════════════════════════════════════════╝
    
    📋 BIDDER INFORMATION
    ──────────────────────────────────────────────────────────────────
    Company Name: {bidder_data.get('company_name', 'Unknown')}
    Annual Turnover: {bidder_data.get('turnover', 'N/A')} Crore
    Project Experience: {bidder_data.get('projects', 'N/A')} Projects
    GST Registered: {'✅ Yes' if bidder_data.get('gst') else '❌ No'}
    ISO Certified: {'✅ Yes' if bidder_data.get('iso') else '❌ No'}
    
    📊 TENDER CRITERIA
    ──────────────────────────────────────────────────────────────────
    Min Turnover Required: {criteria.get('turnover', 'N/A')} Crore
    Min Projects Required: {criteria.get('projects', 'N/A')} Projects
    GST Required: {'✅ Yes' if criteria.get('gst') else '❌ No'}
    ISO Required: {'✅ Yes' if criteria.get('iso') else '❌ No'}
    
    ✅ EVALUATION RESULTS
    ──────────────────────────────────────────────────────────────────
    Turnover: {results.get('turnover', 'N/A')} - {explanation.get('turnover', {}).get('reason', '')}
    Experience: {results.get('projects', 'N/A')} - {explanation.get('projects', {}).get('reason', '')}
    GST: {results.get('gst', 'N/A')} - {explanation.get('gst', {}).get('reason', '') if 'gst' in explanation else 'N/A'}
    ISO: {results.get('iso', 'N/A')} - {explanation.get('iso', {}).get('reason', '') if 'iso' in explanation else 'N/A'}
    
    🎯 FINAL VERDICT
    ──────────────────────────────────────────────────────────────────
    Status: {verdict}
    
    ═════════════════════════════════════════════════════════════════════
    Generated by SmartDOX - AI-Powered Tender Evaluation Platform
    """
    return summary
