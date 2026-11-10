from sqlmodel import Field, Session, SQLModel, create_engine


class HeroeBase(SQLModel):
    nombre: str = Field(index=True)
    nombre_secreto: str
    edad: int | None = Field(default=None, index=True)


class Heroe(HeroeBase, table=True):
    __tablename__ = "heroes"
    id: int | None = Field(default=None, primary_key=True)


DATABASE_URL = "sqlite:///database.db"
connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)


def crear_db_y_tablas():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session