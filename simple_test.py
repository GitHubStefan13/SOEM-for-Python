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
        print("Found", soem.ec_slavecount, "Slave/s")

        wkc = 0
        wkc = soem.ec_receive_processdata(200000)

        # Testprint our slaves...       
        # Option 1, only seems to print the fields not the values itself
        #print(soem.ec_slavet._fields_)
        # Option 2
        soem.__str__(soem.ec_slaves) 

        while True:
            wkc = soem.ec_receive_processdata(200000)
            if wkc == -1:
                print("Error receiving Working Counter")
                break
            else:
                print(wkc)
                if wkc >= 2000:
                    print("Working Counter reached 2000, everything seems to work...stopping now")
                    break


    
    print("Closing interface now...")
    if soem.ec_close:
        print("Interface closed.")