import streamlit as st
st.title("stream input")

st.divider()
name = st.text_input("Enter your name")
age = st.number_input("Enter your age")
feedback = st.text_area("Enter your feedback")
date = st.date_input("Enter your date")
time = st.time_input("Enter your time")
color = st.color_picker("pick a color")


# Display text
st.write("Hello, ", name)
st.write("age,",age)
st.write("feedback,",feedback)
st.write("date,",date)
st.write("time,",time)
st.write("color,",color)

htmlcode = """<!DOCTYPE html>
<html>
<body>

<h2 style = "color:{};">My First JavaScript</h2>

<button type="button"
onclick="document.getElementById('demo').innerHTML = Date()">
Click me to display Date and Time.</button>

<p id="demo"></p>

</body>
</html> 
""".format(color)

st.markdown(htmlcode, unsafe_allow_html=True)

button = st.button("click")
if button:
    st.write("button clicked")

checkbox = st.checkbox("check")
if checkbox:
    st.write("checkbox checked")

radio = st.radio("choose option",["apple","mango","banana"])

box = st.selectbox("choose option",["apple","mango","banana"])
multiselect = st.multiselect("choose option",["apple","mango","banana"])

rating = st.slider("rate",min_value=1,max_value=10,step=1)