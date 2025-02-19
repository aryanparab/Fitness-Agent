import streamlit as st

workout_page = st.Page("workout.py", title="Create a Workout", icon="📝")
reciepe_page = st.Page("chef.py", title="Cook Something Delicious", icon="👨🏻‍🍳")
workout_plan= st.Page("show_workout_plan.py",title="See your Current Workout Plan",icon="🦾")
reciepe_in=st.Page("reciepein.py",title="See your reciepes",icon="🍳")

pg = st.navigation({
    "Your Personal Helps":[workout_page, reciepe_page],
    "Your Plans":[workout_plan,reciepe_in]})
st.set_page_config(page_title="FitFreak", page_icon="🐅")
pg.run()