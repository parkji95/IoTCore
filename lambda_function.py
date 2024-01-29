import json
import boto3

iot = boto3.client('iot')


def lambda_handler(event, context):
    # TODO implement
    #Manufacturer is the thing group name
    
    http_body = event['body']
    dict = json.loads(http_body)
    clientID = dict['vin']
    thingType = dict['model']
    groupName = dict ['manufacturer']
    
    check_thing_group(groupName)
    #Model is the type name
    check_thing_type(thingType) 
    #Number is the client ID/thing name
    
    
    if (check_thing(clientID) == True):
        #get list of cert ARNS attached to that client
        list_cert = get_certificates(clientID)
        
        #detach certificates from thing so that it can be deleted
        for arn in list_cert:
            detach_thing(clientID, arn)
        
        #extract the cert ids from the arn of certificates in the list
        formatted_list = format_certificates(list_cert)
        
        #go through the list of cert ids and make them inactive and delete the certs
        for cert_id in formatted_list:
            update_cert(cert_id)
            delete_certificates(cert_id)
        
    
    output = create_key_cert(clientID)
    #change thing type after creation 
    update_thing(clientID, thingType)
    #add thing to group
    add_thing_to_thing_group(groupName,clientID)


    
    return {
        'statusCode': 200,
        'body': json.dumps(output)
    }


def update_cert(cert):
    update_cert_response = iot.update_certificate(
    certificateId=cert,
    newStatus='INACTIVE'
)


def delete_certificates (cert):
    delete_response = iot.delete_certificate(
        certificateId = cert,
        forceDelete=True
    )


def detach_thing(clientID, cert_arn):
    response = iot.detach_thing_principal(
            thingName=clientID,
            principal=cert_arn
    )

def format_certificates(list):
    fixed_list = []
    for certID in list:
        #change region and account number to your account/region
        cert = certID.replace('arn:aws:iot:Region:accountNumber:cert/', '')
        fixed_list.append (cert)
    return fixed_list   


def get_certificates (clientID):
    list_things_response = iot.list_thing_principals(
        thingName = clientID    
    )
        
    principals = list_things_response['principals']
    return principals



def check_thing (clientID):
    #returns dict with keys
    thing_response = iot.list_things()
    thing_list = thing_response['things']
    
    exists = False
    #go through list of thingnames
    for thing in thing_list:
        name = thing["thingName"]
        
        #if condition to check if the thing name matches the clients ID
        if (clientID == name):
            exists = True
    
    #after going through list, if no thing exists, create the thing
    if (exists == False):
        create_thing(clientID)
        #create_thing_group_response = iot.create_thing_group(
        #    thingGroupName = manufacturer
        #)
        print ("Created the Thing : " + "'" + clientID + "'")
    else:
        print ("Thing " + "'" + clientID + "'" + " already exists")

    return exists


def check_thing_group (manufacturer):
    #returns dict with keys
    groupname_response = iot.list_thing_groups()
    group_list = groupname_response['thingGroups']
    
    exists = False
    #go through list of groupnames
    for group in group_list:
        name =group["groupName"]
        
        #if condition to check if the group name matches the clients manufacture
        if (manufacturer == name):
            exists = True
    
    #after going through list, if no group exists, create the group
    if (exists == False):
        create_thing_group_response = iot.create_thing_group(
            thingGroupName = manufacturer
        )
        print ("Created the Thing Group: " + "'" + manufacturer + "'")
    else:
        print ("Group " + "'" + manufacturer + "'" + " already exists")
    


def check_thing_type(model):
    thing_type_response = iot.list_thing_types()
    thing_type_list = thing_type_response['thingTypes']
    
    exists = False
    #go through list of thing type
    for type in thing_type_list:
        name =type["thingTypeName"]
        #if condition to check if the thing type matches the clients model
        if (model == name):
            exists = True
    
    #after going through list, if no type exists, create the type
    if (exists == False):
        create_thing_type_response = iot.create_thing_type(
            thingTypeName = model
        )
        print ("Created the Thing Type: " + "'" + model + "'")
    else:
        print ("Thing type " + "'" + model + "'" + " already exists")


def create_thing(clientID):
    create_thing_response = iot.create_thing (
        thingName = clientID    
    )
    print ("Successfully created thing: " + "'" + clientID + "'")
    
    

def create_policy ():
    policy_response = iot.create_policy(
        policyName='devicePolicy',
        policyDocument= '{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Action": "*","Resource": "*"}]}'
    )

    
    return(policy_response['policyName'])

def attach_thing_principal (thing, certArn):
    attach_thing_principal_response = iot.attach_thing_principal(
        thingName = thing,
        principal = certArn
        
    ) 
    print ("Successfully attached certificate: "  + "'" + certArn + "'"  + " to thing: " + "'" + thing + "'")

def create_key_cert(thing):
    create_key_response = iot.create_keys_and_certificate(
        setAsActive=True
    )

    output = {
        'certPem': create_key_response['certificatePem'],
        'privateKey': create_key_response['keyPair']['PrivateKey']
    }
    
    #get cert arn to attach cert to policy
    device_cert_arn = (create_key_response['certificateArn'])
    #create policy
    policy_name = 'devicePolicy' #create_policy()
    #attach policy to cert 
    attach_policy(policy_name, device_cert_arn)
    
    
    attach_thing_principal(thing, device_cert_arn)
    
    return (output)



def attach_policy(policy_name, certArn):
    attach_policy_response = iot.attach_policy(
        policyName = policy_name,
        target = certArn
    )
    print ("Successfully attached policy: " + "'" + policy_name + "'" + " to certificate: " + "'" + certArn + "'")



def update_thing(name, type):
    update_thing_response = iot.update_thing(
        thingName= name,
        thingTypeName= type
    )
    print ("Successfully changed the thing type of thing: " + "'" + name + "'" + " to type: " + "'" + type + "'")

def add_thing_to_thing_group(group, thing):
    add_thingto_thing_group_response = iot.add_thing_to_thing_group(
        thingGroupName = group,
        thingName = thing
    )
    print("Successfully added thing: " + "'" + thing + "'" + " to group: " + "'" + group + "'")
    
    
#root certificate:
#https://www.amazontrust.com/repository/AmazonRootCA1.pem