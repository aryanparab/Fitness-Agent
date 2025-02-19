import streamlit as st


reciepe_data= ""


with open('prev_data_reciepe.txt', 'r') as file:
    reciepe_data = file.read()

st.title("Fitness Guru 💪🗓️")
st.subheader("Your Current Reciepes")
st.write(str(reciepe_data))