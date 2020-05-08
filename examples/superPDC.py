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

   for x in range(5):
    ip = str(IPv4Address('127.0.1.10') + x)
    idd = 2 + x
    print(ip)
#127.0.1.10", port=1420
    #pdc(x) = Pdc(pdc_id=7, pmu_ip=ip, pmu_port=4712)
    #pdc1 = Pdc(pdc_id=7, pmu_ip="127.0.0.4", pmu_port=4712)
   # pdc.logger.setLevel("DEBUG")
   # pdc1.logger.setLevel("DEBUG")

    n = os.fork()

    if n == 0:
        print("Child process : ", os.getpid())
        pdc = Pdc(pdc_id=idd, pmu_ip=ip, pmu_port=1420)
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
        p = os.wait()

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
