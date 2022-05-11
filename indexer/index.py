import math
import pandas as pd
import os
import time
import json
import datetime
import multiprocessing as mp

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
def gsodindexer(IMPUTFOLDERGSOD):
    currprogressgsod = 0
    gsodlist = [x for x in os.listdir(IMPUTFOLDERGSOD) if x.endswith(".csv")]
    totalgsod = len(gsodlist)
    gsodtaglist = {}
    for gsod in gsodlist:
        df = pd.read_csv(os.path.join(IMPUTFOLDERGSOD, gsod))
        print(currprogressgsod, "/", totalgsod)
        currprogressgsod += 1
        if (
            len(df) < 20
            or df["NAME"][0] == "nan"
            or df["NAME"][0] == ""
            or df["NAME"][0] == " "
            or df["NAME"][0] == "NaN"
        ):
            continue
        if df["NAME"][0] in masterdatalist:
           gsodtaglist[str(df["NAME"][0])]["gsod"] = str(df["STATION"][0])
        else:
            gsodtaglist[df["NAME"][0]] = {"gsod": str(df["STATION"][0])}
    queue.put(gsodtaglist)
def gsoyindexer(INPUTFOLDERGSOY):
    currprogressgsoy = 0
    gsoylist = [x for x in os.listdir(INPUTFOLDERGSOY) if x.endswith(".csv")]
    totalgsoy = len(gsoylist)
    gsoytaglist = {}
    for gsoy in gsoylist:
        df = pd.read_csv(os.path.join(INPUTFOLDERGSOY, gsoy))
        print(currprogressgsoy, "/", totalgsoy)
        currprogressgsoy += 1
        if (
            len(df) < 20
            or df["NAME"][0] == "nan"
            or df["NAME"][0] == ""
            or df["NAME"][0] == " "
            or df["NAME"][0] == "NaN"
        ):
            continue
        gsoytaglist[str(df["NAME"][0])] = {"gsoy": str(df["STATION"][0])}
    queue.put(gsoytaglist)
if __name__ == "__main__":
    queue = mp.Queue()
    processes = []
    processes.append(mp.Process(target=gsodindexer, args=(IMPUTFOLDERGSOD,)))
    processes.append(mp.Process(target=gsoyindexer, args=(INPUTFOLDERGSOY,)))
    for p in processes:
        p.start()

    for p in processes:
        p.join()
    print("GSOD done, now converting to list")
    finaldata = []
    for key, value in masterdatalist:
        finaldata.append([key,value])

    try:
        with open(OUTPUTFILE, "w") as f:
            json.dump(masterdatalist, f)
    except Exception as e:
        print(f"Error: {e}, Exporting data as a python dictionary")
        try:
            with open("backup.py", "w") as f:
                f.write(f"DATA = {masterdatalist}")
        except Exception as e:
            try:
                print(f"Well im really grasping for straws but here is the error: {e}")
                print("saving to a blank text file")
                with open("backup.txt", "w") as f:
                    f.write(masterdatalist)
            except:
                print("how did you get here?")
                print("printing data as a fallback fallback fallback")
                print(masterdatalist)
    print("Done, took", time.time() - starttime, "seconds")
