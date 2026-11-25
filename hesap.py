"""Öğrenci aylık bütçe hesapları.

Bütçe iki parçadan oluşur:
- Kesin giderler: her öğrencide olan giderler (günde 1 öğün yemek, okul gidiş-dönüş, yurt/kira)
- Ekstralar: kullanıcının kendisi eklediği giderler (ikinci öğün, aktarma, AVM yolculuğu, fatura...)
"""
import calendar

# Bir ekstranın ne sıklıkla olduğu
HER_OKUL_GUNU = "her_okul_gunu"   # tutar × iş günü
AYDA_X_KEZ = "ayda_x_kez"         # tutar × adet
AYDA_BIR = "ayda_bir"             # tutar (sabit)
SIKLIKLAR = (HER_OKUL_GUNU, AYDA_X_KEZ, AYDA_BIR)


# Her yıl aynı tarihe gelen resmi tatiller: (ay, gün) -> adı.
# Dini bayramlar her yıl değiştiği için bu listede yok.
SABIT_RESMI_TATILLER = {
    (1, 1): "Yılbaşı",
    (4, 23): "Ulusal Egemenlik ve Çocuk Bayramı",
    (5, 1): "Emek ve Dayanışma Günü",
    (5, 19): "Atatürk'ü Anma, Gençlik ve Spor Bayramı",
    (7, 15): "Demokrasi ve Milli Birlik Günü",
    (8, 30): "Zafer Bayramı",
    (10, 29): "Cumhuriyet Bayramı",
}


def resmi_tatil_mi(ay: int, gun: int) -> bool:
    return (ay, gun) in SABIT_RESMI_TATILLER


def ay_takvimi(yil: int, ay: int) -> list:
    """Ayın her günü için gün türünü döndürür: okul, hafta_sonu veya tatil."""
    _, gun_sayisi = calendar.monthrange(yil, ay)
    gunler = []
    for gun in range(1, gun_sayisi + 1):
        hafta_gunu = calendar.weekday(yil, ay, gun)  # 0 = Pazartesi
        tatil_adi = SABIT_RESMI_TATILLER.get((ay, gun))
        if hafta_gunu >= 5:
            tur = "hafta_sonu"
        elif tatil_adi:
            tur = "tatil"
        else:
            tur = "okul"
        gunler.append({"gun": gun, "hafta_gunu": hafta_gunu, "tur": tur, "tatil_adi": tatil_adi})
    return gunler


def is_gunu_sayisi(yil: int, ay: int) -> int:
    """Verilen aydaki okul günü sayısı: hafta içi (Pazartesi-Cuma) ve resmi tatil olmayan günler."""
    _, gun_sayisi = calendar.monthrange(yil, ay)
    return sum(
        1
        for gun in range(1, gun_sayisi + 1)
        if calendar.weekday(yil, ay, gun) < 5 and not resmi_tatil_mi(ay, gun)
    )


def kesin_giderler(yil: int, ay: int, ogun_ucreti: float, binis_ucreti: float, konaklama: float = 0) -> dict:
    """Günde 1 öğün yemek, okula gidiş-dönüş (2 biniş) ve yurt/kira."""
    gun = is_gunu_sayisi(yil, ay)
    yemek = gun * ogun_ucreti
    ulasim = gun * 2 * binis_ucreti
    return {
        "is_gunu": gun,
        "yemek": round(yemek, 2),
        "ulasim": round(ulasim, 2),
        "konaklama": round(konaklama, 2),
        "toplam": round(yemek + ulasim + konaklama, 2),
    }


def ekstra_tutari(tutar: float, siklik: str, adet: int, is_gunu: int) -> float:
    """Bir ekstranın aylık tutarını hesaplar."""
    if siklik == HER_OKUL_GUNU:
        return tutar * is_gunu
    if siklik == AYDA_X_KEZ:
        return tutar * adet
    if siklik == AYDA_BIR:
        return tutar
    raise ValueError(f"Bilinmeyen sıklık: {siklik}")


def aylik_butce(yil: int, ay: int, gelen_para: float, ogun_ucreti: float, binis_ucreti: float,
                konaklama: float = 0, ekstralar: list | None = None) -> dict:
    """Kesin giderler + ekstralar; kalan para ve günlük harcanabilir para."""
    kesin = kesin_giderler(yil, ay, ogun_ucreti, binis_ucreti, konaklama)
    ekstra_listesi = []
    for e in ekstralar or []:
        aylik = ekstra_tutari(e["tutar"], e["siklik"], e.get("adet", 1), kesin["is_gunu"])
        ekstra_listesi.append({"ad": e["ad"], "aylik": round(aylik, 2)})
    ekstra_toplam = sum(e["aylik"] for e in ekstra_listesi)
    toplam_gider = kesin["toplam"] + ekstra_toplam
    kalan = gelen_para - toplam_gider
    ayin_gunu = calendar.monthrange(yil, ay)[1]
    return {
        "kesin": kesin,
        "ekstralar": ekstra_listesi,
        "ekstra_toplam": round(ekstra_toplam, 2),
        "toplam_gider": round(toplam_gider, 2),
        "kalan": round(kalan, 2),
        "gun_sayisi": ayin_gunu,
        "gunluk_harcanabilir": round(max(kalan, 0) / ayin_gunu, 2),
        "yetiyor_mu": kalan >= 0,
    }
