import streamlit as st
from PIL import Image
import requests
from dotenv import load_dotenv
import os

# Set page tab display
st.set_page_config(
   page_title="Simple Image Uploader",
   page_icon= '🖼️',
   layout="wide",
   initial_sidebar_state="expanded",
)

# Example local Docker container URL
# url = 'http://api:8000'
# Example localhost development URL
url = 'http://localhost:8000' ## ## this needs to be changed and hardcoded
url = 'https://breastlesion-ojtk5b3jdq-ew.a.run.app/'

# App title and description
st.header('Breast Lesion Detection')
st.markdown('''
            > A project to detect breast lesions using deep learning.
            ''')

st.markdown("---")

### Create a native Streamlit file upload input
st.markdown("### Let's upload your picture. 👇")
img_file_buffer = st.file_uploader('Upload an image')


if img_file_buffer is not None:
    img_bytes = img_file_buffer.getvalue()
    col1, col2 = st.columns(2)

    with col1:
        ### Display the image user uploaded
        st.image(Image.open(img_file_buffer), caption="Here's the image you uploaded ☝️")


## the below col2 code is not running (copy from boilerplate only)
    with col2:
        with st.spinner("Wait for it..."):
            ### Get bytes from the file buffer
            res = requests.post(url + "/predict", files={'img': img_bytes})
            print(res.content)
            st.header(f'Your result: ${res.content.decode("utf-8")}')


            ### Make request to  API (stream=True to stream response as bytes)


        if res.status_code == 200:
            ### Return the prediction
            print(res.content)
            print("Hi I worked")
        else:
            st.markdown("**Oops**, something went wrong 😓 Please try again.")
            print(res.status_code, res.content)
