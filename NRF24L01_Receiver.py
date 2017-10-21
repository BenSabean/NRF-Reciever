import RPi.GPIO as GPIO
from DataBase.DbManager import DbManager
from lib_nrf24 import NRF24
from threading import Thread
import threading
import time
import datetime
import spidev

lock = threading.Lock()
start_data = "START"
end_data = "EOT"
config_data = "CONFIG"

class inputThread(Thread):
    def __init__ (self):
        Thread.__init__(self)

    def run(self):
        x = 0
        while True:
            print("Sending transmit request...")
            print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            lock.acquire()
            radio.stopListening()
            radio.openWritingPipe(module[x])
            radio.write(start_data + '\0')
            radio.startListening()
            lock.release()
            
            print("Module: " + `x`)
            x += 1
            if(x >= len(module)):
                x = 0
            time.sleep(60*5)
            
GPIO.setmode(GPIO.BCM)
db = DbManager("127.0.0.1", "****", "****", "AER-Data")

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

i = 0
for m in module:
    radio.openReadingPipe(i, module[i])
    print("Reading pipe " + `i` + " opened")
    i += 1
    
radio.printDetails()
print("---------------------------")


radio.startListening()

rx_buff = []
lenght = 0
threads = []
data = []

ThInput = inputThread()
ThInput.daemon = True
ThInput.start()
threads.append(ThInput)

while(1):

    # executes when payload available

    lock.acquire()
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
            try:
                address = []
                value = []
                
                for line in data:
                    address.append(line.split(" ")[0])
                    #print("*{}*".format(line.split(" ")[0]))
                    value.append(line.split(" ")[1])
                    #print("*{}*".format(line.split(" ")[1]))

                print("*{}*".format(int(value[0])))
                if(db.insertData(int(address[0]), int(value[0]), ["NUll"] + value[1:])):
                    print("Inserted Data")
                else:
                    print("Failed to insert data")
            except Exception as e:
                print(e)
                print("Corrupt Data")
            data = []
        else:
            data.append(string)
            
        # Printing to screen
        print("Got: *{}*".format(string))

    

    lock.release()
    
    

    
