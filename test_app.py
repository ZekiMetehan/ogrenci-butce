from fastapi.testclient import TestClient

import app as uygulama
import hesap
from app import app

istemci = TestClient(app)

# Aralık 2026: 23 iş günü, 31 gün


def test_is_gunu_sayisi():
    assert hesap.is_gunu_sayisi(2026, 12) == 23
    assert hesap.is_gunu_sayisi(2026, 2) == 20


def test_hafta_icine_denk_gelen_resmi_tatil_dusulur():
    # 29 Ekim 2026 Perşembe: Ekim'de 22 hafta içi gün var, tatil düşülünce 21
    assert hesap.is_gunu_sayisi(2026, 10) == 21


def test_hafta_sonuna_denk_gelen_resmi_tatil_bir_sey_degistirmez():
    # 23 Nisan 2028 Pazar: zaten hafta sonu, Nisan 2028'de 20 hafta içi gün var
    assert hesap.is_gunu_sayisi(2028, 4) == 20


def test_mayista_iki_resmi_tatil():
    # Mayıs 2026: 21 hafta içi gün; 1 Mayıs Cuma ve 19 Mayıs Salı düşülünce 19
    assert hesap.is_gunu_sayisi(2026, 5) == 19


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


def test_takvim_gun_turleri():
    gunler = hesap.ay_takvimi(2026, 10)
    assert len(gunler) == 31
    gun29 = gunler[28]
    assert gun29["tur"] == "tatil" and gun29["tatil_adi"] == "Cumhuriyet Bayramı"
    assert gunler[2]["tur"] == "hafta_sonu"      # 3 Ekim 2026 Cumartesi
    assert gunler[0]["tur"] == "okul"            # 1 Ekim 2026 Perşembe
    okul_gunleri = sum(1 for g in gunler if g["tur"] == "okul")
    assert okul_gunleri == hesap.is_gunu_sayisi(2026, 10)


def test_takvim_api():
    cevap = istemci.get("/api/takvim", params={"yil": 2026, "ay": 12})
    assert cevap.status_code == 200
    assert len(cevap.json()) == 31
    assert istemci.get("/api/takvim", params={"yil": 2026, "ay": 13}).status_code == 422


def _bos_arsiv(tmp_path):
    uygulama.ARSIV_DOSYASI = tmp_path / "arsiv.json"


def test_arsive_kaydet_ve_listele(tmp_path):
    _bos_arsiv(tmp_path)
    istemci.post("/api/arsiv", json={"donem": "2026-11", "gelen_para": 6000, "toplam_gider": 5000, "kalan": 1000, "gunluk_harcanabilir": 33.33})
    istemci.post("/api/arsiv", json={"donem": "2026-12", "gelen_para": 6000, "toplam_gider": 5135, "kalan": 865, "gunluk_harcanabilir": 27.9})
    liste = istemci.get("/api/arsiv").json()
    assert [k["donem"] for k in liste] == ["2026-12", "2026-11"]  # en yeni üstte


def test_ayni_ay_tekrar_kaydedilirse_guncellenir(tmp_path):
    _bos_arsiv(tmp_path)
    istemci.post("/api/arsiv", json={"donem": "2026-12", "gelen_para": 6000, "toplam_gider": 5000, "kalan": 1000, "gunluk_harcanabilir": 32.26})
    istemci.post("/api/arsiv", json={"donem": "2026-12", "gelen_para": 7000, "toplam_gider": 5000, "kalan": 2000, "gunluk_harcanabilir": 64.52})
    liste = istemci.get("/api/arsiv").json()
    assert len(liste) == 1 and liste[0]["kalan"] == 2000


def test_arsivden_sil(tmp_path):
    _bos_arsiv(tmp_path)
    istemci.post("/api/arsiv", json={"donem": "2026-12", "gelen_para": 6000, "toplam_gider": 5000, "kalan": 1000, "gunluk_harcanabilir": 32.26})
    assert istemci.delete("/api/arsiv/2026-12").status_code == 200
    assert istemci.get("/api/arsiv").json() == []
    assert istemci.delete("/api/arsiv/2026-12").status_code == 404


def test_hatali_donem_reddedilir(tmp_path):
    _bos_arsiv(tmp_path)
    cevap = istemci.post("/api/arsiv", json={"donem": "2026-13", "gelen_para": 0, "toplam_gider": 0, "kalan": 0, "gunluk_harcanabilir": 0})
    assert cevap.status_code == 422
