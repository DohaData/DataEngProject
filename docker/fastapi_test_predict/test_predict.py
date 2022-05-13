import os
import requests
import time

# définition de l'adresse de l'API
api_address = 'api'
# port de l'API
api_port = 8000

# Etape d'attente que l'API soit up
status_code = 0
i = 0
while status_code != 200 and i < 10:
	try:
		r = requests.get(url='http://{address}:{port}/status'.format(address=api_address, port=api_port))
		status_code = r.status_code
		time.sleep(1)
	except Exception as e:
		time.sleep(1)
	i += 1

# ============================================================================================
# Premier cas de test (passant)
# ============================================================================================

# requête
r = requests.get(
	url='http://{address}:{port}/predict/v1'.format(address=api_address, port=api_port),
	headers= {
		'Authorization': 'Basic alice:YWxpY2U6d29uZGVybGFuZAo='
	},
    json= {
		'signup_time': '2020-01-08 18:52:50',
		'purchase_time': '2020-01-08 18:59:37',
		'purchase_value': 30,
        'source': 'SEO',
		'browser': 'Chrome',
		'sex': 'M',
        'age': 26
	}
)

output = '''
================================
	Predict test
================================

request done at "/predict/v1"
| username="alice"
| password="YWxpY2U6d29uZGVybGFuZAo=",
| transaction={
		'signup_time': '2020-01-08 18:52:50',
		'purchase_time': '2020-01-08 18:59:37',
		'purchase_value': 30,
        'source': 'SEO',
		'browser': 'Chrome',
		'sex': 'M',
        'age': 26
	}

expected probability = 12%
actual probability = {probability}

==>  {test_status}

'''

# statut de la requête
probability = r.json().get("Fraud probability")

# affichage des résultats
if probability == "12%":
	test_status = 'SUCCESS'
else:
	test_status = 'FAILURE'

output = output.format(probability=probability, test_status=test_status)
print(output)

# impression dans un fichier
if os.environ.get('LOG') == "1":
	with open('./log/api_test.log', 'a') as file:
		file.write(output)

# ============================================================================================
# Deuxième cas de test (passant)
# ============================================================================================

# requête
r = requests.get(
	url='http://{address}:{port}/predict/v2'.format(address=api_address, port=api_port),
	headers= {
		'Authorization': 'Basic alice:YWxpY2U6d29uZGVybGFuZAo='
	},
    json= {
		'signup_time': '2020-01-08 18:52:50',
		'purchase_time': '2020-01-08 18:59:37',
		'purchase_value': 30,
        'source': 'SEO',
		'browser': 'Chrome',
		'sex': 'M',
        'age': 26
	}
)

output = '''
================================
	Predict test
================================

request done at "/predict/v2"
| username="alice"
| password="YWxpY2U6d29uZGVybGFuZAo=",
| transaction={
		'signup_time': '2020-01-08 18:52:50',
		'purchase_time': '2020-01-08 18:59:37',
		'purchase_value': 30,
        'source': 'SEO',
		'browser': 'Chrome',
		'sex': 'M',
        'age': 26
	}

expected probability = 16%
actual probability = {probability}

==>  {test_status}

'''

# statut de la requête
probability = r.json().get("Fraud probability")

# affichage des résultats
if probability == "16%":
	test_status = 'SUCCESS'
else:
	test_status = 'FAILURE'

output = output.format(probability=probability, test_status=test_status)
print(output)

# impression dans un fichier
if os.environ.get('LOG') == "1":
	with open('./log/api_test.log', 'a') as file:
		file.write(output)

# ============================================================================================
# Troisième cas de test (non passant)
# ============================================================================================

# requête
r = requests.get(
	url='http://{address}:{port}/predict/v1'.format(address=api_address, port=api_port),
	headers= {
		'Authorization': 'Basic alice:YWxpY2U6d29uZGVybGFuZAo='
	},
    json= {
		'signup_time': '2020-01-08 18:52:50',
		'purchase_time': '2020-01-08 18:59:37',
		'purchase_value': 30,
        'source': 'SEO',
		'browser': 'Edge',
		'sex': 'M',
        'age': 26
	}
)

output = '''
================================
	Predict test
================================

request done at "/predict/v1"
| username="alice"
| password="YWxpY2U6d29uZGVybGFuZAo=",
| transaction={
		'signup_time': '2020-01-08 18:52:50',
		'purchase_time': '2020-01-08 18:59:37',
		'purchase_value': 30,
        'source': 'SEO',
		'browser': 'Edge',
		'sex': 'M',
        'age': 26
	}

expected message = "Browser must be Chrome, Opera, Safari, IE or FireFox"
actual message = {message}

==>  {test_status}

'''

# statut de la requête
message = r.content

# affichage des résultats
if message == "Browser must be Chrome, Opera, Safari, IE or FireFox":
	test_status = 'SUCCESS'
else:
	test_status = 'FAILURE'

output = output.format(message=message, test_status=test_status)
print(output)

# impression dans un fichier
if os.environ.get('LOG') == "1":
	with open('./log/api_test.log', 'a') as file:
		file.write(output)

