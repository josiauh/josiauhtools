from josiauhtools import synx

def doFirst():
    return 'this', 'function!'

def second(p, a):
    print("i got " + p + " for p, and " + a + " for a.")

synx.then(doFirst, second)