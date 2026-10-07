"""Sécurité du service — squelette à compléter au TP8.

Fournit la dépendance `utilisateur_courant` à brancher sur les routes protégées :
    user: dict = Depends(utilisateur_courant)
"""
from pydantic import BaseModel, Field


class MedicamentCreate(BaseModel):
    nom: str = Field(min_length=1, max_length=100)
    prix: float = Field(
        gt=0,
        description="Prix en dirhams, strictement positif"
    )
    stock: int = Field(
        ge=0,
        default=0
    )


class MedicamentRead(MedicamentCreate):
    id: int