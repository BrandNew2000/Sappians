from llama_cpp import Llama
import sys

import json_formats


DEBUG=False

FILE_TYPE="aadhaar"
PARSE_DATA="TEN oavsmnent ce India AA D HAAR Government of India rated m sre stoeter Gea one amare ATE m elatd OR Hts / Acnss XML / HAST VATU qe slow wart we. Ete CMI CLAM TCM NSC Cal me caaite oe aaa aaa Ua TT MT, Unique Identification Authority of India alert spaie:/ Enrolment No.: 2821/35032/03347 INFORMATION To @ Aadhaar is a proof of identity, not of citizenship. anfeet aig der *Aditi Navendu Vaidya* m Verify identity using Secure QR Code/ Offline XML/ Online *C/O: Navendu Ram Vaidya* Authentication. **Flat No-C-401 The Pearl Wing C : oo . St.No-1/8 Part 9/1,2 This is electronically generated letter. Balewadi Pune City Pune Maharashtra - 411045** **9545149055 **mw one Sua ae se m Sie squeare#n fafae Geant snhtt arent Sar Baud Wars Fad eed Signature Not Verified Grave 'DENT} ES0n 1 JTHORITY: INDIA 05."



llm = Llama(
      model_path=f"{sys.path[0]}/models/gemma-2-2b-it-IQ4_XS.gguf",
      # n_gpu_layers=-1, # Uncomment to use GPU acceleration
      # seed=1337, # Uncomment to set a specific seed
      n_ctx=8192, # Uncomment to increase the context window
      verbose=DEBUG,
)


def get_response_format(file_type):
    return json_formats.get_format(file_type)
    

def get_output(parse_data, json_format):
    output=llm.create_chat_completion(
        messages=[
    #        {
    #            "role": "system",
    #            "content": "You are a helpful assistant that deciphers OCR data outputs in JSON.",
    #        },
            {"role": "user", "content": parse_data},
        ],
        response_format=json_format,
        temperature=0.7,
        max_tokens=None,
    )
    return output

def pull_data(file_type, parse_data):
    json_format=get_response_format(file_type)
    raw_output=get_output(parse_data, json_format)
    if DEBUG:
        print(raw_output)

    return raw_output["choices"][0]["message"]["content"]
        


def main():
    try:
        file_type=sys.argv[1]
        parse_data=sys.argv[2]
    except:
        file_type=FILE_TYPE
        parse_data=PARSE_DATA    
    
    print(pull_data(file_type, parse_data))




if __name__ == "__main__":
    main()
