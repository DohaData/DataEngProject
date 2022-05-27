from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
import asyncio
from pydantic import BaseModel, validator
import pandas as pd
from datetime import datetime
from fraud_detection_models import (MODEL_V1_RESULTS, MODEL_V2_RESULTS,
                                   predict_using_random_line,
                                   predict_using_user_entry)


USERS_DATABASE = {
            "alice": "YWxpY2U6d29uZGVybGFuZAo=",
            "bob": "Ym9iOmJ1aWxkZXIK",
            "clementine": "Y2xlbWVudGluZTptYW5kYXJpbmUK"
            }


class ModelResults(BaseModel):
    precision: float
    recall: float
    f1_score: float


class ModelResultsByTransactionType(BaseModel):
    fraud_transactions: ModelResults
    non_fraud_transactions: ModelResults


class FraudModelEntryData(BaseModel):
    purchase_time: datetime
    signup_time: datetime
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


class FraudModelOutputData(BaseModel):
    used_data: FraudModelEntryData
    fraud_probability: float
    is_fraud: int


class UserNotAuthorisedException(Exception):
	"""defines an exception for the user who doesn't pass the authorization
	"""
	def __init__(self):
		self.message = "User not authorised"


api = FastAPI(title="Fraud detection API",
              description="API to detect fraudulent transactions",
              version="1.0.0")


def check_authorization(authorization):
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
		for key, value in USERS_DATABASE.items():
			if key == username and value == password:
				vb_authorization = True
	if not vb_authorization:
		raise UserNotAuthorisedException()


@api.exception_handler(UserNotAuthorisedException)
def UserNotAuthorisedHandler(
	request: Request,
	exception: UserNotAuthorisedException
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


def check_avaible_models(model_version: str):
    if model_version not in ["v1", "v2"]:
        raise HTTPException(
                status_code=401,
                detail="Unfound model")


@api.get("/status", name="API status")
async def check_app_status()->str:
    return "1"


@api.get("/", name="Welcome message")
async def welcome_message(authentication=Header(""))->str:
    """
    Welcome message to check that the app is properly running
    """
    check_authorization(authentication)
    return f"Hello! fraud detection app is running"


@api.get("/test_performance/{model_version}", name="Models test performance")
async def render_model_test_performance(model_version: str, 
                                        authentication=Header(""))->ModelResultsByTransactionType:
    """
    Render model recorded test performance
    """
    check_authorization(authentication)
    check_avaible_models(model_version)
    model_results = MODEL_V1_RESULTS if model_version == "v1" else MODEL_V2_RESULTS
    return ModelResultsByTransactionType(**model_results)


@api.get("/random_predict/{model_version}", name="Predict a fraud from random selection in dataset")
async def compute_prediction_on_random_data(model_version: str, 
                                            authentication=Header(""))->FraudModelOutputData:
    """
    Predict on random original data
    """
    check_authorization(authentication)
    check_avaible_models(model_version)
    chosen_data, fraud_probability, is_fraud = predict_using_random_line(model_version)
    results = dict()
    results["used_data"] = FraudModelEntryData(**chosen_data.to_dict("records")[0])
    results["fraud_probability"] = fraud_probability
    results["is_fraud"] = is_fraud
    return FraudModelOutputData(**results)


@api.post("/predict/{model_version}", name="Predict a fraud from user datas")
async def predict_on_user_entry(model_version: str,
                                entry_data: FraudModelEntryData, 
                                authentication=Header(""))->FraudModelOutputData:
    """
    Predict on user entry data
    """
    check_authorization(authentication)
    check_avaible_models(model_version)
    entry_data_df = pd.DataFrame.from_records([entry_data.dict()])
    try:
        fraud_probability, is_fraud = predict_using_user_entry(model_version,
                                                               entry_data_df)
    except:
        raise HTTPException(
                status_code=400,
                detail="Invalid data used for prediction")
    results = dict()
    results["used_data"] = FraudModelEntryData(**entry_data.dict())
    results["fraud_probability"] = fraud_probability
    results["is_fraud"] = is_fraud
    return FraudModelOutputData(**results)
