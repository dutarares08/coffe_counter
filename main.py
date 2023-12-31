#################################################################
########  Designed and maintained by Rares Duta     #############
######## This project is under MIT license          #############
#################################################################


from machine import Pin, SPI, I2C, PWM, deepsleep
from ssd1306 import SSD1306_I2C
from mfrc522 import MFRC522
from utils import increment_quantity_by_id, create_csv, create_excel_backup_before_deepsleep, delete_local_logs
from sdcard import SDCard
import uos
import utime
import freesans20
import writer
import framebuf



MASTER_TAG_ID="219963896" # Warning! Once deleted 

###################################################
########    Global variables
##################################################
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT= 64
SCREEN_OFF_TIMEOUT = 18*1000 # 18 Seconds
# DEEP_SLEEP_TIMEOUT =  30*1000 # 60 minutes ##############3testtt
DEEP_SLEEP_TIMEOUT =  50*60*1000 # 60 minutes
EXIT_MENU_TIMEOUT = 6*1000

loaded_data_from_sheet = [] # See data struct type in member list

light_sleep_on = False
deep_sleep_on = False
deep_sleep_timmer = None
no_sd_card_err = False
counter_to_screen_off=None
query_menu_on = False
query_current_slide = 0
query_menu_timmer = None
timeout_erasing_logs = None



###################################################
########    GPIO Pin initialization
##################################################
sdcard_csn = Pin(17, Pin.OUT)
sdcard_sck = Pin(18)
sdcard_mosi=Pin(19)
sdcard_miso=Pin(16)


lcd_scl = Pin(1)
lcd_sda = Pin(0)
buzzer = PWM(Pin(28))
status_led = Pin(21, Pin.OUT, Pin.PULL_DOWN)

scroll_up = Pin(26, Pin.IN, Pin.PULL_UP)
scroll_down = Pin(27, Pin.IN, Pin.PULL_UP)



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
lcd_display = SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, lcd_i2c)
font_writer = writer.Writer(lcd_display, freesans20)
reader = MFRC522(spi_id=1,sck=10,miso=12,mosi=11,cs=9,rst=22)

try:
    sdcard = SDCard(sdcard_spi, sdcard_csn)
    no_sd_card_err = False
except Exception as e:
    print("Exceptie, ", e)
    no_sd_card_err = True

###################################################
########   Images buffering
##################################################
coffee_buffer = bytearray(b'\x00\x07\x01\xc08\x00\x00\x00\x00\x0f\x01\xc0x\x00\x00\x00\x00\x1f\x03\xc0x\x00\x00\x00\x00\x1e\x03\xc0\xf0\x00\x00\x00\x00\x1e\x07\x80\xf0\x00\x00\x00\x00\x1e\x07\x80\xf0\x00\x00\x00\x00\x1e\x03\x80\xf0\x00\x00\x00\x00\x1e\x03\xc0\xf8\x00\x00\x00\x00\x0f\x03\xe0x\x00\x00\x00\x00\x0f\x81\xe0<\x00\x00\x00\x00\x07\x80\xf0<\x00\x00\x00\x00\x03\x80\xf0\x1e\x00\x00\x00\x00\x03\x80\xf0\x1e\x00\x00\x00\x00\x03\x80\xf0\x1c\x00\x00\x00\x00\x07\x81\xf0<\x00\x00\x00\x00\x0f\x81\xe0<\x00\x00\x00\x00\x0f\x01\xe08\x00\x00\x00\x00\x06\x00\x80\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xff\xff\xff\xff\xff\x80\x00\xff\xff\xff\xff\xff\xff\x80\x00\xff\xff\xff\xff\xff\xff\x80\x00\xff\xff\xff\xff\xff\xff\x80\x00\xf0\x00\x00\x00\x00\x03\xff\xc0\xf0\x00\x00\x00\x00\x03\xff\xe0\xf0\x00\x00\x00\x00\x03\xff\xe0\xf0\x00\x00\x00\x00\x07\x80\xf0\xf0\x00\x00\x00\x00\x07\x80\xf0p\x00\x00\x00\x00\x07\x80\xf0p\x00\x00\x00\x00\x07\x80\xf0x\x00\x00\x00\x00\x07\x80\xf0x\x00\x00\x00\x00\x07\x00\xf0x\x00\x00\x00\x00\x0f\x00\xe0<\x00\x00\x00\x00\x0f\x01\xe0<\x00\x00\x00\x00\x0e\x03\xe0<\x00\x00\x00\x00\x1e\x03\xc0\x1e\x00\x00\x00\x00\x1e\x07\xc0\x1e\x00\x00\x00\x00<\x0f\x80\x0f\x00\x00\x00\x00<\x1f\x00\x0f\x00\x00\x00\x00x\xfe\x00\x0f\x80\x00\x00\x00\x7f\xfc\x00\x07\x80\x00\x00\x00\xff\xf0\x00\x03\xc0\x00\x00\x01\xff\xe0\x00\x03\xe0\x00\x00\x01\xfe\x00\x00\x01\xf0\x00\x00\x03\xc0\x00\x00\x00\xf8\x00\x00\x07\xc0\x00\x00\x00|\x00\x00\x0f\x80\x00\x00\x7f\xff\xff\xff\xff\xff\x00\x00\xff\xff\xff\xff\xff\xff\x80\x00\xff\xff\xff\xff\xff\xff\x80\x00\xff\xff\xff\xff\xff\xff\x80\x00|\x00\x00\x00\x00\x0f\x80\x00>\x00\x00\x00\x00?\x00\x00\x1f\x80\x00\x00\x00~\x00\x00\x0f\xff\xff\xff\xff\xfc\x00\x00\x07\xff\xff\xff\xff\xf8\x00\x00\x01\xff\xff\xff\xff\xe0\x00\x00\x00\x7f\xff\xff\xff\x00\x00\x00')
small_coffee_buffer = bytearray(b'\x03\x18@\x00\x03\x18\xc0\x00\x06\x18\xc0\x00\x03\x18\xc0\x00\x03\x1c`\x00\x01\x8c`\x00\x01\x8c`\x00\x03\x0c`\x00\x03\x08@\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x80\xc0\x00\x01\xf0\xc0\x00\x01\xfc\xc0\x00\x01\x8c\xc0\x00\x01\x0c@\x00\x03\x0c`\x00\x03\x0c`\x00\x03\x18`\x00\x0680\x00\x06p8\x00\x0f\xe0\x18\x00\x0f\x80\x0c\x00\x18\x00\x06\x000\x00\xff\xff\xff\x80\xe0\x00\x03\x00p\x00\x07\x00?\xff\xfe\x00\x0f\xff\xf8\x00')
warning_buffer = bytearray(b'\x00\x00\x00\x00\x00\x07\x80\x00\x00\x0f\xc0\x00\x00\x1f\xe0\x00\x008p\x00\x00p8\x00\x00p8\x00\x00\xe0\x1c\x00\x00\xe0\x1c\x00\x01\xc0\x0e\x00\x01\x83\x06\x00\x03\x87\x87\x00\x07\x07\x83\x80\x07\x03\x03\x80\x0e\x03\x01\xc0\x0e\x03\x01\xc0\x1c\x03\x00\xe0\x18\x03\x00`8\x03\x00pp\x00\x008p\x00\x008\xe0\x03\x00\x1c\xe0\x07\x80\x1c\xc0\x03\x00\x0c\xe0\x00\x00\x1c\xe0\x00\x00\x1c\x7f\xff\xff\xf8?\xff\xff\xf0\x0f\xff\xff\xc0\x00\x00\x00\x00')
loading_buffer = bytearray(b'\x00\x00\x00\x00\x00\x03\x00\x00\x00\x03\x00\x00\x00\x03\x00\x00\x00\x03\x00\x00\x0e\x03\x01\xc0\x0f\x03\x03\xc0\x07\x83\x07\x80\x03\xc3\x0f\x00\x01\xe0\x1e\x00\x00\xc0\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\x00\x03\xf8\xff\x00\x03\xfc\xff\x00\x03\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\x00\x00\x01\xe0\x00\x00\x03\xc0\x00\x00\x07\x80\x00\x00\x0f\x03\x00\x00\x0e\x03\x00\x00\x04\x03\x00\x00\x00\x03\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00')
smallest_coffee = bytearray(b'\x08\x90\x00\t\x10\x00\t\x90\x00\x0c\x98\x00\x04\x88\x00\x08\x90\x00\x00\x00\x00\xff\xff\x00\x80\x01\xe0\x80\x01\x10\x80\x01\x10\xc0\x01\x10@\x03 `\x02` \x07\x800\x04\x00\xff\xff\x00\xff\xff\x00`\x03\x00?\xfc\x00')


coffee_fb = framebuf.FrameBuffer(coffee_buffer, 64, 64, framebuf.MONO_HLSB)
small_coffee_fb=framebuf.FrameBuffer(small_coffee_buffer, 30, 30, framebuf.MONO_HLSB)
warning_fb=framebuf.FrameBuffer(warning_buffer, 30, 30, framebuf.MONO_HLSB)
loading_fb=framebuf.FrameBuffer(loading_buffer, 30, 30, framebuf.MONO_HLSB)
smallest_coffee_fb=framebuf.FrameBuffer(smallest_coffee, 20, 20, framebuf.MONO_HLSB)





def boot_setup():
    status_led.value(1)

    lcd_display.fill(0)
    lcd_display.blit(coffee_fb, 32, 4)
    lcd_display.show()
    utime.sleep_ms(1000)
    if no_sd_card_err:
        lcd_display.fill(0)
        lcd_display.blit(warning_fb, 49, 4)
        font_writer.set_textpos(20, 40)
        font_writer.printstring("No SD Card")
        lcd_display.show()
        return False
    
    try:
        vfs = uos.VfsFat(sdcard)
        uos.mount(vfs, "/sdcard")
    except Exception as e:
        lcd_display.fill(0)
        lcd_display.blit(warning_fb, 49, 4)
        font_writer.set_textpos(20, 40)
        font_writer.printstring("SD Error")
        lcd_display.show()
        utime.sleep(2)
        lcd_display.fill(0)
        lcd_display.text("Cannot mount", 0, 0)
        lcd_display.text("SD Card!", 0, 10)
        lcd_display.text("Make sure is", 0, 20)
        lcd_display.text("FAT32 formatted", 0, 30)
        lcd_display.text("TRY TO REBOOT", 0, 50)
        lcd_display.show()
        return False    

    try:
        uos.stat("/sdcard/coffee_report.csv")
    except OSError:
        try:
            create_csv()
        except Exception as e:
            lcd_display.fill(0)
            lcd_display.blit(warning_fb, 49, 4)
            font_writer.set_textpos(20, 40)
            font_writer.printstring("Internal Err")
            lcd_display.show()
            utime.sleep(2)
            lcd_display.fill(0)
            lcd_display.text("Cannot find/", 0, 0)
            lcd_display.text("create excel", 0, 10)
            lcd_display.text("document", 0, 20)
            lcd_display.text("TRY TO REBOOT", 0, 50)
            lcd_display.show()
            return False

    # upload to global variables data readed on init seq
    
    try:
        with open("/sdcard/coffee_report.csv", 'r') as file:
            lines = file.readlines()
            for line in lines:
                values = line.strip().split(',')
                loaded_data_from_sheet.append({
                    "tag_id": values[0],
                    "full_name":values[1],
                    "quantity": values[2] if values[2] else 0    
                })
        loaded_data_from_sheet.pop(0)
    except Exception as e:
        print("Exception, ", e)
        return False

    return True






def update_local_loaded_data(tag_id):
    
    global loaded_data_from_sheet

    print("Loaded data", loaded_data_from_sheet)
    reconstructed_list = []
    for member in loaded_data_from_sheet:
        if member['tag_id'] == tag_id:
            reconstructed_list.append({
                "tag_id":tag_id,
                "full_name":member['full_name'],
                "quantity":str(int(member['quantity'])+1)
            })
        else:
            reconstructed_list.append(member)

    loaded_data_from_sheet = reconstructed_list

def show_normal_screen():
    global counter_to_screen_off, deep_sleep_timmer
    lcd_display.fill(0)
    lcd_display.blit(small_coffee_fb, 49, 4)
    font_writer.set_textpos(20, 40)
    font_writer.printstring("Scan tag !")
    lcd_display.show()

    counter_to_screen_off=utime.ticks_ms()
    deep_sleep_timmer=utime.ticks_ms()



def show_user_data(full_name, quantity):
    lcd_display.fill(0)
    font_writer.set_textpos(5, 5)
    font_writer.printstring(full_name)

    font_writer.set_textpos(45, 42)
    lcd_display.blit(smallest_coffee_fb, 5, 40)
    font_writer.printstring(quantity)
    lcd_display.show()
    

def short_beep_sound():
    buzzer.duty_u16(18000)
    buzzer.freq(3523)
    utime.sleep(0.1)
    buzzer.duty_u16(0)


def read_tag_sound():
    buzzer.duty_u16(8000)
    buzzer.freq(523)
    utime.sleep(0.1)
    buzzer.duty_u16(0)
    utime.sleep(0.01)
    buzzer.duty_u16(8000)
    buzzer.freq(659)
    utime.sleep(0.1)
    buzzer.duty_u16(0)

def error_sound():
    buzzer.freq(1000)
    for i in range(8):
        buzzer.duty_u16(4000)
        utime.sleep_ms(100)
        buzzer.duty_u16(0)
        utime.sleep_ms(50)



device_booted = boot_setup()
if device_booted:
    utime.sleep(3)
    show_normal_screen()




counter_to_screen_off=utime.ticks_ms()
deep_sleep_timmer=utime.ticks_ms()



while device_booted:


    if scroll_up.value() == 0 or scroll_down.value() == 0:
        print(loaded_data_from_sheet)
        
        if light_sleep_on:
            lcd_display.poweron()

        short_beep_sound()
        counter_to_screen_off=utime.ticks_ms()
        deep_sleep_timmer=utime.ticks_ms()
        query_menu_timmer = utime.ticks_ms()

        if not query_menu_on:
            query_menu_on = True
        else:
            if scroll_up.value() == 0:
                
                if query_current_slide >= (len(loaded_data_from_sheet) -1) :
                    query_current_slide=0
                else:
                    query_current_slide=query_current_slide+1
            else:
                if query_current_slide <=0:
                    query_current_slide =  len(loaded_data_from_sheet) -1
                else:
                    query_current_slide=query_current_slide-1        
            # print(loaded_data_from_sheet)
            # print(query_current_slide)
    if query_menu_on:

        current = loaded_data_from_sheet[query_current_slide]
        show_user_data(current['full_name'], current['quantity'])


    current_ticks = utime.ticks_ms()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            if light_sleep_on:
                lcd_display.poweron()

            card = int.from_bytes(bytes(uid),"little",False)




            counter_to_screen_off=None
            deep_sleep_timmer = utime.ticks_ms()

            query_menu_on=False
            query_current_slide=0


            ########## Here read tag ############
    
            lcd_display.fill(0)
            lcd_display.blit(loading_fb, 48, 4)
            font_writer.set_textpos(5, 40)
            font_writer.printstring("Reading TAG")
            lcd_display.show()


            if str(card) == MASTER_TAG_ID:
                if timeout_erasing_logs is not None:
                    # perform deletion
                    lcd_display.fill(0)
                    lcd_display.blit(warning_fb, 49, 4)
                    font_writer.set_textpos(20, 40)
                    font_writer.printstring("Erasing...")
                    lcd_display.show()
                    delete_local_logs()
                    utime.sleep_ms(400)
                    
                    lcd_display.fill(0)
                    lcd_display.blit(warning_fb, 49, 4)
                    font_writer.set_textpos(20, 40)
                    font_writer.printstring("Done :)")
                    lcd_display.show()
                    utime.sleep_ms(900)

                    timeout_erasing_logs = None
                    show_normal_screen()

                else:
                    #show screen with message
                    lcd_display.fill(0)
                    lcd_display.text("Are you sure?", 0, 0)
                    lcd_display.text("This action will", 0, 10)
                    lcd_display.text("delete all logs", 0, 20)
                    lcd_display.text("Scan Again to", 0, 40)
                    lcd_display.text("perfrom action", 0, 50)
                    lcd_display.show()
                    timeout_erasing_logs=utime.ticks_ms()
                
            else:

                update_result = increment_quantity_by_id(str(card))
            
                if update_result is None:
                    # user not found
                    lcd_display.fill(0)
                    lcd_display.blit(warning_fb, 49, 4)
                    font_writer.set_textpos(20, 40)
                    font_writer.printstring("Not Found")
                    lcd_display.show()
                    error_sound()
                    utime.sleep(3)
                    show_normal_screen()
                elif update_result is False:
                    lcd_display.fill(0)
                    lcd_display.blit(warning_fb, 49, 4)
                    font_writer.set_textpos(20, 40)
                    font_writer.printstring("Please Reboot")
                    lcd_display.show()
                    error_sound()
                    utime.sleep(3)

                else:
                    read_tag_sound()
                    update_local_loaded_data(str(card))
                    # print("Result ", update_result)
                    # update excel doc and retreive data about name and quantity
                    # after updating document show this
                    show_user_data(update_result['user_name'], update_result['quantity'])
                    utime.sleep(7)
                    show_normal_screen()


    
    

    if timeout_erasing_logs is not None and utime.ticks_diff(current_ticks, timeout_erasing_logs) > 3000:
        timeout_erasing_logs = None
        show_normal_screen()


    if query_menu_timmer is not None and utime.ticks_diff(current_ticks, query_menu_timmer) > EXIT_MENU_TIMEOUT:
        query_menu_on = False
        query_current_slide = 0
        query_menu_timmer = None
        show_normal_screen()

    if counter_to_screen_off is not None and utime.ticks_diff(current_ticks, counter_to_screen_off) > SCREEN_OFF_TIMEOUT:
        query_menu_on = False
        lcd_display.poweroff()
        light_sleep_on=True
        counter_to_screen_off = None
        query_menu_timmer = None

    if deep_sleep_timmer is not None and utime.ticks_diff(current_ticks, deep_sleep_timmer) > DEEP_SLEEP_TIMEOUT:
        reader.sleep()
        lcd_display.poweroff()
        status_led.value(0)
        create_excel_backup_before_deepsleep(loaded_data_from_sheet)
        deepsleep()
    
    if query_menu_on:
        utime.sleep_ms(15)
    else:
        utime.sleep_ms(500)




###################################################
############## TODO ##############################
##################################################

# 1) Failback to internal flash - done
# 2) Notepad logs - done
# 3) Sleep mode optimize - done
# 4) led for deeep sleep mode - done
# 5) Before entering deep sleep make a 3rd backup on internal flash - progress
