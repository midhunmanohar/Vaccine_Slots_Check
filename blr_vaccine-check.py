import requests
from requests import get
import datetime
import json
import time
import os

dist_id1 = 294
dist_id2 = 265

path = '<session file path>'

numdays = 1 
age = 18
vax_limit = 19
dose1_limit = 20
vax_filecount_limit = 40 

#Telegram API links
tele18= "https://api.telegram.org/<>"
tele45 = "https://api.telegram.org/<>"
telelog = "https://api.telegram.org/<>"

headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
#date_str = [x.strftime("%d-%m-%Y") for x in date_list]
date_str = [x.strftime("X%d-X%m-%Y").replace('X0','X').replace('X','') for x in date_list]

def bbmp():
    count = 0
    fileexistcount = 0
    newfilecount = 0
    fileexist_newcount = 0
    fileremovecount = 0
    newfile = ""
    fileremoved = ""
    for INP_DATE in date_str:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print("Timestamp: ", current_time)
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(dist_id1, INP_DATE)
        response = requests.get(URL,headers=headers)
        if (response.status_code != 200):
            print(response)
            requests.get(telelog+"45%2b: URL Fail "+str(response))
        if response.ok:
            try:
                resp_json = response.json()
            except:
                return
            if "centers" in resp_json:
                for center in resp_json["centers"]:
                    for session in center["sessions"]:
                        filename = session["session_id"]
                        if session["min_age_limit"] >= age and session["available_capacity"] > vax_limit and session["available_capacity_dose1"] > dose1_limit:
                            if(session["vaccine"] != ''):
                                if os.path.exists(os.path.join(path,filename)):
                                    with open(os.path.join(path,filename), 'r') as file:
                                        vaxcount = file.read()
                                        if((int(vaxcount))  < session["available_capacity_dose1"]):
											fileexist_newcount = fileexist_newcount + 1
                                        if(int(vaxcount) != session["available_capacity_dose1"]):
                                            with open(os.path.join(path,filename), 'w+') as file:
                                                file.write(str(session["available_capacity_dose1"]))
                                            fileexist_newcount = fileexist_newcount + 1
                                    fileexistcount = fileexistcount + 1
                                else:
                                    with open(os.path.join(path,filename), 'w+') as file:
                                        file.write(str(session["available_capacity_dose1"]))
                                        newfilecount = newfilecount + 1
                                    newfile = newfile + filename + "\n"
                                    try:
                                        if(session["min_age_limit"]==18):
                                            requests.get(tele18+str(center["pincode"])+"\nBBMP \n"+str(session["date"])+"\n"+center["name"]+"\n"+center["block_name"]+"\nVaccine: "+(session["vaccine"])+"\nPrice: "+center["fee_type"]+"\nAvailable Capacity: "+str(session["available_capacity"])+"\nFor Dose1: "+str(session["available_capacity_dose1"])+"\nFor Dose2: "+str(session["available_capacity_dose2"])+"\nAge Limit: "+str(session["min_age_limit"])+"%2b")
                                            print("Bangalore BBMP \nDate: "+str(session["date"])+"\nAge Limit: "+str(session["min_age_limit"])+"%2b\n"+center["name"]+"\n"+center["block_name"]+"\n"+str(center["pincode"])+"\nPrice: "+center["fee_type"]+"\nAvailable Capacity: "+str(session["available_capacity"])+"\nFor Dose1: "+str(session["available_capacity_dose1"])+"\nFor Dose2: "+str(session["available_capacity_dose2"])+"\nVaccine: "+(session["vaccine"])+"\n\n")
                                            time.sleep(1)
                                        if(session["min_age_limit"]==45):
                                            requests.get(tele45+str(center["pincode"])+"\nBBMP \n"+str(session["date"])+"\n"+center["name"]+"\n"+center["block_name"]+"\nVaccine: "+(session["vaccine"])+"\nPrice: "+center["fee_type"]+"\nAvailable Capacity: "+str(session["available_capacity"])+"\nFor Dose1: "+str(session["available_capacity_dose1"])+"\nFor Dose2: "+str(session["available_capacity_dose2"])+"\nAge Limit: "+str(session["min_age_limit"])+"%2b")
                                            print("Bangalore BBMP \nDate: "+str(session["date"])+"\nAge Limit: "+str(session["min_age_limit"])+"%2b\n"+center["name"]+"\n"+center["block_name"]+"\n"+str(center["pincode"])+"\nPrice: "+center["fee_type"]+"\nAvailable Capacity: "+str(session["available_capacity"])+"\nFor Dose1: "+str(session["available_capacity_dose1"])+"\nFor Dose2: "+str(session["available_capacity_dose2"])+"\nVaccine: "+(session["vaccine"])+"\n\n")
                                            time.sleep(1)
                                    except:
                                        print("BBMP Telegram error")
                            count = count + 1
                        else:
                            if os.path.exists(os.path.join(path,filename)):
                                os.remove(os.path.join(path,filename))
                                fileremovecount = fileremovecount + 1
                                fileremoved = fileremoved + filename + "\n"
            else:
                print("No available slots on {} under Bangalore BBMP".format(INP_DATE))
    if(count > 0):
        print("Count:"+str(count))
        print("File Exist Count:"+str(fileexistcount))
        print("File Exist New Count:"+str(fileexist_newcount))
        print("New File Count:"+str(newfilecount))
        print("Removed File Count:"+str(fileremovecount)+"\n\n")
    if(fileexist_newcount >= 1 or newfilecount >= 1 or fileremovecount >= 1):
        requests.get(telelog+"Slots\nBBMP\nTotal Count:"+str(count)+"\nFile Exist Count:"+str(fileexistcount)+"\nFile Exist New Count:"+str(fileexist_newcount)+"\nNew File Count:"+str(newfilecount)+"\n"+newfile+"\nRemoved File Count:"+str(fileremovecount)+"\n"+fileremoved)

def blrurban():
    count = 0
    fileexistcount = 0
    newfilecount = 0
    fileexist_newcount = 0
    fileremovecount = 0
    newfile = ""
    fileremoved = ""
    for INP_DATE in date_str:
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(dist_id2, INP_DATE)
        response = requests.get(URL,headers=headers)
        if (response.status_code != 200):
            print(response)
        if response.ok:
            try:
                resp_json = response.json()
            except:
                return
            if "centers" in resp_json:
                for center in resp_json["centers"]:
                    for session in center["sessions"]:
                        filename = session["session_id"]
                        if session["min_age_limit"] == age and session["available_capacity"] > vax_limit and session["available_capacity_dose1"] > dose1_limit:
                            if(session["vaccine"] != ''):
                                if os.path.exists(os.path.join(path,filename)):
                                    with open(os.path.join(path,filename), 'r') as file:
                                        vaxcount = file.read()
                                        if(int(vaxcount) < session["available_capacity_dose1"]):
											fileexist_newcount = fileexist_newcount + 1
                                        if(int(vaxcount) != session["available_capacity_dose1"]):
                                            with open(os.path.join(path,filename), 'w+') as file:
                                                file.write(str(session["available_capacity_dose1"]))
                                            fileexist_newcount = fileexist_newcount + 1
                                    fileexistcount = fileexistcount + 1
                                else:
                                    with open(os.path.join(path,filename), 'w+') as file:
                                        file.write(str(session["available_capacity_dose1"]))
                                        newfilecount = newfilecount + 1
                                    newfile = newfile + filename + "\n"
                                    try:
                                        if(session["min_age_limit"]==18):
                                            requests.get(tele18+str(center["pincode"])+"\nUrban \n"+str(session["date"])+"\n"+center["name"]+"\n"+center["block_name"]+"\nVaccine: "+(session["vaccine"])+"\nPrice: "+center["fee_type"]+"\nAvailable Capacity: "+str(session["available_capacity"])+"\nFor Dose1: "+str(session["available_capacity_dose1"])+"\nFor Dose2: "+str(session["available_capacity_dose2"])+"\nAge Limit: "+str(session["min_age_limit"])+"%2b")
                                            print("Bangalore Urban \nDate: "+str(session["date"])+"\nAge Limit: "+str(session["min_age_limit"])+"%2b\n"+center["name"]+"\n"+center["block_name"]+"\n"+str(center["pincode"])+"\nPrice: "+center["fee_type"]+"\nAvailable Capacity: "+str(session["available_capacity"])+"\nFor Dose1: "+str(session["available_capacity_dose1"])+"\nFor Dose2: "+str(session["available_capacity_dose2"])+"\nVaccine: "+(session["vaccine"])+"\n\n")
                                            time.sleep(1)
                                        if(session["min_age_limit"]==45):
                                            requests.get(tele45+str(center["pincode"])+"\nUrban \n"+str(session["date"])+"\n"+center["name"]+"\n"+center["block_name"]+"\nVaccine: "+(session["vaccine"])+"\nPrice: "+center["fee_type"]+"\nAvailable Capacity: "+str(session["available_capacity"])+"\nFor Dose1: "+str(session["available_capacity_dose1"])+"\nFor Dose2: "+str(session["available_capacity_dose2"])+"\nAge Limit: "+str(session["min_age_limit"])+"%2b")
                                            print("Bangalore Urban \nDate: "+str(session["date"])+"\nAge Limit: "+str(session["min_age_limit"])+"%2b\n"+center["name"]+"\n"+center["block_name"]+"\n"+str(center["pincode"])+"\nPrice: "+center["fee_type"]+"\nAvailable Capacity: "+str(session["available_capacity"])+"\nFor Dose1: "+str(session["available_capacity_dose1"])+"\nFor Dose2: "+str(session["available_capacity_dose2"])+"\nVaccine: "+(session["vaccine"])+"\n\n")
                                            time.sleep(1)
                                    except:
                                        print("BLR URBAN - Telegram error")
                            count = count + 1
                        else:
                            if os.path.exists(os.path.join(path,filename)):
                                os.remove(os.path.join(path,filename))
                                fileremovecount = fileremovecount + 1
                                fileremoved = fileremoved + filename + "\n"
            else:
                print("No available slots on {} under Bangalore Urban".format(INP_DATE))
    if(count > 0):
        print("Count:"+str(count))
        print("File Exist Count:"+str(fileexistcount))
        print("File Exist New Count:"+str(fileexist_newcount))
        print("New File Count:"+str(newfilecount))
        print("Removed File Count:"+str(fileremovecount)+"\n\n")
    if(fileexist_newcount >= 1 or newfilecount >= 1 or fileremovecount >= 1):
       requests.get(telelog+"Slots\nUrban\nTotal Count:"+str(count)+"\nFile Exist Count:"+str(fileexistcount)+"\nFile Exist New Count:"+str(fileexist_newcount)+"\nNew File Count:"+str(newfilecount)+"\n"+newfile+"\nRemoved File Count:"+str(fileremovecount)+"\n"+fileremoved+"\n")

while(True):
    try:
        bbmp()
        time.sleep(4)
    except:
         requests.get(telelog+"BBMP method failed")
    try:
        blrurban()
        time.sleep(4)
    except:
        requests.get(telelog+"Urban method failed")
