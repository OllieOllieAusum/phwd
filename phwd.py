import json
import requests
import re
import os



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
            print(url)
            r = requests.get(url)
            if r.status_code == 200:
                failcounter = 0
                with open(f"{self.folder}/{str(i)}-{stationid}.csv", "w") as f:
                    f.write(r.text)
            else:
                failcounter += 1
                print(f"{i} failed")
            if failcounter > 5:
                print("Failed 5 times, assuming no more data is available")
                break

    def getdatafromyear(self, stationid, year):
        url = self.formaturl(year, stationid)
        r = requests.get(url)
        if r.status_code == 200:
            with open(f"{self.folder}/{str(year)}-{stationid}.csv", "w") as f:
                f.write(r.text)
        else:
            print(f"{year} failed")

    def getdatafromrange(self, stationid, startyear, endyear):
        for i in range(startyear, endyear):
            self.getdatafromyear(stationid, i)

    def usrinput(self, pagesize=os.get_terminal_size().lines - 3):
        print(
            "Enter 1 to search for a specific place, press 2 if you have the station id"
        )
        choice = input()
        page = 1
        if choice == "1":
            results = []
            print("Enter the name of the place")
            print(
                "Fun fact: If you want to search for a place in a state, you just put the abreviation then US"
            )
            print("Like this: CA US")
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
                    print(f"╚╝", flush=True)
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
