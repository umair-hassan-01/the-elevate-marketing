from fastapi import FastAPI , Request
from fastapi.responses import Response , HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import json
import helpers

app = FastAPI()
helper = helpers.Helper()

templates = Jinja2Templates(directory = "templates")
app.mount('/static' , StaticFiles(directory="./static") , name="static")

def load_questions()->List[dict]:
    with open("questions.json" , 'r') as file:
        return json.load(file)


@app.get('/')
def test_root(request:Request):
    print("Home request coming")
    testimonials = helper.load_testimonials()
    for testimonial in testimonials:
        print(testimonial)

    return templates.TemplateResponse("index.html" , {"request":request , 'testimonials':testimonials})

@app.get('/contact' , response_class=HTMLResponse)
def get_contact(request:Request):
    print("contact form request coming")
    return templates.TemplateResponse("contact.html" , {"request":request})

@app.get('/plans' , response_class=HTMLResponse)
def get_plans(request:Request):
    plans = helper.load_plans()
    for plan in plans:
        print(plan)
    return templates.TemplateResponse("plans.html" , {"request":request , 'plans':plans})

@app.get('/faq' , response_class=HTMLResponse)
def get_faq(request:Request):
    faqs = load_questions()
    for faq in faqs:
        print(faq)
    return templates.TemplateResponse("faq.html" , {"request":request , 'faqs' :faqs})

@app.get('/refund-policy' , response_class=HTMLResponse)
def get_faq(request:Request):
    return templates.TemplateResponse("refund.html" , {"request":request})

@app.get('/test')
def test(request:Request):
    print("Testing..........")
    return {
        "message":"server is up and running"
    }