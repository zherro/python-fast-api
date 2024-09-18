# python-fast-api
 Sample for use of Python with FastApi

### Estrutura do Projeto:
```bash
fastapi_project/
│
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   └── items.py
│   │   └── dependencies.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   └── item.py
│   ├── schemas/
│   │   └── item.py
│   ├── crud/
│   │   └── item.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── main.py
└── requirements.txt
```

### Arquivos e Conteúdo:

#### 1. **`requirements.txt`**:
Lista de dependências para o projeto.
```txt
fastapi
uvicorn
sqlalchemy
pydantic
```

#### 2. **`app/main.py`**:
O arquivo principal que inicializa o FastAPI e inclui os roteadores.
```python
from fastapi import FastAPI
from app.api.endpoints import items

app = FastAPI(
    title="FastAPI Project",
    description="An organized FastAPI project following best practices.",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Include the items router
app.include_router(items.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI project!"}
```

#### 3. **`app/api/endpoints/items.py`**:
Define as rotas e operações de `items`.
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.item import ItemCreate, ItemRead
from app.crud.item import get_item, create_item
from app.db.session import get_db

router = APIRouter(
    prefix="/items",
    tags=["items"],
)

@router.post("/", response_model=ItemRead)
def create_new_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db=db, item=item)

@router.get("/{item_id}", response_model=ItemRead)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
```

#### 4. **`app/schemas/item.py`**:
Define os esquemas (modelos de dados) usando **Pydantic**.
```python
from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str

class ItemCreate(ItemBase):
    price: float

class ItemRead(ItemBase):
    id: int
    price: float

    class Config:
        orm_mode = True
```

#### 5. **`app/models/item.py`**:
Modelo de banco de dados usando **SQLAlchemy**.
```python
from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)
```

#### 6. **`app/crud/item.py`**:
Funções de CRUD (Create, Read, Update, Delete) para os itens.
```python
from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def create_item(db: Session, item: ItemCreate):
    db_item = Item(name=item.name, description=item.description, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
```

#### 7. **`app/db/session.py`**:
Configuração da sessão de banco de dados.
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### 8. **`app/db/base.py`**:
Base de dados para os modelos.
```python
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
```

#### 9. **`app/core/config.py`**:
Configurações centrais do app (separando variáveis sensíveis como chaves de API).
```python
class Settings:
    PROJECT_NAME: str = "FastAPI Project"
    PROJECT_VERSION: str = "1.0.0"

settings = Settings()
```

#### 10. **`app/core/security.py`** (Opcional):
Gerenciar aspectos de segurança, como autenticação e autorização. Se necessário, adicione autenticação com JWT, OAuth2, etc.

---

### Instruções para rodar o projeto:

1. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute a API**:
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Acesse a documentação do Swagger**:
   - Abra seu navegador e vá para [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para ver a documentação interativa gerada automaticamente.

Esse projeto segue boas práticas de organização, com separação de responsabilidades (como modelos, esquemas, CRUD, e endpoints), e é escalável para projetos maiores.