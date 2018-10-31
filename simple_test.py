import soem

# Listening to user_input, in form '\\Device\\NPF_{12345678-1234-1234-1234-123456789xxx}' or eth0 for Linux(not tested)
npf_device = input('Enter the devices (npf)name: ')

print("Starting EtherCat interface...")
if soem.ec_init(npf_device):
    print("Successfully started interface")

    if soem.ec_config_init(False) == 1:
        print("Found", soem.ec_slavecount.value, "Slave/s")

        # DEBUG print("Slave 0: ", soem.__str__(soem.ec_slaves[0]))
        # DEBUG print("Slave 1: ", soem.__str__(soem.ec_slaves[1]))
        for i in range(soem.EC_MAXSLAVE):
            slave = soem.ec_slaves[i]
            # Test Device: AXL E EC DI8 DO8 M12 6P
            if slave.eep_man == 0x84 and slave.eep_id == 0x2938D0:
                print("Found device: " + str(slave.name) + " at Pos.: " + str(i))

        soem.ec_config_overlap(True, soem.IOMap)

        soem.ec_configdc()
        soem.ec_dcsync0(0, True, 1000000, 0)

        soem.ec_statecheck(0, soem.EC_STATE_SAFE_OP, soem.EC_TIMEOUTSTATE * 4)

        soem.ec_slaves[0].state = soem.EC_STATE_OPERATIONAL
        
        # Send one valid process data to make outputs in slaves happy
        soem.ec_send_processdata()
        wkc = soem.ec_receive_processdata(soem.EC_TIMEOUTRET)
        print("WKC: " + str(wkc))

        soem.ec_writestate(0)
        soem.ec_statecheck(0, soem.EC_STATE_OPERATIONAL, soem.EC_TIMEOUTSTATE)

        if soem.ec_slaves[0].state == soem.EC_STATE_OPERATIONAL:
            inOp = True
            print("Everything is working...quitting now.")
        else:
            inOp = False
            print("Something went wrong :(")
       
    else:
        print("No EtherCat-Slaves found")

    print("Closing interface now...")
    if soem.ec_close:
        print("Interface closed.")

else:
    print("Could not start interface on the Device.")




