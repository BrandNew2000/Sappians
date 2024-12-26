from .img_processing.image_processing import *
import joblib
import os
import json

def read_model():
        
    try:
        # Load the saved model
        loaded_model = joblib.load(f'{os.path.abspath(os.path.dirname(__file__))}/model_save/xgb_model.sav')

        # Load the saved vectorizer
        loaded_vectorizer = joblib.load(f'{os.path.abspath(os.path.dirname(__file__))}/model_save/tfidf_vectorizer.sav')

        # Load labels
        with open(f'{os.path.abspath(os.path.dirname(__file__))}/model_save/labels.sav') as f:
            labels = json.load(f)

    except:
        raise(FileNotFoundError)

    print("Model, vectorizer and labels loaded successfully!")

    return loaded_model, loaded_vectorizer, labels

def predict(model, vectorizer, filename, labels):
    #  Predict the category using the trained XGBoost model
    image = convert_from_path(filename,first_page=1,last_page=1,dpi=300)
    image[0].save(f"{os.path.abspath(os.path.dirname(__file__))}/processing/image.png", "PNG")
    processed_text=clean_text(extract_text_from_image(f"{os.path.abspath(os.path.dirname(__file__))}/processing/image.png"))
    os.remove(f"{os.path.abspath(os.path.dirname(__file__))}/processing/image.png")
    document_tfidf = vectorizer.transform([processed_text])
    #retrieving the lost label names
    from sklearn.preprocessing import LabelEncoder

    label_encoder = LabelEncoder()
    label_encoder.fit(list(set(labels)))

    # Retrieve the mapping
    label_map = {index: label for index, label in enumerate(label_encoder.classes_)}
    predicted_class_index = model.predict(document_tfidf)[0]
    #print(label_map)

    predicted_label = label_map[predicted_class_index]
    
    return predicted_label, processed_text
    

def analyze_doc(filename):
    print("Starting model")
    model, vectorizer, labels = read_model()

    print("Reading file")
    return predict(model, vectorizer, filename, labels)

