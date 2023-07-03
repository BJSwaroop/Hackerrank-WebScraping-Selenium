from fastapi import FastAPI
from pydantic import BaseModel
from hackerrank_main import HRMain
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Credentials(BaseModel):
    username: str
    password: str
    contest: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.post("/fetchUsers/")
# async def create_item():

#     hr = HRMain()
#     users = hr.fetchData()
#     d = {}
#     d["users"] = users
#     # print(item.username)
#     # print(item.password)
#     # print(item.contest)
#     return d
@app.post("/fetchold/")
async def create_item(cred: Credentials):
    """
    this will get the current users in the database with their scores.
    """
    # hr = HRMain(cred.username,cred.password,cred.contest)
    # users = hr.fetchData()
    users = [
    { "username": '20PA1A0412', "score": 80 },
    { "username": '20Pa1a5430', "score": 95 },
    { "username": '20pa1a5435', "score": 70 }
    ]
    return users
@app.post("/fetchlatest/")
async def create_item(cred: Credentials):
    """
    It will fetch the latest users. By scrapping the data.  
    """
    hr = HRMain(cred.username,cred.password,cred.contest)

    # print(cred.username,cred.password,cred.contest)
    # users = hr.fetchData()
    users = [
    { "username": '20PA1A0412', "score": 80 },
    { "username": '20Pa1a5430', "score": 95 },
    ]
    # print(item.username)
    # print(item.password)
    # print(item.contest)
    return users