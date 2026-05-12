import streamlit as st
import time
st.title("status and progress")

empty = st.empty()
empty.text("download")
time.sleep(5)
empty.text("downloading")

# progress bar 
progress = st.progress(0)
status_text = st.empty()
for i in range(101):
    # Update the progress bar with one item at a time.
    time.sleep(0.1)
    progress.progress(i)
    status_text.text("Progress:{}" .format(i))
status_text.text("downloaded")

with st.spinner("waiting"):
    time.sleep(5)

st.success("Installed")
st.warning("warning")
st.error("error")
st.info("information")

st.snow()
st.balloons()