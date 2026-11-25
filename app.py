"""Öğrenci Bütçe: öğrencinin aylık kesin giderlerini ve ekstralarını hesaplayan web uygulaması."""
from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

import hesap

KLASOR = Path(__file__).parent
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
