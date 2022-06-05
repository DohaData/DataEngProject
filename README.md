# DataEngProject

`DataEngProject` is a fraud transactions detection API developed with the FastAPI 
Python framework. The user can enter the characteristics of a transaction such as 
the age of the customer, the date, the browser, the purchase value... and get a 
probability of fraud.

The project also contains an example of API deployment health checks managed in 
a docker-compose file as well as a Kubernetes deployment files structure.

## API

Here are the different API routes possible, all routes require authentication except 
the /status one:
- /status -> return 1 if API is running and up
- / -> return a welcome message
- /test_performance/{model_version} -> return the performance (precision, recall 
and f1_score) of the chosen model on the evaluation dataset
- /random_predict/{model_version} -> return the fraud prediction (probability + class) 
for the chosen model and a random transaction chosen in the original dataset
- /predict/{model_version} -> return the fraud prediction for the chosen model and a 
transaction entered by the user in the body request (JSON format, 7 mandatory 
attributes, see the example section)

Two different machine learning models have been trained for this API and can be 
called for the predictions, {model_version} stands for the chosen model:
- {model_version} = v1 -> A Random Forest Classifier
- {model_version} = v2 -> A Light Gradient Boosting Machine

Authentication can be done with three users:
- alice:YWxpY2U6d29uZGVybGFuZAo=
- bob:Ym9iOmJ1aWxkZXIK
- clementine:Y2xlbWVudGluZTptYW5kYXJpbmUK

## Examples

Use API locally:

```text
cd project_fast_api
uvicorn fraud_detection_app:api --reload

curl -X 'GET' \
  'http://localhost:8000/status'
  
curl -X 'GET' \
  'http://localhost:8000/' \
  -H 'authentication: Basic alice:YWxpY2U6d29uZGVybGFuZAo='
  
curl -X 'GET' \
  'http://localhost:8000/test_performance/v2' \
  -H 'authentication: Basic alice:YWxpY2U6d29uZGVybGFuZAo='
  
curl -X 'GET' \
  'http://localhost:8000/random_predict/v2' \
  -H 'authentication: Basic alice:YWxpY2U6d29uZGVybGFuZAo='

curl -X 'POST' \
  'http://localhost:8000/predict/v2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "signup_time": "2022-04-30T11:35:43.727Z",
  "purchase_time": "2022-04-30T11:38:43.727Z",
  "purchase_value": 40,
  "source": "Ads",
  "browser": "Chrome",
  "sex": "F",
  "age": 30
}' -H 'authentication: Basic alice:YWxpY2U6d29uZGVybGFuZAo='
```

Launch API tests (Docker must be installed on the machine and Docker daemon 
is running):

```text
cd project_fast_api_tests
./setup.sh
```

Deployment with Kubernetes:

```text
cd project_fast_api_kubernetes
kubectl create -f fraud-detection-deployment.yml
kubectl create -f fraud-detection-service.yml
kubectl create -f fraud-detection-ingress.yml
```

