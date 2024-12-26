DEBUG=True

# Import stuff

from pdf2image import convert_from_path
# import cv2
import pytesseract
from PIL import Image

import os
# import re
# import json

import numpy as np
from sklearn.preprocessing import LabelBinarizer


from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
# from pytesseract import image_to_string
import xgboost as xgb
# from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import pandas as pd


import string
import nltk
from langdetect import detect,LangDetectException
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')


INPUT_FLDR=f'{os.path.abspath(os.path.dirname(__file__))}/train_data'
OUTPUT_FLDR=f'{os.path.abspath(os.path.dirname(__file__))}/processed_txt_data'

def debug(text):
    if DEBUG:
        print(text)

# Create the output structure
def create_output_dir_structure(input_folder=INPUT_FLDR, output_folder=OUTPUT_FLDR):
    category_list=os.listdir(input_folder)
    debug(category_list)
    for category in category_list:
        category_path=os.path.join(output_folder,category)
        os.makedirs(category_path,exist_ok=True)


# Extract image data
def extract_text_from_image(image_path):
    """Extract text from an image using pytesseract"""
    img = Image.open(image_path)
    custom_config = r'--psm 1'
    text = pytesseract.image_to_string(img,config=custom_config)
    if len(text)<5:
      return None
    return text


# Clean up the OCR text.
def clean_text(text):
  try:
    language = detect(text)
  except LangDetectException as e:
    print(f"Skipping file due to error: {str(e)}")

  text = text.lower()

  tokens = word_tokenize(text)

  stop_words = set(stopwords.words(language)) if language in stopwords.fileids() else set()
  tokens_cleaned = [word for word in tokens if word not in stop_words]

    # Keep only the first 30 words

  cleaned_text = ' '.join(tokens_cleaned[:30])
  return cleaned_text


# Process the input data
def process_images_in_folder(input_folder, output_folder):
  for category in os.listdir(input_folder):
    debug(category)
    category_path=os.path.join(input_folder,category)

    if os.path.isdir(category_path):
    # Create a corresponding subfolder in the output folder if it doesn't exist
      output_category_folder = os.path.join(output_folder, category)

      if not os.path.exists(output_category_folder):
          os.makedirs(output_category_folder)

    for image_file in os.listdir(category_path):
      image_path=os.path.join(category_path,image_file)

      if os.path.isfile(image_path) and image_file.lower().endswith(('.png','.jpg','.jpeg')):
        extracted_text=extract_text_from_image(image_path)
        if extracted_text is None:
          cleaned_text1=''
        else:
          cleaned_text1=clean_text(extracted_text)


        text_filename=f"{os.path.splitext(image_file)[0]}.txt"
        output_text_path = os.path.join(output_category_folder, text_filename)
        with open(output_text_path,'w',encoding='utf-8') as f:
          f.write(cleaned_text1)


def load_data_from_folder(directory):
    texts = []
    labels = []
    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if filename.endswith('.txt'):
                    with open(os.path.join(folder_path, filename), 'r') as file:
                        texts.append(file.read())
                    labels.append(folder)  # Folder name will be the label
    return texts, labels

#print(labels)


def train(X_train, y_train, y_val):
    
    label_encoder = LabelEncoder()
    label_encoder.fit(np.concatenate((y_train, y_val)))
    y_train = label_encoder.fit_transform(y_train)
    y_val = label_encoder.transform(y_val)


    vectorizer = TfidfVectorizer(max_features=10000)

    # Transform the text data into TF-IDF features
    X_train_tfidf = vectorizer.fit_transform(X_train)

    xgb_model = xgb.XGBClassifier(n_estimators=5000, random_state=4)

    # Train the model
    xgb_model.fit(X_train_tfidf, y_train)

    return xgb_model, vectorizer, y_val


def evaluate(X_val, y_val, xgb_model, vectorizer):
   # Predict on validation set
    X_val_tfidf = vectorizer.transform(X_val)
    y_pred_xgb = xgb_model.predict(X_val_tfidf)

    # Evaluate the XGBoost model
    print("XGBoost Classification Report:")
    print(classification_report(y_val, y_pred_xgb))

    # Calculate accuracy
    accuracy = (y_pred_xgb == y_val).mean()
    print(f"XGBoost Accuracy: {accuracy:.4f}")


def main():
    create_output_dir_structure(INPUT_FLDR, OUTPUT_FLDR)
    process_images_in_folder(INPUT_FLDR, OUTPUT_FLDR)
    texts, labels = load_data_from_folder(OUTPUT_FLDR)
    X_train, X_val, y_train, y_val = train_test_split(texts, labels, test_size=0.3, random_state=42, stratify=labels)

    xgb_model, vectorizer, y_val=train(X_train, y_train, y_val)
    evaluate(X_val, y_val, xgb_model, vectorizer)


if __name__=="__main__":
   main()