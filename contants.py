
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
