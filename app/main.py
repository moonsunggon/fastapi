from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List
import csv
import io

from app.db.session import get_db, engine
from app.models import item as item_model
from app.schemas.item import Item, ItemCreate
from app.db.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="아이템 관리 및 CSV 처리 API (with SQLAlchemy)",
    description="FastAPI와 SQLAlchemy를 사용한 아이템 관리 시스템과 CSV 파일 처리 기능을 제공합니다.",
    version="2.0.0"
)

@app.get("/", include_in_schema=False)
async def root():
    """
    루트 경로에서 자동으로 API 문서 페이지로 리다이렉트합니다.
    """
    print('message: "환영합니다! FastAPI와 SQLAlchemy를 사용한 예제 애플리케이션입니다."')
    return RedirectResponse(url="/docs")

@app.post("/items", response_model=Item, tags=["items"])
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    새로운 아이템을 생성합니다.
    """
    db_item = item_model.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items", response_model=List[Item], tags=["items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    아이템 목록을 반환합니다.
    """
    items = db.query(item_model.Item).offset(skip).limit(limit).all()
    return items

@app.get("/items/{item_id}", response_model=Item, tags=["items"])
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
    지정된 ID의 아이템을 반환합니다.
    """
    db_item = db.query(item_model.Item).filter(item_model.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=Item, tags=["items"])
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    """
    지정된 ID의 아이템을 업데이트합니다.
    """
    db_item = db.query(item_model.Item).filter(item_model.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}", tags=["items"])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    지정된 ID의 아이템을 삭제합니다.
    """
    db_item = db.query(item_model.Item).filter(item_model.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}

@app.post("/items-from-csv/", response_model=List[Item], tags=["csv"])
async def create_items_from_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    CSV 파일을 업로드하여 새로운 아이템들을 생성합니다.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드 가능합니다.")

    try:
        contents = await file.read()
        decoded = contents.decode()
        csv_reader = csv.DictReader(io.StringIO(decoded))
        new_items = []
        for row in csv_reader:
            item = item_model.Item(
                name=row['name'],
                description=row.get('description', None),
                price=float(row['price'])
            )
            db.add(item)
            new_items.append(item)
        db.commit()
        for item in new_items:
            db.refresh(item)
        return new_items
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"CSV 파일의 형식이 올바르지 않습니다. 누락된 열: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"CSV 파일의 데이터 형식이 올바르지 않습니다: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 처리 중 오류가 발생했습니다: {str(e)}")