from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from datetime import datetime
import os, re


current_path = os.path.dirname(os.path.abspath(__file__))
mypath = '/var/spool/gammu/inbox/'

app = FastAPI()
app.mount("/static", StaticFiles(directory=f"{current_path}/static/css"), name="static")

templates = Jinja2Templates(directory=f"{current_path}/templates")


@app.get('/', response_class=HTMLResponse)
async def get_webpage(request: Request):  
    files = os.listdir(mypath)
    
    # postss to dict
    smss_list = [
        {
            "number": re.search(r'_\d\d_(.*)_\d*\.txt', file).group(1),
            "text": open(mypath+file, "r").read(),
            "date": datetime.fromtimestamp(os.path.getctime(mypath+file)),
        }
        for file in files
    ]
    newlist = sorted(smss_list,reverse=True, key=lambda d: d['date'] )
    return templates.TemplateResponse("index.html", {"request": request,"smsss": newlist, "title": "All"})
