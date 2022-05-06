from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel, ValidationError, validator
import pandas as pd
from datetime import datetime
import joblib
from fastapi.responses import JSONResponse
import base64

class Transaction(BaseModel):
    """Data model for user input transaction
    """
    signup_time: datetime
    purchase_time: datetime
    purchase_value: int
    source: str
    browser: str
    sex: str
    age: int
    
    @validator("signup_time")
	def signup_time_must_be_anterior_to_purchase_time(cls, v, values):
		if v >= values["purchase_time"]:
			raise ValueError("Signup time must be anterior to purchase time")
		return v
        
    @validator("purchase_value")
	def purchase_value_must_be_positive(cls, v):
		if v < 0:
			raise ValueError("Purchase value must be positive")
		return v
        
    @validator("source")
	def source_choice_limitation(cls, v):
		if v != "Ads" and v != "SEO" and v != "Direct":
			raise ValueError("Source must be Ads, SEO or Direct")
		return v
        
    @validator("browser")
	def browser_choice_limitation(cls, v):
		if v != "Chrome" and v != "Opera" and v != "Safari" and v != "IE" and v != "FireFox":
			raise ValueError("Browser must be Chrome, Opera, Safari, IE or FireFox")
		return v
        
    @validator("sex")
	def sex_must_be_F_or_M(cls, v):
		if v != "F" and v != "M":
			raise ValueError("Sex must be F or M")
		return v
        
class userNotAuthorisedException(Exception):
	"""defines an exception for the user who doesn't pass the authorization
	"""
	def __init__(self):
		self.message = "User not authorised"
        
def preprocessing_df(original_df):
    df = original_df.copy()
    df["purchase_date"] = df.purchase_time.dt.date
    df["purchase_hour"] = df.purchase_time.dt.hour
    df["purchase_weekday"] = df.purchase_time.dt.weekday
    df["purchase_month"] = df.purchase_time.dt.month
    df["purchase_day"] = df.purchase_time.dt.day
    df["signup_date"] = df.signup_time.dt.date
    df["days_till_signup"] = df.purchase_date - df.signup_date
    df.days_till_signup = df.days_till_signup.dt.days
    df = df[["days_till_signup", "purchase_month", "purchase_day", "purchase_weekday", 
              "purchase_hour", "purchase_value", "age"]]
    df = df.join(pd.get_dummies(original_df[["source", "browser"]], drop_first=True))
    df = df.join(original_df.sex.replace(["M", "F"], [0,1]))
    
    return df
    
df_models = pd.read_csv('https://assets-datascientest.s3-eu-west-1.amazonaws.com/de/total/fraud.csv', parse_dates = ['signup_time','purchase_time'])
model_rfc = joblib.load("fraud_rfc.pkl")
model_lgb = joblib.load("fraud_lgb.pkl")
identifiants = {
	"alice": "YWxpY2U6d29uZGVybGFuZAo=",
	"bob": "Ym9iOmJ1aWxkZXIK",
	"clementine": "Y2xlbWVudGluZTptYW5kYXJpbmUK"
	}

def checkAuthorization(authorization):
	"""checks the user credentials
	"""
	username = ""
	password = ""
	vb_authorization = False
	if len(authorization) > 6:
		if authorization[:6] == "Basic " and ":" in authorization:
			username = authorization[6:].split(":")[0]
			password = authorization[6:].split(":")[1]
	if username != "" and password != "":
		for key, value in identifiants.items():
			if key == username and value == password:
				vb_authorization = True
	if not vb_authorization:
		raise userNotAuthorisedException()
        
@api.exception_handler(userNotAuthorisedException)
def UserNotAuthorisedHandler(
	request: Request,
	exception: userNotAuthorisedException
	):
	"""defines the response of a UserNotAuthorised exception
	"""
	return JSONResponse(
		status_code=401,
		content={
			'url': str(request.url),
			'message': exception.message
		}
	) 
        
api = FastAPI(
	title="API Fraud",
	description="Fraud detection API",
	version="1.0.0")

@api.get('/', name="Welcome message")
async def get_root(authorization=Header("")):
	"""Returns a welcome message
	"""
    checkAuthorization(authorization)

	return {
		"message": "Welcome to the fraud detection API"
	}
    
@api.get('/status', name="API status")
async def get_status(authorization=Header("")):
	"""Returns API status
	"""
    checkAuthorization(authorization)

	return {
		"status": 1
	}
    
@api.get('/test_performance/{model_version}', name="Models test performance")
async def get_test_performance(model_version:str, authorization=Header("")):
	"""Returns model test performance
	"""
    checkAuthorization(authorization)
    
    if model_version.lower() != "v1" and model_version.lower() != "v2":
        raise HTTPException(
            status_code=400,
            detail='The version provided does not exist, please choose between v1 or v2.'
        )
    elif model_version.lower() == "v1":
        return {
            "Fraud transactions":{
                "F1": 0.70,
                "Recall": 0.54,
                "Precision": 1.00
            },
            "Non fraud transactions":{
                "F1": 0.98,
                "Recall": 1.00,
                "Precision": 0.95
            }
        }
    else:
        return {
            "Fraud transactions":{
                "F1": 0.71,
                "Recall": 0.55,
                "Precision": 1.00
            },
            "Non fraud transactions":{
                "F1": 0.81,
                "Recall": 1.00,
                "Precision": 0.68
            }
        }
        
@api.post('/predict/{model_version}', name="Predict a fraud from user datas")
async def post_transaction(model_version:str, transaction:Transaction, authorization=Header("")):
	"""Post a transaction for fraud prediction
	"""
    checkAuthorization(authorization)
    
	if model_version.lower() != "v1" and model_version.lower() != "v2":
        raise HTTPException(
            status_code=400,
            detail='The version provided does not exist, please choose between v1 or v2.'
        )
    else:
        transaction_df = pd.DataFrame(data=transaction.dict())
        transaction_processed = preprocessing_df(transaction_df)
    
    if model_version.lower() == "v1":
        model = model_rfc
    else:
        model = model_lgb
            
    return {
        "Fraud probability": str(round(model.predict_proba(transaction_processed)[0, 1] * 100)) + "%"
    }
    
@api.post('/random_predict/{model_version}', name="Predict a fraud from random selection in dataset")
async def get_random_predict(model_version:str, authorization=Header("")):
	"""Get a prediction from a random transaction selected in the model dataset
	"""
    checkAuthorization(authorization)
    
	if model_version.lower() != "v1" and model_version.lower() != "v2":
        raise HTTPException(
            status_code=400,
            detail='The version provided does not exist, please choose between v1 or v2.'
        )
    else:
        transaction_df = df_models.sample()
        transaction_processed = preprocessing_df(transaction_df)
    
    if model_version.lower() == "v1":
        model = model_rfc
    else:
        model = model_lgb
            
    return {
        "Random transaction": transaction_processed.to_dict("records")[0],
        "Fraud probability": str(round(model.predict_proba(transaction_processed)[0, 1] * 100)) + "%"
    }
    
