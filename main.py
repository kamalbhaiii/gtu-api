from typing import Optional
import CircularScraper
import ResultListScraper
from fastapi import FastAPI, Response, status
import time
import numpy as np
import os
from dotenv import load_dotenv
from starlette.responses import FileResponse
import datetime

date = datetime.datetime.now()
todaysDate = [date.strftime(f'%d-%B-%Y').split('-')]
todaysDate = f"{todaysDate[0][0]}-{todaysDate[0][1][0:3]}-{todaysDate[0][2]}"

favicon_path = './browser.png'
app = FastAPI()
scrap = CircularScraper.CircularScraper.scraper()
resultScrap = ResultListScraper.ResultListScraper.scraper()

envPath = os.path.join(".env")
load_dotenv(envPath)
apiKey = os.getenv('API_KEY')
apiKey = np.array(os.getenv('API_KEY').replace(" ", "").split(","))
apiName = os.getenv('NAME')
apiName = np.array(os.getenv('NAME').replace(" ", "").split(","))

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(favicon_path)

@app.get("/", status_code=404)
async def res_unauthorized(response : Response):
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"head":"Welcome to the GTU API",
        "remark":"No API Key Found",
        "last-updated":time.asctime()}

@app.get("/{api_key}/", status_code=200)
async def initial_auth_page(api_key : str, response : Response):
    if api_key in apiKey and (not(api_key) == "public"):
        response.status_code = status.HTTP_200_OK
        idx = np.where(api_key == apiKey)
        return {"head":f"Welcome to the GTU API, {apiName[idx[0][0]]}",
            "end-points":[f"{api_key}/circular", f"{api_key}/circular/<--circular_number-->", f"{api_key}/circular/date", f"{api_key}/circular/date?circular_date={todaysDate}", f"{api_key}/result"],
            "total-number-of-circular":len(scrap.keys()),
            "total-number-of-result-declared":len(resultScrap.keys()),
            "last-updated":time.asctime()}
    elif api_key in apiKey and api_key == "public":
        response.status_code = status.HTTP_200_OK
        idx = np.where(api_key == apiKey)
        return {"head":f"Welcome to the GTU API, {apiName[idx[0][0]]}",
            "end-points":f"{api_key}/circular",
            "total-number-of-circular":len(scrap.keys()),
            "total-number-of-result-declared":len(resultScrap.keys()),
            "last-updated":time.asctime()}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"head":"Welcome to the GTU API",
            "remark":"Invalid API Key (Unauthorized)",
            "last-updated":time.asctime()}

@app.get("/{api_key}/circular/", status_code = 200)
async def circular_auth_page(api_key : str, response : Response):
    if api_key in apiKey:
        response.status_code = status.HTTP_200_OK
        return scrap
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"head":"Welcome to the GTU API",
            "remark":"Invalid API Key (Unauthorized)",
            "last-updated":time.asctime()}
    

@app.get("/{api_key}/circular/{circular_number}/", status_code= 200)
async def cirNo_auth_page(api_key : str, circular_number : int, response : Response):
    if api_key in apiKey and (not(api_key) == "public"):
        response.status_code = status.HTTP_200_OK
        return {"circular_number":circular_number, "circular_data":scrap[circular_number]}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"head":"Welcome to the GTU API",
            "remark":"Invalid API Key (Unauthorized)",
            "last-updated":time.asctime()}

@app.get("/{api_key}/circular/date", status_code= 200)
async def cirNo_auth_page(api_key : str, response : Response, circular_date : Optional[str] = todaysDate):
    if api_key in apiKey and (not(api_key) == "public"):
        response.status_code = status.HTTP_200_OK
        return {"circular_date":circular_date, "circular_data":[scrap[i] for i in range(len(scrap)) if circular_date in scrap[i].values()]}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"head":"Welcome to the GTU API",
            "remark":"Invalid API Key (Unauthorized)",
            "last-updated":time.asctime()}

@app.get("/{api_key}/result/", status_code= 200)
async def resList_auth_page(api_key : str, response : Response):
    if api_key in apiKey and (not(api_key) == "public"):
        response.status_code = status.HTTP_200_OK
        return resultScrap
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"head":"Welcome to the GTU API",
            "remark":"Invalid API Key (Unauthorized)",
            "last-updated":time.asctime()}