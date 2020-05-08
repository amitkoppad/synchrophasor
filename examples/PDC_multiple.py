from synchrophasor.pmu import Pmu
from synchrophasor.pmu import ConfigFrame2
from synchrophasor.pdc import Pdc
from synchrophasor.frame import DataFrame
import os
from ipaddress import IPv4Address

"""
tinyPDC will connect to pmu_ip:pmu_port and send request
for header message, configuration and eventually
to start sending measurements.
"""


if __name__ == "__main__":

   for x in range(4):
    ip = str(IPv4Address('127.0.0.2') + x)
    idd = 2 + x
    print(ip)
    #pdc(x) = Pdc(pdc_id=7, pmu_ip=ip, pmu_port=4712)
    #pdc1 = Pdc(pdc_id=7, pmu_ip="127.0.0.4", pmu_port=4712)
   # pdc.logger.setLevel("DEBUG")
   # pdc1.logger.setLevel("DEBUG")

    n = os.fork()

    if n == 0:
        print("Child process : ", os.getpid())
        pdc = Pdc(pdc_id=idd, pmu_ip=ip, pmu_port=4712)
        pdc.logger.setLevel("DEBUG")
        pdc.run()
        header = pdc.get_header()
        config = pdc.get_config()
        pdc.start()
        while True:
             data = pdc.get()

             if type(data) == DataFrame:
                    print(data.get_measurements())

             if not data:
                    pdc.quit()
                    break
    else:
        print("Parent process: ", os.getpid())
        if x == 4:
           pmu = Pmu(ip="127.0.1.10", port=1420)
    #pmu.set_config(cfg)
           pmu.logger.setLevel("DEBUG")

           pmu.set_configuration()  # This will load default PMU configuration specified in IEEE C37.118.2 - Annex D (Table D.2)
           pmu.set_header()  # This will load default header message "Hello I'm tinyPMU!"

           pmu.run()  # PMU starts listening for incoming connections

           while True:
              if pmu.clients:  # Check if there is any connected PDCs
                 pmu.send(pmu.ieee_data_sample)  # Sending sample data frame specified in IEEE C37.118.2 - Annex D (Table D.1)

           pmu.join()
#        p = os.wait()

#    pdc.run()  # Connect to PMU
#    pdc1.run()
#    header = pdc.get_header()  # Get header message from PMU
#    header1 = pdc1.get_header() # Get header message from PMU2
#    config = pdc.get_config()  # Get configuration from PMU
#    config1 = pdc1.get_config() # Get config from PMU2

#    pdc.start()  # Request to start sending measurements
#    pdc1.start()
#    while True:

#        data = pdc.get()  # Keep receiving data
#        data1 = pdc1.get()

#        if type(data) == DataFrame:
#            print(data.get_measurements())

#        if not data:
#            pdc.quit()  # Close connection
#            break

#        if type(data1) == DataFrame:
#            print(data1.get_measurements())

#        if not data1:
#           pdc1.quit()
#            break
