import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.exa import ExaTools
import time
import json

st.title("FitFreak 🐅")
st.subheader("Your Personal Trainer 💪")
st.caption("This app will create a custom Fitness plan for you to help you achieve your goals")

md = "llama-3.3-70b-versatile"
workout_data = {}
reciepe_data= ""


with open('prev_data_workout.json', 'r') as file:
        workout_data = json.load(file)



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


#STREAMLIT Stuff

with st.form("my_form"):
   
   sex = st.selectbox("Your Sex",['Male','Female'])
   exercise_freq = st.selectbox("Your Current Exercise Frequency ",["Daily","5 times a week","thrice a week","I have a busy schedule"])
   age = st.number_input('Select Age',min_value=15)
   goal = st.multiselect("Your Fitness Goal is to become",
                         ["Muscular","Fit","Lean Body","Get Six Pack abs","Running","Improvement in sports"],
                         max_selections=3)
   days_to_workout = st.slider("No. of days to workout per week",1,7)
   gym_access = st.selectbox("Do you have access to a Gym?",["Yes","No"])
   include_steps = st.selectbox("Do you want your workout to include a step goal?",["Yes","No"])

   submit = st.form_submit_button('Fight On!')

if submit:
    input_statement = f"""
        Hi trainer!! My name is User. I am a {age} year old {sex} who exercises {exercise_freq}. 
            My goal is to become {goal}. Please provide me with a workout plan for {days_to_workout} days per week.
            Does User have access to gym: {gym_access}. 
            Include cardio and steps goal :{include_steps} """
    print(input_statement)
    # response = input_statement
    # st.write("Done")
    response = exercise_agent.run(input_statement, stream=False)
    st.write(str(response.content))
    with open('prev_data_workout.json', 'w') as file:
            workout_data.update({time.ctime():response.content})
            print(workout_data)
            json.dump(workout_data, file, indent=4)

    

