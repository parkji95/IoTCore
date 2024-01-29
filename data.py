
##########################################################################################


#Car data used for IoT thing generation

#data = {
#    "vin": "7777",
#    "model": "Model3",
#    "manufacturer": "Tesla"
#}

#data = {
#    "vin": "1111",
#    "model": "Avante",
#    "manufacturer": "Kia"
#}

#data = {
#    "vin": "9999",
#    "model": "GTR",
#    "manufacturer": "Nissan"
#}



data = {
    "vin": "3333",
    "model": "K5",
    "manufacturer": "Kia"
}


CLIENT_ID = data['vin']
#IoT Core Endpoint

ENDPOINT = "<your IoT endpoint found in aws console under settings in IoT Core>"

#PATH_TO_CERTIFICATE = path['certificate']#certificate_name
PATH_TO_CERTIFICATE = "/home/iotLambda/certificates/"+ data['vin'] + "/" + CLIENT_ID + "-certificate.pem.crt"
#PATH_TO_PRIVATE_KEY = path['key']#private_key_name
PATH_TO_PRIVATE_KEY = "/home/iotLambda/certificates/"+ data['vin'] + "/" + CLIENT_ID + "-private.pem.key"
#PATH_TO_AMAZON_ROOT_CA_1 = path ['root']#root_ca_name
PATH_TO_AMAZON_ROOT_CA_1 = "/home/iotLambda/certificates/AmazonRootCA1.pem"


#Certificate path directories
path = {
    'cert_path': PATH_TO_CERTIFICATE,
    'key_path': PATH_TO_PRIVATE_KEY,
    'root_path': PATH_TO_AMAZON_ROOT_CA_1 
}

