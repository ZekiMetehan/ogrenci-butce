from fastapi.testclient import TestClient

import hesap
from app import app

istemci = TestClient(app)

# Aralık 2026: 23 iş günü, 31 gün


def test_is_gunu_sayisi():
    assert hesap.is_gunu_sayisi(2026, 12) == 23
    assert hesap.is_gunu_sayisi(2026, 2) == 20


def test_kesin_giderler():
    k = hesap.kesin_giderler(2026, 12, ogun_ucreti=45, binis_ucreti=20, konaklama=1500)
    assert k["yemek"] == 23 * 45          # 1035
    assert k["ulasim"] == 23 * 2 * 20     # 920
    assert k["toplam"] == 1035 + 920 + 1500


def test_ekstra_siklik_turleri():
    assert hesap.ekstra_tutari(120, "her_okul_gunu", 1, is_gunu=23) == 23 * 120  # ikinci öğün
    assert hesap.ekstra_tutari(20, "ayda_x_kez", 6, is_gunu=23) == 120           # AVM yolculuğu
    assert hesap.ekstra_tutari(300, "ayda_bir", 1, is_gunu=23) == 300            # telefon faturası


def test_butce_ekstralarla():
    s = hesap.aylik_butce(
        2026, 12, gelen_para=8000, ogun_ucreti=45, binis_ucreti=20, konaklama=1500,
        ekstralar=[
            {"ad": "İkinci öğün", "tutar": 120, "siklik": "her_okul_gunu"},
            {"ad": "AVM yolculuğu", "tutar": 20, "siklik": "ayda_x_kez", "adet": 6},
            {"ad": "Telefon faturası", "tutar": 300, "siklik": "ayda_bir"},
        ],
    )
    assert s["ekstra_toplam"] == 2760 + 120 + 300
    assert s["toplam_gider"] == 3455 + 3180
    assert s["kalan"] == 8000 - 6635
    assert s["gunluk_harcanabilir"] == round(1365 / 31, 2)
    assert s["yetiyor_mu"] is True


def test_para_yetmezse():
    s = hesap.aylik_butce(2026, 12, gelen_para=1000, ogun_ucreti=45, binis_ucreti=20)
    assert s["yetiyor_mu"] is False
    assert s["gunluk_harcanabilir"] == 0


def test_butce_api():
    cevap = istemci.post("/api/butce", json={
        "yil": 2026, "ay": 12, "gelen_para": 6000, "ogun_ucreti": 45, "binis_ucreti": 20,
        "konaklama": 1500,
        "ekstralar": [{"ad": "Telefon", "tutar": 300, "siklik": "ayda_bir"}],
    })
    assert cevap.status_code == 200
    assert cevap.json()["toplam_gider"] == 3455 + 300


def test_butce_api_hatali_siklik():
    cevap = istemci.post("/api/butce", json={
        "yil": 2026, "ay": 12, "gelen_para": 6000, "ogun_ucreti": 45, "binis_ucreti": 20,
        "ekstralar": [{"ad": "X", "tutar": 10, "siklik": "haftada_bir"}],
    })
    assert cevap.status_code == 422
