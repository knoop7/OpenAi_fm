
DOMAIN = "openai_stt"

CONF_VOICE = "voice"
CONF_PROMPT = "prompt"

DEFAULT_VOICE = "alloy"
DEFAULT_LANG = "en"

DEFAULT_PROMPT = """Affect/personality: A cheerful guide 
Tone: Friendly, clear, and reassuring, creating a calm atmosphere and making the listener feel confident and comfortable.
Pronunciation: Clear, articulate, and steady, ensuring each instruction is easily understood while maintaining a natural, conversational flow.
Pause: Brief, purposeful pauses after key instructions (e.g., "cross the street" and "turn right") to allow time for the listener to process the information and follow along.
Emotion: Warm and supportive, conveying empathy and care, ensuring the listener feels guided and safe throughout the journey."""

STATE_READY = "就绪"
STATE_SPEAKING = "说话中"
STATE_ERROR = "失败"

SUPPORTED_VOICES = {
    "alloy": {"name": "Alloy", "lang": "en"},
    "shimmer": {"name": "Shimmer", "lang": "en"},
    "sage": {"name": "Sage", "lang": "en"},
    "nova": {"name": "Nova", "lang": "en"},
    "echo": {"name": "Echo", "lang": "en"},
    "fable": {"name": "Fable", "lang": "en"},
    "onyx": {"name": "Onyx", "lang": "en"},
    "coral": {"name": "Coral", "lang": "en"},
    "verse": {"name": "Verse", "lang": "en"},
    "ash": {"name": "Ash", "lang": "en"},
    "ballad": {"name": "Ballad", "lang": "en"},
}

SUPPORTED_LANGUAGES = ["en", "zh-CN", "zh-TW", "fr", "de", "it", "ja", "ko", "pt", "ru", "es"]