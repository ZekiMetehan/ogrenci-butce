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
