from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from typing import List, Optional

app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

items = []


@app.get("/", include_in_schema=False)
async def root():
    print(f'message": "환영합니다! FastAPI 예제 애플리케이션입니다.')
    return RedirectResponse(url="/docs")


@app.get("/items", response_model=List[Item])
async def read_items():
    return items


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    item = next((item for item in items if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items", response_model=Item)
async def create_item(item: Item):
    items.append(item)
    return item


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    index = next((i for i, x in enumerate(items) if x.id == item_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    items[index] = item
    return item


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    index = next((i for i, x in enumerate(items) if x.id == item_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    items.pop(index)
    return {"message": "Item deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
