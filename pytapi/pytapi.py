"""
Python TSAPI API

Library that uses TSAPI calls to interface with AES
Copyright (C) 2013 Alejandro Guirao Rodríguez
"""

import time
from ctypes import *


class CstaConnection:
    """
    Class that represents a CSTA Connection
    """

    """
    Global constants
    """
    csta = windll.csta32
    ST_CSTA = c_ushort(1)
    LIB_GEN_ID = c_ushort(1)
    ACS_LEVEL1 = c_ushort(1)
    SEND_QUEUE_SIZE = c_ushort(0)
    RECEIVE_QUEUE_SIZE = c_ushort(0)
    SEND_EXTRA_BUF_SIZE = c_ushort(5)
    RECEIVE_EXTRA_BUF_SIZE = c_ushort(5)
    US_EVENT_BUF_SIZE = c_ushort(512)
    ENCODING = "UTF-8"

    """
    Class methods
    """

    def __init__(self, login_id, password, app_name, api_version="TS1-2"):
        """
        Initializes the connection
        """
        self.login_id = create_string_buffer(bytes(login_id,
                                                   self.ENCODING), 49)
        self.password = create_string_buffer(bytes(password,
                                                   self.ENCODING), 49)
        self.app_name = create_string_buffer(bytes(app_name,
                                                   self.ENCODING), 49)
        self.api_version = create_string_buffer(bytes(api_version,
                                                      self.ENCODING), 49)
        self.usNumEvents = c_ushort(0)
        self.invoke_id = c_ulong(0)
        self.handle = c_ulong(0)
        self.AES_sv_name = None
        # Callback function prototypes
        self.sfsn_cfunc = CFUNCTYPE(c_bool, c_char_p, c_ulong)
        self.esr_cfunc = CFUNCTYPE(None, c_ulong)

    """
    Methods for callback handlers
    """

    def cb_sfs(self, service_name, l_param):
        """
        Callback for selecting the first advertised AES Service Name
        """
        self.AES_sv_name = create_string_buffer(service_name, 49)
        return True

    def cb_ESR(self, l_param):
        """
        Callback for managing the incoming events
        """
        print("cb_ESR triggered")
        """
        TO BE TESTED
        self.cstaEvent = create_string_buffer(self.US_EVENT_BUF_SIZE.value)
        ret = self.csta.acsGetEventBlock(self.handle,
                                         byref(self.cstaEvent),
                                         byref(self.US_EVENT_BUF_SIZE),
                                         None,
                                         byref(self.usNumEvents))
        """

    """
    CSTA - equivalent methods
    """
    def connect(self, AES_sv_name=None):
        """
        Connects to an AES advertised service. If not an AES_sv_name is
        passed, it queries the AES for the AdvertisedServerNames and picks the
        first one.

        """
        if not AES_sv_name:
            # Picks the first advertised service
            self.csta.acsEnumServerNames(self.ST_CSTA,
                                         self.sfsn_cfunc(self.cb_sfs),
                                         None)
            while not self.AES_sv_name:
                # Wait until the service name is set
                time.sleep(1)
        else:
            # AES_sv_name as a parameter of connect
            self.AES_sv_name = create_string_buffer(bytes(AES_sv_name,
                                                          self.ENCODING),
                                                    49)

        ret_code = self.csta.acsOpenStream(byref(self.handle),
                                           self.LIB_GEN_ID,
                                           0, # invoke_id
                                           self.ST_CSTA,
                                           byref(self.AES_sv_name),
                                           byref(self.login_id),
                                           byref(self.password),
                                           byref(self.app_name),
                                           self.ACS_LEVEL1,
                                           byref(self.api_version),
                                           self.SEND_QUEUE_SIZE,
                                           self.SEND_EXTRA_BUF_SIZE,
                                           self.RECEIVE_QUEUE_SIZE,
                                           self.RECEIVE_EXTRA_BUF_SIZE,
                                           None)

        if ret_code < 0:
            return ret_code

        self.invoke_id = ret_code
        """
        ret_code = self.csta.acsSetESR(self.handle,
                                       self.esr_cfunc(self.cb_ESR),
                                       byref(self.handle), True)
        """
        return ret_code

    def make_call(self, calling_device, called_device):
        """
        Makes a call from the calling device to the called device
        """
        calling_d = create_string_buffer(bytes(calling_device, self.ENCODING))
        called_d = create_string_buffer(bytes(called_device, self.ENCODING))
        ret_code = self.csta.cstaMakeCall(self.handle, 0, byref(calling_d),
                                          byref(called_d), None)
        self.invoke_id = ret_code
        return ret_code

    def abort_connection(self):
        """
        Aborts the current connection
        """
        ret_code = self.csta.acsAbortStream(self.handle, None)
        return ret_code

    def check_event(self):
        """
        Returns the next event and the number of queued events 
        """
        self.csta_event = create_string_buffer(self.US_EVENT_BUF_SIZE.value)
        ret_code = self.csta.acsGetEventPoll(self.handle, 
                                             byref(self.csta_event),
                                             byref(self.US_EVENT_BUF_SIZE),
                                             None,
                                             byref(self.usNumEvents))
        buff = self.csta_event.raw
        del self.csta_event
        return ret_code, buff, self.usNumEvents 
