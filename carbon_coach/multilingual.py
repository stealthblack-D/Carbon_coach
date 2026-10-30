"""
multilingual.py - Multilingual support for Carbon Coach (Telugu, Hindi, English).
Provides language detection, keyword recognition, and localized prompt framing.
"""

from typing import Dict, Any, Tuple
import re

# Language codes
LANG_EN = "en"
LANG_TE = "te"  # Telugu
LANG_HI = "hi"  # Hindi

# Unicode ranges
TELUGU_RANGE = (0x0C00, 0x0C7F)
DEVANAGARI_HINDI_RANGE = (0x0900, 0x097F)

def detect_language(text: str) -> str:
    """Detects whether text is primarily Telugu, Hindi, or English."""
    telugu_count = 0
    hindi_count = 0
    for ch in text:
        cp = ord(ch)
        if TELUGU_RANGE[0] <= cp <= TELUGU_RANGE[1]:
            telugu_count += 1
        elif DEVANAGARI_HINDI_RANGE[0] <= cp <= DEVANAGARI_HINDI_RANGE[1]:
            hindi_count += 1

    if telugu_count > 2:
        return LANG_TE
    if hindi_count > 2:
        return LANG_HI
    return LANG_EN


# Localized terminology & prompts for system instructions
MULTILINGUAL_INSTRUCTIONS = {
    LANG_EN: {
        "greeting": "Hello! I am your Carbon Coach. Tell me what you did today (e.g. 'I travelled 12 km by bus and ran the AC for 4 hours') and I will calculate your carbon footprint!",
        "system_rule": "Respond in English. Every emission number must be taken from tool execution.",
        "units": "kg CO₂e",
    },
    LANG_TE: {
        "greeting": "నమస్కారం! నేను మీ కార్బన్ కోచ్ (Carbon Coach). మీరు ఈరోజు చేసిన పనులను నాకు చెప్పండి (ఉదాహరణకు: 'నేను 12 కిమీ బస్సులో ప్రయాణించాను మరియు 4 గంటలు ఏసీ వాడాను'), మీ కార్బన్ ఉద్గారాలను నేను లెక్కిస్తాను!",
        "system_rule": "యూజర్ తెలుగులో అడిగితే తప్పనిసరిగా స్పష్టమైన, సరళమైన తెలుగులో సమాధానం ఇవ్వండి. గణాంకాలు టూల్స్ ద్వారా మాత్రమే రావాలి (నో మేడ్-అప్ నంబర్స్). kg CO₂e ఉద్గారాలు, ఆదా చేసే చిట్కాలను తెలుగులో వివరించండి.",
        "units": "కిలోల CO₂e (kg CO₂e)",
    },
    LANG_HI: {
        "greeting": "नमस्ते! मैं आपका कार्बन कोच (Carbon Coach) हूँ। मुझे बताइए कि आपने आज क्या किया (जैसे: 'मैंने 12 किमी बस से यात्रा की और 4 घंटे एसी चलाया'), मैं आपके कार्बन उत्सर्जन की सटीक गणना करूँगा!",
        "system_rule": "उपयोगकर्ता अगर हिंदी में बात करे तो स्पष्ट और सहज हिंदी में उत्तर दें। सभी आंकड़े टूल्स से ही प्राप्त करें। kg CO₂e उत्सर्जन और बचत के सुझाव हिंदी में समझाएं।",
        "units": "किलोग्राम CO₂e (kg CO₂e)",
    }
}

# Common transliterated / native keywords for intent parsing
KEYWORD_MAPPINGS = {
    # Transport
    "bus": ["bus", "RTC", "బస్సు", "बस"],
    "train": ["train", "railway", "రైలు", "ट्रेन", "रेल"],
    "metro": ["metro", "మెట్రో", "मेट्रो"],
    "car": ["car", "కారు", "कार", "गाड़ी"],
    "bike": ["bike", "motorcycle", "scooter", "బైక్", "మోటార్ సైకిల్", "बाइक", "स्कूटर"],
    "auto": ["auto", "rickshaw", "ఆటో", "ऑटो", "रिक्शा"],
    "walk": ["walk", "walking", "నడక", "पैदल"],
    "cycle": ["cycle", "bicycle", "సైకిల్", "साइकिल"],
    
    # Electricity / Appliances
    "ac": ["ac", "air conditioner", "ఏసీ", "ఎయిర్ కండీషనర్", "एसी"],
    "fan": ["fan", "ఫ్యాన్", "పంఖా", "पंखा"],
    "light": ["light", "led", "bulb", "లైట్", "బల్బ్", "बल्ब", "लाइट"],
    "laptop": ["laptop", "computer", "ల్యాప్‌టాప్", "लैपटॉप"],
    "geyser": ["geyser", "water heater", "గీజర్", "गीज़र"],
    
    # Food
    "vegetarian": ["veg", "vegetarian", "thali", "శాకాహారం", "కూరగాయలు", "शाकाहारी", "सब्जी"],
    "vegan": ["vegan", "వీగన్", "वीगन"],
    "chicken": ["chicken", "నాన్ వెజ్", "చికెన్", "चिकन", "मांसाहारी"],
    "mutton": ["mutton", "lamb", "beef", "మటన్", "मटन"]
}
