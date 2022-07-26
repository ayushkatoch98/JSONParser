from contants import *


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