import streamlit as st
from datetime import datetime
import json 

reciepe_data = {}

def convert(date_time):
    format = '%a %b %d %H:%M:%S %Y'
    datetime_str = datetime.strptime(date_time, format)
    return datetime_str

with open('prev_data_reciepe.json', 'r') as file:
    reciepe_data = json.load(file)

st.title("FitFreak 💪🗓️")
st.subheader("Your Next Delicacy")
key,check = "",""
for i in reciepe_data.keys():
    ks = convert(i)
    if check=="" or ks>check:
        key = i
        check = ks

st.caption(key)
st.write(reciepe_data[key])

