"""Öğrenci Bütçe: öğrencinin aylık kesin giderlerini ve ekstralarını hesaplayan web uygulaması."""
import json
import os
import re
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

import hesap

KLASOR = Path(__file__).parent
ARSIV_DOSYASI = Path(os.environ.get("ARSIV_DOSYASI", KLASOR / "arsiv.json"))
app = FastAPI(title="Öğrenci Bütçe")


class Ekstra(BaseModel):
    ad: str = Field(min_length=1, max_length=50)
    tutar: float = Field(ge=0)
    siklik: Literal["her_okul_gunu", "ayda_x_kez", "ayda_bir"]
    adet: int = Field(default=1, ge=0, le=500)


class ButceIstegi(BaseModel):
    yil: int = Field(ge=2000, le=2100)
    ay: int = Field(ge=1, le=12)
    gelen_para: float = Field(ge=0)
    ogun_ucreti: float = Field(ge=0)
    binis_ucreti: float = Field(ge=0)
    konaklama: float = Field(default=0, ge=0)
    ekstralar: list[Ekstra] = []


@app.get("/")
def anasayfa():
    return FileResponse(KLASOR / "static" / "index.html")


@app.post("/api/butce")
def butce(istek: ButceIstegi):
    veri = istek.model_dump()
    return hesap.aylik_butce(**veri)


@app.get("/api/takvim")
def takvim(yil: int = Query(ge=2000, le=2100), ay: int = Query(ge=1, le=12)):
    return hesap.ay_takvimi(yil, ay)


# ---------- Arşiv: hesaplanan ayları saklama ----------

class ArsivKaydi(BaseModel):
    donem: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")  # ör. 2026-12
    gelen_para: float = Field(ge=0)
    toplam_gider: float = Field(ge=0)
    kalan: float
    gunluk_harcanabilir: float = Field(ge=0)


def arsivi_oku() -> list:
    if not ARSIV_DOSYASI.exists():
        return []
    return json.loads(ARSIV_DOSYASI.read_text(encoding="utf-8"))


def arsive_yaz(kayitlar: list) -> None:
    ARSIV_DOSYASI.write_text(json.dumps(kayitlar, ensure_ascii=False, indent=2), encoding="utf-8")


@app.get("/api/arsiv")
def arsiv_listele():
    return sorted(arsivi_oku(), key=lambda k: k["donem"], reverse=True)  # en yeni ay en üstte


@app.post("/api/arsiv", status_code=201)
def arsive_kaydet(kayit: ArsivKaydi):
    kayitlar = [k for k in arsivi_oku() if k["donem"] != kayit.donem]  # aynı ay varsa üzerine yaz
    kayitlar.append(kayit.model_dump())
    arsive_yaz(kayitlar)
    return kayit


@app.delete("/api/arsiv/{donem}")
def arsivden_sil(donem: str):
    if not re.fullmatch(r"\d{4}-\d{2}", donem):
        raise HTTPException(status_code=400, detail="Dönem YYYY-AA biçiminde olmalı.")
    kayitlar = arsivi_oku()
    kalanlar = [k for k in kayitlar if k["donem"] != donem]
    if len(kalanlar) == len(kayitlar):
        raise HTTPException(status_code=404, detail="Bu ay arşivde yok.")
    arsive_yaz(kalanlar)
    return {"silindi": donem}
