import streamlit as st
import streamlit.components.v1 as components
from textblob import TextBlob
from PIL import Image
import text2emotion as te
import plotly.graph_objects as go
import pandas as pd
import json
import numpy as np
import cv2
import modals  # Ensure modals.py exists

getEmoji = {
    "happy": "😊",
    "neutral": "😐",
    "sad": "😔",
    "disgust": "🤢",
    "surprise": "😲",
    "fear": "😨",
    "angry": "😡",
}

def showEmotionData(emotion, topEmotion, image, idx):
    x, y, w, h = tuple(emotion["box"])
    cropImage = image[y:y+h, x:x+w]
    
    cols = st.columns(7)
    keys = list(emotion["emotions"].keys())
    values = list(emotion["emotions"].values())
    emotions = sorted(emotion["emotions"].items(), key=lambda kv: (kv[1], kv[0]))
                
    st.components.v1.html(f"""
        <h3 style="color: #ef4444; font-family: Source Sans Pro, sans-serif; font-size: 20px; margin-bottom: 0px; margin-top: 0px;">Person detected {idx}</h3>
    """, height=30)
    
    col1, col2, col3 = st.columns([3, 1, 2])
    
    with col1:
        st.image(cropImage, width=200)
    with col2:
        for i in range(3):
            st.metric(f"{keys[i].capitalize()} {getEmoji[keys[i]]}", round(values[i], 2), None)
    with col3:
        for i in range(3, 7):
            st.metric(f"{keys[i].capitalize()} {getEmoji[keys[i]]}", round(values[i], 2), None)
        
        st.metric("Top Emotion", f"{emotions[-1][0].capitalize()} {getEmoji[topEmotion[0]]}", None)

    st.components.v1.html("<hr>", height=5)

def load_image(image_file):
    return Image.open(image_file)

def uploadFile():
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        content = Image.open(uploaded_file)
        content = np.array(content)
        shape = np.shape(content)
        if len(shape) < 3:
            st.error('Your image has a bit-depth less than 24. Please upload an image with a bit-depth of 24.')
            return
        
        emotions, topEmotion, image = modals.imageEmotion(content)  # Ensure modals.imageEmotion is implemented
        
        st.subheader("Image information")
        file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "filesize": uploaded_file.size}
        with st.expander("See JSON Object"):
            st.json(json.dumps(file_details))
            st.image(uploaded_file, caption=uploaded_file.name, width=250)
        
        if emotions:
            printResultHead()
            with st.expander("Expand to see individual result"):
                for i in range(len(emotions)):
                    showEmotionData(emotions[i], topEmotion, content, i + 1)

            col1, col2 = st.columns([4, 2])
            with col1:
                st.image(image, width=300)
            with col2:
                st.metric("Top Emotion", f"{topEmotion[0].capitalize()} {getEmoji[topEmotion[0]]}", None)
                st.metric("Emotion Percentage", f"{round(topEmotion[1] * 100, 2)}%", None)

def renderPage():
    st.title("Sentiment Analysis 😊😐😕😡")
    st.subheader("Image Analysis")
    st.text("Input an image and let's find sentiments in there.")
    
    option = st.selectbox('How would you like to provide an image?', ('Upload One',))
    if option == "Upload One":
        uploadFile()
