def then(first, thenDo):
    """
    Works like making a promise in javascript.
    The first paramater is what to do first. 
    This is turned into the second parameter as parameters for the function.
    """
    params = first()
    print(params)
    thenDo(params)

class ArthimeticOperation():
    """
    A simple class for creating arthimetic operations.
    The operations supported right now:
        Addition: +
        Subtraction: -
        Division: /
        Multiplication: *, x
    """
    oType = "none"
    num1 = 0
    num2 = 0
    __succeeded = False
    __numseperate = []
    operations = [
        "+", "-", "/", "*", "x"
    ]
    def __init__(self, val: str) -> None:
        for idx in range(len(val)):
            if (val[idx] in self.operations):
                self.oType = val[idx]
                self.__numseperate = val.split(" ")
                self.__numseperate.remove(val[idx])
                self.__succeeded = True
        if (self.__succeeded == False):
            raise Exception("No valid operation.")
    def execute(self):
        if (self.oType == "+"):
            return int(self.__numseperate[0]) + int(self.__numseperate[1])
        elif (self.oType == "-"):
            return int(self.__numseperate[0]) - int(self.__numseperate[1])
        elif (self.oType == "/"):
            return int(self.__numseperate[0]) / int(self.__numseperate[1])
        elif (self.oType == "*" or self.oType == "x"):
            return int(self.__numseperate[0]) * int(self.__numseperate[1])
        else:
            raise Exception("Could not execute: unknown operation type.")
        
            
            
