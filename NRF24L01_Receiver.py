import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
from threading import Thread
import time
import datetime
import spidev

class inputThread(Thread):
    def __init__ (self):
        Thread.__init__(self)

    def run(self):
        tx_string = ""
        x = 0
        while True:
            print("Sending transmit request...")
            print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            radio.openWritingPipe(module[x])
            radio.stopListening()
            radio.write(`start_data` + '\0')
            radio.startListening()

            x += 1
            if(x >= len(module)):
                x = 0
            time.sleep(5)
            

GPIO.setmode(GPIO.BCM)

module = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xe7, 0xe7, 0xe7, 0xe7, 0xc1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.powerUp()
radio.setChannel(110)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setPayloadSize(32)
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
threads = []
lenght = 0
start_data = 0xDA7A

ThInput = inputThread()
ThInput.start()
threads.append(ThInput)

while(1):

    # executes when payload available

    if(radio.available()):

        # Reading the payload
        lenght = radio.getDynamicPayloadSize()
        radio.read(rx_buff, lenght)
        # Converting to string
        string = ""
        for n in rx_buff:
            string += chr(n)
        # Printing to screen
        print("Got: {}".format(string))

for t in threads:
    t.join()
    

    
