# Proje Mimarisi ve Klasör Yapısı (SmartLead AI)

Bu proje, ölçeklenebilir, test edilebilir ve bakımı kolay bir yazılım geliştirmek amacıyla **"Separation of Concerns" (Sorumlulukların Ayrılığı)** ilkesine uygun katmanlı bir mimariyle inşa edilmiştir.

---

## Dizin Ağacı

```text
smartlead_ai/
│
├── run.py                     # Uygulama giriş noktası (Entrypoint)
├── config.py                  # Çevre değişkenleri ve merkezi yapılandırma
├── requirements.txt           # Python bağımlılıkları ve kütüphaneler
├── .env                       # Hassas API anahtarları (Git'e eklenmez)
├── .gitignore                 # Versiyon kontrolü dışı bırakılan dosyalar
│
└── app/
    ├── __init__.py            # Application Factory (Flask başlatıcı ve CORS)
    ├── routes.py              # HTTP rotaları, istek karşılama ve uç noktalar
    ├── database.py            # Veri erişim katmanı (SQLite işlemleri - İleri faz)
    │
    ├── services/
    │   ├── __init__.py
    │   └── ai_service.py      # LLM / Groq API entegrasyonu ve iş mantığı
    │
    └── templates/
        └── index.html         # Web arayüzü ve Render test karşılama sayfası
```
## Katmanlar ve Dosya Sorumlulukları
| Katman / Dosya | Rolü / Sorumluluğu | Önemi |
|---|---|---|
| config.py | Yapılandırma Katmanı.env dosyasındaki çevre değişkenlerini, model parametrelerini ve sistem talimatını (BUSINESS_CONTEXT) okur. | Kodun içine sabit (hardcoded) anahtar ve ayar yazılmasını engeller; ortamlar arası (dev/prod) geçişi kolaylaştırır. |
| app/services/ai_service.py | Servis Katmanı (İş Mantığı)Groq API istemcisini yönetir, prompt'u kullanıcı mesajıyla birleştirir ve model yanıtını döndürür. | Flask ve HTTP katmanından tamamen bağımsızdır. İleride yapay zekâ sağlayıcısı (Groq, OpenAI, Gemini) değiştiğinde sadece bu servis güncellenir. |
| app/database.py | Veri Katmanı (Data Access)SQLite veritabanı bağlantısını ve müşteri adayı (leads) kayıt sorgularını yönetir. | SQL sorgularını rota fonksiyonlarından izole eder, SQL Injection riskini önler ve veri tabanı bağımlılığını tek merkezde toplar. |
| app/routes.py | Kontrolcü (Controller / Routing)Gelen HTTP isteklerini karşılar, JSON verisini doğrular, ilgili servisi çağırır ve HTTP yanıtı üretir. | "Trafik polisi" görevi görür; doğrudan veritabanı veya yapay zekâ algoritması çalıştırmaz, yalnızca yönlendirme yapar. |
| app/`__init__.py `| Uygulama Fabrikası (App Factory)create_app() fonksiyonu ile Flask örneğini oluşturur, CORS politikalarını ve Blueprint rotalarını sisteme bağlar. | Global değişken kirliliğini önler, test yazmayı kolaylaştırır ve döngüsel içe aktarma (circular import) hatalarını engeller. |
| app/templates/index.html | Sunum Katmanı (Presentation)Render üzerinde canlı yayında sistemin çalıştığını gösteren ve API ile haberleşen hafif web arayüzü. | Tarayıcı üzerinden görsel ve işlevsel bir test ortamı sunar. |
| run.py | Çalıştırma NoktasıUygulamayı yerel ortamda veya Render sunucusunda (gunicorn run:app) ayağa kaldıran dosyadır. | Sunucu çalıştırma mantığı ile uygulama çatısını birbirinden ayırır. |

## İstek ve Yanıt Akışı (Request Lifecycle)
Bir kullanıcı sisteme soru sorduğunda veri akışı şu sırayı takip eder:
```[Kullanıcı / Web Arayüzü]
           │
           ▼ (HTTP POST /api/sohbet)
   [app/routes.py]  ─────────► Girdiyi doğrular (Boş mu? JSON formatında mı?)
           │
           ▼
[app/services/ai_service.py] ──► Config'den sistem promptunu alır, Groq API'ye iletir
           │
           ▼
     [Groq LLM]     ─────────► Cevabı üretir
           │
           ▼
   [app/routes.py]  ─────────► Cevabı JSON formatına dönüştürür (HTTP 200)
           │
           ▼
[Kullanıcı / Web Arayüzü]
```
## Neden Bu Mimari Seçildi?
Tek Sorumluluk İlkesi (Single Responsibility): Her modül yalnızca tek bir işi en iyi şekilde yapar.

Güvenlik: API anahtarları .env ve .gitignore ile kaynak koddan ayrılmıştır.

Sürdürülebilirlik: Spagetti kod yapısından kaçınılarak projenin ilerleyen teslimlerinde yeni özellikler (örneğin lead toplama, e-posta bildirimi) kolayca eklenebilir hale getirilmiştir.