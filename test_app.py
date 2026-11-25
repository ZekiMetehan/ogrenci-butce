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


def test_aktarma_ucretsizse_sadece_ilk_binis_odenir():
    # Aralık 2026: 23 iş günü, günde 2 yolculuk, her yolculukta 1 aktarma (ücretsiz)
    sonuc = hesap.ulasim_hesapla(2026, 12, gunluk_yolculuk=2, yolculuk_basina_binis=2, binis_ucreti=20, aktarma_ucreti=0)
    assert sonuc["toplam_yolculuk"] == 46
    assert sonuc["toplam_aktarma"] == 46
    assert sonuc["toplam"] == 920


def test_aktarma_ucretliyse_eklenir():
    sonuc = hesap.ulasim_hesapla(2026, 12, gunluk_yolculuk=2, yolculuk_basina_binis=2, binis_ucreti=20, aktarma_ucreti=5)
    assert sonuc["toplam"] == 920 + 46 * 5


def test_ulasim_api():
    cevap = istemci.post("/api/ulasim", json={
        "yil": 2026, "ay": 12, "gunluk_yolculuk": 2,
        "yolculuk_basina_binis": 1, "binis_ucreti": 20,
    })
    assert cevap.status_code == 200
    assert cevap.json()["toplam"] == 920


def test_ozet_kalan_ve_gunluk_para():
    # Aralık 2026: 31 gün
    s = hesap.ozet_hesapla(2026, 12, gelen_para=6000, yemek=1035, ulasim=920, konaklama=1500, telefon=300)
    assert s["toplam_gider"] == 3755
    assert s["kalan"] == 2245
    assert s["gunluk_harcanabilir"] == round(2245 / 31, 2)
    assert s["yetiyor_mu"] is True


def test_para_yetmezse_uyari():
    s = hesap.ozet_hesapla(2026, 12, gelen_para=1000, yemek=1035, ulasim=920)
    assert s["yetiyor_mu"] is False
    assert s["gunluk_harcanabilir"] == 0
