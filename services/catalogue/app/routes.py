from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.db import SessionLocal
from app.models import Medicament
from app.schemas import MedicamentCreate, MedicamentRead

router = APIRouter(prefix="/medicaments", tags=["medicaments"])


@router.get("", response_model=list[MedicamentRead])
async def lister():
    async with SessionLocal() as session:
        result = await session.execute(select(Medicament))
        return result.scalars().all()


@router.get("/{medicament_id}", response_model=MedicamentRead)
async def consulter(medicament_id: int):
    async with SessionLocal() as session:
        medicament = await session.get(Medicament, medicament_id)
        if medicament is None:
            raise HTTPException(status_code=404, detail="Médicament introuvable")
        return medicament


@router.post("", response_model=MedicamentRead, status_code=201)
async def creer(medicament: MedicamentCreate):
    async with SessionLocal() as session:
        nouveau = Medicament(**medicament.model_dump())
        session.add(nouveau)
        await session.commit()
        return nouveau


@router.put("/{medicament_id}", response_model=MedicamentRead)
async def modifier(medicament_id: int, medicament: MedicamentCreate):
    async with SessionLocal() as session:
        existant = await session.get(Medicament, medicament_id)
        if existant is None:
            raise HTTPException(status_code=404, detail="Médicament introuvable")
        for champ, valeur in medicament.model_dump().items():
            setattr(existant, champ, valeur)
        await session.commit()
        return existant


@router.delete("/{medicament_id}", status_code=204)
async def supprimer(medicament_id: int):
    async with SessionLocal() as session:
        existant = await session.get(Medicament, medicament_id)
        if existant is None:
            raise HTTPException(status_code=404, detail="Médicament introuvable")
        await session.delete(existant)
        await session.commit()