from fastapi import APIRouter, HTTPException

from app.schemas import ProduitCreate, ProduitRead

router = APIRouter(prefix="/produits", tags=["produits"])

_db: dict[int, ProduitRead] = {}  # stockage en mémoire pour cette séance

_next_id = 1


@router.get("", response_model=list[ProduitRead])
async def lister():
    return list(_db.values())


@router.get("/{produit_id}", response_model=ProduitRead)
async def consulter(produit_id: int):
    if produit_id not in _db:
        raise HTTPException(
            status_code=404,
            detail="Produit introuvable"
        )

    return _db[produit_id]


@router.post("", response_model=ProduitRead, status_code=201)
async def creer(produit: ProduitCreate):
    global _next_id

    nouveau = ProduitRead(id=_next_id, **produit.model_dump())
    _db[_next_id] = nouveau
    _next_id += 1

    return nouveau


@router.put("/{produit_id}", response_model=ProduitRead)
async def modifier(produit_id: int, produit: ProduitCreate):
    if produit_id not in _db:
        raise HTTPException(
            status_code=404,
            detail="Produit introuvable"
        )

    modifie = ProduitRead(id=produit_id, **produit.model_dump())
    _db[produit_id] = modifie

    return modifie


@router.delete("/{produit_id}", status_code=204)
async def supprimer(produit_id: int):
    if produit_id not in _db:
        raise HTTPException(
            status_code=404,
            detail="Produit introuvable"
        )

    del _db[produit_id]