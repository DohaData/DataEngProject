import os
import requests
import base64
import time


output = '''
============================
    Prediction test
============================

request done at "/predict"
| username={username}
| password={password}

expected fraud probability = {expected_fraud_probability}
actual fraud probability = {actual_fraud_probability}

expected is fraud = {expected_is_fraud}
actual is fraud = {actual_is_fraud}

==>  {test_status}

'''


API_ADDRESS = "fraud_detection_api"
API_PORT = 8000


def save_output(output):
    # impression dans un fichier
    if os.environ.get('LOG') == '1':
        print('SAVING LOGS')
        with open('/home/logs/api_test.log', 'a') as file:
            file.write(output)


def test_prediction(username, password, model_version="v1",
                     fraud_probability=0.35,
                     is_fraud=0):

    data = {"user_id": 123,
            "signup_time": "2022-04-30T11:35:43.727Z",
            "purchase_time": "2022-04-30T11:35:43.727Z",
            "purchase_value": 40,
            "device_id": "XX",
            "source": "XX",
            "browser": "XX",
            "sex": "F",
            "age": 30,
            "ip_address": "XX"}
    auth_phrase = ":".join([username, password]).encode("utf-8")
    time.sleep(1)
    r = requests.post(
        url='http://{address}:{port}/predict/{model_version}'.format(address=API_ADDRESS, port=API_PORT, model_version=model_version),
        headers={"accept":"application/json",
                 "Content-Type":"application/json",
                 "Authorization":base64.b64encode(auth_phrase).decode("utf-8")},
        json = data
    )

    prediction_results = r.json()

    if (prediction_results["fraud_probability"] == fraud_probability) and (prediction_results["is_fraud"] == is_fraud):
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    save_output(output.format(username=username,
                              password=password,
                              expected_fraud_probability=fraud_probability,
                              actual_fraud_probability=prediction_results["fraud_probability"],
                              expected_is_fraud=is_fraud,
                              actual_is_fraud=prediction_results["is_fraud"],
                              test_status=test_status))
    print(output.format(username=username,
                        password=password,
                        expected_fraud_probability=fraud_probability,
                        actual_fraud_probability=prediction_results["fraud_probability"],
                        expected_is_fraud=is_fraud,
                        actual_is_fraud=prediction_results["is_fraud"],
                        test_status=test_status))

################ executing_tests ###################
test_prediction("alice", "wonderland", model_version="v1", fraud_probability=0.35, is_fraud=0)
