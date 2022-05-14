import pandas as pd
import joblib


ORIGINAL_DATA = pd.read_csv("https://assets-datascientest.s3-eu-west-1.amazonaws.com/de/total/fraud.csv",
                            parse_dates=["signup_time","purchase_time"],
                            dtype={"purchase_value": int,
                                   "source": str,
                                   "browser": str,
                                   "sex": str,
                                   "age": int,
                                   "is_fraud": int})


MODEL_V1_RESULTS = {"fraud_transactions": {"precision": 0.99,
                    "recall": 0.54,
                    "f1_score": 0.70},
                    "non_fraud_transactions": {"precision": 0.95,
                    "recall": 1.00,
                    "f1_score": 0.98}}


MODEL_V2_RESULTS = {"fraud_transactions": {"precision": 1.00,
                    "recall": 0.54,
                    "f1_score": 0.70},
                    "non_fraud_transactions": {"precision": 0.95,
                    "recall": 1.00,
                    "f1_score": 0.98}}


MODEL_V1 = joblib.load("fraud_rfc.pkl")


MODEL_V2 = joblib.load("fraud_lgb.pkl")


def _encode_categorical_feature(original_df, feature, category):
    df = original_df.copy()
    df[f"{feature}_{category}"] = 0
    df[f"{feature}_{category}"] = df[f"{feature}"].apply(lambda x: 1 if x == f"{category}" else 0)
    return df


def preprocess_new_data(original_df):
    """
    Preprocess new data by accentuating the cyclical character of temporal data
    Input: original_df pd.DataFrame
    Ouput: df pd.DataFrame
    """
    df = original_df.copy()
    df["purchase_date"] = df.purchase_time.dt.date
    df["purchase_hour"] = df.purchase_time.dt.hour
    df["purchase_weekday"] = df.purchase_time.dt.weekday
    df["purchase_month"] = df.purchase_time.dt.month
    df["purchase_day"] = df.purchase_time.dt.day
    df["signup_date"] = df.signup_time.dt.date
    df["days_till_signup"] = df.purchase_date - df.signup_date
    df.days_till_signup = df.days_till_signup.dt.days
    df["sex"] = df["sex"].replace(["M", "F"], [0,1])
    for source in ["Direct", "SEO"]:
        df = _encode_categorical_feature(df, "source", source)
    for browser in ["FireFox", "IE", "Opera", "Safari"]:
        df = _encode_categorical_feature(df, "browser", browser)
    df = df[["days_till_signup", "purchase_month", "purchase_day", "purchase_weekday", 
             "purchase_hour", "purchase_value", "age", "source_Direct", "source_SEO",
             "browser_FireFox", "browser_IE", "browser_Opera", "browser_Safari", "sex"]]
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
