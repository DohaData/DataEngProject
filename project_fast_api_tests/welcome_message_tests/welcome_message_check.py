import os
import requests
import base64
import time


output = '''
============================
    Welcome message test
============================

request done at "/"
| username={username}
| password={password}

expected result = {expected_result}
actual restult = {actual_result}

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


def test_welcome_message(username, password, expected_result=200):
    auth_phrase = ":".join([username, password]).encode("utf-8")
    time.sleep(1)
    r = requests.get(
        url='http://{address}:{port}/'.format(address=API_ADDRESS, port=API_PORT),
        headers={"Authorization":base64.b64encode(auth_phrase).decode("utf-8")}
    )

    actual_result = r.status_code

    if actual_result == expected_result:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    save_output(output.format(username=username,
                              password=password,
                              expected_result=expected_result,
                              actual_result=actual_result,
                              test_status=test_status))
    print(output.format(username=username,
                        password=password,
                        expected_result=expected_result,
                        actual_result=actual_result,
                        test_status=test_status))

################ executing_tests ###################
test_welcome_message("alice", "wonderland", expected_result=200)
test_welcome_message("ani", "banani", expected_result=401)
