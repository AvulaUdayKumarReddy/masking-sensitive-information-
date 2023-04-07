from project1 import main
import re

txt="Johnson was born on 12/2/2000, He lives in Texas and hs phone number is (812) 568-1234"

# function for the
def test_name_redact():
    status=[] # just to facilitate the functions of redaction
    redact_txt,status=main.name_redact(txt,status)
    assert redact_txt.find('Johnson')==-1

def test_phone_redact():
    status=[] # just to facilitate the functions of redaction
    redact_txt,status=main.phone_redact(txt,status)
    assert redact_txt.find('(812) 568-1234')==-1

def test_dates_redact():
    status=[] # just to facilitate the functions of redaction
    redact_txt,status=main.dates_redact(txt,status)
    assert redact_txt.find('12/2/2000')==-1

def test_address_redact():
    status=[] # just to facilitate the functions of redaction
    redact_txt,status=main.address_redact(txt,status)
    assert redact_txt.find('Texas')==-1

def test_gender_redact():
    status=[] # just to facilitate the functions of redaction
    redact_txt,status=main.gender_redact(txt,status)
    assert redact_txt.find('He')==-1

class test_args:
    names=True
    dates=True
    phones=True
    genders=True
    address=True

def test_input_redact():
    

    #testingFile for testing the file data
    file='docs/testingFile.txt'
    redact_txt,status=main.input_redaction(file,test_args)
    assert len(status) > 0

def test_find_files():
    #name to test the find_files function
    name='*.txt'
    list=main.find_files(name)
    assert len(list)>0

def test_stats():
    file='docs/testingFile.txt'
    redact_txt,status=main.input_redaction(file,test_args)
    path="testFileOutput"
    fileRead="testFileOutput"
    main.stats(path,fileRead,status)
    f=open(file,'r')
    txt=f.read()
    assert txt is not None



