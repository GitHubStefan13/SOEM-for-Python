import ctypes
import os
import platform 

# The global variables, also received from the DLL
global ec_slavecount
global ec_slaves
global slaves

# Possible States for the Slaves
EC_STATE_NONE        = 0x00
EC_STATE_INIT        = 0x01
EC_STATE_PRE_OP      = 0x02
EC_STATE_BOOT        = 0x03
EC_STATE_SAFE_OP     = 0x04
EC_STATE_OPERATIONAL = 0x08
EC_STATE_ACK         = 0x10
EC_STATE_ERROR       = 0x10

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
# max. mailbox size */
EC_MAXMBX = 1486
# max. eeprom PDO entries */
EC_MAXEEPDO = 0x200
# max. SM used */
EC_MAXSM = 8
# max. FMMU used */
EC_MAXFMMU = 4
# max. Adapter */
EC_MAXLEN_ADAPTERNAME = 128
# define maximum number of concurrent threads in mapping */
EC_MAX_MAPT = 1
# return value general error */
EC_ERROR           = -3
# return value no frame returned */
EC_NOFRAME         = -1
# return value unknown frame received */
EC_OTHERFRAME      = -2
# maximum EtherCAT frame length in bytes */
EC_MAXECATFRAME    = 1518
# maximum EtherCAT LRW frame length in bytes */
# MTU - Ethernet header - length - datagram header - WCK - FCS */
EC_MAXLRWDATA      = (EC_MAXECATFRAME - 14 - 2 - 10 - 2 - 4)
# size of DC datagram used in first LRW frame */
EC_FIRSTDCDATAGRAM = 20
# standard frame buffer size in bytes */
EC_BUFSIZE         = EC_MAXECATFRAME
# datagram type EtherCAT */
EC_ECATTYPE        = 0x1000
# number of frame buffers per channel (tx, rx1 rx2) */
EC_MAXBUF          = 16
# timeout value in us for tx frame to return to rx */
EC_TIMEOUTRET      = 2000
# timeout value in us for safe data transfer, max. triple retry */
EC_TIMEOUTRET3     = (EC_TIMEOUTRET * 3)
# timeout value in us for return "safe" variant (f.e. wireless) */
EC_TIMEOUTSAFE     = 20000
# timeout value in us for EEPROM access */
EC_TIMEOUTEEP      = 20000
# timeout value in us for tx mailbox cycle */
EC_TIMEOUTTXM      = 20000
# timeout value in us for rx mailbox cycle */
EC_TIMEOUTRXM      = 700000
# timeout value in us for check statechange */
EC_TIMEOUTSTATE    = 2000000
# size of EEPROM bitmap cache */
EC_MAXEEPBITMAP    = 128
# size of EEPROM cache buffer */
EC_MAXEEPBUF       = EC_MAXEEPBITMAP << 5
# default number of retries if wkc <= 0 */
EC_DEFAULTRETRIES  = 3
# max entries in Object Description list */
EC_MAXODLIST       = 1024
# max entries in Object Entry list */
EC_MAXOELIST       = 256

# Importing the DLL
main_directory = os.path.dirname(os.path.abspath(__file__)) 
platform.system()
print(main_directory)
dll_path = main_directory + "\\DLL\\x86\\soem.dll"
ethercat = ctypes.cdll.LoadLibrary(dll_path)

# C Structure for SM
class ec_sm(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("StartAddr", ctypes.c_ushort),
        ("SMlength", ctypes.c_ushort),
        ("SMflags", ctypes.c_uint)
        ]

# C Structure for FMMU
class ec_fmmu(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("LogStart", ctypes.c_uint),
        ("LogLength", ctypes.c_ushort),
        ("LogStartbit", ctypes.c_uint8),
        ("LogEndbit", ctypes.c_uint8),
        ("PhysStart", ctypes.c_ushort),
        ("PhysStartBit", ctypes.c_uint8),
        ("FMMUtype", ctypes.c_uint8),
        ("FMMUactive", ctypes.c_uint8),
        ("unused1", ctypes.c_uint8),
        ("unused2", ctypes.c_ushort)
        ]

# Mapping the IO's of the Slave's
IOMap = ctypes.c_char * (4096)
#PIOMap = ctypes.POINTER(IOMap)

# Array for SM(Sync Manager)
sm_array = ec_sm * (EC_MAXSM)

# Array of SM Types(0=unused, 1=MbxWr, 2=MbxRd, 3=Outputs, 4=Inputs)
smtype_array = ctypes.c_uint8 * (EC_MAXSM)

# Array for FMMU(Fieldbus Memory Management Unit)
fmmu_array = ec_fmmu * (EC_MAXFMMU)

slavename = ctypes.c_char * (EC_MAXNAME + 1) 

# Define callback function
PO2SOconfig = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_ushort)

# C structure for our slave
class ec_slavet(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("state", ctypes.c_ushort), 
        ("ALstatuscode", ctypes.c_ushort),
        ("configadr", ctypes.c_ushort), 
        ("aliasadr", ctypes.c_ushort),
        ("eep_man", ctypes.c_uint), 
        ("eep_id", ctypes.c_uint),
        ("eep_rev", ctypes.c_uint), 
        ("Itype", ctypes.c_ushort),
        ("Dtype", ctypes.c_ushort), 
        ("Obits", ctypes.c_ushort),
        ("Obytes", ctypes.c_uint), 
        ("outputs", ctypes.POINTER(ctypes.c_uint8)),
        ("Ostartbit", ctypes.c_uint8),
        ("Ibits", ctypes.c_ushort), 
        ("Ibytes", ctypes.c_uint),
        ("inputs", ctypes.POINTER(ctypes.c_uint8)), 
        ("Istartbit", ctypes.c_uint8),
        ("SM", sm_array),
        ("SMtype", smtype_array),
        ("FMMU", fmmu_array), 
        ("FMMU0func", ctypes.c_uint8),
        ("FMMU1func", ctypes.c_uint8), 
        ("FMMU2func", ctypes.c_uint8),
        ("FMMU3func", ctypes.c_uint8), 
        ("mbx_l", ctypes.c_ushort),
        ("mbx_wo", ctypes.c_ushort), 
        ("mbx_rl", ctypes.c_ushort),
        ("mbx_ro", ctypes.c_ushort), 
        ("mbx_proto", ctypes.c_ushort),
        ("mbx_cnt", ctypes.c_uint8), 
        ("hasdc", ctypes.c_bool),
        ("ptype", ctypes.c_uint8), 
        ("topology", ctypes.c_uint8),
        ("activeports", ctypes.c_uint8), 
        ("consumedports", ctypes.c_uint8),
        ("parent", ctypes.c_ushort), 
        ("parentport", ctypes.c_uint8),
        ("entryport", ctypes.c_uint8), 
        ("DCrtA", ctypes.c_int),
        ("DCrtB", ctypes.c_int), 
        ("DCrtC", ctypes.c_int),
        ("DCrtD", ctypes.c_int), 
        ("pdelay", ctypes.c_int),
        ("DCnext", ctypes.c_ushort), 
        ("DCprevious", ctypes.c_ushort),
        ("DCcycle", ctypes.c_long), 
        ("DCshift", ctypes.c_long),
        ("DCactive", ctypes.c_uint8), 
        ("configindex", ctypes.c_ushort),
        ("SIIindex", ctypes.c_ushort), 
        ("eep_8byte", ctypes.c_uint8),
        ("eep_pdi", ctypes.c_uint8), 
        ("CoEdetails", ctypes.c_uint8),
        ("FoEdetails", ctypes.c_uint8), 
        ("EoEdetails", ctypes.c_uint8),
        ("SoEdetails", ctypes.c_uint8), 
        ("Ebuscurrent", ctypes.c_ushort),
        ("blockLRW", ctypes.c_uint8), 
        ("group", ctypes.c_uint8),
        ("FMMUunused", ctypes.c_uint8), 
        ("islost", ctypes.c_bool),
        ("PO2SOconfig", PO2SOconfig), 
        ("name", slavename)
    ]


# Initialise lib in single NIC mode
#    * @param[in] ifname   = Dev name, f.e. "eth0"
#    * @return >0 if OK
c_ec_init = ethercat.ec_init
c_ec_init.argtypes = [ctypes.c_char_p]
c_ec_init.restype = ctypes.c_int

#Enumerate and init all slaves.
#       
#        @param[in] usetable     = TRUE when using configtable to init slaves, FALSE otherwise
#        @return Workcounter of slave discover datagram = number of slaves found
c_ec_config_init = ethercat.ec_config_init
c_ec_config_init.argtypes = [ctypes.c_bool]
c_ec_config_init.restype = ctypes.c_int

# Locate DC slaves, measure propagation delays.
#       
#        @return boolean if slaves are found with DC
c_ec_configdc = ethercat.ec_configdc
c_ec_configdc.argtypes = None
c_ec_configdc.restype = ctypes.c_bool

# Set DC of slave to fire sync0 at CyclTime interval with CyclShift offset.
#      
#       @param [in] slave            Slave number.
#       @param [in] act              TRUE = active, FALSE = deactivated
#       @param [in] CyclTime         Cycltime in ns.
#       @param [in] CyclShift        CyclShift in ns.
c_ec_dcsync0 = ethercat.ec_dcsync0
c_ec_dcsync0.argtypes = [ctypes.c_ushort, ctypes.c_bool, ctypes.c_long, ctypes.c_int]
c_ec_dcsync0.restype = None

# Map all PDOs from slaves to IOmap with Outputs/Inputs in sequential order (legacy SOEM way).
#       
#        @param[out] pIOmap     = pointer to IOmap
#        @return IOmap size
c_ec_config_map = ethercat.ec_config_map
c_ec_config_map.argtypes = [ctypes.c_void_p]
c_ec_config_map.restype = ctypes.c_int

# Enumerate / map and init all slaves.
#      
#       @param[in] usetable    = TRUE when using configtable to init slaves, FALSE otherwise
#       @param[out] pIOmap     = pointer to IOmap
#       @return Workcounter of slave discover datagram = number of slaves found
c_ec_config_overlap = ethercat.ec_config_overlap
c_ec_config_overlap.argtypes = [ctypes.c_uint8, ctypes.c_void_p]
c_ec_config_overlap.restype = ctypes.c_int

# Check actual slave state.
#        This is a blocking function.
#        @param[in] slave       = Slave number, 0 = all slaves
#        @param[in] reqstate    = Requested state
#        @param[in] timeout     = Timout value in us
#        @return Requested state, or found state after timeout.
c_ec_statecheck = ethercat.ec_statecheck
c_ec_statecheck.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_int]
c_ec_statecheck.restype = ctypes.c_uint

# Write slave state, if slave = 0 then write to all slaves.
#        The function does not check if the actual state is changed.
#        @param[in] slave = Slave number, 0 = master
#        @return 0
c_ec_writestate = ethercat.ec_writestate
c_ec_writestate.argtypes = [ctypes.c_ushort]
c_ec_writestate.restype = ctypes.c_int

# Transmit processdata to slaves.
#      * @see ec_send_overlap_processdata_group
c_ec_send_overlap_processdata = ethercat.ec_send_overlap_processdata
c_ec_send_overlap_processdata = None
c_ec_send_overlap_processdata = ctypes.c_int

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
ec_slavecount = ctypes.c_uint8.in_dll(ethercat, 'ec_slavecount')
ec_slaves = (ec_slavet * EC_MAXSLAVE).in_dll(ethercat, 'ec_slave')

#

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

def ec_configdc():
    return c_ec_configdc

def ec_dcsync0(slave, act, CyclTime, CyclShift):
    return c_ec_dcsync0(slave, act, CyclTime, CyclShift)

def ec_config_map(PIOMap):
    return c_ec_config_map(PIOMap)

def ec_config_overlap(usetable, PIOMap):
    return c_ec_config_overlap(usetable, PIOMap)

def ec_statecheck(slave, reqstate, timeout):
    return c_ec_statecheck(slave, reqstate, timeout)

def ec_writestate(slave):
    return c_ec_writestate(slave)

def ec_send_overlap_processdata():
    return c_ec_send_overlap_processdata

# Returns a structure as String: See https://stackoverflow.com/questions/20986330/print-all-fields-of-ctypes-structure-with-introspection
def __str__(self):
    return "{}: {{{}}}".format(self.__class__.__name__,
                               ", ".join(["{}: {}".format(field[0],
                                                          getattr(self,
                                                                  field[0]))
                                          for field in self._fields_]))

