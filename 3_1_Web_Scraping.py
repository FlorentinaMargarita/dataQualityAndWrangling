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
import csv 


if __name__ == "__main__":
    def some_function():
        print("Hello World!")

d = dirname(dirname(abspath(__file__)))
sys.path.append(d)

urls = []
with open('urls.csv') as file_obj:
    reader_obj = csv.reader(file_obj)
    for row in reader_obj:
        urls.append(row[0])

# sys.path.append("/Desktop/wrangleIubh/DLBDSDQDW01")

# creating a python dictionary to check my results, since VSCode cannot display hdf5
date_and_hour = str(datetime.now().strftime("%Y-%m-%dT%H"))
hf = h5py.File("records.h5", "r+")
personalJsonFileForCheckingData = {"date and hour": str(date_and_hour)}

# Californias Gas price
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
}
page = requests.get(urls[0], headers=headers)

contents = page.content
soup = BeautifulSoup(page.content)
caliPrice = soup.find(class_="price-text price-text--blue")
stringConversion = str(caliPrice)
indexOfDollar = stringConversion.find("$")
priceOfGas = stringConversion[indexOfDollar + 1 : indexOfDollar + 6]

# hf.create_dataset("californiaAverageGasPrice", data=priceOfGas)
personalJsonFileForCheckingData["californiaAverageGasPrice"] = priceOfGas

# California's need for electricity in megawatts
data = requests.get(
    f"{urls[1]}?data[0]=value&facets[type][]=D&facets[respondent][]=CISO&frequency=hourly&api_key={apiKeys.EIA_API_KEY}&start={date_and_hour}&end={date_and_hour}",

    headers=headers,
).json()
# print(data, 'data')
myData = []
allData = data["response"]["data"]
interestingValues = [myData.append([x["value"], x["period"]]) for x in allData]
print(myData, "myData")
megawatthours_demanded  = myData[0][0]
personalJsonFileForCheckingData['megawatthours_demanded'] = megawatthours_demanded

# stock prices for the biggest EV-manefacturers Tesla, Rivian and Lucid.
import finnhub

finnhub_client = finnhub.Client(api_key=apiKeys.FINNHUB_API_KEY)

tesla_price = int(finnhub_client.quote("TSLA")["c"])
# print(tesla_price, "Tesla")
rivian_price = int(finnhub_client.quote("RIVN")["c"])
# print(rivian_price, "rivian_price")
lucid_price = int(finnhub_client.quote("LCID")["c"])
# print(lucid_price, "Lucid")

personalJsonFileForCheckingData["Tesla"] = tesla_price
personalJsonFileForCheckingData["Rivian"] = rivian_price
personalJsonFileForCheckingData["Lucid"] = lucid_price

data_to_be_stored = [priceOfGas, megawatthours_demanded, tesla_price, rivian_price, lucid_price]
# data_to_be_stored.attrs['DateTime'] = date_and_hour


if date_and_hour not in list(hf.keys()):
    dataset = hf.create_dataset(date_and_hour, (1, 5))
    dataset[...] = data_to_be_stored


dir_containing_file = os.getcwd()

# 👇️ change to directory containing file
os.chdir(dir_containing_file)

file_name = 'controlData.json'

with open(file_name, 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open(file_name, "r") as file_name:
    data = json.load(file_name)


data[date_and_hour] = personalJsonFileForCheckingData

with open('controlData.json', "w") as f:
    json.dump(data, f)

hf.close()