import os
import logging
from PIL import Image
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configure Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input_text, image_parts, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro-vision")
        response = model.generate_content([input_text, image_parts[0], prompt])

        # Assuming response.parts is an iterable of Part objects; access its properties correctly
        if response.parts:
            part = response.parts[
                0
            ]  # Assuming parts is a list and we need the first part
            if hasattr(part, "text"):
                return part.text
            else:
                logging.error("No text attribute in response part: %s", part)
                return "No text attribute found in the model's output."
        else:
            logging.error("Response does not contain parts: %s", response)
            return "No parts found in the response."
    except Exception as e:
        logging.error("Detailed error: %s", str(e))
        return f"Failed to get response from the model. Error: {str(e)}"


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Streamlit app setup
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Application")

input_prompt = st.text_input("Input Prompt:", key="input")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the image")

input_description = """
You are an expert in understanding invoices.
You will receive input images as invoices &
you will have to answer questions based on the input image
"""

if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_description, image_data, input_prompt)
        st.subheader("The Response is")
        st.write(response)
    except FileNotFoundError as e:
        st.error("Error: No image file uploaded.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
