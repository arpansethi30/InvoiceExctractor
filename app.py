from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

### Funciton to load Gemini Pro Vision
model = genai.GenerativeModel("gemini-pro-vision")


def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        return FileNotFoundError("No image uploaded.")


### Intializing the Streamlit App

st.set_page_config(page_title="Multilanguage Invoice Exctrator")
st.header("Multilanguage Invoice Exctrator")
input = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader(
    "Choose an image of the invoice...", type=["jpg", "jpeg", "png"]
)
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about invoice")
input_prompt = """
You are an expert in invoice analysis. We will upload an image of an invoice, and you will need to extract and interpret the information contained in it. This includes identifying key details such as the invoice number, date, item descriptions, quantities, prices, total amount, and any other relevant information. Additionally, you will answer any specific questions related to the invoice content.
"""
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
