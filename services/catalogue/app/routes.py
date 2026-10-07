from fastapi import APIRouter, HTTPException
from app.schemas import MedicamentCreate, MedicamentRead

router = APIRouter(prefix="/medicaments", tags=["medicaments"])

_db: dict[int, MedicamentRead] = {}  # stockage en mémoire pour cette séance
_next_id = 1

@router.get("", response_model=list[MedicamentRead])
async def lister():
    return list(_db.values())

@router.get("/{medicament_id}", response_model=MedicamentRead)
async def consulter(medicament_id: int):
    if medicament_id not in _db:
        raise HTTPException(status_code=404, detail="Médicament introuvable")
    return _db[medicament_id]

@router.post("", response_model=MedicamentRead, status_code=201)
async def creer(medicament: MedicamentCreate):
    global _next_id
    nouveau = MedicamentRead(id=_next_id, **medicament.model_dump())
    _db[_next_id] = nouveau
    _next_id += 1
    return nouveau

@router.put("/{medicament_id}", response_model=MedicamentRead)
async def modifier(medicament_id: int, medicament: MedicamentCreate):
    if medicament_id not in _db:
        raise HTTPException(status_code=404, detail="Médicament introuvable")
    modifie = MedicamentRead(id=medicament_id, **medicament.model_dump())
    _db[medicament_id] = modifie
    return modifie

@router.delete("/{medicament_id}", status_code=204)
async def supprimer(medicament_id: int):
    if medicament_id not in _db:
        raise HTTPException(status_code=404, detail="Médicament introuvable")
    del _db[medicament_id]
