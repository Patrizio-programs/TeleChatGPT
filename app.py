import streamlit as st

st.set_page_config(page_title="TeleChatPT Bot", initial_sidebar_state="collapsed")




# Setting the heading at the top of the page
st.title('TeleChatGPT')

# Adding information about TeleChatGPT
st.write(
  "TeleChatGPT is a highly advanced Telegram bot that utilizes the remarkable capabilities of ChatGPT 3.5 turbo to offer unparalleled chat services. With its sophisticated algorithms, TeleChatGPT can understand human language and provide coherent, intelligent, and natural responses in real-time. Whether you're looking for assistance with your daily tasks, need direction on your next travel destination, or want to have a casual conversation with a bot, TeleChatGPT has got you covered. It's precise, efficient, and simplifies chat experience. Powered by one of the leading language models globally, TeleChatGPT guarantees smooth communication, making it the go-to bot for Telegram users."
)


st.header("Support the Creator...")
# Adding the iframe
st.write(
  "<iframe id='kofiframe' src='https://ko-fi.com/patrizothedev/?hidefeed=true&widget=true&embed=true&preview=true' style='border:none;width:100%;padding:4px;background: rgb(251,0,0); background: radial-gradient(circle, rgba(251,0,0,1) 0%, rgba(190,175,14,1) 100%, rgba(0,212,255,1) 100%, rgba(95,36,36,1) 100%);' height='600' title='patrizothedev'></iframe>", 
  unsafe_allow_html=True)

# Adding images at the bottom
col1, col2, col3 = st.columns(3)

with col3:
  st.image("https://i.ibb.co/WPNQ72v/Screenshot-20230419-234300-Telegram.jpg")

with col2:
  st.image("https://i.ibb.co/2qXcpyx/Screenshot-20230419-234317-Telegram.jpg")

with col1:
  st.image("https://i.ibb.co/WFwwmYF/Screenshot-20230419-234422-Telegram.jpg")


