# from mfrc522 import MFRC522
# import utime


# reader = MFRC522(spi_id=1,sck=10,miso=12,mosi=11,cs=9,rst=22)
 
# print("Bring TAG closer...")
# print("")
 

# reader.init()
# while True:
#     reader.init()
#     # reader.write(reader.REQIDL, "17412652183861270")
#     (stat, tag_type) = reader.request(reader.REQIDL)
#     if stat == reader.OK:
#         (stat, uid) = reader.SelectTagSN()
#         if stat == reader.OK:
#             card = int.from_bytes(bytes(uid),"little",False)
#             print("CARD ID: "+str(card))


#     utime.sleep_ms(500) 


# # 17412652183861270

import mfrc522
import ustruct
import utime

# Crearea obiectului MFRC522
# rfid = mfrc522.MFRC522(0, 1, 2, 3, 4)
rfid = mfrc522.MFRC522(spi_id=1,sck=10,miso=12,mosi=11,cs=9,rst=22)
# Codul pe care doriți să-l scrieți pe tag
cod_string = "CodulTauAici"

# Convertirea șirului în bytes
cod_bytes = bytearray(cod_string, 'little')

try:
    while True:
        # Detectarea unui card NFC
        (stat, tag_type) = rfid.request(rfid.REQIDL)
        
        if stat == rfid.OK:
            print("Card detectat")
            
            # Selectarea cardului
            (stat, raw_uid) = rfid.SelectTagSN()
            print(stat)
            
            if stat == rfid.OK:
                # Scrierea datelor pe card
                stat = rfid.write(16, cod_bytes)
                
                if stat == rfid.OK:
                    print("Scriere cu succes!")
                else:
                    print("Eroare la scriere")
                
                # Eliberarea cardului
                rfid.select_tag(None)
        
        # Pauza între citiri
        utime.sleep(1)
        
except KeyboardInterrupt:
    print("Oprire de la tastatură")
finally:
    rfid.cleanup()