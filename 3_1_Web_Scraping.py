from bs4 import BeautifulSoup
import requests
import h5py
import json
from datetime import datetime
import numpy as np
import apiKeys 
import sys
from os.path import dirname, abspath
import os

if __name__ == "__main__":
    def some_function():
        print("Hello World!")

d = dirname(dirname(abspath(__file__)))
sys.path.append(d)
print(sys.path, 'ahhhh')

# sys.path.append("/Desktop/wrangleIubh/DLBDSDQDW01")

# crating the hdf5 file
# crating a python dictionary to check my results, since VSCode cannot display hdf5
date_and_hour = str(datetime.now().strftime("%Y-%m-%dT%H"))
file_name = "{date_and_hour} records"
hf = h5py.File("records", "w")

personalJsonFileForCheckingData = {"date and hour": str(date_and_hour)}

# Californias Gas price
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
}
page = requests.get("https://gasprices.aaa.com/?state=CA", headers=headers)
contents = page.content
soup = BeautifulSoup(page.content)
caliPrice = soup.find(class_="price-text price-text--blue")
stringConversion = str(caliPrice)
indexOfDollar = stringConversion.find("$")
priceOfGas = stringConversion[indexOfDollar + 1 : indexOfDollar + 6]
print(priceOfGas, "priceOfGas")

hf.create_dataset("californiaAverageGasPrice", data=priceOfGas)
personalJsonFileForCheckingData["californiaAverageGasPrice"] = priceOfGas

# Californias need for electricity in megawatts
data = requests.get(
    f"https://api.eia.gov/v2/electricity/rto/region-data/data?data[0]=value&facets[type][]=D&facets[respondent][]=CISO&frequency=hourly&api_key={apiKeys.EIA_API_KEY}&start={date_and_hour}&end={date_and_hour}",
    headers=headers,
).json()
myData = []
allData = data["response"]["data"]
interestingValues = [myData.append([x["value"], x["period"]]) for x in allData]
print(myData, "myData")
personalJsonFileForCheckingData['megawatthours_demanded'] = myData[0][0]
hf.create_dataset('megawatthours_demanded', data=myData[0][0])

# stock prices for the biggest EV-manefacturers Tesla, Rivian and Lucid.

import finnhub

finnhub_client = finnhub.Client(api_key=apiKeys.FINNHUB_API_KEY)

tesla_price = int(finnhub_client.quote("TSLA")["c"])
print(tesla_price, "Tesla")
rivian_price = int(finnhub_client.quote("RIVN")["c"])
print(rivian_price, "rivian_price")
lucid_price = int(finnhub_client.quote("LCID")["c"])
print(lucid_price, "Lucid")

personalJsonFileForCheckingData["Tesla"] = tesla_price
personalJsonFileForCheckingData["Rivian"] = rivian_price
personalJsonFileForCheckingData["Lucid"] = lucid_price

hf.create_dataset("TeslaPrice", data=tesla_price)
hf.create_dataset("RivianPrice", data=rivian_price)
hf.create_dataset("Lucid", data=lucid_price)

print(personalJsonFileForCheckingData, "personalJsonFileForCheckingData")

# my_absolute_path = r'C:/Users/flore/Desktop/wrangleIubh/DLBDSDQDW01/Unit_3_Data_Acquisition/controlData.json'

dir_containing_file = os.getcwd()
print(dir_containing_file, 'dir contianing faile')

# 👇️ change to directory containing file
os.chdir(dir_containing_file)

file_name = 'controlData.json'

with open(file_name, 'r', encoding='utf-8') as f:
    lines = f.readlines()

    print(lines)

with open(file_name, "r") as file_name:
    data = json.load(file_name)


data[date_and_hour] = personalJsonFileForCheckingData
# hammer = str(data)
#
with open('controlData.json', "w") as f:
    json.dump(data, f)

# with open('controlData.json', "w") as f:
#     json.dump({'hi': 'ho'}, f)


with h5py.File('records', 'r') as jsonFile:
    lucid_check = jsonFile.get('Lucid')
    lucid_check = np.array(lucid_check)
    print(lucid_check.shape, 'lucid_check')