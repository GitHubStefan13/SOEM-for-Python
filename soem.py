import ctypes
import os
import platform 

global ec_slavecount
global ec_slaves

# Importing the DLL
main_directory = os.path.dirname(os.path.abspath(__file__)) 
platform.system()
print(main_directory)
dll_path = main_directory + "\\DLL\\x64\\soem.dll";
ethercat = ctypes.cdll.LoadLibrary(dll_path)

#TODO Implement correctly
class ec_slavet(ctypes.Structure):
    _fields_ = [
        ("First values", ctypes.c_int), 
        ("First values", ctypes.c_int)
    ]

# Define the Arguments and Parameters for ec_init
c_ec_init = ethercat.ec_init
c_ec_init.argtypes = [ctypes.c_char_p]
c_ec_init.restype = ctypes.c_int

# Define the Arguments and Parameters for ec_config_init
# c_ec_config_init = ethercat.ec_config_init
# c_ec_config_init.argtyprs = [ctypes.c_bool]
# c_ec_config_init.restype = ctypes.c_int

# Define the Arguments and Parameters for ec_close
c_ec_close = ethercat.ec_close
c_ec_close.argtypes = None
c_ec_close.restype = ctypes.c_int 

# Defining were we find our exported variables
ec_slavecount = ctypes.c_int.in_dll(ethercat, 'ec_slavecount').value
ec_slaves = ec_slavet.in_dll(ethercat, 'ec_slave')

# Initiliaze the ethercat interface
def ec_init(npf_device):
    return c_ec_init(npf_device) 

# Configure the Slaves
def ec_config_init(usetable):
    return False #c_ec_config_init(usetable)
 
# Close the ethercat interface
def ec_close():
    return c_ec_close