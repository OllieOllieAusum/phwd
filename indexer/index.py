import time

starttime = time.time()
import math
import pandas as pd
import os
import datetime
import json
import logging
logging.basicConfig(filename='IndexLog.log', level=logging.DEBUG, format='%(levelname)s from module %(module)s at %(asctime)s: %(message)s')
logging.info('Started logging')
currentprogress = 0
totaltime = 0
OUTPUTFILE = "gsoytags.json"
INPUTFOLDERGSOY = "indexer/gsoy-latest"
IMPUTFOLDERGSOD = "indexer/gsod-latest"
BACKUPFILE = "indexer/backup.py"
"""
    Global summary of the day uses a different station id standard than 
    Global summary of the year/month so both need to be indexed
    (This takes a lot of space so neither of the archives are included in git)
    the year for gsod is 2021
"""
if os.path.exists(BACKUPFILE):
    filehandle = open(BACKUPFILE, "r")
    logging.info("Found backup file, checking validity")
    backup = filehandle.read()
    print("".join(backup[:10]))
    if "".join(backup[:10]) == "GSODBACKUP":
        logging.info("Successfully validated backup file, skipping index creation")
        isbackup = True
    else:
        logging.info("Backup file is invalid, creating new index")
        isbackup = False
if not isbackup:  # if the backup files don't exist
    gsoylist = [x for x in os.listdir(INPUTFOLDERGSOY) if x.endswith(".csv")]
    gsodlist = [x for x in os.listdir(IMPUTFOLDERGSOD) if x.endswith(".csv")]
    totalfiles = len(gsoylist) + len(gsodlist)
    print("Total files:", totalfiles)
    gsoydatalist = []
    for gsoy in gsoylist:
        x = time.time()
        currentprogress += 1
        df = pd.read_csv(os.path.join(INPUTFOLDERGSOY, gsoy))
        if len(df) < 20 or len(df["NAME"][0]) <= 0 :
            continue
        gsoydatalist.append(
            {"location": str(df["NAME"][0]), "gsoy": str(df["STATION"][0])}
        )
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
        if len(df) < 20 or len(df["NAME"][0]) <= 0:
            continue
        gsoddatalist.append(
            {"location": str(df["NAME"][0]), "gsod": str(df["STATION"][0])}
        )
        totaltime += time.time() - x
        print(
            f"EST: {datetime.timedelta(seconds=math.floor((totaltime/currentprogress)*(totalfiles-currentprogress)))}| {currentprogress} out of {totalfiles}"
        )
    print("GSOD done, now saving both files as backups")
    with open(BACKUPFILE, "w") as f:
        f.write(f"GSODBACKUP = {tuple(gsoddatalist)}\n")
        f.write(f"GSOYBACKUP = {tuple(gsoydatalist)}")
    print("Backup done. now combining")
else:
    logging.info("Importing backup 'module'")
    import backup
    gsoddatalist = backup.GSODBACKUP
    gsoydatalist = backup.GSOYBACKUP

masterdata = []
namelist = []
totallen = len(gsoddatalist) + len(gsoydatalist)
print("Sorting data and discarding invalid data")
sortedgsoddatalist = []
sortedgsoydatalist = []
discardcount = 0
for data in gsoddatalist:
    if data["location"] == "nan":
        discardcount += 1
        continue
    else:
        sortedgsoddatalist.append(data)
print(f"Discarded {discardcount} invalid datasets in Global Summary of the Day")
discardcount = 0
for data in gsoydatalist:
    if data["location"] == "nan":
        discardcount += 1
        continue
    else:
        sortedgsoydatalist.append(data)
print(f"Discarded {discardcount} invalid datasets in Global Summary of the Year")
print("Done, took", time.time() - starttime, "seconds")
