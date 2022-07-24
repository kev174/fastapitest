# https://fastapi.tiangolo.com/tutorial/first-steps/ 
# https://web.deta.sh/home/kev17404/default/micros/first_micro
# http://127.0.0.1:8000/docs
# Create FastApi with directories and deploy API Gateway and Lambda function. Below
# https://github.com/deadbearcode/simple-serverless-fastapi-example
# uvicorn main:app --reload 

from fastapi import FastAPI, Query
from typing import Union
from mangum import Mangum
from enum import Enum
from pydantic import BaseModel

class AmazonItem(BaseModel):
    name: str
    description: Union[str, None] = None    #python 3.10> description: str | None = None
    price: float
    tax: Union[float, None] = None

class ModelName(str, Enum):
    decision_tree = "decision_tree"
    neural_networks = "neural_networks"
    linear_regression = "linear_regression"
    
# This is similar to a POJOs but description and tax can be left out and assigned a default value
class Widget(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
app = FastAPI()

# http://127.0.0.1:8000/amznitem/ Postman POST Request with AmazonItem POJO
@app.post("/amznitem/")
async def create_item(amazonitem: AmazonItem):
    return amazonitem
    
# http://127.0.0.1:8000/widget/99/?query=kevin  Postman (POST): Body, Raw, JSON: 
#   { "name": "Widget","description": "Some Widget","price": 49.99,"tax": 21}
# Notice this url contains an integer, Widget POJO and an optional query string
# I also limited the size of the query within the URL (Kevin = 5 chars)
@app.post("/widget/{widget_id}")
# async def create_item(widget_id: int, widget: Widget, query: str | None = Query(default=None, max_length=5)):
async def create_item(widget_id: int, widget: Widget, query: Union[str, None] = Query(default=None, max_length=5)):
    widget_dict = widget.dict()
    if widget.tax:
        price_with_tax = widget.price + widget.tax
        widget_dict.update({"price_with_tax": price_with_tax, "price_with_parametre entry": widget_id, "query param": query})
    return widget_dict

# http://127.0.0.1:8000/itemss/?skip=0&limit=2
@app.get("/itemss/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# This method allows you to add a file directory: mybucket/kevin/test.txt
# http://127.0.0.1:8000/files/mybucket/kevin/test.txt
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# http://127.0.0.1:8000/models/decision_tree
# http://127.0.0.1:8000/models/neural_networks
# http://127.0.0.1:8000/models/linear_regression
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.decision_tree:
        return {"model_name": model_name, "message": "This ia a decision_tree"}

    if model_name.value == "neural_networks":
        return {"model_name": model_name, "message": "This a a Neural Network"}

    return {"model_name": model_name, "message": "This is Linear Regression"}

# http://127.0.0.1:8000/items/54
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id_string": item_id}

# http://127.0.0.1:8000/item/Hi%20Kevin
@app.get("/item/{item_id}")
async def read_user(item_id: str):
    return {"Item_id": item_id}

# http://127.0.0.1:8000/inventory/foo
@app.get("/inventory/foo")
async def read_user():
    return {"Hi ../Inventory/Foo Endpoint"}
	
handler = Mangum(app=app) # to make it work with Amazon Lambda, we create a handler object using Mangum
