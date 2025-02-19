import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.exa import ExaTools
import json
from datetime import datetime
import time

st.title("FitFreak 💪🗓️")
st.subheader("Your Personal Chef 🧑‍🍳")
st.caption("This app will create a reciepes for you based on your workout plan and items in your kitchen")

md = "llama-3.3-70b-versatile"
workout_data = {}
reciepe_data= ""

try:
    with open('prev_data_workout.json', 'r') as file:
        workout_data = json.load(file)
except:
     pass

with open('prev_data_reciepe.json', 'r') as file:
    reciepe_data = json.load(file)


cook_agent = Agent(
    description="You will help the user with reciepes with the ingredients they have.",
    model = Groq(id=md),
    name ="Chef",
    tools=[ExaTools(api_key= "de8ed4f8-7cd1-4be0-8e2b-7d9beeb7f21b")],
    add_history_to_messages=True,
    markdown=True,
    instructions=[
        "Search for recipes based on the ingredients and time available from the knowledge base.",
        "Include the exact calories,all ingredients required, preparation time, cooking instructions, and highlight allergens for the recommended recipes.",
        "Always search exa for recipe links or tips related to the recipes apart from knowledge base.",
        "Provide a list of recipes that match the user's requirements and preferences.",
        "If the user has not provided many ingredients or only core element of the food, provide an easy reciepe which doesn't require many ingredients."
        "Always return steps of the cooking process"
    ],
)

summarizer = Agent(
    description="Your job is to summarize the input data for optimal usage in LLM models",
    model = Groq(id=md),
    name = "Summarizer",
    instructions=[
        "You are a text summarizer",
        "your goal is to take a workout plan as input and create a summary for of it.",
        "the summary will be used by a chef to cook meals",
        "Ensure that the summary includes parts and information that will help the chef with nutrition"
    ]
)


#STREAMLIT Stuff

with st.form("my_form"):
   ingredients = st.text_input("Input list of Ingredients in your fridge",placeholder="Chicken, rice, eggs, potato, milk, garlic, pasta")
   take_exercise= st.selectbox("Do you want me to take your current workout in to account? ",["Yes","No"])
   cook_duration = st.number_input('Maximum time to cool your meal (in mins)',min_value=15)
   type_of_dish = st.multiselect("What kind of dish would you like? ",
                                 [
                                      "Savoury","Healthy","Calorie Controlled","Stomach filling","Cheat meal"
                                 ],max_selections=2)

   submit = st.form_submit_button('Fight On!')

def convert(date_time):
    format = '%a %b %d %H:%M:%S %Y'
    datetime_str = datetime.strptime(date_time, format)
    return datetime_str

if submit:
    rr="No routine"
    if take_exercise=="Yes":
        key,check = "",""
        for i in workout_data.keys():
            ks = convert(i)
            if check=="" or ks>check:
                key = i
                check = ks
        
        rr =  summarizer.run(workout_data[key])
    if ingredients=="":
         ingredients="None"
    input_statement = f"""
        Hi Chef!! My name is User. I want you to help me with some awesome reciepes which are {type_of_dish}.
        Currently the ingredients with me are : {ingredients}.
        Maximum cooking duration should be {cook_duration}.    
        My current workout routine is {rr}.
             """
    print(input_statement)
    response = cook_agent.run(input_statement, stream=False)
    st.write(str(response.content))
    with open('prev_data_reciepe.json', 'w') as file:
            reciepe_data.update({time.ctime():response.content})
            
            json.dump(reciepe_data, file, indent=4)

    

