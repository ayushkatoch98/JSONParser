import sys
from os import listdir
from os.path import isfile, join



data = ""

try:
    data = open("test.json" , "r").read()
except Exception as ex:
    assert 5 == 6 , "Unable to read file " + str(ex)     


DEFINED_TOKENS = {
    "string" : "STRING" ,
    "number" : "NUMBER" ,
    "boolean" : "BOOLEAN" ,
    "null" : "NULL" ,
    "lbrack" : "LBRACK" ,  # left curly bracket
    "rbrack" : "RBRACK" ,  # right curly bracket
    "lsqbrack" : "LSQBRACK" , # left square brackets
    "rsqbrack" : "RSQBRACK" , # rght square bracket
    "colon" : "COLON" ,
    "comma" : "COMMA",
}
DIGITS = ["1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9" , "0"]
BOLEANS = ["true" , "false"]
NULLS = ["null"]


class Token():
    def __init__(self, token, type, kind, sIndex, eIndex = 0):
        self.token = token
        self.type = type.upper()
        self.kind = kind
        self.sIndex = sIndex
        self.eIndex = eIndex

    def __str__(self):
        # return """Token : {0},\nType : {1},\nsIndex : {2},\neIndex : {3}\n\n""".format(self.token , self.type , self.sIndex , self.eIndex)  
        spaces = 30 - len(self.token)
        return """Token : {0} {1} Type {2}""".format(self.token , "-" * spaces , self.type)


class Lexer():

    def __init__(self , data):
        self.data = data
        self.tokens = []

    def _parseBoolean(self, sIndex, data):
        word = ""
        maxSearchLen = 5 # because false is 5 letter long
        
        if data[sIndex] == "t":
            maxSearchLen = 4
        
        maxSearchLen += sIndex
        maxSearchLen = min(maxSearchLen , len(data))

        for i in range(sIndex , maxSearchLen):
            word += data[i]

            if word in BOLEANS:
                return i , word

        raise Exception("Invalid Boolean Token `" + word.strip() + "`")

    def _parseNull(self, sIndex, data):
        word = ""
        maxSearchLen = 4 # because false is 5 letter long
        
        maxSearchLen += sIndex
        maxSearchLen = min(maxSearchLen , len(data))

        for i in range(sIndex , maxSearchLen):
            word += data[i]

            if word == "null":
                return i , word

        raise Exception("Invalid Null Token `" + word.strip() + "`")

    def _parseNumber(self, sIndex , data):
        dataLenght = len(data)
        totalDots = 0
        number = ""
        expecting = []
        for i in range(sIndex , dataLenght):  
            letter = data[i]

            if letter in DIGITS + ["." , "-" , "e" , "+"]:

                if letter in expecting:
                    number += letter
                    expecting = []
                elif letter == "-":
                    if len(number) != 0 : raise Exception("Invalid Number token, near `" + data[i] + "` , " + data[sIndex:sIndex+i])
                    number += letter
                    
                elif letter == ".":
                    if totalDots == 1: raise Exception("Invalid Number token, near `" + data[i] + "` , " + data[sIndex:sIndex+i])
                    totalDots += 1
                    number += letter
                elif letter == "e":
                    number += letter
                    expecting = ["+" , "-"]
                else:
                    number += letter
            else:
                if len(number) != 0:
                    if number[0] == "0" and totalDots == 0:
                        raise Exception("Invalid Number token, near `" + data[i] + "` , " + data[sIndex:sIndex+i])
                    return i - 1 , number
                raise Exception("Invalid Token, empty number " + data[sIndex:sIndex+20])

        raise Exception("Invalid Token Number " + data[sIndex:sIndex+20])


    def _parseString(self, sIndex , data):

        assert data[sIndex] == "\"" , "String must start with a \""
        
        dataLength = len(data)
        word = data[sIndex]
        sIndex += 1
        
        for i in range(sIndex , dataLength):
            letter = data[i]
            word += data[i]
            
            if data[i-1:i+1] == "\\\"":                
                pass
            elif letter == "\"":
                return i , word 

        raise Exception("Invalid Token string " + data[sIndex : sIndex + 10])

    def sdf(self, word):
        if word == "true" or word == "false":
            return True
        return False


    def printTokens(self):
        for token in self.tokens:
            print(token)

    def lexer(self):

        dataLength = len(self.data)
        sIndex = 0 # startIndex
        index = 0  
        commentMode = False

        while index < dataLength:
            # print("Index is " , index , " / " , dataLength)
            letter = self.data[index]
            word = self.data[sIndex:index]

            # print("Letter is `" , letter , "`" , commentMode , letter == "\n")

            if letter in [" " , "\n" , "\t"]:
                pass
            # elif commentMode:
            #     pass
            # comment end 
            # elif letter == "\n" and commentMode:
            #     commentMode = False

            # elif letter == "*" and commentMode:
            #     if index+1 < dataLength and self.data[index+1] == "/":
            #         commentMode = False
            #     else: raise Exception("Error: Invalid Token `" + letter.strip() + "`")

            # comment start
            # elif letter == "/":
            #     if index+1 < dataLength and (self.data[index+1] == "/" or self.data[index:index+2] == "/*"):
            #         commentMode = True
            #     else: raise Exception("Error: Invalid Token `" + letter.strip() + "`")

            elif letter == "{":
                self.tokens.append(Token(letter , DEFINED_TOKENS["lbrack"] , index , index+1))
            elif letter == "}":
                self.tokens.append(Token(letter , DEFINED_TOKENS["rbrack"] , index , index+1))
            elif letter in "[":
                self.tokens.append(Token(letter , DEFINED_TOKENS["lsqbrack"] , index , index+1))
            elif letter in "]":
                self.tokens.append(Token(letter , DEFINED_TOKENS["rsqbrack"] , index , index+1))
            elif letter in [":"]:
                self.tokens.append(Token(letter , DEFINED_TOKENS["colon"] , index , index+1))
            elif letter in [","]:
                self.tokens.append(Token(letter , DEFINED_TOKENS["comma"] , index , index+1))

            elif letter in ["t" , "f"]:
                eIndex , word = self._parseBoolean(index, self.data)
                self.tokens.append(Token(word , DEFINED_TOKENS["boolean"] , index , eIndex))
                index = eIndex
            elif letter == "n":
                eIndex , word = self._parseNull(index, self.data)
                self.tokens.append(Token(word , DEFINED_TOKENS["null"] , index , eIndex))
                index = eIndex

            elif letter in DIGITS + ["-"]:
                eIndex , word = self._parseNumber(index, self.data)
                self.tokens.append(Token(word , DEFINED_TOKENS["number"] , index , eIndex))
                index = eIndex
                
            elif letter == "\"":
                eIndex , word = self._parseString(index, self.data)
                self.tokens.append(Token(word , DEFINED_TOKENS["string"] , index , eIndex))
                index = eIndex
            else:
                raise Exception("Invalid Token near `" + self.data[index] + "` " + self.data[index:index+10])
                
            index += 1

def commonElement(a , b):

    for i in a:
        for j in b:
            if i == j: return i
    return None
    

class Parser():
    def __init__(self , tokens):
        self.tokens = tokens
        self.jsonStarter = [DEFINED_TOKENS["lbrack"] , DEFINED_TOKENS["lsqbrack"]]
        self.jsonEnder = [DEFINED_TOKENS["rbrack"] , DEFINED_TOKENS["rsqbrack"]]
        self.valueTokens = DEFINED_TOKENS.copy()
        
        del self.valueTokens["comma"]
        del self.valueTokens["colon"]
        del self.valueTokens["rbrack"]
        del self.valueTokens["rsqbrack"]

        self.json = ""

    
    def parseKeyValue(self, sIndex):

        skips = 3
        data = ""

        keyExpected = self.tokens[sIndex]
        colonExpected = self.tokens[sIndex+1]
        valueExpected = self.tokens[sIndex+2]

        if keyExpected.type == DEFINED_TOKENS["string"]:
            data += keyExpected.token

        if colonExpected.type == DEFINED_TOKENS["colon"]:
            data += colonExpected.token + " "

        if valueExpected.type.lower() in self.valueTokens:
            # print("GOT" , valueExpected)
            if valueExpected.type == DEFINED_TOKENS["lbrack"]:
                tempData , tempSkips = self.parseObject(sIndex+2)
                data += tempData
                skips += tempSkips
            elif valueExpected.type == DEFINED_TOKENS["lsqbrack"]:
                tempData , tempSkips = self.parseArray(sIndex+2)
                
                data += tempData
                skips += tempSkips
            else:
                data += valueExpected.token

        return data , skips

    def parseObject(self, sIndex):

        data = "{"

        assert self.tokens[sIndex].type == DEFINED_TOKENS["lbrack"] , "Object must start with ` { `"

        expecting = [DEFINED_TOKENS["string"] , DEFINED_TOKENS["rbrack"]]

        sIndex += 1
        skips = 1

        while sIndex < len(self.tokens):
            token = self.tokens[sIndex]

            if token.type in expecting:

                if token.type == DEFINED_TOKENS["rbrack"]:
                    return data + "}" , skips
                    
                elif token.type == DEFINED_TOKENS["string"]:
                    temp , tempSkips = self.parseKeyValue(sIndex)
                    data += temp
                    sIndex += tempSkips - 1
                    skips += tempSkips - 1
                    expecting = [DEFINED_TOKENS["comma"] , DEFINED_TOKENS["rbrack"] , DEFINED_TOKENS["rsqbrack"]]
                    
                elif token.type == DEFINED_TOKENS["comma"]:
                    data += token.token + " "
                    expecting = [DEFINED_TOKENS["string"]]
            
            else: raise Exception("Error: Object Expecting " + str(expecting) + " but got " + token.token + " type " + token.type)

            sIndex += 1
            skips += 1

        raise Exception("Error: object wasnt closed")

    def parseArray(self, sIndex):
        data = "["

        assert self.tokens[sIndex].type == DEFINED_TOKENS["lsqbrack"] , "Array must start with ` [ `"

        allValuesArray = [ self.valueTokens[key] for key in self.valueTokens]

        expecting = allValuesArray + [DEFINED_TOKENS["rsqbrack"]]

        sIndex += 1
        skips = 1

        while sIndex < len(self.tokens):
            token = self.tokens[sIndex]

            if token.type in expecting:

                if token.type == DEFINED_TOKENS["rsqbrack"]:
                    return data + "]" , skips
                
                elif token.type in [DEFINED_TOKENS["string"] , DEFINED_TOKENS["number"] , DEFINED_TOKENS["null"] , DEFINED_TOKENS["boolean"]]:
                    data += token.token
                    expecting = [DEFINED_TOKENS["comma"] , DEFINED_TOKENS["rsqbrack"] , "toktok"]

                elif token.type == DEFINED_TOKENS["lbrack"]:
                    tempData , tempSkips = self.parseObject(sIndex)
                    data += tempData
                    skips +=  tempSkips
                    sIndex += tempSkips
                    # print("Current " , self.tokens[sIndex])
                    expecting = allValuesArray + [DEFINED_TOKENS["comma"] , DEFINED_TOKENS["rsqbrack"] , "okok"]

                elif token.type == DEFINED_TOKENS["lsqbrack"]:
                    tempData , tempSkips = self.parseArray(sIndex)
                    data += tempData
                    skips +=  tempSkips
                    sIndex += tempSkips
                    expecting = allValuesArray + [DEFINED_TOKENS["comma"] , DEFINED_TOKENS["rsqbrack"] , "hehe"]
                
                elif token.type == DEFINED_TOKENS["comma"]:
                    data += token.token + " "
                    expecting = allValuesArray

            else: raise Exception("Error: Array Expecting " + str(expecting) + " but got " + token.token + " type " + token.type + "previous" + self.tokens[sIndex - 1].token + "MAIN DATA" + data)
            sIndex += 1
            skips += 1
        

    def parse(self):
        totalTokens = len(self.tokens)

        if totalTokens == 0:
            raise Exception("No tokens")
        
        skip = 0

        if self.tokens[0].type in [DEFINED_TOKENS["boolean"] , DEFINED_TOKENS["null"] , DEFINED_TOKENS["string"] , DEFINED_TOKENS["number"]]:
            data = self.tokens[0].token
            skip = 1
        elif self.tokens[0].type == DEFINED_TOKENS["lbrack"]:
            data , skip = self.parseObject(0)
        elif self.tokens[0].type == DEFINED_TOKENS["lsqbrack"]:
            data , skip = self.parseArray(0)

        else:
            raise Exception("Invalid Start of JSON")

        # print("TRYING " , skip , totalTokens - 1)
        if skip < totalTokens - 1:
            raise Exception("Invalid Token HUEHUE")
        else:
            return data
            


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
        
        Parser(lexer.tokens).parse()
        print("== Parsing" , fileName.split("/")[-1][:-5].upper() , "*" * 10 , "True")

    except Exception as ex:
        if workingOn == "Lexer":
            print("==" , "Lexer" , fileName.split("/")[-1][:-5].upper() , "==" , "Lexer" , "Error:" , ex)
        else:
            print("== Parsing" , fileName.split("/")[-1][:-5].upper() , "*" * 10 , "False")
        
def driver():
    
    onlyfiles = ["./tests/" + f for f in listdir("./tests/") if isfile(join("./tests/", f))]

    for file in onlyfiles:
        run(file)
    

    
driver()