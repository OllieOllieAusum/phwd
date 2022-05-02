# phwd: The historical weather data library for python
PHWD is short for Python Historical Weather Data.
This library is used to get weather history data from NOAA NCEI.
The data goes back to 1929, but the ammount of data is limited the further back you go.
The data is retrived from NOAA NCEI is in a csv format.

## Data fetching Functions


**getalldata(stationid)** is used to get all the data from the NCEI for a specific station. Getting all the data from the NCEI weather archive would take a 
large amount of disk space, so this function is used to only get data thats needed.

**getdatafromyear(stationid,year)** is used to get the data for a specific year from the NCEI.

**getdatafromrange(stationid,startyear,endyear)** is used to get the data for a specific range of years from the NCEI without having to download all of a station's data.

## Misc. Functions

**formaturl(year,stationid)** is used to format the url to get the data. mainly for internal use.

**usrinput()** is used to get the user input for a station. This function contains the ability to seach or just input a stationid. 
This function does not get data by itself, but returns the stationid to be used by the other data fetching functions. 
The pagesize variable is used to set the number of data points to be returned per page. 
Default is the rows of the terminal minus 4.

**cscreen()** Clears the screen. This is also mainly for internal use.
## Files
**tags.json** is used to get the station id for a specific station from the seach function in usrinput.

**validids.py** is used to validate a station id inputed by the user to prevent useless requests to NCEI.

**example.py** example file for basic library usage