Description: This is used for creating and registering a client device as a Thing in IoT core. The "vin" set in "data.py" is the "Thing Name", the "model" the "Thing Type" and the "Manufacturer" the "Group" of the IoT Thing.

"main.py" runs functions found in "check.py" and "connection.py"


"check.py" checks to see if the client device already has certificates downloaded and in its local directory. 
In the case that the certificates do not exist, then the "cert_generation()" function is called, where certificates are created after an IoT Thing is also created.

The "cert_generation()" function makes an http post request to an existing API gateway which is a trigger to the "lambda_function.py" w;hich provisions and IoT Thing on your behalf
