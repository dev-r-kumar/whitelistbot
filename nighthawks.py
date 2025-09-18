import os, json, random, string, requests
from datetime import datetime, timedelta

base_dir = os.path.dirname(__file__)  # Path to the current .py file
file_path = os.path.join(base_dir, "static", "license_metadata.json")
panel_file_path = os.path.join(base_dir, "static", "metadata.json")


class Generator:
    def __init__(self):
        pass

    def generate_segment(self, length=6):
        # Mixed case letters and digits
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=length))

    def generateKey(self, signature="", length = 0):
        segments = [self.generate_segment() for _ in range(length)]
        return f"{signature}-" + '-'.join(segments)

    def generateLicenseKey(self, note="", subscripiton_level=0, duration=0):
        key = self.generateKey(signature="NIGHTHAWKS", length=6)
        license_key = {
            "license_key": key,
            "note": note,
            "used": False,
            "expiry_date": "",
            "level": subscripiton_level,
            "duration": duration, 
            "username": "",
            "password": "",
            "hwind": ""
        }

        # read the old data
        with open(file_path, "r") as jsondata:
            data = json.load(jsondata)

        # append new data to dictionary
        data.append(license_key)

        # write new data
        with open(file_path, "w") as jsondata:
            json.dump(data, jsondata, indent=4)

        return key

class Handler:
    def __init__(self, level_0 = 3, level_1 = 7, level_2 = 30):
        # subscription levels
        self.level_0 = level_0
        self.level_1 = level_1
        self.level_2 = level_2

       


    def GetExpiry(self, subscription_level, subscription_unit):
        total_days = 0

        match (subscription_level):
            case 0:
                total_days = self.level_0 * subscription_unit
            case 1:
                total_days = self.level_1 * subscription_unit
            case 2:
                total_days = self.level_2 * subscription_unit

        creation_date = datetime.now()
        duration = timedelta(days=total_days)
        expiry_date = creation_date + duration

        return datetime.strftime(expiry_date, "%Y-%m-%d %H:%M:%S")
    

    def RegisterAccount(self, license_key, username, password, hwind):
        with open(file_path, "r") as jsondata:
            data = json.load(jsondata)


        for ii in range(len(data)):
            if (data[ii]['license_key'] == license_key):

                if (data[ii]['used'] == False):
                    level = data[ii]['level']
                    duration = data[ii]['duration']

                    data[ii]['used'] = True
                    data[ii]['username'] = username
                    data[ii]['password'] = password
                    data[ii]['expiry_date'] = self.GetExpiry(level, duration)
                    data[ii]['hwind'] = hwind

                    with open(file_path, 'w') as updated_account:
                        json.dump(data, updated_account, indent=4)



                    return "Account registered successfully..."
                
                else:
                    return "License key already taken !"
        return "License key not found !"
                
     
    def LoginAccount(self, username, password, hwind = "", is_bot_request = False):
        with open(file_path, "r") as jsondata:
            data = json.load(jsondata)

        for ii in range(len(data)):
            if (data[ii]['username'] == username):
                # username found
                if (data[ii]['password'] == password):
                    # check hwind here...
                    if not is_bot_request:
                        if (hwind != data[ii]['hwind']):
                            return "Hwind Error !"
                    elif (str(hwind).lower().endswith("_freeze")):
                        return "Account Freeze"
                    else:
                        # make final login here...
                        return "Login Success"
                else:
                    return "Invalid Password !"
        return "No user found !"


    def DaysLeft(self, username, password):
        with open(file_path, 'r') as license_data_file:
            data = json.load(license_data_file)


        for ii in range(len(data)):
            if (data[ii]['username'] == username):
                if (data[ii]['password'] == password):
                    expiry_date = data[ii]['expiry_date']
                    expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d %H:%M:%S")
                    days_left = expiry_date - datetime.now()

        return str(days_left.days)
                

class NightHawks:
    def __init__(self):
        pass

    def patchStatus(self, status):
        with open(panel_file_path, 'r') as panel_config:
            data = json.load(panel_config)

        data[0]['panel']['pc_panel']['is_panel_on'] = status

        with open(panel_file_path, 'w') as new_panel_data:
            json.dump(data, new_panel_data, indent=4)


        return "Server Status Changed..."

    def LoadPanelData(self):
        with open(panel_file_path, 'r') as panel_config:
            data = json.load(panel_config)

        return data
    

    def patchPattern(self, aob_pattern):
        with open(panel_file_path, 'r') as old_panel_data:
            data = json.load(old_panel_data)

        data[0]['panel']['pc_panel']['pattern'] = aob_pattern

        with open(panel_file_path, 'w') as new_panel_data:
            json.dump(data, new_panel_data, indent=4)

        return "AOB Pattern Patched..."


    def patchHeadOffset(self, head_offset):
        with open(panel_file_path, 'r') as old_panel_data:
            data = json.load(old_panel_data)

        data[0]['panel']['pc_panel']['offset_head'] = head_offset

        with open(panel_file_path, 'w') as new_panel_data:
            json.dump(data, new_panel_data, indent=4)

        return "Headshot Offset Patched..."


    def patchLeftEarOffset(self, left_ear_offset):
        with open(panel_file_path, 'r') as old_panel_data:
            data = json.load(old_panel_data)

        data[0]['panel']['pc_panel']['offset_left_ear'] = left_ear_offset

        with open(panel_file_path, 'w') as new_panel_data:
            json.dump(data, new_panel_data, indent=4)

        return "Left Ear Offset Patched..."


    def patchRightEarOffset(self, right_ear_offset):
        with open(panel_file_path, 'r') as old_panel_data:
            data = json.load(old_panel_data)

        data[0]['panel']['pc_panel']['offset_right_ear'] = right_ear_offset

        with open(panel_file_path, 'w') as new_panel_data:
            json.dump(data, new_panel_data, indent=4)

        return "Right Ear Offset Patched..."


    def patchLeftShoulderOffset(self, left_shoulder_offset):
        with open(panel_file_path, 'r') as old_panel_data:
            data = json.load(old_panel_data)

        data[0]['panel']['pc_panel']['offset_left_shoulder'] = left_shoulder_offset

        with open(panel_file_path, 'w') as new_panel_data:
            json.dump(data, new_panel_data, indent=4)

        return "Left Shoulder Offset Patched..." 


    def patchRightShoulderOffet(self, right_shoulder_offset):
        with open(panel_file_path, 'r') as old_panel_data:
            data = json.load(old_panel_data)

        data[0]['panel']['pc_panel']['offset_right_shoulder'] = right_shoulder_offset

        with open(panel_file_path, 'w') as new_panel_data:
            json.dump(data, new_panel_data, indent=4)

        return "Right Shoulder Offset Patched..." 
    




class UIDBypass:
    def __init__(self):
        pass
    
    def whitelistUid(self, uid: str, username: str, password: str):
        try:
            with open("static\\whitelist.json", 'r') as json_file:
                data = json.load(json_file)

            if not isinstance(data, list):
                data = []

            # Check if the username + password combination already exists
            for entry in data:
                if entry['username'] == username and entry['password'] == password:
                    return "Auth is already used !"  # block if same username + password exists

            # Check if UID exists → update credentials if different
            for entry in data:
                if entry['uid'] == uid:
                    entry['username'] = username
                    entry['password'] = password
                    with open("static\\whitelist.json", 'w') as updated:
                        json.dump(data, updated, indent=2)
                    return "Updated subscription"

            # UID not found → add new entry
            data.append({
                "uid": uid,
                "username": username,
                "password": password
            })
            with open("static\\whitelist.json", 'w') as updated:
                json.dump(data, updated, indent=2)
            return "Whitelist Success ✅"

        except Exception as e:
            return str(e)




            
        

    def getUidData(uid: str):
        pass




if __name__ == "__main__":
    # Init Classes...
    nighthwaks = NightHawks()
    license_generator = Generator()
    accountManager = Handler(level_0 = 3, level_1 = 7, level_2 = 30)
    bypass = UIDBypass()


    # Auth Methods...
    def createLicense(note, level, duration):
        key = license_generator.generateLicenseKey(
            note=note,
            subscripiton_level=level,
            duration=duration
        )

        return key
    
    def daysLeft(username, password):
        days_left = accountManager.DaysLeft(username=username, password=password)
        return days_left
        
    def register(key, user, password, hwind):
        response = accountManager.RegisterAccount(
            license_key=key, 
            username=user, 
            password=password,
            hwind=hwind
        )
        return response

    def login(username, password, hwind):
        response = accountManager.LoginAccount(username=username, password=password, hwind=hwind)
        return response
    
    # Panel Patching Methods...
    def patch_pattern(pattern):
        response = nighthwaks.patchPattern(aob_pattern=pattern)
        return response
    
    def patch_head_offset(offset):
        response = nighthwaks.patchHeadOffset(head_offset=offset)
        return response
    
    def patch_left_ear_offset(offset):
        response = nighthwaks.patchLeftEarOffset(left_ear_offset=offset)
        return response
    
    def patch_right_ear_offset(offset):
        response = nighthwaks.patchRightEarOffset(right_ear_offset=offset)
        return response
    
    def patch_left_shoulder_offset(offset):
        response = nighthwaks.patchLeftShoulderOffset(left_shoulder_offset=offset)
        return response
    
    def patch_right_shoulder_offset(offset):
        response = nighthwaks.patchRightShoulderOffet(right_shoulder_offset=offset)
        return response
    

    def load_panel_data():
        return nighthwaks.LoadPanelData()
    

    def patch_status(status):
        return nighthwaks.patchStatus(status=status)
    

    def whitelist_uid(uid: str, username: str, password: str):
        return bypass.whitelistUid(uid=uid, username=username, password=password)
