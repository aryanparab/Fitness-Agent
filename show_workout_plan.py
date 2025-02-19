import streamlit as st
from datetime import datetime
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.exa import ExaTools
import json 


md = "llama-3.3-70b-versatile"
exercise_agent = Agent(
    description="you will create for the user a workout plan based on their preferences.",
    model = Groq(id=md),
    name = "Trainer",
    instructions=[
        "You are a highly skilled fitness trainer agent",
        "Your goal is to create a workout plan for your users, and if they provide a workout plan you should be able to improve it",
        "The workout plan should be matched to the goal that the user wants to achieve",
        "Include for every exercise how it should be done and what muscles are activated during the same.",
        "The size of output should be less than 6000 words"
    ]
    , 
    tools=[ExaTools(api_key= "de8ed4f8-7cd1-4be0-8e2b-7d9beeb7f21b")]
)

workout_data = {}

def convert(date_time):
    format = '%a %b %d %H:%M:%S %Y'
    datetime_str = datetime.strptime(date_time, format)
    return datetime_str

with open('prev_data_workout.json', 'r') as file:
    workout_data = json.load(file)

st.title("FitFreak 💪🗓️")
st.subheader("Your Current Workout Plan")
key,check = "",""
for i in workout_data.keys():
    ks = convert(i)
    if check=="" or ks>check:
        key = i
        check = ks

st.caption(key)
st.write(workout_data[key])

with st.form("Changes form"):
    changes = st.text_area("Do you want to make any changes to the above plan? ")
    submit2 = st.form_submit_button("Make Changes!")
    if submit2:
        input_statement = workout_data[key] + " Make the following changes to the above routine : " + changes
        resp = exercise_agent.run(input_statement,stream=False)
        with open('prev_data_workout.json', 'w') as file:
            workout_data.update({key:workout_data[key] + " " + resp.content})
            #workout_data.remove(key)
           
            json.dump(workout_data, file, indent=4)

