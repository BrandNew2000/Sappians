import os
import sqlite3


DATABASE_PATH=f"{os.path.abspath(os.path.dirname(__file__))}/database.sqlite"

#############
def dict_to_string(data, indent=0):
    """Convert a dictionary to a structured string."""
    result = ""
    spaces = " " * indent
    if isinstance(data, dict):
        for key, value in data.items():
            if key=="person_name":
                continue
            result += f"{spaces}{key}: "
            if isinstance(value, (dict, list)):
                result += ", " + dict_to_string(value, indent + 4)
            else:
                result += f"{value}, "
    elif isinstance(data, list):
        for item in data:
            result += f"{spaces}- "
            if isinstance(item, (dict, list)):
                result += ", " + dict_to_string(item, indent + 4)
            else:
                result += f"{item}, "
    else:
        result += f"{spaces}{data}, "
    return result.replace("|",";")
############


def init_database():
    connection = sqlite3.connect(DATABASE_PATH)

    table = """ CREATE TABLE MASTER (
            Key VARCHAR(10) NOT NULL,
            Name CHAR(25) NOT NULL,
            File CHAR(25) NOT NULL,
            Details CHAR(255) NOT NULL
        );"""
    
    connection.execute(table)
    connection.commit()
    connection.close()


def database_insert(person_name, file_type, string_output, key):
    
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute(f'''INSERT INTO MASTER VALUES ('{key}', '{person_name}', '{file_type}', '{string_output}')''')
    connection.commit()
    connection.close()


def update(file_type, llm_data, key=0):

    if not os.path.isfile(DATABASE_PATH):
        init_database()
    
    person_name=llm_data["person_name"]
    string_output=dict_to_string(llm_data)

    database_insert(person_name, file_type, string_output, key)


def main():
    update("aadhaar", {"person_name":"meow", "add":"kitty"})

if __name__=="__main__":
    main()
