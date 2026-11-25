# 💸 Öğrenci Bütçe

## Hangi problemi çözüyor, kimin için?

Üniversite öğrencisinin her ay eline belli bir para geçiyor (burs, KYK, harçlık). Bu paranın büyük kısmı zorunlu giderlere gidiyor: **okul yemek kartı**, **otobüs**, **yurt ücreti ya da ev kirası** ve **telefon faturası**. Ama ay başında "yemek kartına ne kadar yüklemeliyim, otobüse ne kadar gidecek, geriye ne kalacak, günde ne kadar harcayabilirim?" sorusunun cevabı belli değil. Çünkü her ayın iş günü sayısı farklı ve otobüste aktarma süresi içinde binince ücret alınmayabiliyor.

**Öğrenci Bütçe**, öğrencinin seçtiği aya göre:
- yemek kartına yüklemesi gereken parayı (iş günü × öğün × öğün ücreti),
- aylık otobüs parasını (yolculuk, aktarma ve biniş ücretine göre),
- gelen paradan yemek, ulaşım, yurt/kira ve telefon düşüldükten sonra **geriye kalan parayı**,
- ve ay sonuna kadar **günde ne kadar harcayabileceğini**

hesaplayan küçük bir web uygulamasıdır.

## Pano

Proje panosu: https://github.com/users/ZekiMetehan/projects/1

| Kart | Durum |
|---|---|
| #1 Proje iskeleti ve README | Tamamlandı |
| #2 Yemek kartı hesabı | Tamamlandı |
| #3 Ulaşım hesabı ve aylık özet (yurt/kira, telefon, günlük harcama) | Tamamlandı |
| #4 Otomatik testler (GitHub Actions) | Tamamlandı |
| #5 Resmi tatilleri iş günlerinden düşme | Yapılacak |

## Nasıl çalıştırılır?

Gerekenler: Python 3.10 veya üstü.

```bash
git clone https://github.com/ZekiMetehan/ogrenci-butce.git
cd ogrenci-butce
pip install -r requirements.txt
uvicorn app:app --reload
```

Tarayıcıda **http://127.0.0.1:8000** adresini aç.

Otomatik testleri çalıştırmak için:

```bash
pytest
```

## İki özellik nasıl denenir?

### Özellik 1: Yemek kartı hesabı (#2)
1. "Hangi ay?" kısmından **Aralık 2026**'yı seç.
2. Öğün ücretine `45`, günde kaç öğün kısmına `1` yaz ve **Hesapla**'ya bas.
3. **Beklenen:** "Bu ay **23 iş günü** var → 23 öğün" ve "Yemek kartına yüklemen gereken: **1.035,00 TL**" yazar.

### Özellik 2: Ulaşım hesabı ve aylık özet (#3)
1. Ay yine **Aralık 2026** olsun. Ulaşım kısmına şunları yaz: günde `2` yolculuk, bir yolculukta `2` biniş (aktarmalı), biniş ücreti `20`, aktarma ücreti `0` (aktarma ücretsiz). **Hesapla**'ya bas.
2. **Beklenen:** "46 yolculuk (46 aktarma)" ve "Aylık otobüs parası: **920,00 TL**" yazar. Aktarma ücretsiz olduğu için sadece ilk binişler ücretlendirilir.
3. Aylık özet kısmına gelen para `6000`, yurt/kira `1500`, telefon `300` yaz ve **Özeti göster**'e bas.
4. **Beklenen:** Toplam zorunlu gider **3.755,00 TL**, geriye kalan **2.245,00 TL** (yeşil) ve "Bu ay **günde 72,42 TL** harcayabilirsin (31 gün)." yazar.
5. Gelen parayı `1000` yaparsan kalan eksiye düşer, kırmızı görünür ve "Gelen para zorunlu giderlere yetmiyor" uyarısı çıkar.

## Kullanılan teknolojiler

- **Backend:** Python, FastAPI
- **Frontend:** HTML, JavaScript
- **Test:** pytest, GitHub Actions
