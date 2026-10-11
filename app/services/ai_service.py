import sys
from groq import (
    Groq,
    APIConnectionError,
    AuthenticationError,
    RateLimitError,
    GroqError,
)
from config import Config

class AIServiceError(Exception):
    """Yapay zeka servisi için özel hata sınıfı"""
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.status_code = status_code

class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = Config.GROQ_MODEL
        self.client = None

        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"Groq istemcisi başlatılamadı: {e}")
        else:
            print("Uyarı: GROQ_API_KEY tanımlanmamış, demo modu devrede.")

    def yanit_uret(self, soru: str) -> str:
        """Kullanıcı sorusunu alır ve Groq API üzerinden yanıt döndürür."""
        if not self.client:
            return "Air Asistanı Demo Modu: API anahtarı girilmediği için test yanıtı üretildi."

        try:
            cevap = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": Config.BUSINESS_CONTEXT},
                    {"role": "user", "content": soru},
                ],
            )
            return cevap.choices[0].message.content

        except AuthenticationError:
            raise AIServiceError("Geçersiz API anahtarı.", 401)
        except RateLimitError:
            raise AIServiceError("İstek limiti aşıldı. Lütfen daha sonra tekrar deneyin.", 429)
        except APIConnectionError:
            raise AIServiceError("Groq sunucusuna bağlanılamadı.", 503)
        except GroqError as e:
            raise AIServiceError(f"Groq API hatası: {str(e)}", 500)
        except Exception as e:
            raise AIServiceError(f"Beklenmeyen AI hatası: {str(e)}", 500)

# Tekil servis örneği
ai_service = AIService()