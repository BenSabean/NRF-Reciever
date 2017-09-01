import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.setmode(GPIO.BCM)

pipe = "2Node"

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

radio.setChannel(110)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipe)
radio.printDetails()
radio.startListening()

while(1):

    if(radio.available()):
        rx_buff = []
        radio.read(rx_buff, radio.getDynamicPayloadSize())
        print("Received: {}".format(rx_buff))
        string = ""
        for n in rx_buff:
            string += chr(n)
        print("Decoded: {}".format(string))
    
