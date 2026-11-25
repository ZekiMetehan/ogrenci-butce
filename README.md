# 💸 Öğrenci Bütçe

## Hangi problemi çözüyor, kimin için?

Üniversite öğrencisinin her ay eline belli bir para geçiyor (burs, KYK, harçlık). Bu paranın büyük kısmı zorunlu giderlere gidiyor: **okul yemek kartı**, **otobüs**, **yurt ücreti ya da ev kirası** ve **telefon faturası**. Ama ay başında "yemek kartına ne kadar yüklemeliyim, otobüse ne kadar gidecek, geriye ne kalacak, günde ne kadar harcayabilirim?" sorusunun cevabı belli değil. Çünkü her ayın iş günü sayısı farklı ve otobüste aktarma süresi içinde binince ücret alınmayabiliyor.

**Öğrenci Bütçe**, öğrencinin giderlerini ikiye ayırır:

- **Kesin giderler** (her öğrencide olan): her okul günü 1 öğün yemek, okula gidiş-dönüş (2 biniş) ve yurt ücreti ya da ev kirası. Uygulama ayın okul günlerini kendisi sayar: hafta sonlarını ve sabit tarihli resmi tatilleri (23 Nisan, 1 Mayıs, 19 Mayıs, 15 Temmuz, 30 Ağustos, 29 Ekim, 1 Ocak) düşer.
- **Ekstralar** (öğrencinin kendisi eklediği): ikinci öğün, aktarma, AVM/çarşı yolculuğu, telefon faturası ya da kendi yazdığı herhangi bir gider. Her ekstra için tutar ve sıklık ("her okul günü", "ayda X kez", "ayda bir") seçilir.

Sonunda gelen paradan bütün giderler düşülür; **geriye kalan para** ve ay sonuna kadar **günde ne kadar harcanabileceği** gösterilir.

## Pano

Proje panosu: https://github.com/users/ZekiMetehan/projects/1

| Kart | Durum |
|---|---|
| #1 Proje iskeleti ve README | Tamamlandı |
| #2 Yemek kartı hesabı | Tamamlandı |
| #3 Ulaşım hesabı ve aylık özet | Tamamlandı |
| #4 Otomatik testler (GitHub Actions) | Tamamlandı |
| #5 Resmi tatilleri iş günlerinden düşme | Tamamlandı (PR ile) |
| #6 Kesin giderler ve kullanıcının eklediği ekstralar | Tamamlandı |

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

### Özellik 1: Kesin giderler (#2, #3, #6)
1. "Hangi ay?" kısmından **Aralık 2026**'yı seç, gelen paraya `6000` yaz.
2. Kesin giderlerde öğün ücreti `45`, otobüs biniş ücreti `20`, yurt/ev kirası `1500` olsun. Ekstra ekleme.
3. **Hesapla**'ya bas.
4. **Beklenen:**
   - "Bu ay **23 okul günü** var."
   - Yemek (23 öğün) **1.035,00 TL**, okul ulaşımı (46 biniş) **920,00 TL**, yurt/ev **1.500,00 TL**
   - Kesin giderler **3.455,00 TL**, geriye kalan **2.545,00 TL** (yeşil), "günde **82,10 TL** harcayabilirsin (31 gün)"
5. Gelen parayı `1000` yaparsan kalan eksiye düşer, kırmızı görünür ve "Gelen para giderlere yetmiyor" uyarısı çıkar.

### Özellik 2: Ekstralar (#6)
1. Yukarıdaki değerlerle, gelen parayı `8000` yap.
2. Ekstralar kısmında hazır düğmelerden **+ İkinci öğün** (120 TL, her okul günü), **+ AVM / çarşı yolculuğu** (20 TL, sayıyı `6` yap) ve **+ Telefon faturası** (300 TL, ayda bir) düğmelerine bas.
3. **+ Kendi ekstranı ekle** ile `Spor salonu`, `500` TL, "Ayda bir" ekle.
4. **Hesapla**'ya bas.
5. **Beklenen:**
   - İkinci öğün **2.760,00 TL** (23 × 120), AVM **120,00 TL** (6 × 20), telefon **300,00 TL**, spor salonu **500,00 TL**
   - Ekstralar **3.680,00 TL**, toplam gider **7.135,00 TL**
   - Geriye kalan **865,00 TL**, "günde **27,90 TL** harcayabilirsin"
6. Bir ekstranın yanındaki **✕** ile silip tekrar hesaplarsan toplam güncellenir.

### Resmi tatiller (#5)
- Ayı **Ekim 2026** yapıp **Hesapla**'ya bas. 29 Ekim Perşembe'ye denk geldiği için "Bu ay **21 okul günü** var" yazar (22 hafta içi gün − 1 tatil).
- Dini bayramlar her yıl değiştiği için şimdilik hesaba katılmıyor.

## Kullanılan teknolojiler

- **Backend:** Python, FastAPI
- **Frontend:** HTML, JavaScript
- **Test:** pytest, GitHub Actions
