import ctypes
import os
import platform 

# The global variables, also received from the DLL
global ec_slavecount
global ec_slaves

# Some constant entries taken from SOEM
# max. entries in EtherCAT error list
EC_MAXELIST = 64
# max. length of readable name in slavelist and Object Description List 
EC_MAXNAME  = 40
# max. number of slaves in array 
EC_MAXSLAVE = 200
# max. number of groups 
EC_MAXGROUP = 2
# max. number of IO segments per group
EC_MAXIOSEGMENTS = 64

# Importing the DLL
main_directory = os.path.dirname(os.path.abspath(__file__)) 
platform.system()
print(main_directory)
dll_path = main_directory + "\\DLL\\x64\\soem.dll";
ethercat = ctypes.cdll.LoadLibrary(dll_path)

#TODO Correct some fields, define structures
class ec_slavet(ctypes.Structure):
    _fields_ = [
        ("state", ctypes.c_uint), 
        ("ALstatuscode", ctypes.c_uint),
        ("configadr", ctypes.c_uint), 
        ("aliasadr", ctypes.c_uint),
        ("eep_man", ctypes.c_uint), 
        ("eep_id", ctypes.c_uint),
        ("eep_rev", ctypes.c_uint), 
        ("Itype", ctypes.c_uint),
        ("Dtype", ctypes.c_uint), 
        ("Obits", ctypes.c_uint),
        ("Obytes", ctypes.c_uint), 
        ("outputs", ctypes.POINTER(ctypes.c_uint8)),
        ("Ostartbit", ctypes.c_uint8),
        ("Ibits", ctypes.c_uint), 
        ("Ibytes", ctypes.c_uint),
        ("inputs", ctypes.POINTER(ctypes.c_uint8)), 
        ("Istartbit", ctypes.c_uint8),
        ("SM", ctypes.c_int), #TODO make structure SM 
        ("SMtype", ctypes.c_int), #TODO make structure SM
        ("FMMU", ctypes.c_int), #TODO make structure FMMU
        ("FMMU0func", ctypes.c_uint8),
        ("FMMU1func", ctypes.c_uint8), 
        ("FMMU2func", ctypes.c_uint8),
        ("FMMU3func", ctypes.c_uint8), 
        ("mbx_l", ctypes.c_uint),
        ("mbx_wo", ctypes.c_uint), 
        ("mbx_rl", ctypes.c_uint),
        ("mbx_ro", ctypes.c_uint), 
        ("mbx_proto", ctypes.c_uint),
        ("mbx_cnt", ctypes.c_uint8), 
        ("hasdc", ctypes.c_bool),
        ("ptype", ctypes.c_uint8), 
        ("topology", ctypes.c_uint8),
        ("activeports", ctypes.c_uint8), 
        ("consumedports", ctypes.c_uint8),
        ("parent", ctypes.c_uint), 
        ("parentport", ctypes.c_uint8),
        ("entryport", ctypes.c_uint8), 
        ("DCrtA", ctypes.c_uint),
        ("DCrtB", ctypes.c_uint), 
        ("DCrtC", ctypes.c_uint),
        ("DCrtD", ctypes.c_uint), 
        ("pdelay", ctypes.c_uint),
        ("DCnext", ctypes.c_uint), 
        ("DCprevious", ctypes.c_uint),
        ("DCcycle", ctypes.c_uint), 
        ("DCshift", ctypes.c_uint),
        ("DCactive", ctypes.c_uint8), 
        ("configindex", ctypes.c_uint),
        ("SIIindex", ctypes.c_uint), 
        ("eep_8byte", ctypes.c_uint8),
        ("eep_pdi", ctypes.c_uint8), 
        ("CoEdetails", ctypes.c_uint8),
        ("FoEdetails", ctypes.c_uint8), 
        ("EoEdetails", ctypes.c_uint8),
        ("SoEdetails", ctypes.c_uint8), 
        ("Ebuscurrent", ctypes.c_uint),
        ("blockLRW", ctypes.c_uint8), 
        ("group", ctypes.c_uint8),
        ("FMMUunused", ctypes.c_uint8), 
        ("islost", ctypes.c_bool),
        ("PO2SOconfig", ctypes.c_int), 
        ("name", ctypes.c_char)
    ]

# Define the Arguments and Parameters for ec_init
c_ec_init = ethercat.ec_init
c_ec_init.argtypes = [ctypes.c_char_p]
c_ec_init.restype = ctypes.c_int

# Define the Arguments and Parameters for ec_config_init
c_ec_config_init = ethercat.ec_config_init
c_ec_config_init.argtyprs = [ctypes.c_bool]
c_ec_config_init.restype = ctypes.c_int

# Define the Arguments and Parameters for ec_close
c_ec_close = ethercat.ec_close
c_ec_close.argtypes = None
c_ec_close.restype = ctypes.c_int 

# Define the Arguments and Parameters for ec_readstate
c_ec_readstate = ethercat.ec_readstate
c_ec_readstate.argtyprs = None
c_ec_readstate.restype = ctypes.c_int

# Define the Arguments and Parameters for ec_readstate
c_ec_send_processdata = ethercat.ec_send_processdata
c_ec_send_processdata.argtyprs = None
c_ec_send_processdata.restype = ctypes.c_int

# Define the Arguments and Parameters for ec_readstate
c_ec_receive_processdata = ethercat.ec_receive_processdata
c_ec_receive_processdata.argtyprs = [ctypes.c_int]
c_ec_receive_processdata.restype = ctypes.c_int

# Defining were we find our exported variables
ec_slavecount = ctypes.c_int.in_dll(ethercat, 'ec_slavecount').value
ec_slaves = ec_slavet.in_dll(ethercat, 'ec_slave')

# Initiliaze the ethercat interface
def ec_init(npf_device):
    # The String needs to be encoded for the DLL Call 
    return c_ec_init(npf_device.encode('utf-8')) 

# Configure the Slaves
def ec_config_init(usetable):
    return c_ec_config_init(usetable)

# Send processdata
def ec_send_processdata():
    return c_ec_send_processdata()

# Receive processdata from slaves
def ec_receive_processdata(timeout):
    return c_ec_receive_processdata(timeout)

# Receive state
def ec_readstate():
    return c_ec_readstate
 
# Close the ethercat interface
def ec_close():
    return c_ec_close