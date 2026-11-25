"""Öğrenci aylık bütçe hesapları."""
import calendar


def is_gunu_sayisi(yil: int, ay: int) -> int:
    """Verilen aydaki hafta içi (Pazartesi-Cuma) gün sayısını döndürür."""
    _, gun_sayisi = calendar.monthrange(yil, ay)
    return sum(1 for gun in range(1, gun_sayisi + 1) if calendar.weekday(yil, ay, gun) < 5)


def yemek_hesapla(yil: int, ay: int, ogun_ucreti: float, gunluk_ogun: int) -> dict:
    """Yemek kartına o ay yüklenmesi gereken parayı hesaplar."""
    gun = is_gunu_sayisi(yil, ay)
    return {
        "is_gunu": gun,
        "toplam_ogun": gun * gunluk_ogun,
        "toplam": round(gun * gunluk_ogun * ogun_ucreti, 2),
    }


def ulasim_hesapla(
    yil: int,
    ay: int,
    gunluk_yolculuk: int,
    yolculuk_basina_binis: int,
    binis_ucreti: float,
    aktarma_ucreti: float = 0,
) -> dict:
    """Aylık otobüs parasını hesaplar.

    Her yolculuğun ilk binişi tam ücret, sonraki binişler aktarma ücretidir.
    Aktarma süresi içinde binildiğinde ücret alınmıyorsa aktarma_ucreti = 0 girilir.
    """
    gun = is_gunu_sayisi(yil, ay)
    toplam_yolculuk = gun * gunluk_yolculuk
    toplam_aktarma = toplam_yolculuk * (yolculuk_basina_binis - 1)
    toplam = toplam_yolculuk * binis_ucreti + toplam_aktarma * aktarma_ucreti
    return {
        "is_gunu": gun,
        "gunluk_yolculuk": gunluk_yolculuk,
        "toplam_yolculuk": toplam_yolculuk,
        "toplam_aktarma": toplam_aktarma,
        "toplam": round(toplam, 2),
    }


def ozet_hesapla(yil: int, ay: int, gelen_para: float, yemek: float, ulasim: float,
                 konaklama: float = 0, telefon: float = 0) -> dict:
    """Gelen paradan zorunlu giderleri düşer, günlük harcanabilecek parayı bulur."""
    gider = yemek + ulasim + konaklama + telefon
    kalan = gelen_para - gider
    gun_sayisi = calendar.monthrange(yil, ay)[1]
    return {
        "toplam_gider": round(gider, 2),
        "kalan": round(kalan, 2),
        "gun_sayisi": gun_sayisi,
        "gunluk_harcanabilir": round(max(kalan, 0) / gun_sayisi, 2),
        "yetiyor_mu": kalan >= 0,
    }
