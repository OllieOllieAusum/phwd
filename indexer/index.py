import math
import pandas as pd
import os
import time
import json
import datetime

OUTPUTFILE = "gsoytags.json"
INPUTFOLDERGSOY = "indexer/gsoy-latest"
IMPUTFOLDERGSOD = "indexer/gsod-latest"
BACKUPGSOD = "gsodbackup.py"
BACKUPGSOY = "gsoybackup.py"
"""
    Global summary of the day uses a different station id standard than 
    Global summary of the year/month so both need to be indexed
    (This takes a lot of space so neither of the archives are included in git)
    the year for gsod is 2021
"""
if not os.path.exists(BACKUPGSOD) and not os.path.exists(BACKUPGSOY):  # if the backup files don't exist
    gsoylist = [x for x in os.listdir(INPUTFOLDERGSOY) if x.endswith(".csv")]
    gsodlist = [x for x in os.listdir(IMPUTFOLDERGSOD) if x.endswith(".csv")]
    totalfiles = len(gsoylist) + len(gsodlist)
    print("Total files:", totalfiles)
    gsoydatalist = []
    currentprogress = 0
    starttime = time.time()
    totaltime = 0
    for gsoy in gsoylist:
        x = time.time()
        currentprogress += 1
        df = pd.read_csv(os.path.join(INPUTFOLDERGSOY, gsoy))
        if (
            len(df) < 20
            or df["NAME"][0] == ""
        ):
            continue
        gsoydatalist.append({
            "location": str(df["NAME"][0]),
            "gsoy": str(df["STATION"][0])
            })
        totaltime += time.time() - x
        print(
            f"EST: {datetime.timedelta(seconds=math.floor((totaltime/currentprogress)*(totalfiles-currentprogress)))}| {currentprogress} out of {totalfiles}"
        )
    print("GSOY done, now GSOD")
    gsoddatalist = []
    for gsod in gsodlist:
        x = time.time()
        currentprogress += 1
        df = pd.read_csv(os.path.join(IMPUTFOLDERGSOD, gsod))
        if (
            len(df) < 20
            or df["NAME"][0] == ""
        ):
            continue
        gsoddatalist.append({
            "location": str(df["NAME"][0]),
            "gsod": str(df["STATION"][0])
            })
        totaltime += time.time() - x
        print(
            f"EST: {datetime.timedelta(seconds=math.floor((totaltime/currentprogress)*(totalfiles-currentprogress)))}| {currentprogress} out of {totalfiles}"
        )
    print("GSOD done, now saving both files as backups")
    with open(BACKUPGSOD, "w") as f:
        f.write(f"GSODBACKUP = {tuple(gsoddatalist)}")
    with open(BACKUPGSOY, "w") as f:
        f.write(f"GSOYBACKUP = {tuple(gsoydatalist)}")
    print("Backup done. now combining")
else:
    print("Backup found, loading")
    import gsodbackup
    import gsoybackup
    gsoddatalist = gsodbackup.GSODBACKUP
    gsoydatalist = gsoybackup.GSOYBACKUP
masterdata = []
namelist = []
for gsoy in gsoydatalist:
    masterdata.append(gsoy)
    namelist.append(gsoy["location"])
for gsod in gsoddatalist:
    if gsod["location"] in namelist:
        indexer = namelist.index(gsod["location"])
        masterdata[indexer]["gsod"] = gsod["gsod"]
print("Done, took", time.time() - starttime, "seconds")
