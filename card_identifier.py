from mfrc522 import MFRC522
import utime


reader = MFRC522(spi_id=1,sck=10,miso=12,mosi=11,cs=9,rst=22)
 
print("Bring TAG closer...")
print("")
 

reader.init()
while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            print("CARD ID: "+str(card))


    utime.sleep_ms(500) 


