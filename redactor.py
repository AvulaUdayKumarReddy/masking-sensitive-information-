import argparse
from project1 import main
import os

def saveFile(txt,file,redacted_path):
    path="./"+redacted_path+file+".redacted"
    file=open(path,'w')
    file.write(txt)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="files in txt format.")
    parser.add_argument("--names",action='store_true',help="redaction flag for name.")
    parser.add_argument("--dates",action='store_true',help="redaction flag for date.")
    parser.add_argument("--phones",action='store_true',help="redaction flag for phone.")
    parser.add_argument("--genders",action='store_true',help="redaction flag for genders.")
    parser.add_argument("--address",action='store_true', help="redaction flag for address.")
    parser.add_argument("--output",type=str,required=True,help="output file folder")
    parser.add_argument("--stats",type=str,required=True,help="status file folder")

    
        
    args = parser.parse_args()

    if args.output:
        redacted_path=args.output
    if args.stats:
        status_path=args.stats
        if os.path.exists(status_path):
            os.remove(status_path)
    if args.input:
        filesList=main.find_files(args.input)
        for file in filesList:
            txt,status=main.input_redaction(file,args)
            main.stats(status_path,file,status)
            saveFile(txt,file,redacted_path)
            
    

    
    
    
    