from digi.xbee.devices import *
import time

print('Started')

class local():
        def __init__(self):
                self.device=0
                self.Local()
                self.data=0
                
        def Local(self):
                for i in range(256):
                        try:
                                local = XBeeDevice("/dev/ttyUSB"+str(i), 9600)
                                local.open()
                                print('/dev/ttyUSB'+str(i))
                                local.close()
                                self.device=local
                        except:
                                local.close()
                                pass
        def breaker(self):
            print('iteration realeased')
            time.sleep(4)
            self.read()
        def read(self):
                def my_data_received_callback(xbee_message):
                                print('data!')
                                data = xbee_message.data.decode()
                                self.data=data
                                print("Received data from %s" % (data))
                                self.device.del_data_received_callback(my_data_received_callback)
                                self.answer()
                try:
                    self.device.open()
                    for i in range(9000000):
                        self.device.add_data_received_callback(my_data_received_callback)                   
                    self.device.close()
                    self.breaker()
                                     
                except:
                    self.device.close()
                    print('There is a problem about device, so has been closed!')
        def answer(self):
            try:
                time.sleep(2)
                li=self.data.split('-')
                print(li[0])
                xbee_network=self.device.get_network()
                back_device=xbee_network.get_device_by_64(XBee64BitAddress.from_hex_string(li[0]))
                self.device.send_data_async(back_device,"Hate u")
                print('date has been send!')
                self.device.close()
                
                self.read()
            except:
                print('problem')
lcl=local()
lcl.read()
