import streamlit as st

workout_data = ""


with open('prev_data_workout.txt', 'r') as file:
    workout_data = file.read()

st.title("Fitness Guru 💪🗓️")
st.subheader("Your Current Workout Plan")
st.write(str(workout_data))