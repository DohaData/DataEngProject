import os
import requests


output = '''
============================
    Status test
============================

request done at "/status"

expected result = {expected_result}
actual result = {actual_result}

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


def test_status(expected_result="1"):
    r = requests.get(
        url='http://{address}:{port}/status'.format(address=API_ADDRESS, port=API_PORT)
    )

    actual_result = r.text.replace('"', '')

    if actual_result == expected_result:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    save_output(output.format(expected_result=expected_result,
                              actual_result=actual_result,
                              test_status=test_status))
    print(output.format(expected_result=expected_result,
                        actual_result=actual_result,
                        test_status=test_status))

################ executing_tests ###################
test_status(expected_result="1")
