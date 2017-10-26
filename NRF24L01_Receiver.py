import RPi.GPIO as GPIO
from DataBase.DbManager import DbManager
from lib_nrf24 import NRF24
from threading import Thread
from Queue import Queue
import threading
import time
import datetime
import spidev
import json

lock = threading.Lock()
start_data = "START"
end_data = "EOT"
config_data = "CONFIG"
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

class ModuleThread(Thread):
    def __init__ (self, myIndex, myInterval):
        Thread.__init__(self)
        self.index = myIndex
        self.interval = myInterval

    def run(self):
        time.sleep(1)
        while True:
            q.join()
            print("Sending transmit request...")
            print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            lock.acquire()
            radio.stopListening()
            radio.openWritingPipe(module[self.index])
            radio.write(start_data + '\0')
            q.put(self.index)
            radio.startListening()
            lock.release()
            
            time.sleep(60*self.interval)
            
GPIO.setmode(GPIO.BCM)
db = DbManager(data["mysql"]["host"], data["mysql"]["user"],
               data["mysql"]["passwd"], data["mysql"]["db"])

module = [[0xe7, 0xe7, 0xe7, 0xe7, 0x01]
          #, [0xe7, 0xe7, 0xe7, 0xe7, 0x02]
          ]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.powerUp()
radio.setChannel(100)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setPayloadSize(32)
radio.setAutoAck(True)
radio.enableDynamicPayloads()

radio.openWritingPipe(module[0])

rx_buff = []
lenght = 0
threads = []
data = []
q = Queue()

i = 0
for m in module:
    radio.openReadingPipe(i, module[i])
    print("Reading pipe " + `i` + " opened")

    print("Spawning thread " + `i+1`)
    thModule = ModuleThread(i, db.getSampleRate(i+1))
    thModule.daemon = True
    thModule.start()
    threads.append(thModule)
    
    i += 1
    
radio.printDetails()
print("---------------------------")


radio.startListening()

while(1):

    # executes when payload available
    print("Module: " + `q.get()`)
    listen = True
    lock.acquire()
    while listen:
        if(radio.available()):
            # Reading the payload
            lenght = radio.getDynamicPayloadSize()
            radio.read(rx_buff, lenght)
            
            # Converting to string
            string = ""
            for n in rx_buff:
                string += chr(n)
            string = string[:-1]
            if(string == end_data):
                print("Ending Transmission")
                listen = False
                try:
                    address = []
                    value = []
                    for line in data:
                        address.append(line.split(" ")[0])
                        value.append(line.split(" ")[1])
                    #print(db.getSampleRate(int(address[0])))

                    if(db.insertData(int(address[0]), int(value[0]), ["NUll"] + value[1:])):
                        print("Inserted Data")
                    else:
                        print("Failed to insert data")
                except Exception as e:
                    print(e)
                    print("Corrupt Data")
                data = []
                q.task_done()
            else:
                data.append(string)
                
            # Printing to screen
            print("Got: *{}*".format(string))

    lock.release()
    
    

    
