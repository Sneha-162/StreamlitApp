import streamlit as st 
image = st.image("Screenshot (13).png")


image = st.file_uploader("Google's logo:")
if image:
    st.image(image)

audio = "acoustic-indie-folk-years-113186.mp3"
st.audio(audio , format="audio/mp3")

audio = st.file_uploader("upload a file:", type=["mp3","wav","midi"])
if audio:
    st.audio(audio)

video = st.video("https://www.youtube.com/watch?v=hKTN6Njxqxk&list=PLc2rvfiptPSSpZ99EnJbH5LjTJ_nOoSWW&index=9")

upload = st.file_uploader("upload a file:", accept_multiple_files= True)
for f in upload:
    st.write(f)

text_file = "this is a text file"
st.download_button("Download",text_file,file_name="text_file")
