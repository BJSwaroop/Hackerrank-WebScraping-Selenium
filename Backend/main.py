from fastapi import FastAPI
from pydantic import BaseModel
from hackerrank_main import HRMain


class Credentials(BaseModel):
    username: str
    password: str
    contest: str
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/fetchUsers/")
async def create_item():

    hr = HRMain()
    users = hr.fetchData()
    d = {}
    d["users"] = users
    # print(item.username)
    # print(item.password)
    # print(item.contest)
    return d
# @app.post("/fetchUsers/")
# async def create_item(cred: Credentials):

#     hr = HRMain(cred.username,cred.password,cred.contest)
#     users = hr.fetchData()
#     d = {}
#     d["users"] = users
#     # print(item.username)
#     # print(item.password)
#     # print(item.contest)
#     return d