"""
Multilingual translation service
"""
import logging
from typing import Dict, Any, Optional
from app.services.llm_service import llm_service
from app.config import settings

logger = logging.getLogger(__name__)

class TranslationService:
    """Handle multilingual translations"""
    
    def __init__(self):
        self.supported_languages = settings.SUPPORTED_LANGUAGES
        self.translations_cache = {}
        
        # Static translations for common UI elements
        self.static_translations = {
            "en": {
                "dashboard": "Dashboard",
                "upload": "Upload",
                "analysis": "Analysis",
                "insights": "Insights",
                "reports": "Reports",
                "forecast": "Forecast",
                "settings": "Settings",
                "revenue": "Revenue",
                "expenses": "Expenses",
                "profit": "Profit",
                "loss": "Loss",
                "assets": "Assets",
                "liabilities": "Liabilities",
                "health_score": "Health Score",
                "credit_score": "Credit Score",
                "risk_level": "Risk Level",
                "recommendations": "Recommendations",
                "export": "Export",
                "download": "Download"
            },
            "hi": {
                "dashboard": "डैशबोर्ड",
                "upload": "अपलोड करें",
                "analysis": "विश्लेषण",
                "insights": "अंतर्दृष्टि",
                "reports": "रिपोर्ट",
                "forecast": "पूर्वानुमान",
                "settings": "सेटिंग्स",
                "revenue": "राजस्व",
                "expenses": "खर्च",
                "profit": "लाभ",
                "loss": "हानि",
                "assets": "संपत्ति",
                "liabilities": "देनदारियाँ",
                "health_score": "स्वास्थ्य स्कोर",
                "credit_score": "क्रेडिट स्कोर",
                "risk_level": "जोखिम स्तर",
                "recommendations": "सिफारिशें",
                "export": "निर्यात",
                "download": "डाउनलोड"
            },
            "te": {
                "dashboard": "డాష్‌బోర్డ్",
                "upload": "అప్‌లోడ్",
                "analysis": "విశ్లేషణ",
                "insights": "అంతర్దృష్టులు",
                "reports": "నివేదికలు",
                "forecast": "అంచనా",
                "settings": "సెట్టింగ్‌లు",
                "revenue": "ఆదాయం",
                "expenses": "ఖర్చులు",
                "profit": "లాభం",
                "loss": "నష్టం",
                "assets": "ఆస్తులు",
                "liabilities": "బాధ్యతలు",
                "health_score": "ఆరోగ్య స్కోరు",
                "credit_score": "క్రెడిట్ స్కోరు",
                "risk_level": "రిస్క్ స్థాయి",
                "recommendations": "సిఫార్సులు",
                "export": "ఎగుమతి",
                "download": "డౌన్‌లోడ్"
            },
            "ta": {
                "dashboard": "டாஷ்போர்டு",
                "upload": "பதிவேற்றம்",
                "analysis": "பகுப்பாய்வு",
                "insights": "நுண்ணறிவுகள்",
                "reports": "அறிக்கைகள்",
                "forecast": "முன்னறிவிப்பு",
                "settings": "அமைப்புகள்",
                "revenue": "வருவாய்",
                "expenses": "செலவுகள்",
                "profit": "லாபம்",
                "loss": "இழப்பு",
                "assets": "சொத்துக்கள்",
                "liabilities": "பொறுப்புகள்",
                "health_score": "ஆரோக்கிய மதிப்பெண்",
                "credit_score": "கடன் மதிப்பெண்",
                "risk_level": "இடர் நிலை",
                "recommendations": "பரிந்துரைகள்",
                "export": "ஏற்றுமதி",
                "download": "பதிவிறக்கம்"
            },
            "kn": {
                "dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
                "upload": "ಅಪ್‌ಲೋಡ್",
                "analysis": "ವಿಶ್ಲೇಷಣೆ",
                "insights": "ಒಳನೋಟಗಳು",
                "reports": "ವರದಿಗಳು",
                "forecast": "ಮುನ್ಸೂಚನೆ",
                "settings": "ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
                "revenue": "ಆದಾಯ",
                "expenses": "ವೆಚ್ಚಗಳು",
                "profit": "ಲಾಭ",
                "loss": "ನಷ್ಟ",
                "assets": "ಸ್ವತ್ತುಗಳು",
                "liabilities": "ಹೊಣೆಗಾರಿಕೆಗಳು",
                "health_score": "ಆರೋಗ್ಯ ಸ್ಕೋರ್",
                "credit_score": "ಕ್ರೆಡಿಟ್ ಸ್ಕೋರ್",
                "risk_level": "ಅಪಾಯ ಮಟ್ಟ",
                "recommendations": "ಶಿಫಾರಸುಗಳು",
                "export": "ರಫ್ತು",
                "download": "ಡೌನ್‌ಲೋಡ್"
            },
            "mr": {
                "dashboard": "डॅशबोर्ड",
                "upload": "अपलोड",
                "analysis": "विश्लेषण",
                "insights": "अंतर्दृष्टी",
                "reports": "अहवाल",
                "forecast": "अंदाज",
                "settings": "सेटिंग्ज",
                "revenue": "महसूल",
                "expenses": "खर्च",
                "profit": "नफा",
                "loss": "तोटा",
                "assets": "मालमत्ता",
                "liabilities": "दायित्वे",
                "health_score": "आरोग्य स्कोअर",
                "credit_score": "क्रेडिट स्कोअर",
                "risk_level": "जोखीम पातळी",
                "recommendations": "शिफारसी",
                "export": "निर्यात",
                "download": "डाउनलोड"
            },
            "gu": {
                "dashboard": "ડેશબોર્ડ",
                "upload": "અપલોડ",
                "analysis": "વિશ્લેષણ",
                "insights": "આંતરદૃષ્ટિ",
                "reports": "અહેવાલો",
                "forecast": "પૂર્વાનુમાન",
                "settings": "સેટિંગ્સ",
                "revenue": "આવક",
                "expenses": "ખર્ચ",
                "profit": "નફો",
                "loss": "નુકસાન",
                "assets": "સંપત્તિ",
                "liabilities": "જવાબદારીઓ",
                "health_score": "આરોગ્ય સ્કોર",
                "credit_score": "ક્રેડિટ સ્કોર",
                "risk_level": "જોખમ સ્તર",
                "recommendations": "ભલામણો",
                "export": "નિકાસ",
                "download": "ડાઉનલોડ"
            },
            "bn": {
                "dashboard": "ড্যাশবোর্ড",
                "upload": "আপলোড",
                "analysis": "বিশ্লেষণ",
                "insights": "অন্তর্দৃষ্টি",
                "reports": "প্রতিবেদন",
                "forecast": "পূর্বাভাস",
                "settings": "সেটিংস",
                "revenue": "রাজস্ব",
                "expenses": "ব্যয়",
                "profit": "লাভ",
                "loss": "ক্ষতি",
                "assets": "সম্পদ",
                "liabilities": "দায়",
                "health_score": "স্বাস্থ্য স্কোর",
                "credit_score": "ক্রেডিট স্কোর",
                "risk_level": "ঝুঁকির স্তর",
                "recommendations": "সুপারিশ",
                "export": "রপ্তানি",
                "download": "ডাউনলোড"
            }
        }
    
    async def translate(self, text: str, target_language: str, use_llm: bool = False) -> Dict[str, Any]:
        """Translate text to target language"""
        try:
            # Return original if English or unsupported language
            if target_language == "en" or target_language not in self.supported_languages:
                return {
                    "success": True,
                    "translated_text": text,
                    "source_language": "en",
                    "target_language": target_language
                }
            
            # Check static translations first
            if not use_llm:
                static_translation = self._get_static_translation(text, target_language)
                if static_translation:
                    return {
                        "success": True,
                        "translated_text": static_translation,
                        "source_language": "en",
                        "target_language": target_language,
                        "method": "static"
                    }
            
            # Use LLM for dynamic content
            result = await llm_service.translate_content(text, target_language)
            
            if result.get("success"):
                return {
                    "success": True,
                    "translated_text": result.get("content", text),
                    "source_language": "en",
                    "target_language": target_language,
                    "method": "llm"
                }
            else:
                # Fallback to original text
                return {
                    "success": True,
                    "translated_text": text,
                    "source_language": "en",
                    "target_language": target_language,
                    "method": "fallback",
                    "error": result.get("error")
                }
                
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "translated_text": text  # Return original on error
            }
    
    def _get_static_translation(self, text: str, target_language: str) -> Optional[str]:
        """Get static translation if available"""
        text_lower = text.lower().strip()
        
        if target_language in self.static_translations:
            translations = self.static_translations[target_language]
            
            # Direct match
            if text_lower in translations:
                return translations[text_lower]
            
            # Check English to target
            en_translations = self.static_translations.get("en", {})
            for en_key, en_value in en_translations.items():
                if en_value.lower() == text_lower:
                    return translations.get(en_key)
        
        return None
    
    async def translate_report(self, report_data: Dict[str, Any], target_language: str) -> Dict[str, Any]:
        """Translate entire report to target language"""
        try:
            if target_language == "en":
                return {
                    "success": True,
                    "translated_report": report_data
                }
            
            translated_report = report_data.copy()
            
            # Translate specific fields
            fields_to_translate = [
                "title", "summary", "executive_summary",
                "recommendations", "insights", "analysis"
            ]
            
            for field in fields_to_translate:
                if field in report_data and isinstance(report_data[field], str):
                    result = await self.translate(report_data[field], target_language, use_llm=True)
                    if result.get("success"):
                        translated_report[field] = result.get("translated_text")
            
            # Translate list fields
            if "recommendations" in report_data and isinstance(report_data["recommendations"], list):
                translated_recommendations = []
                for rec in report_data["recommendations"]:
                    if isinstance(rec, str):
                        result = await self.translate(rec, target_language, use_llm=True)
                        translated_recommendations.append(result.get("translated_text", rec))
                    else:
                        translated_recommendations.append(rec)
                translated_report["recommendations"] = translated_recommendations
            
            return {
                "success": True,
                "translated_report": translated_report,
                "target_language": target_language
            }
            
        except Exception as e:
            logger.error(f"Report translation error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "translated_report": report_data
            }
    
    def get_language_name(self, language_code: str) -> str:
        """Get language name from code"""
        language_names = {
            "en": "English",
            "hi": "हिन्दी (Hindi)",
            "te": "తెలుగు (Telugu)",
            "ta": "தமிழ் (Tamil)",
            "kn": "ಕನ್ನಡ (Kannada)",
            "mr": "मराठी (Marathi)",
            "gu": "ગુજરાતી (Gujarati)",
            "bn": "বাংলা (Bengali)"
        }
        return language_names.get(language_code, language_code)
    
    def get_available_languages(self) -> List[Dict[str, str]]:
        """Get list of available languages"""
        return [
            {"code": code, "name": self.get_language_name(code)}
            for code in self.supported_languages
        ]

# Singleton instance
translation_service = TranslationService()
