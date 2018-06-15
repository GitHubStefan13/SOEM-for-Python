import soem

# You have to enter your interface name here
# TODO Implement: get interfacename 
npf_device = "ENTER YOUR INTERFACENAME"
b_nof_device = npf_device.encode('utf-8')

print("Starting EtherCat interface...")
if soem.ec_init(b_nof_device):
    print("Successfully started interface")
    if soem.ec_config_init(False) != 1:
        print("No EtherCat-Slaves found")
    print("Found", soem.ec_slavecount, "Slaves")
    print(soem.ec_slavet._fields_)
    print("Closing interface now...")
    if soem.ec_close:
        print("Interface closed.")