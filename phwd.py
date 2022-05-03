import json
import requests
import re
import os
import pandas as pd



class getweatherdata:
    def __init__(self, folder):
        self.folder = folder
        self.resurl = "https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/"

    def formaturl(self, year, stationid):
        return f"{self.resurl}{str(year)}/{str(stationid)}.csv"

    def cscreen(self):
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")

    def getalldata(self, stationid):
        for i in range(2022, 1929, -1):
            url = self.formaturl(i, stationid)
            data = []
            r = requests.get(url)
            if r.status_code == 200:
                failcounter = 0
                with open(f"{self.folder}/{str(i)}-{stationid}.csv", "w") as f:
                    f.write(r.text)
                data.append(self.csvToJson(f"{self.folder}/{str(i)}-{stationid}.csv"))
            else:
                failcounter += 1
                print(f"{i} failed")
            if failcounter > 5:
                print("Failed 5 times, assuming no more data is available")
                break
        return data

    def getdatafromyear(self, stationid, year):
        url = self.formaturl(year, stationid)
        r = requests.get(url)
        if r.status_code == 200:
            with open(f"{self.folder}/{str(year)}-{stationid}.csv", "w") as f:
                f.write(r.text)
            return self.csvToJson(f"{self.folder}/{str(year)}-{stationid}.csv")
        else:
            print(f"{year} failed")

    def getdatafromrange(self, stationid, startyear, endyear):
        data = []
        for i in range(startyear, endyear):
            self.getdatafromyear(stationid, i)
            data.append(self.csvToJson(f"{self.folder}/{str(i)}-{stationid}.csv"))
        return data

        

    def usrinput(self, pagesize=os.get_terminal_size().lines - 4):
        print(
            "Enter 1 to search for a specific place, press 2 if you have the station id"
        )
        choice = input()
        page = 1
        if choice == "1":
            results = []
            print("Enter the name of the place you want to get the weather data for."                           )
            print("Fun fact: If you want to search for a place in a state, you just put the abreviation then US")
            print("Like this: CA US")
            print("If you live in a country besides the US, this will unfornuatly not work.")                                                                            
            place = input()
            searchterm = re.compile(place, re.IGNORECASE)
            with open("tags.json") as f:
                data = json.load(f)
            for i in data:
                if searchterm.search(i["location"]):
                    results.append(i)
            print(len(results))
            if len(results) == 0:
                print("No results found")
                self.usrinput()
            elif len(results) == 1:
                print("Found 1 result")
                print(f"{i['location']}")
                print("Does this look right? (y/n)")
                choice = input()
                if choice == "y":
                    return i["id"]
                elif choice == "n":
                    self.usrinput()
            else:
                pagenumber = 0
                for i in range(len(results)):
                    if i % pagesize == 0:
                        pagenumber += 1
                print(len(results))
                print(pagenumber)
                print(
                    f"╔╗Found multiple results. Please select one of the following. Page {page} of {int(pagenumber)}"
                )
                for i in range(len(results)):
                    print(f"║║ » {i+1}. {results[i]['location']}")
                    if i % pagesize == 0 and i > pagesize - 1:
                        print(f"╚╝Press Enter for next page", flush=True)
                        usrinpt = input()
                        if usrinpt != "":
                            usrinpt = int(usrinpt)
                            return results[usrinpt - 1]["station"]
                        self.cscreen()
                        page += 1
                        print(
                            f"╔╗Found multiple results. Please select one of the following. Page {page} of {int(pagenumber)}"
                        )
                print(f"╚╝Press Enter to go to start", flush=True)
                usrinpt = input()
                if usrinpt != "":
                    usrinpt = int(usrinpt)
                    return results[usrinpt - 1]["station"]
                elif usrinpt == "":
                    self.usrinput()
        elif choice == "2":
            print("Enter the station id:", flush=True, end="")
            stationid = input()
            stationid = int(stationid)
            from validids import VALID

            if stationid in VALID:
                return stationid
            else:
                print("Invalid station id")
                self.usrinput()
    def csvToJson(self, file, remove = True):
        df = pd.read_csv(file)
        daydata = []
        for i in range(len(df)):
            dayta = {
                "date": str(df["DATE"][i]),
                "temp": float(df["TEMP"][i]),
                "max_temp": float(df["MAX"][i]),
                "max_attrib": str(df["MAX_ATTRIBUTES"][i]),
                "min_temp": float(df["MIN"][i]),
                "min_attrib": str(df["MIN_ATTRIBUTES"][i]),
                "temp_attribs": str(df["TEMP_ATTRIBUTES"][i]),
                "dewpoint": float(df["DEWP"][i]),
                "dewp_attribs": str(df["DEWP_ATTRIBUTES"][i]),
                "sea_level_pressure": float(df["SLP"][i]),
                "sea_level_pressure_attribs": str(df["SLP_ATTRIBUTES"][i]),
                "station_pressure": float(df["STP"][i]),
                "station_pressure_attribs": str(df["STP_ATTRIBUTES"][i]),                                                                                                                            # Braden was here
                "visibility": float(df["VISIB"][i]),
                "visibility_attribs": str(df["VISIB_ATTRIBUTES"][i]),
                "wind_speed": float(df["WDSP"][i]),
                "wind_speed_attribs": str(df["WDSP_ATTRIBUTES"][i]),
                "max_sustained_wind": float(df["MXSPD"][i]),
                "max_wind_speed": float(df["GUST"][i]),
                "precipitation": float(df["PRCP"][i]),
                "FRSHTT": str(df["FRSHTT"][i]),
            }
            daydata.append(dayta)
            print(".", end="", flush=True)
        finaldata = {
            "station": int(df["STATION"][0]),
            "longitude": float(df["LONGITUDE"][0]),
            "latitude": float(df["LATITUDE"][0]),
            "elevation": float(df["ELEVATION"][0]),
            "data": daydata,
        }
        with open(f"{self.folder}/{str(df['DATE'][0]).split('-')[0]}-{str(df['STATION'][0])}.json", "w") as f:
            f.write(json.dumps(finaldata, indent=4))
        if remove: os.remove(file)
        return finaldata
        
