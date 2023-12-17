import ast
import json
from fastapi import FastAPI, Request
from pydantic import BaseModel
from hackerrank_main import HRMain
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Query
from hackerrank_plagiarismCheck import plagiariseCodes
templates = Jinja2Templates(directory="templates")
app = FastAPI()
# origins = [
#     "http://localhost:4200",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )



@app.get("/", response_class=HTMLResponse)
async def homePage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,"data":{}})

@app.get("/fetchLatest/")
async def fetchLatest(request: Request):
    """
    It will fetch the latest users. By scrapping the data.  
    """
    # adminUsername= "capmentor01" 
    # adminPassword=    "VITBHackers21!"
    # contest_slug=   "test-contest00"
    adminUsername = request.query_params.get("username", None)
    adminPassword = request.query_params.get("password", None)
    contest_slug = request.query_params.get("contestSlug", None)
    hr = HRMain(adminUsername,adminPassword,contest_slug)
    data = hr.fetchData()
    return templates.TemplateResponse("index.html", {"request": request, "data": data})

@app.get("/fetchOld/")
async def fetchOld(request: Request):
    adminUsername = request.query_params.get("username", None)
    adminPassword = request.query_params.get("password", None)
    contest_slug = request.query_params.get("contestSlug", None)
    hr = HRMain(adminUsername,adminPassword,contest_slug)
    data = hr.fetchOldData()
    return templates.TemplateResponse("userAttempts.html", {"request": request, "data": data})

@app.get("/plagiariseCode/")
async def plagiarise_code(request: Request, userData: str = Query(...)):
    try:
        userData = ast.literal_eval(userData)
    except (ValueError, SyntaxError) as e:
        return {"error": f"Invalid userData format: {str(e)}"}
    res = plagiariseCodes(userData)
    return templates.TemplateResponse("result.html", {"request": res})