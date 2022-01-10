import CircularScraper
import ResultListScraper
from fastapi import FastAPI, Response, status
import time
import numpy as np
import os
from dotenv import load_dotenv


app = FastAPI()
scrap = CircularScraper.CircularScraper.scraper()
resultScrap = ResultListScraper.ResultListScraper.scraper()

envPath = os.path.join(".env")
load_dotenv(envPath)
apiKey = os.getenv('API_KEY')
apiKey = np.array(os.getenv('API_KEY').replace(" ", "").split(","))
apiName = os.getenv('NAME')
apiName = np.array(os.getenv('NAME').replace(" ", "").split(","))


@app.get("/", status_code=404)
async def res_unauthorized(response : Response):
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"head":"Welcome to the GTU API",
        "remark":"No API Key Found",
        "last-updated":time.asctime()}

@app.get("/{api_key}/", status_code=200)
async def initial_auth_page(api_key : str, response : Response):
    if api_key in apiKey:
        response.status_code = status.HTTP_200_OK
        idx = np.where(api_key == apiKey)
        return {"head":f"Welcome to the GTU API, {apiName[idx[0][0]]}",
            "end-points":[f"{api_key}/circular", f"{api_key}/circular/<--circular_number-->", f"{api_key}/result"],
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
    if api_key in apiKey:
        response.status_code = status.HTTP_200_OK
        return {"circular_number":circular_number, "circular_data":scrap[circular_number]}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"head":"Welcome to the GTU API",
            "remark":"Invalid API Key (Unauthorized)",
            "last-updated":time.asctime()}

@app.get("/{api_key}/result/", status_code= 200)
async def resList_auth_page(api_key : str, response : Response):
    if api_key in apiKey:
        response.status_code = status.HTTP_200_OK
        return resultScrap
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"head":"Welcome to the GTU API",
            "remark":"Invalid API Key (Unauthorized)",
            "last-updated":time.asctime()}