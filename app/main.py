
from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Optional
import csv
import io

app = FastAPI(
    title="아이템 관리 API",
    description="FastAPI를 사용한 간단한 아이템 관리 시스템입니다.",
    version="1.0.0"
)

class Item(BaseModel):
    """
    아이템 정보를 나타내는 모델

    Attributes:
        id (int): 아이템의 고유 식별자
        name (str): 아이템의 이름
        description (Optional[str]): 아이템에 대한 설명 (선택사항)
        price (float): 아이템의 가격
    """
    id: int
    name: str
    description: Optional[str] = None
    price: float

items = []

@app.get("/", include_in_schema=False)
async def root():
    """
    루트 경로에서 자동으로 API 문서 페이지로 리다이렉트합니다.
    """
    print('message: "환영합니다! FastAPI 예제 애플리케이션입니다."')
    return RedirectResponse(url="/docs")

@app.get("/items", response_model=List[Item], tags=["items"])
async def read_items():
    """
    모든 아이템의 목록을 반환합니다.

    Returns:
        List[Item]: 등록된 모든 아이템의 목록
    """
    return items

@app.get("/items/{item_id}", response_model=Item, tags=["items"])
async def read_item(item_id: int):
    """
    지정된 ID의 아이템을 반환합니다.

    Args:
        item_id (int): 조회할 아이템의 ID

    Returns:
        Item: 요청된 ID에 해당하는 아이템

    Raises:
        HTTPException: 아이템을 찾을 수 없는 경우 404 에러 발생
    """
    item = next((item for item in items if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=Item, tags=["items"])
async def create_item(item: Item):
    """
    새로운 아이템을 생성합니다.

    Args:
        item (Item): 생성할 아이템의 정보

    Returns:
        Item: 생성된 아이템의 정보
    """
    items.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item, tags=["items"])
async def update_item(item_id: int, item: Item):
    """
    지정된 ID의 아이템을 업데이트합니다.

    Args:
        item_id (int): 업데이트할 아이템의 ID
        item (Item): 업데이트할 아이템의 새로운 정보

    Returns:
        Item: 업데이트된 아이템의 정보

    Raises:
        HTTPException: 아이템을 찾을 수 없는 경우 404 에러 발생
    """
    index = next((i for i, x in enumerate(items) if x.id == item_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    items[index] = item
    return item

@app.delete("/items/{item_id}", tags=["items"])
async def delete_item(item_id: int):
    """
    지정된 ID의 아이템을 삭제합니다.

    Args:
        item_id (int): 삭제할 아이템의 ID

    Returns:
        dict: 삭제 성공 메시지

    Raises:
        HTTPException: 아이템을 찾을 수 없는 경우 404 에러 발생
    """
    index = next((i for i, x in enumerate(items) if x.id == item_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    items.pop(index)
    return {"message": "Item deleted successfully"}

@app.post("/items-from-csv/", response_model=List[Item], tags=["csv", "items"])
async def create_items_from_csv(file: UploadFile = File(...)):
    """
    CSV 파일을 업로드하여 새로운 아이템들을 생성합니다. 예제 파일 : customer_test.csv

    Args:
        file (UploadFile): 업로드할 CSV 파일 (id, name, description, price 열 포함)

    Returns:
        List[Item]: 생성된 아이템들의 리스트

    Raises:
        HTTPException: 파일 형식이 잘못되었거나 처리 중 오류가 발생한 경우
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드 가능합니다.")

    try:
        contents = await file.read()
        decoded = contents.decode()
        csv_reader = csv.DictReader(io.StringIO(decoded))
        new_items = []
        for row in csv_reader:
            item = Item(
                id=int(row['id']),
                name=row['name'],
                description=row.get('description', None),
                price=float(row['price'])
            )
            items.append(item)
            new_items.append(item)
        return new_items
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"CSV 파일의 형식이 올바르지 않습니다. 누락된 열: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"CSV 파일의 데이터 형식이 올바르지 않습니다: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 처리 중 오류가 발생했습니다: {str(e)}")