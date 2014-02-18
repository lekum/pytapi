pytapi
======

Library that uses TSAPI calls to interface with AES

Functionality
-------------

Currently, the functionality of TSAPI exposed by this API is:

- cstaConnect()
- cstaMakeCall()
- cstaAbortConnection()

Installation
------------

Requires the TSAPI client library `csta.dll` registered in the machine (Windows OS).

Example usage
-------------

	import pytapi
	import time
	import struct

	conn = pytapi.CstaConnection("username", "password", "example")
	ret = conn.connect("AVAYA#AESP0#CSTA#AESP01")
	print("Return of connect:", ret)
	time.sleep(4)
	ret_code, buf, num_e = conn.check_event()
	binary_format = "LHHL21s21s21s21s"
	ret_struct = struct.unpack(binary_format, buf[0:struct.calcsize(binary_format)])
	for x in ret_struct:
	    if isinstance(x, bytes):
	        print(x.decode())
	    else:
	        print(x)
	ret = conn.make_call("70233", "70218")
	print("Return of make_call:", ret)
	time.sleep(3)
	ret = conn.abort_connection()
	print("Return of abort_connection:", ret)
