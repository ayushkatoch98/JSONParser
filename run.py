from lexer import Lexer
import parser
from os import listdir
from os.path import isfile, join



def run(fileName): 
    data = ""
    try: 
        data = open(fileName, encoding="utf-8").read()
    except Exception as ex:
        print("Unable to open file" , fileName , "Error Message" , ex) 
    
    lexer = Lexer(data)
    workingOn = "Lexer"
    try:
        lexer.lexer()
        print("== Lexing" , fileName.split("/")[-1][:-5].upper() , "*" * 10 , "SUCCESS")
        
        workingOn = "Parser"
        
        parser.Parser(lexer.tokens).parse()
        print("== Parsing" , fileName.split("/")[-1][:-5].upper() , "*" * 10 , "True")

    except Exception as ex:
        if workingOn == "Lexer":
            print("==" , "Lexer" , fileName.split("/")[-1][:-5].upper() , "==" , "Lexer" , "Error:" , ex)
        else:
            print("== Parsing" , fileName.split("/")[-1][:-5].upper() , "*" * 10 , "False")






onlyfiles = ["./tests/" + f for f in listdir("./tests/") if isfile(join("./tests/", f))]

for file in onlyfiles:
    run(file)

