from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Medicament(Base):
    __tablename__ = "medicaments"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(unique=True)
    prix: Mapped[float]
    stock: Mapped[int] = mapped_column(default=0)
    nomfournisseur: Mapped[str] = mapped_column()