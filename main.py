from fastapi import FastAPI , Request
from fastapi.responses import Response , HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory = "templates")
app.mount('/static' , StaticFiles(directory="./static") , name="static")

@app.get('/')
def test_root(request:Request):
    print("Home request coming")
    return templates.TemplateResponse("index.html" , {"request":request})

@app.get('/contact' , response_class=HTMLResponse)
def get_contact(request:Request):
    print("contact form request coming")
    return templates.TemplateResponse("contact.html" , {"request":request})

@app.get('/plans' , response_class=HTMLResponse)
def get_plans(request:Request):
    return templates.TemplateResponse("plans.html" , {"request":request})

@app.get('/faq' , response_class=HTMLResponse)
def get_faq(request:Request):
    return templates.TemplateResponse("faq.html" , {"request":request})

@app.get('/refund-policy' , response_class=HTMLResponse)
def get_faq(request:Request):
    return templates.TemplateResponse("refund.html" , {"request":request})

@app.get('/test')
def test(request:Request):
    print("Testing..........")
    return {
        "message":"server is up and running"
    }