import RPi.GPIO as GPIO
from DataEntry.DataEntry import DataEntry
from lib_nrf24 import NRF24
from threading import Thread
import threading
import time
import datetime
import spidev

lock = threading.Lock()
start_data = 0xDA7A
end_data = "EOT"
store_data = 0xA7A7

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
            radio.write(`start_data` + '\0')
            radio.startListening()
            lock.release()
            
            print("Module: " + `x`)
            x += 1
            if(x >= len(module)):
                x = 0
            time.sleep(5)
            

GPIO.setmode(GPIO.BCM)
db = DataEntry("127.0.0.1", "****", "****", "AER-Data")

module = [[0xe7, 0xe7, 0xe7, 0xe7, 0x01], [0xe7, 0xe7, 0xe7, 0xe7, 0x02]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.powerUp()
radio.setChannel(110)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setPayloadSize(32
                     )
radio.setAutoAck(True)
radio.enableDynamicPayloads()

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

        if(string == "EOT"):
            if(db.insertData(data[0], ["NUll"] + data[1:])):
                print("Inserted Data")
            else:
                print("Failed to insert data")
            data = []
        else:
            data.append(string)
            
        # Printing to screen
        print("Got: *{}*".format(string))

    lock.release()

'''
        try:
            print("Got Adress: {}".format(int(string, 16)))
        except:
            print("Got: {}".format(string))
'''
for t in threads:
    t.join()
    

    
