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

with h5py.File('records.h5', 'r') as filinger:
    lucid_check = filinger.get('2022-11-30T21')
    make_array = lucid_check[...]
    print(np.array(lucid_check), 'lucid_check')

all_dates = list(hf.keys())

print(all_dates, 'alldates')