import streamlit as st
st.title("Hello World!!!!")
st.header("Streamlit Python: Tutorial")
st.subheader("What Is Streamlit?")
st.text("Streamlit is a free and open-source framework to rapidly build and share beautiful machine learning and data science web apps.It is a Python-based library specifically designed for machine learning engineers. Data scientists or machine learning engineers are not web developers and they're not interested in spending weeks learning to use these frameworks to build web apps. Instead, they want a tool that is easier to learn and to use, as long as it can display data and collect needed parameters for modeling.")
st.write("this is different",)


## markdown cheatsheet link = https://www.markdownguide.org/cheat-sheet/
st.markdown("this is a markdown text")
st.markdown("#***this is h2***")
st.markdown(">blackquote")
st.markdown("""
1. Apple
2. banana
3. orange

- First item
- Second item
- Third item

`code`

""")
st.markdown("---")
st.caption("hii it is a caption")
st.markdown("[Markdown cheatsheet]( https://www.markdownguide.org/cheat-sheet/)")
st.markdown("![sorry can not be loaded] (https://wallpapers.com/images/hd/high-on-music-shinchan-aesthetic-92hep3vz56qev2cx.jpg)")

# emojis
st.markdown(":i_love_you_hand_sign: :coffee: :santa:")

st.markdown("##HTML")
htmlcode = """<!DOCTYPE html>
<html>
<body>

<h2>My First JavaScript</h2>

<button type="button"
onclick="document.getElementById('demo').innerHTML = Date()">
Click me to display Date and Time.</button>

<p id="demo"></p>

</body>
</html> 
"""
st.markdown(htmlcode, unsafe_allow_html=True)
st.markdown("## Latex Code")

st.divider()

st.latex(" a_1^2 + a_2^2 = a_3^2 ")
st.latex(" \int\limits_0^1 x^2 + y^2 \ dx ")
st.latex("\sqrt{x^2+1}")
st.latex("E=mc^2")
