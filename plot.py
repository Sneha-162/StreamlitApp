import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px

# df = pd.read_csv("autism_screening.csv")
# st.write(df.head())

# st.area_chart(df[['age','ethnicity']])
# st.bar_chart(df[['age','ethnicity']].head(20))  
# st.line_chart(df[['age','ethnicity']].head(200)) 

# st.sidebar.title("welcome!!!")
# st.sidebar.button("button")
# page = st.sidebar.selectbox("select page", ["page1", "page2"])
# page = st.sidebar.radio("Go to", ["home" , "About" , "Contact"])

# if page == "home":
#     st.title("Home page")

#     with st.popover("open"):

#         st.markdown("Hello :smile:")
#         name = st.text_input("Enter your name")
#     st.write("Welcome", name)
#     with st.expander("click mee"):
#         st.write("This is a expander")

# elif page == "About":
#     st.title("About page")

# else :
#     st.title("Contact page")


# page configuration

st.set_page_config(
   
    page_title="Autism Screening Tool",
    page_icon="💁🏻",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.google.com",
        "Report a bug": "https://www.google.com",
        "About": "https://www.google.com",
    }
)

st.title("working with configuration")

st.sidebar.title("Page configuration")

col = st.columns(3)

col[0].button("button 1")
col[0].write("  click 1")

col[1].button("button 2")
col[1].write("  click 2")

col[2].button("button 3")
col[2].write("  click 3")

col = st.columns([1,2,3])
col[0].write("  click 1")
col[1].write("  click 2")
col[2].write("  click 3")

container = st.container(border=True , height=200)

container.write("Form")
with st.form("Enter Details Here:"):
    name = st.text_input("Enter your name")
    submit_button = st.form_submit_button("Submit")
    age = st.number_input("Enter your age")
   

if submit_button:
    st.write("Thanks for submitting the form")

tab1,tab2,tab3 = st.tabs(["Tab1","Tab2","Tab3"])

with tab1:
    st.write("This is tab 1")
    st.image("game-design.png")