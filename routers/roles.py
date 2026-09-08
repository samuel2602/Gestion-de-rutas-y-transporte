from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Rol
from schemas import RolCreate, RolResponse


router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)


@router.get("/", response_model=list[RolResponse])
def obtener_roles(db: Session = Depends(get_db)):
    return db.query(Rol).all()


@router.post("/", response_model=RolResponse)
def crear_rol(rol: RolCreate, db: Session = Depends(get_db)):
    nuevo_rol = Rol(
        nombre=rol.nombre,
        descripcion=rol.descripcion
    )

    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)

    return nuevo_rol