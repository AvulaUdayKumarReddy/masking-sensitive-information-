import spacy
import glob
import re
import argparse
import redactor

def find_files(name):
    fileList=glob.glob(name)
    return fileList


status_names=[] # an array that used to print the masked elements category in stats file

def input_redaction(sample,args):
    #sample is file name and args are parsed command line Name space
    status=[] # a list that contains dictionaries
    
    file=open(sample,'r')
    redact_txt=file.read()
    #args = parser.parse_args()
    # if args have names, then redact
    if args.names:
        redact_txt,status=name_redact(redact_txt,status)
        status_names.append("--names")
    # if args have phones, then redact
    if args.phones:
        redact_txt,status=phone_redact(redact_txt,status)
        status_names.append("--phones")
    # if args have dates ,then redact
    if args.dates:
        redact_txt,status=dates_redact(redact_txt,status)
        status_names.append("--dates")
    # if args have address, then redact
    if args.address:
        redact_txt,status=address_redact(redact_txt,status)
        status_names.append("--address")
    # if args have genders, then redcat
    if args.genders:
        redact_txt,status=gender_redact(redact_txt,status)
        status_names.append("--genders")
    return redact_txt,status


#names redact function
def name_redact(txt_str,status):
    #using spacy to get names
    En_nlp=spacy.load('en_core_web_sm')
    dataList={}
    
    txt=En_nlp(txt_str)
    # redaction and storing of elements
    for item in txt:
        #using entity type person to get the names 
        if(item.ent_type_=='PERSON'):
            #print(str(item))
            
            length=len(item)
            #item_str=str(item)
            if(len(str(item))>2):
                if str(item) in dataList:
                    dataList[str(item)]+=1
                else:
                    dataList[str(item)]=1
                txt_str=txt_str.replace(str(item),length*'\u2588')
    status.append(dataList)
    return txt_str,status
    #print('--------------')

            
# phones redact function
def phone_redact(txt,status):
    dataList={}# dictionary to store the elemnets
    # regex to match different kinds of phone numbers
    match_phone=re.findall(r'(\(\d{3}\)\s\d{3}-\d{4}|[+]?[\d{1,2}]?[\-\s\(]{1}?\d{3}[\-\s\)]{1}?\d{3}[\-\s]{1}?\d{4})',txt)
    #print(match_phone)
    # redaction and storing process
    
    for phone in match_phone:
        
        length=len(phone)
        if phone in dataList:
            dataList[phone]+=1
        else:
            dataList[phone]=1
        #phone=str(phone)
        #ch=chr(u"\u2588")
        txt=txt.replace(phone,length*'\u2588')
    status.append(dataList)
    return txt,status
# dates redact function
def dates_redact(txt,status):
    dataList={} # dictionary to store the elements
    # regular expressions to find all the dates of different formats
    match_date=re.findall(r'(\d{1,2}\s[a-zA-Z]{1,8}\s\d{2,4}|\d{1,2}/\d{1,2}/\d{2,4}|[JFMASOND]{1}[a-z]{2,9}\s\d{1,2},\s\d{1,4}|January\s\d{1,2}|February\s\d{1,2}|March\s\d{1,2}|April\s\d{1,2}|May\s\d{1,2}|June\s\d{1,2}|July\s\d{1,2}|August\s\d{1,2}|September\s\d{1,2}|October\s\d{1,2}|November\s\d{1,2}|December\s\d{1,2})',txt)
    #print(match_date)
    # element storing and redaction process
    for date in match_date:
        length=len(date)
        if date in dataList:
            dataList[date]+=1
        else:
            dataList[date]=1
        txt=txt.replace(date,length*'\u2588')
    status.append(dataList)
    return txt,status
#address redact function
def address_redact(txt_str,status):
    # using spacy to get the address with GPE and LOC entity types and regex to get pincodes
    En_nlp=spacy.load('en_core_web_sm')
    dataList={} # dictionary to store the elemnets
    # for pin code extraction using the 5 digit regex
    match_pincode=re.findall(r'\s\d{5}\s',txt_str)
    for pincode in match_pincode:
        length=len(pincode)
        if pincode in dataList:
            dataList[pincode]+=1
        else:
            dataList[pincode]=1
        txt_str=txt_str.replace(pincode,length*'\u2588')
    # spacy to get the address with GPE and LOC entity types
    txt=En_nlp(txt_str)
    for item in txt:
        if(item.ent_type_=='GPE' or item.ent_type_=='LOC'):
            
            if str(item) in dataList:
                dataList[str(item)]+=1
            else:
                dataList[str(item)]=1
            length=len(item)
            #item_str=str(item)
            
            txt_str=txt_str.replace(str(item),length*'\u2588')
    status.append(dataList)
    #print(dataList)
    #print(txt_str)
    return txt_str,status
# gender redact function
def gender_redact(txt,status):
    dataList={}# dictionary to store the elements
    # using two kinds of regex for male and female with all possible expected values
    match_gender_male=re.findall(r'(\s[Hh]e\s|\s[Hh]im\s|\s[Ff]ather\s|\s[Ss]on\s|\s[Mm]en\s|\s[Mm]an\s|\s[Bb]oy\s|\s[Mm]ale\s|\s[Bb]rother\s)',txt)
    match_gender_female=re.findall(r'(\s[Ss]he\s|\s[Hh]er\s|\s[Mm]other\s|\s[Dd]aughter\s|\s[Ww]omen\s|\s[Wo]man\s|\s[Gg]irl\s|\s[Ss]ister\s|\s[Fe]male\s)',txt)
    # redaction and storage of count  of an element process
    #for gender male
    for male in match_gender_male:
        length=len(male)
        if male in dataList:
            dataList[male]+=1
        else:
            dataList[male]=1
        txt=txt.replace(male,length*'\u2588')
    #for gender female
    for female in match_gender_female:
        length=len(female)
        if female in dataList:
            dataList[female]+=1
        else:
            dataList[female]=1
        txt=txt.replace(female,length*'\u2588')
    status.append(dataList)
    return txt,status
    #print(txt)



# function for printing statstics to file
def stats(path,fileRead,status):
    # function to save the stats to a file
    file=open(path,'a')
    file.write("\n")
    # fileRead is name of the file
    file.write("--------"+fileRead+"------------")
    file.write("\n")
    # status is an list of dictionaries 
    for li in range(len(status)):
        total=0
        for i in status[li]:
            total+=status[li][i]
        file.write("\n")
        file.write(status_names[li])
        file.write(" has been masked ")
        file.write(str(total))
        file.write(" times")
        
    











