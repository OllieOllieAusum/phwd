import json
import os
import re
import textbox
import pandas as pd
import requests
import string


class getdailydata:
    def __init__(self, folder, eraseonexit=True):
        self.folder = folder
        self.resurl = "https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/"

    def formaturl(self, year, stationid):
        return f"{self.resurl}{str(year)}/{str(stationid)}.csv"

    def cscreen(self):
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")

    def getalldata(
        self, stationid, returnfilelist=True, supressoutput=False, supresswarnings=False
    ):
        if not returnfilelist and not supressoutput:
            print(
                "Warning: returning the raw dictionary may be very slow, use with caution"
            )
        data = []
        for i in range(2022, 1929, -1):
            url = self.formaturl(i, stationid)
            r = requests.get(url)
            if r.status_code == 200:
                failcounter = 0
                with open(f"{self.folder}/{str(i)}-{stationid}.csv", "w") as f:
                    f.write(r.text)
                data.append(
                    self.csvToJson(
                        f"{self.folder}/{str(i)}-{stationid}.csv",
                        supresswarnings=supresswarnings,
                    )
                )
            else:
                failcounter += 1
                if not supressoutput:
                    print(f"{i} failed")
            if failcounter > 5:
                if not supressoutput:
                    print("Failed 5 times, assuming no more data is available")
                break
        return data

    def getdatafromyear(self, stationid, year, returnfilelist=False):
        url = self.formaturl(year, stationid)
        r = requests.get(url)
        if r.status_code == 200:
            with open(f"{self.folder}/{str(year)}-{stationid}.csv", "w") as f:
                f.write(r.text)
            return self.csvToJson(
                f"{self.folder}/{str(year)}-{stationid}.csv",
                returnfilelist=returnfilelist,
            )
        else:
            print(f"{year} failed")

    def getdatafromrange(
        self, stationid, startyear, endyear, supresswarnings=False, returnfilelist=True
    ):
        data = []
        if not returnfilelist and not supresswarnings:
            print(
                "Warning: returning the raw dictionary may be very slow, use with caution"
            )
        for i in range(startyear, endyear):
            data.append(self.getdatafromyear(stationid, i))
        return data

    def usrinput(self, pagesize=os.get_terminal_size().lines - 6):
        print(
            "Enter 1 to search for a specific place, press 2 if you have the station id"
        )
        choice = input()
        page = 1
        if choice == "1":
            results = []
            box = textbox.box()
            box.addtext("Enter the name of the place you want to get the weather from.")
            box.addtext(
                "Fun fact: If you want to search for a place in a state, you just put the abreviation then US"
            )
            box.addtext("Like this: CA US")
            box.addtext(
                "If you live in a country besides the US, this will unfornuatly not work."
            )
            box.print()
            place = input()
            searchterm = re.compile(place, re.IGNORECASE)
            with open("gsoytags.json") as f:
                data = json.load(f)
            results = [match for match in data if searchterm.search(match)]
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
                    return i
                elif choice == "n":
                    self.usrinput()
            else:
                pagenumber = 0
                for i in range(len(results)):
                    if i % pagesize == 0:
                        pagenumber += 1
                print(len(results))
                print(pagenumber)
                box = textbox.box()
                box.addtext(
                    f"Found multiple results. Please select one of the following. Page {page} of {int(pagenumber)}"
                )
                for i in range(len(results)):
                    cname = f"{string.capwords(results[i]['location'].split(',')[0])},{results[i]['location'].split(',')[1]}"
                    box.addtext(f"» {i+1}. {cname}")
                    if i % pagesize == 0 and i > pagesize - 1:
                        box.addtext(f"Press Enter for next page")
                        box.print()
                        usrinpt = input()
                        if usrinpt != "":
                            usrinpt = int(usrinpt)
                            return results[usrinpt - 1]["station"]
                        self.cscreen()
                        page += 1
                        box = textbox.box()
                        box.addtext(
                            f"Found multiple results. Please select one of the following. Page {page} of {int(pagenumber)}"
                        )
                box.addtext(f"Press Enter to go to start")
                box.print()
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

    def frshttconv(self, frshtt):
        x = list(str(int(frshtt)))
        flist = {}
        nofrshtt = True
        try:
            if x[0] == "1":
                flist["fog"] = True
                nofrshtt = False
            if x[1] == "1":
                flist["raindriz"] = True
                nofrshtt = False
            if x[2] == "1":
                flist["snow"] = True
                nofrshtt = False
            if x[3] == "1":
                flist["hail"] = True
                nofrshtt = False
            if x[4] == "1":
                flist["thunder"] = True
                nofrshtt = False
            if x[5] == "1":
                flist["tornado"] = True
                nofrshtt = False
                print(self.dayinfo)
            return flist
        except IndexError:
            if not nofrshtt:
                return flist  # if there are no frshtt codes
            else:
                return None

    def csvToJson(self, file, remove=True, supresswarnings=False, returnfilelist=True):
        df = pd.read_csv(file)
        daydata = []
        for i in range(len(df)):
            self.dayinfo = f"location{df['STATION'][i]} at {df['DATE'][i]}"
            self.dayta = {
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
                "station_pressure_attribs": str(
                    df["STP_ATTRIBUTES"][i]
                ),  # Braden was here
                "visibility": float(df["VISIB"][i]),
                "visibility_attribs": str(df["VISIB_ATTRIBUTES"][i]),
                "wind_speed": float(df["WDSP"][i]),
                "wind_speed_attribs": str(df["WDSP_ATTRIBUTES"][i]),
                "max_sustained_wind": float(df["MXSPD"][i]),
                "max_wind_speed": float(df["GUST"][i]),
                "precipitation": float(df["PRCP"][i]),
                "FRSHTT": str(self.frshttconv(df["FRSHTT"][i])),
            }
            daydata.append(self.dayta)
        for i in range(len(daydata)):
            if daydata[i]["max_wind_speed"] == 999.9:
                daydata[i].pop("max_wind_speed")
        finaldata = {
            "station": int(df["STATION"][0]),
            "longitude": float(df["LONGITUDE"][0]),
            "latitude": float(df["LATITUDE"][0]),
            "elevation": float(df["ELEVATION"][0]),
            "data": daydata,
        }
        path = f"{self.folder}/{str(df['DATE'][0]).split('-')[0]}-{str(df['STATION'][0])}.json"
        with open(path, "w") as f:
            f.write(json.dumps(finaldata, indent=4))
        if remove:
            os.remove(file)
        if returnfilelist:
            return path
        else:
            return finaldata

    def cleanup(self):
        for file in os.listdir(self.folder):
            if file.endswith(".json"):
                os.remove(f"{self.folder}/{file}")


class gethourlydata:  # has to be seperate class because of how the data is formatted between the two
    def __init__(s, downloadfolder):
        s.folder = downloadfolder
        s.url = "https://www.ncei.noaa.gov/data/global-hourly/access/"

    def formaturl(s, stationid, year):
        return f"{s.url}{year}/{stationid}.csv"

    def getdatafromyear(s, stationid, year):
        url = s.formaturl(stationid, year)
        print(url)
        x = requests.get(url)
        if x.status_code == 200:
            with open(f"{s.folder}/{year}-{stationid}.csv", "w") as f:
                f.write(x.text)
        else:
            print(f"{x.status_code}")
