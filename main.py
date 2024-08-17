import os
from fastapi import FastAPI , Request,HTTPException
from fastapi.responses import Response , HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import json
import helpers
import stripe
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
helper = helpers.Helper()

STRIPE_API = os.getenv('STRIPE_KEY')

stripe.api_key = STRIPE_API

my_templates = Jinja2Templates(directory = "templates")
app.mount('/static' , StaticFiles(directory="./static") , name="static")

class email_template(BaseModel):
    name:str
    email:str
    message:str
    subject:str

class checkout_template(BaseModel):
    productId:str


def load_questions()->List[dict]:
    with open("questions.json" , 'r') as file:
        return json.load(file)


@app.get('/')
def test_root(request:Request):
    print("Home request coming")
    testimonials = helper.load_testimonials()

    return my_templates.TemplateResponse("index.html" , {"request":request , 'testimonials':testimonials})

@app.get('/contact' , response_class=HTMLResponse)
def get_contact(request:Request):
    print("contact form request coming")
    return my_templates.TemplateResponse("contact.html" , {"request":request})

@app.get('/plans' , response_class=HTMLResponse)
def get_plans(request:Request):
    plans = helper.load_plans()
    return my_templates.TemplateResponse("plans.html" , {"request":request , 'plans':plans})

@app.get('/faq' , response_class=HTMLResponse)
def get_faq(request:Request):
    faqs = load_questions()
    return my_templates.TemplateResponse("faq.html" , {"request":request , 'faqs' :faqs})

@app.get('/refund-policy' , response_class=HTMLResponse)
def get_faq(request:Request):
    return my_templates.TemplateResponse("refund.html" , {"request":request})


@app.get('/youtube-services' , response_class=HTMLResponse)
@app.get('/soundcloud-services' , response_class=HTMLResponse)
@app.get('/spotify-services' , response_class=HTMLResponse)
def get_services(request:Request):
    path_name = request.url.path[1:]
    services = helper.load_services()
    service_name = " ".join(path_name.split('-')).capitalize()
    
    return my_templates.TemplateResponse("service.html" , {"request":request ,'name':service_name, 'services':services[path_name]})

@app.get('/applemusic-services' , response_class=HTMLResponse)
def get_applemusic(request:Request):
    return my_templates.TemplateResponse("applemusic.html" , {"request":request})

# create checkout session for payment
@app.post('/create-checkout-session')
def create_checkout_session(request:checkout_template):
    print("create checkout session request coming")
    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=f"{os.getenv("DOMAIN")}/payment-success",
            cancel_url=f"{os.getenv("DOMAIN")}/payment-cancel",
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price":request.productId,
                    "quantity":1
                }
            ]
        )

        return {"sessionId":checkout_session["id"]}
    except Exception as e:
        print("EXCEPTION IN CHECKOUT")
        print(e)
        
        
    return {"sessionId":"wrong"}

@app.get('/payment-success' , response_class=HTMLResponse)
@app.get('/payment-cancel' , response_class=HTMLResponse)
def get_payment_result(request:Request):
    path_url = request.url.path
    path_url = path_url[1:]

    payment_message = " ".join(path_url.split('-')).capitalize()
    page = 1
    if(path_url.__eq__("payment-success")):
        page = 0

    return my_templates.TemplateResponse("payment-result.html" , {"request":request ,"page":page, "paymentmessage":payment_message})

@app.post('/handle-email' , response_class=JSONResponse)
def post_email(request:email_template):
    print("Sending email")
    print(request.name)
    return "OK"

@app.get('/all' , response_class=HTMLResponse)
def get_all(request:Request):
    return my_templates.TemplateResponse("all.html" , {"request":request})
@app.get('/test')
def test(request:Request):
    print("Testing..........")
    return "OK"