import streamlit as st
from PIL import Image
import requests
from dotenv import load_dotenv
import os
import base64



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


# Load the background image
image_path = "final image_resized.jpg"
with open(image_path, "rb") as img_file:
    img_encoded = base64.b64encode(img_file.read()).decode()

# Set CSS with background image
css = f"""
    <style>
        .title-container {{
            background-image: url('data:image/jpg;base64,{img_encoded}');
            background-size: cover;  /* Maintain aspect ratio while covering the width */
            background-repeat: no-repeat;
            padding: 20px;
            border-radius: 10px;
            color: white;
            margin-top: -50px; /* Adjust the margin */
        }}
        .title-container h1 {{
            color: white;  /* Change the color of the title to white */
        }}
    </style>
"""

# Display the title and description
st.markdown(
    css +
    """
    <div class="title-container">
        <h1>Breast Lesion Classification</h1>
        <p>This application utilizes a deep learning model to predict breast lesion images from ultrasound scans.</p>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown("---")

### Create a native Streamlit file upload input
st.markdown("<h3 style='font-size: 20px;'>Let's upload your picture. <span>👇</span></h3>", unsafe_allow_html=True)
img_file_buffer = st.file_uploader('Upload an image')


if img_file_buffer is not None:
    img_bytes = img_file_buffer.getvalue()
    col1, col2 = st.columns(2)

    with col1:
        ### Display the image user uploaded
        uploaded_image = Image.open(img_file_buffer)
        uploaded_image.thumbnail((100, 100))  # Resize image
        st.image(uploaded_image, caption="Here's the image you uploaded ☝️")




## the below col2 code is not running (copy from boilerplate only)
    with col2:
        with st.spinner("Wait for it..."):
            ### Get bytes from the file buffer
            res = requests.post(url + "/predict", files={'img': img_bytes})
            proba_benign=eval(res.content.decode("utf-8"))[0]
            proba_malignant=eval(res.content.decode("utf-8"))[1]
            print(proba_malignant)
            #print(res.content.decode("utf-8"))
            #st.markdown(f'<div style="display: flex; justify-content: center;"><div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center;"><h3 style="font-size: 24px;">Your result: ${res.content.decode("utf-8")}</h3></div></div>', unsafe_allow_html=True)
            if proba_benign >= 0.7:
                st.success(f'The predicted probability of the lesion being benign is {int(proba_benign*100)}%')
            elif proba_malignant>= 0.7:
                st.error(f'The predicted probability of the lesion being malignant is {int(proba_malignant*100)}%')
            else:
                st.warning(f'Uncertainty warning! The predicted probability of the lesion being benign is only: {int(proba_benign*100)}%, and being malignant: {int(proba_malignant*100)}%')
            ### Make request to  API (stream=True to stream response as bytes)

        if res.status_code == 200:
            ### Return the prediction
            print(res.content)
            print("Hi I worked")
        else:
            st.markdown("**Oops**, something went wrong 😓 Please try again.")
            print(res.status_code, res.content)




st.markdown("---")
st.markdown("""
<h3 style='font-size: 10px;'>Legal Disclaimer</h3>
<p style='font-size: 10px;'>This tool is designed for use by health care professionals as an aid in the assessment of breast lesions. It is intended to provide support and a second opinion by analyzing medical images through artificial intelligence technology.</p>
<p style='font-size: 10px;'><strong>IMPORTANT NOTICE:</strong> The information and results provided by this tool are to be used as a supplemental resource and should not replace the clinical judgment or expertise of qualified health professionals. We make no representation or warranty of any kind, express or implied, regarding the accuracy, adequacy, validity, reliability, availability, or completeness of any information produced by this tool.</p>
<p style='font-size: 10px;'><strong>LIABILITY DISCLAIMER:</strong> Under no circumstances shall we be liable for any direct, indirect, incidental, consequential, special, or exemplary damages arising out of or in connection with the use of this tool or reliance on any information it provides. The use of this tool and reliance on its outputs are solely at the risk of the user.</p>
<p style='font-size: 10px;'>Health care professionals are encouraged to use their own clinical expertise and judgment in conjunction with this tool when evaluating the results. Always consult relevant clinical guidelines and consider patient-specific factors when making any clinical decision.</p>
""", unsafe_allow_html=True)
