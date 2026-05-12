import streamlit as st
import pandas as pd

# json
json_data = {
    "name": "John",
    "age": 30,
    "city": "New York"
}
st.json(json_data)

df = pd.read_csv("autism_screening.csv")
# st.write(df)
st.dataframe(df.head())
st.table(df.head())
st.code("""
json_data = {
    "name": "John",
    "age": 30,
    "city": "New York"
    }"""
)

st.metric("Accuracy:", value=76 , delta=80-76)

edited_data = st.data_editor(df.head())
st.write(edited_data)
edited_data.to_csv("autism_screening.csv1", index=False)
