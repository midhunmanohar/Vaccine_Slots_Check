import requests
from requests import get
import datetime
import json


BBMP = 294
Blr_urban = 265

numdays = 5 #Days to check ahead of schedule
age = 30

teleurl = "https://api.telegram.org/bot[bot_token]/sendMessage?chat_id=@blrvaxcheck&text="

base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]

headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

def bbmp():
    count = 0
    check = 0
    for INP_DATE in date_str:
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(BBMP, INP_DATE)
        response = requests.get(URL,headers=headers)
        if response.ok:
            resp_json = response.json()
            if resp_json["centers"]:
                #print("Bangalore BBMP\nDate: {}".format(INP_DATE))
                for center in resp_json["centers"]:
                    for session in center["sessions"]:
                        if session["min_age_limit"] <= age and session["available_capacity"] > 0:
                            if count == 0:
                                #print("Bangalore BBMP\nDate: {}".format(INP_DATE))
                                date = INP_DATE
                                count = 1
                            #print("\t", center["name"])
                            #print("\t", center["block_name"])
                            #print("\t Price: ", center["fee_type"])
                            #print("\t Available Capacity: ", session["available_capacity"])
                            
                            if(session["vaccine"] != '' and check == 0):
                                #print("\t Vaccine: ", session["vaccine"])
                                requests.get(teleurl+"Bangalore BBMP\nDate: "+str(date)+"\n\t"+center["name"]+"\n\t"+center["block_name"]+"\n\tPrice: "+center["fee_type"]+"\n\tAvailable Capacity: "+str(session["available_capacity"])+"\n\tVaccine: "+(session["vaccine"]))
                                #print("Bangalore BBMP\nDate: "+str(date)+"\n\t"+center["name"]+"\n\t"+center["block_name"]+"\n\tPrice: "+center["fee_type"]+"\n\tAvailable Capacity: "+str(session["available_capacity"])+"\n\tVaccine: "+(session["vaccine"]))
                                check = 1
                            else:
                                print("No Stock\n")
                            if check == 0:
                                requests.get(teleurl+"Bangalore BBMP\nDate: "+str(date)+"\n\t"+center["name"]+"\n\t"+center["block_name"]+"\n\tPrice: "+center["fee_type"]+"\n\tAvailable Capacity: "+str(session["available_capacity"]))
                                #print("Bangalore BBMP\nDate: "+str(date)+"\n\t"+center["name"]+"\n\t"+center["block_name"]+"\n\tPrice: "+center["fee_type"]+"\n\tAvailable Capacity: "+str(session["available_capacity"]))
                            
                            print("\n\n")
            else:
                print("No available slots on {} under Bangalore BBMP".format(INP_DATE, BBMP))
                #request.get(teleurl+"No available slots on {} under Bangalore BBMP".format(INP_DATE, BBMP))

bbmp()

def blrurban():
    count = 0
    check = 0
    for INP_DATE in date_str:
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(Blr_urban, INP_DATE)
        response = requests.get(URL,headers=headers)
        if response.ok:
            resp_json = response.json()
            if resp_json["centers"]:
                #print("Bangalore Urban\nDate: {}".format(INP_DATE))
                for center in resp_json["centers"]:
                    for session in center["sessions"]:
                        if session["min_age_limit"] <= age and session["available_capacity"] > 0:
                            if count == 0:
                                #print("Bangalore Urban\nDate: {}".format(INP_DATE))
                                date = INP_DATE
                                count = 1
                            #print("\t", center["name"])
                            #print("\t", center["block_name"])
                            #print("\t Price: ", center["fee_type"])
                            #print("\t Available Capacity: ", session["available_capacity"])
                            if(session["vaccine"] != '' and check == 0):
                                #print("\t Vaccine: ", session["vaccine"])
                                requests.get(teleurl+"Bangalore Urban\nDate: "+str(date)+"\n\t"+center["name"]+"\n\t"+center["block_name"]+"\n\tPrice: "+center["fee_type"]+"\n\tAvailable Capacity: "+str(session["available_capacity"])+"\n\tVaccine: "+(session["vaccine"]))
                                #print("Bangalore BBMP\nDate: "+str(date)+"\n\t"+center["name"]+"\n\t"+center["block_name"]+"\n\tPrice: "+center["fee_type"]+"\n\tAvailable Capacity: "+str(session["available_capacity"])+"\n\tVaccine: "+(session["vaccine"]))
                                check = 1
                            else:
                                print("No Stock\n")
                            if check == 0:
                                requests.get(teleurl+"Bangalore Urban\nDate: "+str(date)+"\n\t"+center["name"]+"\n\t"+center["block_name"]+"\n\tPrice: "+center["fee_type"]+"\n\tAvailable Capacity: "+str(session["available_capacity"]))
                                #print("Bangalore BBMP\nDate: "+str(date)+"\n\t"+center["name"]+"\n\t"+center["block_name"]+"\n\tPrice: "+center["fee_type"]+"\n\tAvailable Capacity: "+str(session["available_capacity"]))
                            
                            print("\n\n")
            else:
                print("No available slots on {} under Bangalore Urban".format(INP_DATE))
                #requests.get(teleurl+"No available slots on {} under Bangalore Urban".format(INP_DATE, BBMP))
blrurban()
