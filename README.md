# Team Name placeholder
Appian Challenge '24

## How to run:
 - Follow the instructions in the _ocr_analysis_ README to download the required llm model.
 - Start flask server by running website/app.py
 - Delete the database.csv file (if required).
 - Run main\_script.py _input.pdf_ to analyze a pdf.
 - The entry should become visible in the web interface (after reloading). The file will be renamed (as per the key visible in the web\_interface) and saved in sorted\_files.

## Training the classification model:
 - Run classification/train_model. The dataset is present in classfication/training/train_data

### TO-DO:
 - Add various formats for documents in ocr\_analysis/json_formats.py and test out other data. (DONE!) 
