from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from datetime import datetime
import os, re


current_path = os.path.dirname(os.path.abspath(__file__))
mypath = '/var/spool/gammu/inbox/'

app = FastAPI()
app.mount("/static", StaticFiles(directory=f"{current_path}/static/css"), name="static")

templates = Jinja2Templates(directory=f"{current_path}/templates")

@app.get("/", response_class=RedirectResponse)
def to_index():
    return RedirectResponse(url="/index",status_code=status.HTTP_302_FOUND)

@app.get('/index', response_class=HTMLResponse)
async def get_webpage(request: Request):  
    files = os.listdir(mypath)
    num_list =[]
    for file in files:
        num_list.append(re.search(r'_\d\d_(.*)_\d*\.txt', file).group(1))
    num_list_uniq = list(set(num_list))
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
    return templates.TemplateResponse("index.html", {"request": request,"smsss": newlist, "title": "All", "nums":num_list_uniq})

@app.get('/index/{num}', response_class=HTMLResponse)
async def get_webpage(request: Request, num:str):  
    files = os.listdir(mypath)
    num_list =[]
    for file in files:
        num_list.append(re.search(r'_\d\d_(.*)_\d*\.txt', file).group(1))
    num_list_uniq = list(set(num_list))
    # postss to dict
    smss_list = [
        {
            "number": re.search(r'_\d\d_(.*)_\d*\.txt', file).group(1),
            "text": open(mypath+file, "r").read(),
            "date": datetime.fromtimestamp(os.path.getctime(mypath+file)),
        }
        for file in files if num == re.search(r'_\d\d_(.*)_\d*\.txt', file).group(1)
    ]
    newlist = sorted(smss_list,reverse=True, key=lambda d: d['date'] )
    return templates.TemplateResponse("index.html", {"request": request,"smsss": newlist, "title": "All", "nums":num_list_uniq})


@app.get("/check_balanse", response_class=RedirectResponse)
def send_command():
    balan = os.getenv('CHECK_B')
    command = f"gammu-smsd-inject USSD {balan}"
    # Open the named pipe for writing
    pipe = os.open("/listener", os.O_WRONLY)
    # Write the command to the pipe
    os.write(pipe, command.encode())
    # Close the pipe
    os.close(pipe)
    return RedirectResponse(url="/index",status_code=status.HTTP_302_FOUND)