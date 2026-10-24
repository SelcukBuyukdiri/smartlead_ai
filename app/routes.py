from flask import Blueprint, render_template, request, jsonify
from app.services.ai_service import ai_service, AIServiceError
from app import database

main_bp = Blueprint("main", __name__)
api_bp = Blueprint("api", __name__, url_prefix="/api")

# --- Web Arayüzü & Mesaj Rotaları ---
@main_bp.route("/")
def index():
    # Render'da yayınlanacak örnek karşılama/mesaj HTML sayfası
    return render_template("index.html")

@main_bp.route("/health")
def health():
    return jsonify({
        "basari": True,
        "durum": "aktif",
        "mesaj": "SmartLead AI servisi calisiyor."
    }), 200

# --- API Uç Noktaları ---
@api_bp.route("/sohbet", methods=["POST"])
def sohbet():
    veri = request.get_json()
    if not veri:
        return jsonify({"basari": False, "hata": "JSON verisi gönderilmedi."}), 400

    soru = veri.get("soru")
    if not soru or not soru.strip():
        return jsonify({"basari": False, "hata": "Soru boş olamaz."}), 400

    try:
        cevap = ai_service.yanit_uret(soru.strip())
        return jsonify({
            "basari": True,
            "cevap": cevap
        }), 200
    except AIServiceError as e:
        return jsonify({"basari": False, "hata": str(e)}), e.status_code
    except Exception as e:
        return jsonify({"basari": False, "hata": f"Sunucu hatası: {str(e)}"}), 500

@api_bp.route("/leads", methods=["POST"])
def lead_kaydet():
    veri = request.get_json() or {}
    isim = veri.get("isim")
    telefon = veri.get("telefon")
    mesaj = veri.get("mesaj", "")

    if not isim or not telefon:
        return jsonify({"basari": False, "hata": "İsim ve telefon zorunludur."}), 400

    yeni_id = database.lead_ekle(isim, telefon, mesaj)
    return jsonify({"basari": True, "id": yeni_id, "mesaj": "Kayıt başarılı."}), 201

@api_bp.route("/leads", methods=["GET"])
def lead_listele():
    kayitlar = database.tum_leadler()
    return jsonify({"basari": True, "leads": kayitlar}), 200
