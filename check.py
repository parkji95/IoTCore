
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#v2
from awscrt import io, mqtt, auth, http
#from awsiot import mqtt_connection_builder
import time as t
import json
import os.path
from data import *
from certgeneration import cert_generation
#from tokengeneration import token_generation



##########################################################################
#def checker (data, path, token):
def checker (data, path):
    check_cert = os.path.isfile(PATH_TO_CERTIFICATE)

    check_key = os.path.isfile(PATH_TO_PRIVATE_KEY)

    if (check_cert == False and check_key == False):
        #maybe delete the existing files in the local directory first
        #message = cert_generation(data, path, token)
        message = cert_generation(data, path)

        print ("Code:", message['code'])
        print ("Message:", message['message'])
        if (message['code'] != 200):
            quit()    
    else:
        print ("Certificates already exists")



