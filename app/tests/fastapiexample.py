# https://github.com/deadbearcode/simple-serverless-fastapi-example
# https://www.youtube.com/watch?v=6fE31084Uks

from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel


class ModelName(str, Enum):
    decision_tree = "decision_tree"
    neural_networks = "neural_networks"
    linear_regression = "linear_regression"
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
app = FastAPI()

# https://h663km.deta.dev/itemss/?skip=1&limit=10
@app.get("/itemss/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
	
# This method allows you to add a file directory: mybucket/kevin/test.txt
# https://h663km.deta.dev/files/mybucket/kevin/test.txt
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
	
# https://h663km.deta.dev/models/decision_tree
# https://h663km.deta.dev/models/neural_networks
# https://h663km.deta.dev/models/linear_regression
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.decision_tree:
        return {"model_name": model_name, "message": "This ia a decision_tree"}

    if model_name.value == "neural_networks":
        return {"model_name": model_name, "message": "This a a Neural Network"}

    return {"model_name": model_name, "message": "This is Linear Regression"}
	
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items")
def read_items():
    return {"Hello": "Kevin"}
	
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
	
# https://h663km.deta.dev/item/Hi%20Kevin
@app.get("/item/{item_id}")
async def read_user(item_id: str):
    return {"Item_id": item_id}

