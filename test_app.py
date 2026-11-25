from fastapi.testclient import TestClient

import hesap
from app import app

istemci = TestClient(app)


def test_is_gunu_sayisi():
    assert hesap.is_gunu_sayisi(2026, 12) == 23  # Aralık 2026
    assert hesap.is_gunu_sayisi(2026, 2) == 20   # Şubat 2026


def test_yemek_hesabi():
    sonuc = hesap.yemek_hesapla(2026, 12, ogun_ucreti=45, gunluk_ogun=1)
    assert sonuc == {"is_gunu": 23, "toplam_ogun": 23, "toplam": 1035}


def test_yemek_api():
    cevap = istemci.post("/api/yemek", json={"yil": 2026, "ay": 12, "ogun_ucreti": 45, "gunluk_ogun": 2})
    assert cevap.status_code == 200
    assert cevap.json()["toplam"] == 2070


def test_yemek_api_hatali_ay():
    cevap = istemci.post("/api/yemek", json={"yil": 2026, "ay": 13, "ogun_ucreti": 40, "gunluk_ogun": 1})
    assert cevap.status_code == 422
