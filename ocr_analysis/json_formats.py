def get_format(file_type):
    return aadhaar


aadhaar = {
    "type": "json_object",
    "schema": {
        "type": "object",
        "properties": {"person_name": {"type": "string"}, "phone_number": {"type": "string"}, "address": {"type": "string"}},
        "required": ["person_name", "phone_number", "address"],
    },
}