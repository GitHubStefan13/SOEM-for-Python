import soem

# Listening to user_input
npf_device = input('Enter the device name: ')


print("Starting EtherCat interface...")
if soem.ec_init(npf_device):
    print("Successfully started interface")

    if soem.ec_config_init(False) != 1:
        print("No EtherCat-Slaves found")
    else:
        soem.ec_send_processdata()
        print("Found", soem.ec_slavecount, "Slaves")
        print(soem.ec_receive_processdata(50))
        print(soem.ec_slavet._fields_)
    
    print("Closing interface now...")
    if soem.ec_close:
        print("Interface closed.")