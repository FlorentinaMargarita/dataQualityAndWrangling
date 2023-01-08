from email.policy import default
from ssl import get_default_verify_paths
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import h5py

#supressing scientific notation
np.set_printoptions(suppress=True)

hf = h5py.File("records.h5", "r")

all_gasprices = []
megawatthours_demanded = []
all_tesla_data = []
all_rivian_data = []
all_lucid_data = []

all_dates = list(hf.keys())

all_data = []

time_line_dates  = []
clean_dates = [x[0:10] for x in all_dates]
unique_dates = []
for x in clean_dates: 
    if x not in unique_dates:
        unique_dates.append(x)

used_dates = []
#cleaning data to get only one row of values per day.
with h5py.File('records.h5', 'r') as filinger:
    for date in all_dates:
        formatted_date = date[0:10]
        if formatted_date not in used_dates:
            lucid_check = filinger.get(date)
            make_array = lucid_check[...]
            all_data.append({formatted_date: make_array})
            used_dates.append(formatted_date)



for data in all_data:

        all_gasprices.append(make_array[0][0])
        megawatthours_demanded.append(make_array[0][1])
        all_tesla_data.append(make_array[0][2])
        all_rivian_data.append(make_array[0][3])
        all_lucid_data.append(make_array[0][4])


df = pd.DataFrame({'Date': used_dates,
                     
                   'Gasprice': all_gasprices,
                     
                   'Megawatth': megawatthours_demanded,
                     
                   'Tesla': all_tesla_data,
                   'Rivian': all_rivian_data,
                   'Lucid': all_lucid_data})

df.plot()
plt.show()