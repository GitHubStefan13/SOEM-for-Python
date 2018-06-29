import soem

# Listening to user_input
npf_device = input('Enter the devices (npf)name: ')


print("Starting EtherCat interface...")
if soem.ec_init(npf_device):
    print("Successfully started interface")

    if soem.ec_config_init(False) != 1:
        print("No EtherCat-Slaves found")
    else:
        soem.ec_send_processdata()
        print("Found", soem.ec_slavecount.value, "Slave/s")

        wkc = 0
        wkc = soem.ec_receive_processdata(2000000)

        for x in range(0, 200):
            print(soem.c_get_ec_slaves(x))

        while True:
		    soem.ec_send_processdata
            wkc = soem.ec_receive_processdata(2000000)
            if wkc == -1:
                print("Error receiving Working Counter")
                break
            else:
                print(wkc)
                if wkc >= 2:
                    print("Working Counter reached 2, everything seems to work...stopping now")
                    break


    
    print("Closing interface now...")
    if soem.ec_close:
        print("Interface closed.")
