
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#v2
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json

import os.path
from data import *
from tokengeneration import token_generation
from check import checker
from connection import connect_message
#from certgeneration import cert_generation



##########################################################################
#Steps:
#1 Get tokens (tokengeneration.py -> token_generation())
#2 Check for certs, if not create certs depending on current status (check.py -> checker() -> cert_generation() -> file_generation)
#3 connect (connection.py -> connect_message())


#get token using token_generation and add to variable token

#token = (token_generation(token_data))
checker(data, path)
connect_message()


##########################################################################

