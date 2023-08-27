import utime
from member_list import member_list



def something_wrong_happened():
    print("==========================Implement this==============================")
    # implement with sound and display




def create_csv():
    utime.sleep(0.5)
    header = 'Tag_ID,Full_Name,Quantity\n'
    with open("/sdcard/coffee_report.csv", 'w') as file:
        file.write(header)
        for member in member_list:
            file.write('{},{},0\n'.format(member['tag_id'], member['full_name']))
    return True



def increment_quantity_by_id(tag_id):
    new_lines=[]
    user_found=None

    with open("/sdcard/coffee_report.csv", 'r') as file:
        lines = file.readlines()
    
    try:
        for line in lines:
            values = line.strip().split(',')
            if values[0] == tag_id:
                try:
                    old_value = int(values[2])
                except Exception as e:
                    old_value=0
                user_found = {
                    "user_name":str(values[1]),
                    "quantity":str(old_value+1),
                }
                values[2] = str(old_value+1)
                new_lines.append(','.join(values) + '\n')
            else:
                new_lines.append(line)

    except Exception as e:
        return None

    if user_found is None:
        return None
    
    try:
        with open("/sdcard/coffee_report.csv", 'w') as file:
            for line in new_lines: 
                file.write(line)
        utime.sleep_ms(300)
        return user_found
    except Exception as e:
        return False #False mean is a verry bad thing



