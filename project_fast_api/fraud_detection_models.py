import pandas as pd
import numpy as np
import joblib


ORIGINAL_DATA = pd.read_csv("https://assets-datascientest.s3-eu-west-1.amazonaws.com/de/total/fraud.csv",
                            parse_dates=["signup_time","purchase_time"],
                            dtype={"user_id":int,
                                   "purchase_value": int,
                                   "device_id": str,
                                   "source": str,
                                   "browser": str,
                                   "sex": str,
                                   "age": int,
                                   "api_address": str,
                                   "is_fraud": int})


MODEL_V1_RESULTS = {"precision": 0.99,
                    "recall": 0.55,
                    "f1_score": 0.71}


MODEL_V2_RESULTS = {"precision": 0.99,
                    "recall": 0.55,
                    "f1_score": 0.71}


MODEL_V1 = joblib.load("fraud_lgb.pkl")


MODEL_V2 = joblib.load("fraud_lgb.pkl")


def preprocess_new_data(original_df):
    """
    Preprocess new data by accentuating the cyclical character of temporal data
    Input: original_df pd.DataFrame
    Ouput: df pd.DataFrame
    """
    df = original_df.copy()
    df['delay_signup_purchase'] = (df['signup_time'] - df['purchase_time']).dt.seconds
    for col_prefix in ['signup', 'purchase']:
        df[f'{col_prefix}_year'] = df[f'{col_prefix}_time'].dt.year
        df[f'{col_prefix}_month'] = df[f'{col_prefix}_time'].dt.month
        df[f'{col_prefix}_weekday'] = df[f'{col_prefix}_time'].dt.weekday
        df[f'cos_{col_prefix}_month'] = np.cos(2.*np.pi*df[f'{col_prefix}_month']/12.)
        df[f'sin_{col_prefix}_month'] = np.sin(2.*np.pi*df[f'{col_prefix}_month']/12.)
        df[f'{col_prefix}_hour'] = df[f'{col_prefix}_time'].dt.hour
        df[f'cos_{col_prefix}_hour'] = np.cos(2.*np.pi*df[f'{col_prefix}_hour']/24.)
        df[f'sin_{col_prefix}_hour'] = np.sin(2.*np.pi*df[f'{col_prefix}_hour']/24.)
        df[f'{col_prefix}_minute'] = df[f'{col_prefix}_time'].dt.minute
        df[f'cos_{col_prefix}_minute'] = np.cos(2.*np.pi*df[f'{col_prefix}_minute']/60.)
        df[f'sin_{col_prefix}_minute'] = np.sin(2.*np.pi*df[f'{col_prefix}_minute']/60.)
        df[f'{col_prefix}_int_value'] = df[f'{col_prefix}_time'].apply(lambda x: x.value)
        df = df.drop(columns=[f'{col_prefix}_time'])
    df = df[['purchase_value', 'age', 'delay_signup_purchase', 'signup_hour',
           'signup_minute', 'cos_signup_minute', 'sin_signup_minute',
           'signup_int_value', 'purchase_hour', 'sin_purchase_hour',
           'purchase_minute', 'cos_purchase_minute', 'purchase_int_value']]
    return df


def predict_using_random_line(model_version):
    """
    Take a random line from the original dataframe
    and predict a fraud probability
    Input: model_version Literal["v1", "v2"]
    Output: chosen_data pd.DataFrame, fraud_probability, is_fraud
    """
    chosen_data = ORIGINAL_DATA.sample(n=1)
    preprocess_data = preprocess_new_data(chosen_data)
    used_model = MODEL_V1 if model_version == "v1" else MODEL_V2
    fraud_probability = round(used_model.predict_proba(preprocess_data)[0,1], 2)
    is_fraud = used_model.predict(preprocess_data)[0]
    return chosen_data, fraud_probability, is_fraud


def predict_using_user_entry(model_version, user_data):
    """
    Take user data
    and predict a fraud probability
    Input: model_version Literal["v1", "v2"], user_data pd.DataFrame
    Output: fraud_probability, is_fraud
    """
    preprocess_data = preprocess_new_data(user_data)
    used_model = MODEL_V1 if model_version == "v1" else MODEL_V2
    fraud_probability = round(used_model.predict_proba(preprocess_data)[0,1], 2)
    is_fraud = used_model.predict(preprocess_data)[0]
    return fraud_probability, is_fraud

