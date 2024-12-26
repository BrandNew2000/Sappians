import shutil
import datetime
import update_database
from ocr_analysis import model_run

DEBUG=True

def debug(string):
    if DEBUG:
        print(string)

# Move file from existing location to parsed location and rename it.
def transport_file(file_path, id):
    shutil.copyfile(file_path, f"sorted_files/{id}.pdf")


# ID the file using current epoch in hex (Credits: StackOverflow): 
def makeid():
    timestamp = datetime.datetime.now()
    time_stamp_hex = hex(int(timestamp))
    return time_stamp_hex

# Run OCR on file using Aditi's code. ______________________ TBD
def run_ocr(file_path):
    pass
    ocr_data=0
    return ocr_data


# Run Smitali's code to classify the file. ______________________ TBD
def classify(ocr_data):
    pass
    doc_type="meth"
    return doc_type


# Use Achintya's code to send the data to an llm to pull details.
def extract_llm_data(ocr_data, doc_type):
    return model_run.pull_data(doc_type, ocr_data)


# Update the database with the required data.
def db_update(doc_type, llm_data, id):
    update_database.update(doc_type, llm_data, id)


def run_analysis(file_path):

    debug("Running OCR")
    ocr_data=run_ocr(file_path)
    
    debug("Classifying")
    doc_type=classify(ocr_data)

    debug("Running LLM to extract data")
    extracted_data=extract_llm_data(ocr_data, doc_type)

    debug("Data pulled")
    debug(f"Doc type: {doc_type}, data: {extracted_data}")

    id=makeid()

    debug("\nCopying the file")
    transport_file(file_path, id)

    debug("\nUpdating Database...")
    db_update(doc_type, extracted_data, id)


