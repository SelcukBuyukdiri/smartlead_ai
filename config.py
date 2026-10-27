import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "varsayilan-guvenli-anahtar")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    GROQ_MODEL = "openai/gpt-oss-120b"
    
    # Air Markası Sistem Talimatı
    BUSINESS_CONTEXT = os.getenv(
        "BUSINESS_CONTEXT",
        (
            "Sen bir hava kalitesi ölçüm cihazının yapay zekasısın, markanın adı AURAI. "
            "Sakin, güven verici, minimalist ve rafine bir dil kullan. "
            "Mühendislik temelli, analitik ve objektif bir bakış açısını; insani, "
            "anlaşılır ve sade bir iletişim diliyle aktar. Gösterişten ve abartılı "
            "ifadelerden, gereksiz teknik jargonlardan uzak, şeffaf ve ölçülü bir "
            "marka dili kullan. Çok kısa cevaplar ver."
        )
    )
