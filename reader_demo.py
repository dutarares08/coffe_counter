# from mfrc522 import MFRC522
# import utime
# import machine



# # machine.deepsleep()

# # led = machine.PIN(15)

# wakeup_pin = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)
# led = machine.Pin(25, machine.Pin.OUT)
# led.on()
# utime.sleep(3)
# # machine.deepsleep()
# utime.sleep(6)
# led.off()

# # reader = MFRC522(spi_id=1,sck=10,miso=12,mosi=11,cs=9,rst=22)
 
# # print("Bring TAG closer...")
# # print("")
 

# # #reader.init()
# # while True:
# #     # reader.init()
# #     # reader.sleep()

# #     (stat, tag_type) = reader.request(reader.REQIDL)
# #     if stat == reader.OK:
# #         (stat, uid) = reader.SelectTagSN()
# #         if stat == reader.OK:
# #             card = int.from_bytes(bytes(uid),"little",False)
# #             print("CARD ID: "+str(card))


# # utime.sleep_ms(500) 



# import machine
# p25 = machine.Pin(25, machine.Pin.OUT)

# def foo(_):
#     p25(not p25())  # Toggle the LED

# # Configurați pinul pentru trezire
# wakeup_pin = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UO)
# wakeup_pin.irq(foo, trigger=machine.Pin.IRQ_FALLING)

# while True:
#     machine.lightsleep()

# # # Configurați modul deep sleep
# # def deep_sleep():
# #     # Deconectați toate perifericele neutilizate pentru a economisi energie
# #     # machine.freq(125000)  # Setarea frecvenței reduse
# #     machine.deepsleep()

# # # Verificați starea pinului pentru trezire

# # while True:
# #     if wakeup_pin.value() == 1:
# #         print("Trezire din deep sleep!")
# #     else:
# #         print("Intrând în deep sleep...")
# #         deep_sleep()



# from machine import Pin, lightsleep
# p25 = Pin(25, Pin.OUT)
# p0 = Pin(15, Pin.IN, Pin.PULL_UP)
# def foo(_):
#     p25(not p25())  # Toggle the LED

# p0.irq(foo, trigger=Pin.IRQ_FALLING)
# while True:
#     lightsleep()

# import machine

# # Funcția pentru trezire din deep sleep
# def deep_sleep_wake(source_pin):
#     # Configurăm pinul ca pin de intrare cu rezistor de pull-down
#     pin = machine.Pin(source_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
    
#     # Așteptăm până când pinul se schimbă la HIGH (trezire)
#     while not pin.value():
#         # machine.idle()  # Intrăm în modul de așteptare pentru a economisi energie
#         machine.lightsleep()  # Intrăm în modul de așteptare pentru a economisi energie
#     print("S-a trezit!")

# # Funcția pentru aprinderea și stingerea LED-ului
# def toggle_builtin_led(state):
#     led = machine.Pin(25, machine.Pin.OUT)
#     led.value(state)

# # Verificăm dacă suntem într-un ciclu de trezire sau repornire obișnuită
# if machine.reset_cause() == machine.PWRON_RESET:  # Dacă s-a făcut o repornire obișnuită
#     print("Intrând în deep sleep...")
#     toggle_builtin_led(0)  # Stingem LED-ul
#     deep_sleep_wake(15)    # Intrăm în modul deep sleep, trezire pe pinul 15
# else:  # Dacă s-a trezit din deep sleep
#     print("Trezire din deep sleep!")
#     toggle_builtin_led(1)  # Aprindem LED-ul



# import machine

# # Configurați pinul pentru trezire
# wakeup_pin = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)

# # Verificați starea pinului pentru trezire
# while wakeup_pin.value() == 0:
#     print("Intrând în deep sleep...")
#     machine.deepsleep()

# # Aici ajungeți doar dacă pinul de trezire este în stare HIGH
# print("S-a trezit din deep sleep!")



import machine
import time
# interrupt_flag=0
# debounce_time=0
# pin = Pin(15, Pin.IN, Pin.PULL_UP)
led = machine.Pin("LED", machine.Pin.OUT)
# count=0

# def callback(pin):
#     global interrupt_flag, debounce_time
#     if (time.ticks_ms()-debounce_time) > 500:
#         interrupt_flag= 1
#         debounce_time=time.ticks_ms()

# pin.irq(trigger=Pin.IRQ_FALLING, handler=callback)

# while True:
#     if interrupt_flag is 1:
#         interrupt_flag=0
#         print("Interrupt Detected")
#         led.toggle()
#     lightsleep()

# if machine.reset_cause() == machine.DEEPSLEEP_RESET:
#     print('woke from a deep sleep')

# # put the device to sleep for 10 seconds


while True:
    print("Hello there")
    machine.deepsleep(2000)
    # pyb.wifi()
    led.on()
    print("Byee")