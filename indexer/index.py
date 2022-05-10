import math
import pandas as pd
import os
import time
import json
import datetime

OUTPUTFILE = "gsoytags.json"
INPUTFOLDERGSOY = "indexer/gsoy-latest"
IMPUTFOLDERGSOD = "indexer/gsod-latest"
"""
    Global summary of the day uses a different station id standard than 
    Global summary of the year/month so both need to be indexed
    (This takes a lot of space so neither of the archives are included in git)
    the year for gsod is 2021
"""
gsoylist = [x for x in os.listdir(INPUTFOLDERGSOY) if x.endswith(".csv")]
gsodlist = [x for x in os.listdir(IMPUTFOLDERGSOD) if x.endswith(".csv")]
totalfiles = len(gsoylist) + len(gsodlist)
print("Total files:", totalfiles)
masterdatalist = {}
currentprogress = 0
starttime = time.time()
totaltime = 0
for gsoy in gsoylist:
    x = time.time()
    currentprogress += 1
    df = pd.read_csv(os.path.join(INPUTFOLDERGSOY, gsoy))
    if (
        len(df) < 20
        or df["NAME"][0] == "nan"
        or df["NAME"][0] == ""
        or df["NAME"][0] == " "
        or df["NAME"][0] == "NaN"
    ):
        continue
    masterdatalist[str(df["NAME"][0])] = {"gsoy": str(df["STATION"][0])}
    totaltime += time.time() - x
    print(
        f"EST: {datetime.timedelta(seconds=math.floor((totaltime/currentprogress)*(totalfiles-currentprogress)))}| {currentprogress} out of {totalfiles}"
    )
print("GSOY done, now GSOD")
for gsod in gsodlist:
    x = time.time()
    currentprogress += 1
    df = pd.read_csv(os.path.join(IMPUTFOLDERGSOD, gsod))
    if (
        len(df) < 20
        or df["NAME"][0] == "nan"
        or df["NAME"][0] == ""
        or df["NAME"][0] == " "
        or df["NAME"][0] == "NaN"
    ):
        continue
    if df["NAME"][0] in masterdatalist:
        masterdatalist[str(df["NAME"][0])]["gsod"] = str(df["STATION"][0])
    else:
        masterdatalist[df["NAME"][0]] = {"gsod": str(df["STATION"][0])}
    totaltime += time.time() - x
    print(
        f"EST: {datetime.timedelta(seconds=math.floor((totaltime/currentprogress)*(totalfiles-currentprogress)))}| {currentprogress} out of {totalfiles}"
    )
print("GSOD done, now converting to JSON")
try:
    with open(OUTPUTFILE, "w") as f:
        json.dump(masterdatalist, f)
except Exception as e:
    print(f"Error: {e}, Exporting data as a python dictionary")
    try:
        with open("backup.py", "w") as f:
            f.write(f"DATA = {masterdatalist}")
    except Exception as e:
        print(f"Well im really grasping for straws but here is the error: {e}")
        print("saving to a blank text file")
        with open("backup.txt", "w") as f:
            f.write(masterdatalist)
print("Done, took", time.time() - starttime, "seconds")
