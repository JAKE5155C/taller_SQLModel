from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from database import Heroe, HeroeBase, crear_db_y_tablas, get_session

crear_db_y_tablas()
app = FastAPI()


@app.get("/")
def home():
    return {"mensaje": "API de heroes", "documentacion": "/docs"}


# --- Rutas de la API ---

# Endpoint para crear un héroe
@app.post("/heroes/", response_model=Heroe)
def create_hero(heroe: HeroeBase, session: Session = Depends(get_session)):
    new_heroe = Heroe(
        nombre=heroe.nombre,
        nombre_secreto=heroe.nombre_secreto,
        edad=heroe.edad,
    )
    session.add(new_heroe)
    session.commit()
    session.refresh(new_heroe)
    return new_heroe


# Endpoint para obtener todos los héroes
@app.get("/heroes/", response_model=list[Heroe])
def ver_heroes(session: Session = Depends(get_session)):
    consulta = select(Heroe)
    return session.exec(consulta).all()


# Endpoint para actualizar un héroe por su ID
@app.put("/heroes/{hero_id}", response_model=Heroe)
def update_hero(
    hero_id: int,
    updated_hero: HeroeBase,
    session: Session = Depends(get_session),
):
    heroe = session.get(Heroe, hero_id)
    if heroe is None:
        raise HTTPException(status_code=404, detail="Heroe no encontrado")

    heroe.nombre = updated_hero.nombre
    heroe.nombre_secreto = updated_hero.nombre_secreto
    heroe.edad = updated_hero.edad

    session.add(heroe)
    session.commit()
    session.refresh(heroe)

    return heroe


# Endpoint para borrar un héroe por su ID
@app.delete("/heroes/{hero_id}", response_model=Heroe)
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    heroe = session.get(Heroe, hero_id)
    if heroe is None:
        raise HTTPException(status_code=404, detail="Heroe no encontrado")
    data = {
        "id": heroe.id,
        "nombre": heroe.nombre,
        "nombre_secreto": heroe.nombre_secreto,
        "edad": heroe.edad,
    }
    session.delete(heroe)
    session.commit()
    return data