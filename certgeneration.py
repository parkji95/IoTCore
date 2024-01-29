import requests
import json
import os

##########################################################################################

#original
#def cert_generation(data, path, token): 	
def cert_generation(data, path): 	
	endpoint_url = 'API Gateway url pointing to your Lambda Function'
	headers = {
		'content-type': 'application/json',
		#'authorization-token': token
	}
	response = requests.post(endpoint_url, data=json.dumps(data), headers=headers)
	
	if (response.status_code == 200):		
		response_dict = response.json()
		private_key = response_dict['privateKey']
		cert_pem = response_dict['certPem']
		file_generation(cert_pem, private_key, path, data)
		
		message = {
			'code': response.status_code,
			'message': "Successfully created certificates"
		}
		
		return message
	else:
		
		message = {
			'code': response.status_code,
			'message': response.text
		}
		return message


############Thing to note: if doing http get, the resulting dict and key should be response_dict['body']['certPem'] but if using post the dict and key is response_dict['certPem']
def file_generation(cert_pem, private_key, path, data):

	clientID = data["vin"]
	root_url = 'https://www.amazontrust.com/repository/AmazonRootCA1.pem'




	response_root = requests.get(root_url)
	root_ca = response_root.text

	directory = "/home/iotLambda/certificates/" + clientID
	os.mkdir(directory)


	certificate_name = path['cert_path']
	private_key_name = path['key_path']
	root_ca_name = path ['root_path']


	f = open(certificate_name, 'w')
	f.write(cert_pem)
	f.close


	g = open(private_key_name, 'w')
	g.write(private_key)
	g.close


	h = open(root_ca_name, 'w')
	h.write(root_ca)
	h.close
