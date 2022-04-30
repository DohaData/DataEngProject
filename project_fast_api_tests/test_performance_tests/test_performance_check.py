import os
import requests
import base64
import time


output = '''
============================
    Test performance test
============================

request done at "/test_performance"
| username={username}
| password={password}

expected precision = {expected_precision}
actual precision = {actual_precision}

expected recall = {expected_recall}
actual recall = {actual_recall}

expected f1 score = {expected_f1_score}
actual f1 score = {actual_f1_score}


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


def test_performance(username, password,
                     model_version="v1",
                     precision=0.99,
                     recall=0.55,
                     f1_score=0.71):
    auth_phrase = ":".join([username, password]).encode("utf-8")
    time.sleep(1)
    r = requests.get(
        url='http://{address}:{port}/test_performance/{model_version}'.format(address=API_ADDRESS, port=API_PORT, model_version=model_version),
        headers={"Authorization":base64.b64encode(auth_phrase).decode("utf-8")}
    )

    performance = r.json()

    if (performance["precision"] == precision) and (performance["recall"] == recall) and (performance["f1_score"] == f1_score):
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    save_output(output.format(username=username,
                              password=password,
                              expected_precision=precision,
                              actual_precision=performance["precision"],
                              expected_recall=recall,
                              actual_recall=performance["recall"],
                              expected_f1_score=f1_score,
                              actual_f1_score=performance["f1_score"],
                              test_status=test_status))
    print(output.format(username=username,
                        password=password,
                        expected_precision=precision,
                        actual_precision=performance["precision"],
                        expected_recall=recall,
                        actual_recall=performance["recall"],
                        expected_f1_score=f1_score,
                        actual_f1_score=performance["f1_score"],
                        test_status=test_status))

################ executing_tests ###################
test_performance("alice", "wonderland", model_version="v1", precision=0.99, recall=0.55, f1_score=0.71)

