import re
from pypdf import PdfReader
import json
import sys

def check_email(text_data):
    email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    for i in text_data.split(" "):
        if(re.findall(email, i)):
            email_id = i
        else:
            email_id ='Not Available'
        return email_id
		
def splitting_text(text_data):
    text_data2 =text_data.split("\n \n :")
    file_info = {}
    for i in range(len(text_data2)-1):
        current_content = text_data2[i].split("\n")
        next_content = text_data2[i+1].split("\n")
        file_info[current_content[-1]]=" ".join(next_content[:-1]).strip()
    return file_info
	
def splitting_text1(text_data):
    text_data1 =text_data.split("\n :")
    file_info = {}
    for i in range(len(text_data1)-1):
        current_content = text_data1[i].split("\n")
        next_content = text_data1[i+1].split("\n")
        file_info[current_content[-1]]=" ".join(next_content[:-1]).strip()
    return file_info

if __name__ == "__main__":
    
    reader = PdfReader(sys.argv[2])
    number_of_pages = len(reader.pages)
    text =''
    for i in range(number_of_pages):
        page = reader.pages[i]
        text1 = page.extract_text()
        text = text + text1
    text_data = text
    FILTER_PUNCTUATIONS = '''!()[]{};'"\|,‘<>“?#$%^&+*_~'''
    text_data = text_data.translate(str.maketrans('', '', FILTER_PUNCTUATIONS))
    text_data = "\n".join([x.replace("\n\n ",":") for x in text_data.split("\n\n\n")])
    text_data = text_data.strip()

    data = splitting_text1(text_data)
    data.update(splitting_text(text_data))
    data.update({"email":check_email(text_data)})
    
    with open(sys.argv[4], 'w') as json_obj:
        json.dump(data, json_obj)
else:
    print('Give argument correctly')