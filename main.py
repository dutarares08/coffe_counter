from machine import Pin, SPI, I2C
from ssd1306 import SSD1306_I2C
from oled import Write, SSD1306_I2C
from member_list import member_list

from sdcard import SDCard
import uos
import utime



###################################################
########    Global variables
##################################################
DISPLAY_WIDTH =128
DISPLAY_HEIGHT= 32

recently_used=[
    # This is how objects form this list will look like
    # {
    #     "tag_id":"",
    #     "used_ticks":1232
    # }
]


###################################################
########    GPIO Pin initialization
##################################################
sdcard_csn = Pin(17, Pin.OUT)
sdcard_sck = Pin(18)
sdcard_mosi=Pin(19)
sdcard_miso=Pin(16)

lcd_scl = Pin(1)
lcd_sda = Pin(0)


###################################################
########   Protocols and communication init
##################################################
sdcard_spi = SPI(0,
    baudrate=1000000,
    polarity=0,
    phase=0,
    bits=8,
    firstbit=SPI.MSB,
    sck=Pin(18),
    mosi=Pin(19),
    miso=Pin(16)
)
lcd_i2c=I2C(0, scl=lcd_scl, sda=lcd_sda, freq=200000)



###################################################
########   Objects/Classes instantiations
##################################################

sdcard = SDCard(sdcard_spi, sdcard_csn)
lcd_display = SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, lcd_i2c)

vfs = uos.VfsFat(sdcard)
uos.mount(vfs, "/sdcard")





def something_wrong_happened():
    print("==========================Implement this==============================")
    # implement with sound and display



def create_csv():
    header = 'Tag_ID,Full_Name,Quantity\n'
    with open("/sdcard/coffee_report.csv", 'w') as file:
        file.write(header)
        for member in member_list:
            file.write('{},{},0\n'.format(member['tag_id'], member['full_name']))




def increment_quantity_by_id(tag_id):
    new_lines=[]
    with open("/sdcard/coffee_report.csv", 'r') as file:
        lines = file.readlines()
    
    try:
        for line in lines:
            values = line.strip().split(',')
            if values[0] == tag_id:
                try:
                    old_value = int(values[2])
                except Exception as e:
                    old_value=1
                values[2] = str(old_value+1)
                new_lines.append(','.join(values) + '\n')
            else:
                new_lines.append(line)
    
    except Exception as e:
        return something_wrong_happened()


    try:
        with open("/sdcard/coffee_report.csv", 'w') as file:
            for line in new_lines: 
                file.write(line)
        utime.sleep_ms(300)
        return True
    except Exception as e:
        return something_wrong_happened()


try:
    uos.stat("/sdcard/coffee_report.csv")
except OSError:
    create_csv()
    utime.sleep_ms(2000)



increment_quantity_by_id("22222")

# make a first beep on after scanning and another after saving


lcd_display.text("Test here", 0, 20)
lcd_display.show()
utime.sleep_ms(2000)
lcd_display.fill(0)
lcd_display.show()
# also create a function to log into a notepad a new line (+1) in case of somehthign




# while True:
#     increment_quantity_by_id("1212")
#     utime.sleep_ms(2000)
    

# Increment by index in excel or search tag id in 3rd col