from contants import *

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