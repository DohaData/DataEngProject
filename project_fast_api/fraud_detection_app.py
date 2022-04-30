from fastapi import FastAPI, HTTPException, Request, Depends
import asyncio
from pydantic import BaseModel
from typing import Literal
import pandas as pd
from datetime import datetime
import base64
from fraud_detection_models import (MODEL_V1_RESULTS, MODEL_V2_RESULTS,
                                   predict_using_random_line,
                                   predict_using_user_entry)


USERS_DATABASE = {"alice":"wonderland",
                 "bob":"builder",
                 "clementine":"mandarine"}


class ModelResults(BaseModel):
    precision: float
    recall: float
    f1_score: float


class FraudModelEntryData(BaseModel):
    user_id: int
    signup_time: datetime
    purchase_time: datetime
    purchase_value: int
    device_id: str
    source: str
    browser: str
    sex: Literal["F", "M"]
    age: int
    ip_address: str


class FraudModelOutputData(BaseModel):
    used_data: FraudModelEntryData
    fraud_probability: float
    is_fraud: int


api = FastAPI(title="Fraud detection API",
              description="API to detect fraudulent transactions",
              version="1.0.0")


def authentify_user(request: Request)->str:
    is_user_authentified = False
    encoded_auth_info = request.headers.get("Authorization")
    try:
        auth_info = base64.b64decode(encoded_auth_info).decode("utf-8")
        username, password = auth_info.rstrip().strip().split(":")
        is_user_authentified = username in USERS_DATABASE and USERS_DATABASE[username] == password
    except Exception as e:
        raise HTTPException(
                status_code=403,
                detail="Authentication failed")
    if not is_user_authentified:
        raise HTTPException(
		status_code=401,
		detail="Unauthorized")
    return username


def check_avaible_models(model_version: str):
    if model_version not in ["v1", "v2"]:
        raise HTTPException(
                status_code=401,
                detail="Unfound model")


@api.get("/status")
async def check_app_status()->str:
    return "1"


@api.get("/")
async def welcome_message(username: str = Depends(authentify_user))->str:
    """
    Welcome message to check that the app is properly running
    """
    return f"Hello {username}, fraud detection app is running !"


@api.get("/test_performance/{model_version}", dependencies = [Depends(authentify_user)])
async def render_model_test_performance(model_version: str)->ModelResults:
    """
    Render model recorded test performance
    """
    check_avaible_models(model_version)
    model_results = MODEL_V1_RESULTS if model_version == "v1" else MODEL_V2_RESULTS
    return ModelResults(**model_results)


@api.get("/random_predict/{model_version}", dependencies = [Depends(authentify_user)])
async def compute_prediction_on_random_data(model_version: str)->FraudModelOutputData:
    """
    Predict on random original data
    """
    check_avaible_models(model_version)
    chosen_data, fraud_probability, is_fraud = predict_using_random_line(model_version)
    results = dict()
    results["used_data"] = FraudModelEntryData(**chosen_data.to_dict("records")[0])
    results["fraud_probability"] = fraud_probability
    results["is_fraud"] = is_fraud
    return FraudModelOutputData(**results)


@api.post("/predict/{model_version}", dependencies = [Depends(authentify_user)])
async def predict_on_user_entry(model_version: str,
                                entry_data: FraudModelEntryData)->FraudModelOutputData:
    """
    Predict on user entry data
    """
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
