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
	url='http://{address}:{port}/random_predict/v1'.format(address=api_address, port=api_port),
	headers= {
		'Authorization': 'Basic alice:YWxpY2U6d29uZGVybGFuZAo='
	}
)

output = '''
================================
	Random predict test
================================

request done at "/random_predict/v1"
| username="alice"
| password="YWxpY2U6d29uZGVybGFuZAo="

expected status_code = 200
actual status_code = {status_code}

==>  {test_status}

'''

# statut de la requête
status_code = r.status_code

# affichage des résultats
if status_code == 200:
	test_status = 'SUCCESS'
else:
	test_status = 'FAILURE'

output = output.format(status_code=status_code, test_status=test_status)
print(output)

# impression dans un fichier
if os.environ.get('LOG') == "1":
	with open('./log/api_test.log', 'a') as file:
		file.write(output)

