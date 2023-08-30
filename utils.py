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
    utime.sleep(0.7)
    return True





def increment_quantity_by_id(tag_id):
    new_lines=[]
    user_found=None
    member_name=None

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
                member_name=str(values[1])
                values[2] = str(old_value+1)
                new_lines.append(','.join(values) + '\n')
            else:
                new_lines.append(line)

    except Exception as e:
        return None
    # print("New lines list ", new_lines)


    if user_found is None:
        # here check if existing in member_list array of dict. If so it means
        # was added after first excel generation and will add here at the end of list created above
        found_on_dict = None

        for member in member_list:
            if member["tag_id"] == tag_id:
                found_on_dict = member

        if found_on_dict is None:
            return None
        

        member_name = found_on_dict['full_name']
        to_append=f"{tag_id},{member_name},1\n"
        new_lines.append(to_append)
        user_found={
            "user_name":str(member_name),
            "quantity":"1",
        }
    
    try:
        with open("/backup_logs.txt", "a") as file:
            file.write(f"{tag_id} | {member_name} | 1\n")
    except Exception as e:
        print("Error on backup file")
        return False
    
    try:
        with open("/sdcard/coffee_report.csv", 'w') as file:
            for line in new_lines: 
                file.write(line)
        utime.sleep_ms(300)
        return user_found
    except Exception as e:
        return False #False mean is a verry bad thing




def create_excel_backup_before_deepsleep(variable_data):
    """ Create internal backup before entering deep sleep """
    try:
        with open("/coffee_backup.csv", 'w') as file:
            for user in variable_data:
                full_name = user["full_name"]
                tag_id = user["tag_id"]
                quantity = user["quantity"]
                file.write(f"{tag_id},{full_name},{quantity}\n")
        utime.sleep_ms(300)

        return True
    except Exception as e:
        return False
    

def delete_local_logs():
    with open("/coffee_backup.csv", 'w') as file:
        file.write("")
    with open("/backup_logs.txt", "w") as file:
        file.write("")

    return True
    
# [
#   'Tag_ID,Full_Name,Quantity\n', 
#  '17412652183861270,Rares D.,6\n', 
#  '17250431722076182,Dragos R.,5\n', 
#  '17385414457571350,Silviu A.,0\n', 
#  '17385554413107222,Radu C.,1\n', '17433380333565974,Valentin B.,0\n', '17208063497091094,Alex B.,0\n'
# ]