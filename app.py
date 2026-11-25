"""Öğrenci Bütçe: öğrencinin aylık yemek ve ulaşım masrafını hesaplayan web uygulaması."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

import hesap

KLASOR = Path(__file__).parent
app = FastAPI(title="Öğrenci Bütçe")


class YemekIstegi(BaseModel):
    yil: int = Field(ge=2000, le=2100)
    ay: int = Field(ge=1, le=12)
    ogun_ucreti: float = Field(ge=0)
    gunluk_ogun: int = Field(ge=0, le=5)


@app.get("/")
def anasayfa():
    return FileResponse(KLASOR / "static" / "index.html")


@app.post("/api/yemek")
def yemek(istek: YemekIstegi):
    return hesap.yemek_hesapla(istek.yil, istek.ay, istek.ogun_ucreti, istek.gunluk_ogun)
